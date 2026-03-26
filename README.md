# Weather Advisor — 天气穿衣出行助手

一个基于 Flask 的 Web 应用，通过 OpenWeatherMap API 获取实时天气数据，并根据天气状况智能生成穿衣和出行建议。界面简洁美观，支持响应式布局，手机和电脑均可方便使用。

## ✨ 功能特性

- 🌍 查询任意城市的实时天气（温度、湿度、风速、能见度等）
- 👔 根据温度分层 + 天气状况（雨雪、雾霾等）给出穿衣建议
- 🚗 结合风力、湿度、降水等信息提供出行提示
- 📱 响应式前端界面，在手机、平板、电脑上均能良好显示
- 🔌 提供 RESTful API，可被其他应用调用
- 🚀 支持部署到云平台（Render、Heroku 等），或使用 ngrok 临时暴露本地服务

## 🛠 技术栈

- **后端**：Python 3.8+、Flask、Requests
- **前端**：HTML5、CSS3、JavaScript (Fetch API)
- **API**：OpenWeatherMap API (免费版)
- **部署**：Gunicorn (生产环境)、Render / Heroku / 其他云平台

## 📁 项目结构
- **weather-advisor/**
- **├── app.py # Flask 应用入口**
- **├── weather_advisor.py # 天气获取与建议生成核心逻辑**
- **├── config.py # 配置管理（读取环境变量）**
- **├── requirements.txt # Python 依赖**
- **├── .env.example # 环境变量示例**
- **├── .gitignore**
- **├── templates/**
- **│ └── index.html # 前端页面**
- **└── README.md**


## 🚀 快速开始

### 1. 获取 OpenWeatherMap API Key

- 前往 [OpenWeatherMap](https://openweathermap.org/api) 注册账号
- 登录后，在 API Keys 页面获取一个免费 API Key（免费版每分钟 60 次调用，足够个人使用）

### 2. 克隆项目

```
git clone https://github.com/yourusername/weather-advisor.git
cd weather-advisor
```
### 3. 安装依赖
推荐使用虚拟环境：

```
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 4. 配置环境变量
复制 .env.example 为 .env，并填入你的 API Key：

```
cp .env.example .env
````
编辑 .env 文件：
```
OPENWEATHER_API_KEY=your_api_key_here
DEFAULT_CITY=Beijing
UNITS=metric
```
- **OPENWEATHER_API_KEY：你的 API Key（必需）**
- **DEFAULT_CITY：默认查询城市（可选）**
- **UNITS：温度单位，metric 为摄氏度，imperial 为华氏度（可选）**

### 5. 本地运行
```
python app.py
```


## 📖 使用说明
### 网页端
1.在浏览器中打开应用主页。

2.输入城市英文名（例如 Beijing、London、New York），点击“查询”按钮或按回车键。

3.页面将显示该城市的实时天气信息（温度、体感温度、湿度、风速、能见度等）。

4.下方自动生成穿衣建议和出行建议，帮助您规划当日活动。

## 🚢 部署到生产环境
### 使用 Render（免费）
1.将项目代码推送到 GitHub 仓库。

2.在 Render 注册账号，点击 New + → Web Service。

3.连接 GitHub 仓库，填写配置：

- **Name: 任意**

- **Environment: Python 3**

- **Build Command: pip install -r requirements.txt**

- **Start Command: gunicorn app:app**

4.在 Environment Variables 中添加：

- **OPENWEATHER_API_KEY：你的 API Key**

- **DEFAULT_CITY（可选）**

- **UNITS（可选）**

5.点击 Create Web Service。等待部署完成后，访问 https://your-app-name.onrender.com。

| Render 免费实例在 15 分钟无访问后会自动休眠，再次访问时需等待几秒唤醒。

### 使用 ngrok（临时暴露本地服务）
本地运行 python app.py（确保 app.run(host='0.0.0.0', port=5000)）。

下载并运行 ngrok：
```
ngrok http 5000
```
获得公网地址（如 https://abc123.ngrok.io），即可在手机或朋友电脑上访问。

### 🔧 自定义建议规则
您可以修改 weather_advisor.py 中的 _clothing_advice 和 _travel_advice 方法，根据个人喜好调整建议内容。例如增加对紫外线指数、PM2.5 等数据的支持（需扩展 API 调用）。

### 🙏 致谢
数据来源：OpenWeatherMap

图标库：Font Awesome 6

