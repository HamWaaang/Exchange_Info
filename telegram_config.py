#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Telegram Bot 配置
# 请将以下值替换为你的实际配置

# Bot Token - 从 @BotFather 获取
BOT_TOKEN = "7516579017:AAE_xx_zSxVERnZopBe8fODQefHAt6uvQrg"

# Chat ID - 你的用户ID或群组ID
# 可以通过以下方式获取：
# 1. 发送消息给 @userinfobot
# 2. 或者发送消息给 @RawDataBot
CHAT_ID = "-4866715127"

# 是否启用Telegram通知
ENABLE_TELEGRAM_NOTIFICATION = True

# 通知设置
NOTIFICATION_SETTINGS = {
    'send_start_notification': True,      # 发送开始通知
    'send_completion_notification': True, # 发送完成通知
    'send_changes_notification': True,    # 发送变化通知
    'send_error_notification': True,      # 发送错误通知
    'max_message_length': 4000,          # 最大消息长度
    'timeout': 10                        # 请求超时时间（秒）
} 