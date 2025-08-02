# Telegram 通知设置指南

## 🚀 功能概述

这个项目现在支持通过Telegram发送通知，包括：
- 🚀 开始运行通知
- 🎉 完成运行通知（包含详细统计）
- 🔄 代币变化通知（新增、删除、状态变化）
- ❌ 错误通知

## 📋 设置步骤

### 1. 创建Telegram Bot

1. 在Telegram中搜索 `@BotFather`
2. 发送 `/newbot` 命令
3. 按照提示设置Bot名称和用户名
4. 保存BotFather给你的 `Bot Token`

### 2. 获取Chat ID

#### 方法一：使用 @userinfobot
1. 在Telegram中搜索 `@userinfobot`
2. 发送任意消息给这个Bot
3. 它会回复你的用户ID

#### 方法二：使用 @RawDataBot
1. 在Telegram中搜索 `@RawDataBot`
2. 发送任意消息给这个Bot
3. 在回复中找到 `"id":` 后面的数字

### 3. 配置项目

1. 编辑 `telegram_config.py` 文件
2. 将以下值替换为你的实际配置：

```python
# Bot Token - 从 @BotFather 获取
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  # 替换为你的Bot Token

# Chat ID - 你的用户ID或群组ID
CHAT_ID = "123456789"  # 替换为你的Chat ID

# 是否启用Telegram通知
ENABLE_TELEGRAM_NOTIFICATION = True
```

### 4. 测试配置

运行项目测试Telegram通知是否正常工作：

```bash
python3 main_all.py
```

## 📱 通知示例

### 开始通知
```
🚀 交易所数据收集开始

⏰ 开始时间: 2024-08-02 16:30:00
📊 项目: Exchange Info Collector
🔄 状态: 开始收集数据...

正在收集以下交易所数据:
• Binance
• Coinbase  
• Upbit
• Hyperliquid
• OKX (暂时跳过)
```

### 完成通知
```
🎉 交易所数据收集完成

⏰ 完成时间: 2024-08-02 16:35:00
⏱️ 总耗时: 15.44秒

📊 各交易所耗时:
• Binance: 4.51秒
• Coinbase: 1.46秒
• Upbit: 4.81秒
• Hyperliquid: 4.36秒
• OKX: 0.00秒

📈 数据统计:
• 总代币数: 749 个
• 多交易所代币: 408 个
• 单交易所代币: 341 个

🔄 变化检测结果:
• 新增代币: 2 个
• 删除代币: 2 个
• 状态变化: 5 个
• 总变化数: 9 个
```

### 变化详情通知
```
🔄 代币变化详情

🆕 新增代币 (2 个):
• HOME: 2个交易所
• TREE: 2个交易所

❌ 删除代币 (2 个):
• LOKA: 之前在2个交易所
• NEWCOIN: 之前在3个交易所

🔄 状态变化代币 (5 个):
• BTC: Hyperliquid移除现货
  交易所数量: 5 → 5
• PUMP: Coinbase新增现货, OKX移除合约
  交易所数量: 4 → 4
```

## ⚙️ 配置选项

在 `telegram_config.py` 中可以调整以下设置：

```python
NOTIFICATION_SETTINGS = {
    'send_start_notification': True,      # 发送开始通知
    'send_completion_notification': True, # 发送完成通知
    'send_changes_notification': True,    # 发送变化通知
    'send_error_notification': True,      # 发送错误通知
    'max_message_length': 4000,          # 最大消息长度
    'timeout': 10                        # 请求超时时间（秒）
}
```

## 🔧 故障排除

### 常见问题

1. **Bot Token无效**
   - 检查Bot Token是否正确
   - 确保Bot没有被删除

2. **Chat ID错误**
   - 重新获取Chat ID
   - 确保Bot有权限发送消息

3. **网络连接问题**
   - 检查网络连接
   - 可能需要代理

4. **消息发送失败**
   - 检查Bot是否被阻止
   - 尝试重新启动Bot

### 调试模式

如果遇到问题，可以临时禁用Telegram通知：

```python
ENABLE_TELEGRAM_NOTIFICATION = False
```

## 📝 注意事项

1. **安全性**: 不要将Bot Token分享给他人
2. **频率限制**: Telegram API有频率限制，避免过于频繁的请求
3. **消息长度**: 长消息会自动分段发送
4. **错误处理**: 程序会继续运行即使Telegram通知失败

## 🎯 使用建议

1. **定期运行**: 建议每天运行1-2次
2. **监控变化**: 重点关注新增和状态变化的代币
3. **及时响应**: 收到变化通知后及时查看详细数据
4. **备份配置**: 保存好Bot Token和Chat ID 