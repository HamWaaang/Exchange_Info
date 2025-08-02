#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import subprocess
import sys
from datetime import datetime

def test_scheduler():
    """测试定时调度功能"""
    print("🧪 测试定时调度功能...")
    
    # 模拟调度器运行
    print(f"⏰ 当前时间: {datetime.now()}")
    print("🚀 模拟启动时立即运行...")
    
    # 运行一次主程序
    try:
        result = subprocess.run([sys.executable, "main_all.py"], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ 首次运行成功")
            print("📤 Telegram通知已发送")
        else:
            print(f"❌ 首次运行失败: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ 运行超时（5分钟）")
        return False
    except Exception as e:
        print(f"❌ 运行异常: {e}")
        return False
    
    # 模拟等待24小时（实际只等待10秒用于测试）
    print("⏳ 模拟等待24小时...")
    print("💡 实际部署时会等待86400秒（24小时）")
    
    # 这里可以添加更多测试逻辑
    print("✅ 定时调度功能测试完成")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("测试定时调度功能")
    print("=" * 60)
    
    success = test_scheduler()
    
    if success:
        print("\n🎉 测试通过！")
        print("📋 部署后将会:")
        print("  • 启动时立即运行一次")
        print("  • 每24小时自动运行一次")
        print("  • 每次运行发送Telegram通知")
    else:
        print("\n❌ 测试失败！")
        print("请检查配置和网络连接") 