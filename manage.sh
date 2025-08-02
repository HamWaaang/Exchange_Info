#!/bin/bash

# 交易所信息收集器管理脚本

case "$1" in
    "start")
        echo "🚀 启动服务..."
        docker-compose up -d
        echo "✅ 服务已启动"
        ;;
    "stop")
        echo "🛑 停止服务..."
        docker-compose down
        echo "✅ 服务已停止"
        ;;
    "restart")
        echo "🔄 重启服务..."
        docker-compose restart
        echo "✅ 服务已重启"
        ;;
    "logs")
        echo "📋 查看日志..."
        docker-compose logs -f
        ;;
    "run")
        echo "🧪 手动运行数据收集..."
        docker-compose exec exchange-info python3 main_all.py
        ;;
    "status")
        echo "📊 服务状态..."
        docker-compose ps
        ;;
    "build")
        echo "🔨 重新构建镜像..."
        docker-compose build --no-cache
        echo "✅ 镜像构建完成"
        ;;
    "clean")
        echo "🧹 清理数据..."
        read -p "确定要删除所有数据吗？(y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose down
            rm -rf data/processed/* data/raw/* logs/*
            echo "✅ 数据已清理"
        else
            echo "❌ 取消清理"
        fi
        ;;
    "config")
        echo "🔧 编辑Telegram配置..."
        if command -v nano &> /dev/null; then
            nano telegram_config.py
        elif command -v vim &> /dev/null; then
            vim telegram_config.py
        else
            echo "请手动编辑 telegram_config.py 文件"
        fi
        ;;
    "help"|*)
        echo "📋 交易所信息收集器管理脚本"
        echo ""
        echo "使用方法: $0 {命令}"
        echo ""
        echo "命令:"
        echo "  start    - 启动服务"
        echo "  stop     - 停止服务"
        echo "  restart  - 重启服务"
        echo "  logs     - 查看日志"
        echo "  run      - 手动运行数据收集"
        echo "  status   - 查看服务状态"
        echo "  build    - 重新构建镜像"
        echo "  clean    - 清理数据"
        echo "  config   - 编辑Telegram配置"
        echo "  help     - 显示此帮助信息"
        echo ""
        echo "示例:"
        echo "  $0 start    # 启动服务"
        echo "  $0 run      # 手动运行"
        echo "  $0 logs     # 查看日志"
        ;;
esac 