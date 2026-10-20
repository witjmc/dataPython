# 임포트 & 앱 생성
from flask import Flask, jsonify
import json

app = Flask(__name__)

# YOLO 스크랩트가 매 프레임 갱신하는 파일을 읽는 경로
data_file = r"*\data.json"


#메인 페이지 (/)
# http://localhost:5000 접속 시 반환하는 HTML. 내부 구성
@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>People Counter</title>
     # Chart.js 로드
     # CDN 에서 Chart.js v4 를 로드
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body style="font-family:sans-serif; text-align:center; padding-top:30px;">
      # DOM 요소
      # count -> 현재 사람수
      # duration ->  현재 count 유지 시간
      # countChart -> 차트 그려질 캔버스
        <h1 id="count">People: 0</h1>
        <p id="duration" style="font-size:24px;">Duration: 0.0s</p>

        <div style="width:80%; max-width:800px; margin:20px auto;">
            <canvas id="countChart"></canvas>
        </div>


        <script>
            const ctx = document.getElementById('countChart').getContext('2d');
          # 차트 초기화
            const chart = new Chart(ctx, {
                type: 'line', # 선 그래프
                data: {
                    labels: [], # x축 (시간)
                    datasets: [{
                        label: 'People Count',
                        data: [],  # y축 (count)
                        borderColor: 'green',
                        backgroundColor: 'rgba(0,255,0,0.1)',
                        fill: true, # 선 아래 채움
                        tension: 0.3  # 곡선 부드러움
                    }]
                },
                options: {
                    responsive: true,
                    animation: false, # 애니메이션 끔 (실시간 갱신용)
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { stepSize: 1 } #0부터, 정수만
                        }
                    }
                }
            });

           # 1초마다 폴링
            setInterval(async () => {
                try {
                    const res = await fetch('/api/data');
                    const data = await res.json();
                   # 텍스트 갱신
                    document.getElementById('count').textContent = 'People: ' + data.count;
                    document.getElementById('duration').textContent = 'Duration: ' + data.duration + 's';

                    const now = new Date().toLocaleTimeString();
                   #차트에 1개 추가
                    chart.data.labels.push(now);
                    chart.data.datasets[0].data.push(data.count);

                  # 최대 60개(1분) 유지, 초과 시 맨 앞 제거
                    if (chart.data.labels.length > 60) {
                        chart.data.labels.shift();
                        chart.data.datasets[0].data.shift();
                    }
                    chart.update(); # 차트 다시 렌더
                } catch(e) {
                    console.error(e);
                }
            }, 1000);
        </script>
    </body>
    </html>
    '''

# api 엔드포인트 (/api/data)
@app.route('/api/data')
def api_data():
    try:
        with open(data_file, "r") as f:
            return jsonify(json.load(f))
   # 예외처리
  # FileNotFoundError -  YOLO 스크립트가 아직 시작 안 됨
  # json.JSONDecodeError - YOLO 가 쓰는 중에 파일이 비어있거나 깨진 상태
  # PermissionError - YOLO 가 파일에 쓰기 중이라 Windows 가 읽기 잠금
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
       # 에러 시 {"count": 0, "duration": 0.0} 반환 -> 차트가 0으로 표시.
        return jsonify({"count": 0, zk"duration": 0.0})

# 서버 실행
if __name__ == '__main__':
   # 파라미터 host="0.0.0.0" 외부 네트워크에서도 접근 가능 (LAN 내 다른 기기에서 http://PC-IP"5000)
   # 파라미터 port=5000 포트 5000
   # 파라미터 debug=False 디버그 모드 끔 (파일 변경 시 자동 재시작 안함, 프로덕션용)
    app.run(host="0.0.0.0", port=5000, debug=False)   
