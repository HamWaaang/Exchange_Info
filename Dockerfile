# 使用Python 3.9官方镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements.txt并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY main_all.py .
COPY telegram_notifier.py .
COPY telegram_config.py .
COPY main_binance.py .
COPY main_okx.py .
COPY main_coinbase.py .
COPY main_upbit.py .
COPY main_hyperliquid.py .
COPY scheduler.sh .

# 复制数据收集器
COPY data_collectors/ ./data_collectors/
COPY data_processors/ ./data_processors/

# 创建必要的目录
RUN mkdir -p data/processed data/raw/binance data/raw/okx data/raw/coinbase data/raw/upbit data/raw/hyperliquid

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 运行命令
CMD ["python", "main_all.py"] 