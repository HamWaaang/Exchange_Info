#!/bin/bash

# 交易所信息收集器定时运行脚本

# 设置时区
export TZ=Asia/Shanghai

# 日志文件
LOG_FILE="/app/data/scheduler.log"

# 记录日志的函数
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# 运行数据收集的函数
run_collection() {
    log_message "🚀 开始运行交易所数据收集..."
    
    # 运行主程序
    if python main_all.py; then
        log_message "✅ 数据收集完成"
    else
        log_message "❌ 数据收集失败"
        return 1
    fi
}

# 主循环
main() {
    log_message "📅 定时任务启动"
    log_message "⏰ 时区: $(date)"
    log_message "🔄 运行模式: 启动时立即运行，之后每24小时运行一次"
    
    # 启动时立即运行一次
    log_message "🎯 执行首次运行..."
    run_collection
    
    # 每24小时运行一次
    while true; do
        log_message "⏳ 等待24小时后运行下次任务..."
        sleep 86400  # 24小时 = 86400秒
        
        log_message "🔄 执行定时运行..."
        run_collection
    done
}

# 捕获信号，优雅退出
trap 'log_message "🛑 收到退出信号，正在停止..."; exit 0' SIGTERM SIGINT

# 启动主循环
main 