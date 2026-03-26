import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()


class Config:
    """配置类，从环境变量读取配置"""
    API_KEY = os.getenv('OPENWEATHER_API_KEY')
    DEFAULT_CITY = os.getenv('DEFAULT_CITY', 'Beijing')
    UNITS = os.getenv('UNITS', 'metric')  # metric: 摄氏度, imperial: 华氏度

    # API 端点
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

    @classmethod
    def validate(cls):
        """验证必要配置是否存在"""
        if not cls.API_KEY:
            raise ValueError("未设置 OPENWEATHER_API_KEY 环境变量")