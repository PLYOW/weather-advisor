from flask import Flask, request, jsonify, render_template
from weather_advisor import WeatherAdvisor

app = Flask(__name__)

# 实例化天气建议类
advisor = WeatherAdvisor()


# 首页 - 返回前端界面
@app.route('/')
def index():
    return render_template('index.html')


# 天气 API（与之前一致）
@app.route('/weather', methods=['GET'])
def get_weather_advice():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': '缺少城市参数，请使用 ?city=城市名'}), 400

    try:
        raw_data = advisor.get_weather(city)
        weather_info = advisor.parse_weather(raw_data)
        advice = advisor.generate_advice(weather_info)

        result = {
            'city': weather_info['city'],
            'weather': {
                'description': weather_info['description'],
                'temperature': weather_info['temp'],
                'feels_like': weather_info['feels_like'],
                'humidity': weather_info['humidity'],
                'wind_speed': weather_info['wind_speed'],
                'visibility': weather_info['visibility'],
                'clouds': weather_info['clouds']
            },
            'advice': advice
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
