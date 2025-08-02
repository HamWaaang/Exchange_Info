#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime

class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        """
        初始化Telegram通知器
        
        Args:
            bot_token (str): Telegram Bot Token
            chat_id (str): 聊天ID（你的用户ID或群组ID）
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        
    def send_message(self, message, parse_mode='HTML'):
        """
        发送消息到Telegram
        
        Args:
            message (str): 要发送的消息
            parse_mode (str): 解析模式 ('HTML' 或 'Markdown')
        
        Returns:
            bool: 发送是否成功
        """
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Telegram消息发送成功")
                return True
            else:
                print(f"❌ Telegram消息发送失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Telegram消息发送异常: {e}")
            return False
    
    def send_start_notification(self):
        """发送开始运行通知"""
        message = f"""
🚀 <b>交易所数据收集开始</b>

⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 项目: Exchange Info Collector
🔄 状态: 开始收集数据...

正在收集以下交易所数据:
• Binance
• Coinbase  
• Upbit
• Hyperliquid
• OKX (暂时跳过)
        """
        return self.send_message(message)
    
    def send_completion_notification(self, results, changes_summary=None, latest_tokens=None):
        """
        发送完成通知
        
        Args:
            results (dict): 运行结果统计
            changes_summary (dict): 变化总结
            latest_tokens (dict): 最新代币清单
        """
        # 构建完成消息
        message = f"""
🎉 <b>交易所数据收集完成</b>

⏰ 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
⏱️ 总耗时: {results.get('total_time', 0):.2f}秒

📊 <b>各交易所耗时:</b>
• Binance: {results.get('binance_time', 0):.2f}秒
• Coinbase: {results.get('coinbase_time', 0):.2f}秒
• Upbit: {results.get('upbit_time', 0):.2f}秒
• Hyperliquid: {results.get('hyperliquid_time', 0):.2f}秒
• OKX: {results.get('okx_time', 0):.2f}秒

📈 <b>数据统计:</b>
• 总代币数: {results.get('total_tokens', 0)} 个
• 多交易所代币: {results.get('multi_exchange_tokens', 0)} 个
• 单交易所代币: {results.get('single_exchange_tokens', 0)} 个
        """
        
        # 如果有变化信息，添加到消息中
        if changes_summary:
            message += f"""

🔄 <b>变化检测结果:</b>
• 新增代币: {changes_summary.get('new_tokens', 0)} 个
• 删除代币: {changes_summary.get('removed_tokens', 0)} 个
• 状态变化: {changes_summary.get('status_changes', 0)} 个
• 总变化数: {changes_summary.get('total_changes', 0)} 个
        """
        
        return self.send_message(message)
    
    def send_latest_tokens_notification(self, latest_tokens):
        """
        发送最新代币清单通知
        
        Args:
            latest_tokens (dict): 最新代币清单
        """
        if not latest_tokens:
            return self.send_message("⚠️ 没有找到最新代币数据")
        
        # 多交易所代币（2个以上交易所）
        if latest_tokens.get('multi_exchange'):
            message = "🏆 <b>多交易所代币 (最新10个)</b>\n"
            message += "代币 | cb | bn | okx | ub | hl\n"
            message += "---|--|--|--|--|--\n"
            
            for token in latest_tokens['multi_exchange'][:10]:
                # 现货状态
                cb_spot = "1" if token.get('coinbase_spot') else "0"
                bn_spot = "1" if token.get('binance_spot') else "0"
                okx_spot = "1" if token.get('okx_spot') else "0"
                ub_spot = "1" if token.get('upbit_spot') else "0"
                hl_spot = "1" if token.get('hyperliquid_spot') else "0"
                
                # 合约状态
                cb_futures = "1" if token.get('coinbase_futures') else "0"
                bn_futures = "1" if token.get('binance_futures') else "0"
                okx_futures = "1" if token.get('okx_futures') else "0"
                ub_futures = "1" if token.get('upbit_futures') else "0"
                hl_futures = "1" if token.get('hyperliquid_futures') else "0"
                
                # 格式：现货,合约
                cb = f"{cb_spot},{cb_futures}"
                bn = f"{bn_spot},{bn_futures}"
                okx = f"{okx_spot},{okx_futures}"
                ub = f"{ub_spot},{ub_futures}"
                hl = f"{hl_spot},{hl_futures}"
                
                message += f"{token['baseCurrency']} | {cb} | {bn} | {okx} | {ub} | {hl}\n"
            
            self.send_message(message)
        
        # 单交易所代币
        if latest_tokens.get('single_exchange'):
            message = "💎 <b>单交易所代币 (最新10个)</b>\n"
            message += "代币 | cb | bn | okx | ub | hl\n"
            message += "---|--|--|--|--|--\n"
            
            for token in latest_tokens['single_exchange'][:10]:
                # 现货状态
                cb_spot = "1" if token.get('coinbase_spot') else "0"
                bn_spot = "1" if token.get('binance_spot') else "0"
                okx_spot = "1" if token.get('okx_spot') else "0"
                ub_spot = "1" if token.get('upbit_spot') else "0"
                hl_spot = "1" if token.get('hyperliquid_spot') else "0"
                
                # 合约状态
                cb_futures = "1" if token.get('coinbase_futures') else "0"
                bn_futures = "1" if token.get('binance_futures') else "0"
                okx_futures = "1" if token.get('okx_futures') else "0"
                ub_futures = "1" if token.get('upbit_futures') else "0"
                hl_futures = "1" if token.get('hyperliquid_futures') else "0"
                
                # 格式：现货,合约
                cb = f"{cb_spot},{cb_futures}"
                bn = f"{bn_spot},{bn_futures}"
                okx = f"{okx_spot},{okx_futures}"
                ub = f"{ub_spot},{ub_futures}"
                hl = f"{hl_spot},{hl_futures}"
                
                message += f"{token['baseCurrency']} | {cb} | {bn} | {okx} | {ub} | {hl}\n"
            
            self.send_message(message)
    
    def send_changes_notification(self, changes):
        """
        发送详细变化通知
        
        Args:
            changes (dict): 详细的变化信息
        """
        if not changes:
            message = "✅ 没有发现任何代币变化"
            return self.send_message(message)
        
        message = f"🔄 <b>代币变化详情</b>\n\n"
        
        # 新增代币
        if changes.get('new_tokens'):
            message += f"🆕 <b>新增代币 ({len(changes['new_tokens'])} 个):</b>\n"
            for token in changes['new_tokens']:
                message += f"• {token['name']}: {token['exchanges']}个交易所\n"
            message += "\n"
        
        # 删除代币
        if changes.get('removed_tokens'):
            message += f"❌ <b>删除代币 ({len(changes['removed_tokens'])} 个):</b>\n"
            for token in changes['removed_tokens']:
                message += f"• {token['name']}: 之前在{token['exchanges']}个交易所\n"
            message += "\n"
        
        # 状态变化代币
        if changes.get('status_changes'):
            message += f"🔄 <b>状态变化代币 ({len(changes['status_changes'])} 个):</b>\n"
            for change in changes['status_changes']:
                message += f"• {change['token']}: {change['details']}\n"
                message += f"  交易所数量: {change['previous_exchanges']} → {change['current_exchanges']}\n"
            message += "\n"
        
        # 如果消息太长，分段发送
        if len(message) > 4000:
            # 分段发送
            parts = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for i, part in enumerate(parts):
                if i == 0:
                    self.send_message(part)
                else:
                    self.send_message(f"(续) {part}")
        else:
            self.send_message(message)
    
    def send_error_notification(self, error_message):
        """
        发送错误通知
        
        Args:
            error_message (str): 错误信息
        """
        message = f"""
❌ <b>运行出错</b>

⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🚨 错误信息: {error_message}

请检查网络连接或程序配置。
        """
        return self.send_message(message) 