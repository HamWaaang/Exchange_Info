#!/bin/bash

# 交易所信息收集器监控脚本

echo "📊 交易所信息收集器监控面板"
echo "================================"

# 检查容器状态
echo "🐳 容器状态:"
if docker-compose ps | grep -q "Up"; then
    echo "✅ 容器运行中"
else
    echo "❌ 容器未运行"
    echo "启动命令: docker-compose up -d"
fi

echo ""

# 查看最近日志
echo "📋 最近日志 (最后20行):"
docker-compose logs --tail=20

echo ""

# 查看调度器日志
if [ -f "data/scheduler.log" ]; then
    echo "📅 调度器日志 (最后10行):"
    tail -10 data/scheduler.log
else
    echo "⚠️  调度器日志文件不存在"
fi

echo ""

# 查看数据文件
echo "📁 数据文件状态:"
if [ -d "data/processed" ]; then
    echo "✅ 数据目录存在"
    echo "📊 最新数据文件:"
    ls -la data/processed/ | head -5
else
    echo "❌ 数据目录不存在"
fi

echo ""

# 查看容器资源使用
echo "💻 容器资源使用:"
docker stats --no-stream exchange-info-collector 2>/dev/null || echo "无法获取资源使用信息"

echo ""

# 常用命令提示
echo "🔧 常用命令:"
echo "  查看实时日志: docker-compose logs -f"
echo "  重启服务: docker-compose restart"
echo "  停止服务: docker-compose down"
echo "  进入容器: docker-compose exec exchange-info bash"
echo "  手动运行: docker-compose exec exchange-info python main_all.py" 