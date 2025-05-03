from flask import Flask, request, jsonify, render_template
from textblob import TextBlob
from datetime import datetime
from dateutil.parser import parse  # 추가 설치 필요: pip install python-dateutil

app = Flask(__name__, template_folder='templates')

# 감정 데이터 리스트 (간단한 예시로 사용)
emotion_data = []
#광고 클릭 수
#ad_clicks = []
ad_clicks = {'left': 0, 'center': 0, 'right': 0}

# 감정 분석 함수
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity  # 감정 점수: -1(부정) ~ 1(긍정)

    if sentiment_score > 0.1:
        return "긍정적"
    elif sentiment_score < -0.1:
        return "부정적"
    else:
        return "중립적"
    
# 시간대별 분석을 위한 예시 저장 함수
def analyze_time_of_day(time_str):
    # 문자열을 datetime 객체로 변환
    time_obj = parse(time_str)  # fromisoformat 대신 dateutil의 parse 사용
    
    # 시간을 기반으로 감정 분석 (예: 오전 9시 ~ 12시, 오후 12시 ~ 6시 등)
    if 6 <= time_obj.hour < 12:
        return "오전"
    elif 12 <= time_obj.hour < 18:
        return "오후"
    else:
        return "야간"
    
@app.route('/')
def home():
    return render_template('index.html')  # templates 폴더에 index.html 넣기


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text')
    time = data.get('time')  # 시간 정보 받기
    sentiment = analyze_sentiment(text)
    time_of_day = analyze_time_of_day(time)  # 시간대 분석 추가

    emotion_data.append({
        'sentiment': sentiment,
        'time_of_day': time_of_day,
        'time': time
    })

    # 시간은 그대로 반환
    return jsonify({
        "sentiment": sentiment,
        "time": time,  # 감정 분석과 함께 시간도 반환
        "time_of_day": time_of_day  # 분석된 시간대 정보 반환
    })


@app.route('/dashboard')
def dashboard():
    print("Dashboard data:", emotion_data)  # 로그 찍기
    # 대시보드 화면에 리스트로 감정 데이터를 전달
    return render_template('dashboard.html', emotion_data=emotion_data, ad_clicks=ad_clicks)


@app.route('/ad-click', methods=['POST'])
def ad_click():
    data = request.get_json()
    #ad_clicks.append(data['time'])
    position = data.get('position')  # 'left', 'center', 'right' 중 하나
    if position in ad_clicks:
        ad_clicks[position] += 1  # 해당 위치의 클릭 수 증가
    return '', 204
    

if __name__ == '__main__':
    app.run(debug=True)
