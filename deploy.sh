#!/bin/bash

# 交易所信息收集器 Docker 部署脚本

echo "🚀 开始部署交易所信息收集器..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose未安装，请先安装docker-compose"
    exit 1
fi

# 创建必要的目录
echo "📁 创建数据目录..."
mkdir -p data/processed data/raw/binance data/raw/okx data/raw/coinbase data/raw/upbit data/raw/hyperliquid

# 检查配置文件
if [ ! -f "telegram_config.py" ]; then
    echo "⚠️  未找到 telegram_config.py 配置文件"
    echo "请确保已配置Telegram Bot Token和Chat ID"
fi

# 构建并启动容器
echo "🔨 构建Docker镜像..."
docker-compose build

echo "🚀 启动容器..."
docker-compose up -d

echo "✅ 部署完成！"
echo ""
echo "⏰ 运行模式:"
echo "  • 启动时立即运行一次"
echo "  • 之后每24小时自动运行一次"
echo "  • 每次运行都会发送Telegram通知"
echo ""
echo "📋 常用命令："
echo "  查看日志: docker-compose logs -f"
echo "  监控状态: ./monitor.sh"
echo "  停止服务: docker-compose down"
echo "  重启服务: docker-compose restart"
echo "  进入容器: docker-compose exec exchange-info bash"
echo "  手动运行: docker-compose exec exchange-info python main_all.py"
echo ""
echo "📊 数据文件位置: ./data/"
echo "📅 调度日志: ./data/scheduler.log"
echo "📱 Telegram通知: 请确保已正确配置 telegram_config.py" 