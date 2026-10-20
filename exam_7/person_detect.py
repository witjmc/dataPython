from ultralytics import YOLO
import cv2
import time
import json
import signal
import sys
import numpy as np

# 모델 로드
model = YOLO("yolov8n.pt")

# Flask  가 읽을 실시간 데이터
data_file = r"*\data.json"

# count 변화 이력 로그
log_file = r"*\person_log2.json"

# 로그 저장용 리스트
history = []

# 이전 프레임의 사람 수
prev_count = 0

# 현재 count 가 시작된 시각
count_start_time = time.time()

# 메인 루프 제어 플래그
running = True

#  Ctrl + C 처리 
#  Ctrl + C 를 누르면 running = False 가 되어 루프가 정상 종료 된다.
#  cap.release() 가 실행되어 카메라가 해체된다.
def signal_handler(sig, frame):
    global running
    running = False

signal.signal(signal.SIGINT, signal_handler)

# 카메라 연결 (재시도 5회,2초 간격)
cap = None
for attempt in range(5):
  # 항목 0 : 카메라 인덱스 (0번 장치)
  # 항목 cv2.CAP_DSHOW : DirectShow 백엔드 (Windows 전용, MSMF 보다 안정적)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if cap.isOpened():
        break
    print(f"카메라 연결 실패, {attempt + 1}/5 재시도...")
    time.sleep(2)
    cap.release()

# 해상도/프레임 설정
if cap is None or not cap.isOpened():
    print("카메라를 찾을 수 없습니다. 종료합니다.")
    sys.exit(1)
#640*480, 15fps 로 제한 -> USB 버스 부하 감소 -> 추론 속도 향상.
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 15)

print(f"카메라 연결 성공")
# GUI 스레드
cv2.startWindowThread()

while running:
    ret, frame = cap.read()
  # 프레임 읽기 (읽기 실패 시 1초 대기 후 재시도 - 카메라 일시적 끊김 대응)
    if not ret:
        time.sleep(1)
        continue

   # 추론 + 트래킹
   # 파라미터 persist =True 트래커 상태를 프레임 간 유지 (ID 일관성)
   # verbose=False 추론 로그 출력 끔
   # tracker="bytetrack.yaml" ByteTrack 사용 -> GMC(광학흐름) 안씀 -> not enough matching points 경고 소거 
    results = model.track(frame, persist=True, verbose=False, tracker="bytetrack.yaml")

  #사람 카운팅 + 마스킹
    count = 0
    if results[0].boxes is not None and len(results[0].boxes) > 0:
        for box in results[0].boxes:
          # box.cls[0] -> 예측 클래스 (0=person)
            if int(box.cls[0]) == 0:
                count += 1
                # 사람 영역 검게 마스킹
                # box.xyxy[0] -> 바운딩 박스 좌표[x1,y1,x2,y2] 
                x1, y1, x2, y2 = map(int, box.xyxy[0])
              # 해당 영역을 검은색으로 덮은 (개인정보 보호)
                frame[y1:y2, x1:x2] = 0  

    # 전체 프레임 어둡게 (80% darken)
   # 전체 픽셀값을 20%로 축소,
   # np.zeros 로 하면 완전 검은 화면
    frame = (frame * 0.2).astype(np.uint8)


    # count 변화 시 로그
    if count != prev_count:
        duration = time.time() - count_start_time
        if duration > 0.5: # 0.5 초 미만은 노이즈 무시
            entry = {
                "count": prev_count,  # 이전 count
                "duration": round(duration, 1),  # 그 count 가 유지된 시간
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
          # person_log2.json 에 [{count:0, duration:5,0}, {count:2, duration:3,0},...] 기록
            history.append(entry)
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        prev_count = count
        count_start_time = time.time()

    current_duration = time.time() - count_start_time


    # 화면 표시
    # count 오버레이 (검은 배경 위에는 밝은 색)
    cv2.putText(frame, f"People: {count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Duration: {current_duration:.1f}s", (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

  # putText -> 화면에 count/duration 오버레이
  # imshow -> 창표시
    cv2.imshow("YOLO Person Counter", frame)

  #q 키 ->  running = False -> 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        running = False

#data.json 매 프레임 갱신
# 매 프레임마다 data.json 을 덮어씀 -> Flask 가 이 파일을 1초마다 읽어서 웹에 표시
    with open(data_file, "w") as f:
        json.dump({"count": count, "duration": round(current_duration, 1)}, f)

# 카메라 해체
cap.release()
# 모든 창 닫기
cv2.destroyAllWindows()
print("종료됨.")   
