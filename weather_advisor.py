import requests
import sys
from config import Config


class WeatherAdvisor:
    """天气穿衣出行建议生成器"""

    def __init__(self):
        self.config = Config()
        self.config.validate()

    import time

    import time

    def get_weather(self, city):
        params = {
            'q': city,
            'appid': self.config.API_KEY,
            'units': self.config.UNITS,
            'lang': 'zh_cn'
        }
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(self.config.BASE_URL, params=params, timeout=30)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"请求超时，正在重试 ({attempt + 1}/{max_retries})...")
                    time.sleep(2)
                else:
                    print("多次重试后仍超时，请检查网络或稍后再试。")
                    sys.exit(1)
            except requests.exceptions.RequestException as e:
                print(f"请求失败: {e}")
                sys.exit(1)

    def parse_weather(self, data):
        """解析天气数据，提取关键信息"""
        try:
            # 城市名称
            city_name = data.get('name', '未知')

            # 天气描述
            weather_desc = data['weather'][0]['description'] if data.get('weather') else '未知'

            # 温度
            main = data.get('main', {})
            temp = main.get('temp')
            feels_like = main.get('feels_like')
            humidity = main.get('humidity')

            # 风力
            wind = data.get('wind', {})
            wind_speed = wind.get('speed')

            # 能见度（米）
            visibility = data.get('visibility')

            # 云量（百分比）
            clouds = data.get('clouds', {}).get('all')

            # 天气代码（用于更精细的建议）
            weather_id = data['weather'][0]['id'] if data.get('weather') else None

            return {
                'city': city_name,
                'description': weather_desc,
                'temp': temp,
                'feels_like': feels_like,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'visibility': visibility,
                'clouds': clouds,
                'weather_id': weather_id
            }
        except KeyError as e:
            print(f"解析天气数据失败，缺少字段: {e}")
            sys.exit(1)

    def generate_advice(self, weather_info):
        """根据天气信息生成穿衣和出行建议"""
        temp = weather_info['temp']
        desc = weather_info['description']
        wind = weather_info['wind_speed']
        humidity = weather_info['humidity']
        weather_id = weather_info['weather_id']

        # 穿衣建议
        clothing_advice = self._clothing_advice(temp, weather_id)

        # 出行建议
        travel_advice = self._travel_advice(desc, wind, humidity, weather_id)

        return {
            'clothing': clothing_advice,
            'travel': travel_advice
        }

    def _clothing_advice(self, temp, weather_id):
        """根据温度和天气代码给出穿衣建议"""
        if temp is None:
            return "无法获取温度信息，请根据实际天气判断。"

        # 温度分层建议
        if temp <= 0:
            layer = "羽绒服、厚棉衣、保暖内衣、围巾手套帽子"
        elif temp <= 10:
            layer = "大衣、毛衣、长裤、薄围巾"
        elif temp <= 20:
            layer = "风衣、卫衣、牛仔裤、长袖T恤"
        elif temp <= 30:
            layer = "短袖T恤、薄外套、长裤或短裤"
        else:
            layer = "短袖、短裤、裙子、防晒衣"

        # 根据天气代码调整
        if weather_id and (200 <= weather_id < 600):  # 雨雪天气
            if temp <= 5:
                layer += "，建议穿防水保暖的鞋子"
            else:
                layer += "，建议携带雨具并选择防水外套"
        elif weather_id and (600 <= weather_id < 700):  # 雪
            layer += "，注意防滑保暖"
        elif weather_id and (700 <= weather_id < 800):  # 雾霾
            layer += "，建议佩戴口罩"

        return f"气温{temp}℃：建议穿{layer}。"

    def _travel_advice(self, desc, wind, humidity, weather_id):
        """根据天气描述、风力、湿度等给出出行建议"""
        advice = []

        # 根据天气描述
        if "雨" in desc:
            advice.append("有雨，请携带雨具，路面湿滑，注意防滑。")
            if "暴雨" in desc or "大暴雨" in desc:
                advice.append("暴雨天气，非必要不外出，注意安全。")
        elif "雪" in desc:
            advice.append("降雪天气，注意防寒保暖，路面可能结冰，小心慢行。")
        elif "雾" in desc or "霾" in desc:
            advice.append("能见度低，开车请减速慢行，佩戴口罩，减少户外活动。")
        elif "晴" in desc:
            if weather_id == 800:  # 晴
                advice.append("天气晴朗，适宜户外活动，注意防晒。")
            else:
                advice.append("天气晴好，可以安排出行。")
        elif "多云" in desc:
            advice.append("天气不错，适合出行。")
        elif "阴" in desc:
            advice.append("天气阴沉，心情可能会受影响，但出行无大碍。")

        # 风力影响
        if wind is not None:
            if wind > 10:
                advice.append(f"风力较大（{wind}m/s），注意防风，远离广告牌等危险物。")
            elif wind > 5:
                advice.append(f"有风（{wind}m/s），体感可能较凉，适当增添衣物。")

        # 湿度影响
        if humidity is not None:
            if humidity > 80:
                advice.append("湿度高，感觉闷热，注意补充水分。")
            elif humidity < 30:
                advice.append("空气干燥，多喝水，注意保湿。")

        if not advice:
            advice.append("天气条件良好，适合正常出行。")

        return " ".join(advice)

    def run(self, city=None):
        """主流程：获取天气、生成建议并打印"""
        if not city:
            city = self.config.DEFAULT_CITY

        print(f"正在获取 {city} 的天气信息...")
        raw_data = self.get_weather(city)
        weather_info = self.parse_weather(raw_data)

        # 显示天气摘要
        print(f"\n城市：{weather_info['city']}")
        print(f"天气：{weather_info['description']}")
        print(f"温度：{weather_info['temp']}℃ (体感 {weather_info['feels_like']}℃)")
        print(f"湿度：{weather_info['humidity']}%")
        if weather_info['wind_speed']:
            print(f"风速：{weather_info['wind_speed']} m/s")
        if weather_info['visibility']:
            print(f"能见度：{weather_info['visibility']} 米")

        # 生成建议
        advice = self.generate_advice(weather_info)
        print("\n💡 穿衣建议：")
        print(advice['clothing'])
        print("\n🚗 出行建议：")
        print(advice['travel'])


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='天气穿衣出行建议工具')
    parser.add_argument('city', nargs='?', help='城市名称（如 Beijing, Shanghai）')
    args = parser.parse_args()

    advisor = WeatherAdvisor()
    advisor.run(args.city)


if __name__ == '__main__':
    main()