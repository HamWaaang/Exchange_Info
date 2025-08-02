#!/bin/bash

# 交易所信息收集器 Docker 部署脚本

set -e

echo "🚀 开始部署交易所信息收集器..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p data/processed data/raw/binance data/raw/okx data/raw/coinbase data/raw/upbit data/raw/hyperliquid logs

# 设置目录权限
chmod 755 data logs

# 检查配置文件
if [ ! -f "telegram_config.py" ]; then
    echo "⚠️  未找到telegram_config.py，将创建默认配置..."
    cat > telegram_config.py << EOF
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Telegram Bot 配置
# 请将以下值替换为你的实际配置

# Bot Token - 从 @BotFather 获取
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Chat ID - 你的用户ID或群组ID
CHAT_ID = "YOUR_CHAT_ID_HERE"

# 是否启用Telegram通知
ENABLE_TELEGRAM_NOTIFICATION = False

# 通知设置
NOTIFICATION_SETTINGS = {
    'send_start_notification': True,
    'send_completion_notification': True,
    'send_changes_notification': True,
    'send_error_notification': True,
    'max_message_length': 4000,
    'timeout': 10
}
EOF
    echo "✅ 已创建默认telegram_config.py"
fi

# 构建Docker镜像
echo "🔨 构建Docker镜像..."
docker-compose build

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态..."
docker-compose ps

# 运行一次测试
echo "🧪 运行测试..."
docker-compose exec exchange-info python3 main_all.py

echo "✅ 部署完成！"
echo ""
echo "📋 使用说明："
echo "1. 查看日志: docker-compose logs -f"
echo "2. 停止服务: docker-compose down"
echo "3. 重启服务: docker-compose restart"
echo "4. 手动运行: docker-compose exec exchange-info python3 main_all.py"
echo "5. 查看数据: ls -la data/processed/"
echo ""
echo "🔧 配置Telegram通知："
echo "1. 编辑 telegram_config.py"
echo "2. 设置你的Bot Token和Chat ID"
echo "3. 重启服务: docker-compose restart" 