from main_binance import binance_main
from main_okx import okx_main
from main_coinbase import coinbase_main
from main_upbit import upbit_main
from main_hyperliquid import hyperliquid_main
from telegram_notifier import TelegramNotifier
from telegram_config import BOT_TOKEN, CHAT_ID, ENABLE_TELEGRAM_NOTIFICATION
import pandas as pd
import time
import os
import json
from datetime import datetime

def load_exchange_data():
    """加载五个交易所的数据"""
    # 加载Coinbase数据
    coinbase_df = pd.read_csv('data/processed/coinbase_data.csv')
    
    # 加载OKX数据
    okx_df = pd.read_csv('data/processed/okx_data.csv')
    
    # 加载Binance数据
    binance_df = pd.read_csv('data/processed/binance_data.csv')
    
    # 加载Upbit数据
    upbit_df = pd.read_csv('data/processed/upbit_data.csv')
    
    # 加载Hyperliquid数据
    hyperliquid_df = pd.read_csv('data/processed/hyperliquid_data.csv')
    
    return coinbase_df, okx_df, binance_df, upbit_df, hyperliquid_df

def extract_base_currencies(df, exchange_name, base_col_name):
    """提取基础货币并标记交易所和类型"""
    # 创建结果DataFrame
    result = df[[base_col_name, 'type', 'trading_type']].copy()
    
    # 为所有交易所添加虚拟时间戳（基于数据顺序）
    result['listTime'] = range(len(result))
    
    result['exchange'] = exchange_name
    
    # 重命名列以统一格式
    result = result.rename(columns={base_col_name: 'baseCurrency'})
    
    # 只保留状态为活跃的交易对
    if 'status' in df.columns:
        if exchange_name == 'coinbase':
            result = result[df['status'] == 'online']
        elif exchange_name == 'binance':
            result = result[df['status'] == 'TRADING']
        elif exchange_name == 'okx':
            result = result[df['state'] == 'live']
        elif exchange_name == 'upbit':
            result = result[df['status'] == 'TRADING']
        elif exchange_name == 'hyperliquid':
            result = result[df['status'] == 'TRADING']
    
    return result

def create_comparison_table():
    """创建交易所对比表格"""
    # 加载数据
    coinbase_df, okx_df, binance_df, upbit_df, hyperliquid_df = load_exchange_data()
    
    # 提取基础货币
    coinbase_currencies = extract_base_currencies(coinbase_df, 'coinbase', 'baseCurrency')
    okx_currencies = extract_base_currencies(okx_df, 'okx', 'baseCurrency')
    binance_currencies = extract_base_currencies(binance_df, 'binance', 'baseAsset')
    upbit_currencies = extract_base_currencies(upbit_df, 'upbit', 'baseAsset')
    hyperliquid_currencies = extract_base_currencies(hyperliquid_df, 'hyperliquid', 'baseAsset')
    
    # 合并所有数据
    all_currencies = pd.concat([coinbase_currencies, okx_currencies, binance_currencies, upbit_currencies, hyperliquid_currencies], ignore_index=True)
    
    # 去重并创建唯一的基础货币列表
    unique_currencies = all_currencies['baseCurrency'].unique()
    
    # 创建结果DataFrame
    result_data = []
    
    for currency in unique_currencies:
        # 获取该货币在所有交易所的数据
        currency_data = all_currencies[all_currencies['baseCurrency'] == currency]
        
        # 初始化行数据
        row = {
            'baseCurrency': currency,
            'coinbase_spot': 0,
            'coinbase_futures': 0,
            'okx_spot': 0,
            'okx_futures': 0,
            'binance_spot': 0,
            'binance_futures': 0,
            'upbit_spot': 0,
            'upbit_futures': 0,
            'hyperliquid_spot': 0,
            'hyperliquid_futures': 0,
            'coinbase_time': float('inf'),
            'okx_time': float('inf'),
            'binance_time': float('inf'),
            'upbit_time': float('inf'),
            'hyperliquid_time': float('inf')
        }
        
        # 统计各交易所的现货和合约，并记录各交易所的时间
        for _, record in currency_data.iterrows():
            exchange = record['exchange']
            trading_type = record['trading_type']
            type_name = record['type']
            list_time = record['listTime']
            
            # 记录各交易所的时间
            if exchange == 'coinbase' and list_time < row['coinbase_time']:
                row['coinbase_time'] = list_time
            elif exchange == 'okx' and list_time < row['okx_time']:
                row['okx_time'] = list_time
            elif exchange == 'binance' and list_time < row['binance_time']:
                row['binance_time'] = list_time
            elif exchange == 'upbit' and list_time < row['upbit_time']:
                row['upbit_time'] = list_time
            elif exchange == 'hyperliquid' and list_time < row['hyperliquid_time']:
                row['hyperliquid_time'] = list_time
            
            if trading_type == '现货' or type_name == 'spot':
                if exchange == 'coinbase':
                    row['coinbase_spot'] = 1
                elif exchange == 'okx':
                    row['okx_spot'] = 1
                elif exchange == 'binance':
                    row['binance_spot'] = 1
                elif exchange == 'upbit':
                    row['upbit_spot'] = 1
                elif exchange == 'hyperliquid':
                    row['hyperliquid_spot'] = 1
            elif trading_type == '合约' or trading_type == '永续合约' or type_name == 'futures' or type_name == 'perpetual':
                if exchange == 'coinbase':
                    row['coinbase_futures'] = 1
                elif exchange == 'okx':
                    row['okx_futures'] = 1
                elif exchange == 'binance':
                    row['binance_futures'] = 1
                elif exchange == 'upbit':
                    row['upbit_futures'] = 1
                elif exchange == 'hyperliquid':
                    row['hyperliquid_futures'] = 1
        
        # 计算不同交易所的数量（同一交易所的现货和合约视为一个）
        exchanges_count = 0
        if row['coinbase_spot'] or row['coinbase_futures']:
            exchanges_count += 1
        if row['okx_spot'] or row['okx_futures']:
            exchanges_count += 1
        if row['binance_spot'] or row['binance_futures']:
            exchanges_count += 1
        if row['upbit_spot'] or row['upbit_futures']:
            exchanges_count += 1
        if row['hyperliquid_spot'] or row['hyperliquid_futures']:
            exchanges_count += 1
        
        row['total_exchanges'] = exchanges_count
        
        # 计算最晚上架时间（只考虑实际有上架的交易所）
        valid_times = []
        if row['coinbase_spot'] or row['coinbase_futures']:
            valid_times.append(row['coinbase_time'])
        if row['okx_spot'] or row['okx_futures']:
            valid_times.append(row['okx_time'])
        if row['binance_spot'] or row['binance_futures']:
            valid_times.append(row['binance_time'])
        if row['upbit_spot'] or row['upbit_futures']:
            valid_times.append(row['upbit_time'])
        if row['hyperliquid_spot'] or row['hyperliquid_futures']:
            valid_times.append(row['hyperliquid_time'])
        
        # 使用最晚的时间作为排序标志
        if valid_times:
            row['latest_time'] = max(valid_times)
        else:
            row['latest_time'] = float('inf')
        
        result_data.append(row)
    
    # 创建结果DataFrame
    result_df = pd.DataFrame(result_data)
    
    # 重新排列列顺序，将total_exchanges放在最前面
    columns_order = ['total_exchanges', 'baseCurrency', 'coinbase_spot', 'coinbase_futures', 
                    'okx_spot', 'okx_futures', 'binance_spot', 'binance_futures', 
                    'upbit_spot', 'upbit_futures', 'hyperliquid_spot', 'hyperliquid_futures', 'latest_time']
    result_df = result_df[columns_order]
    
    # 分离只有一个交易所的代币和多个交易所的代币
    single_exchange = result_df[result_df['total_exchanges'] == 1].copy()
    multi_exchange = result_df[result_df['total_exchanges'] > 1].copy()
    
    # 对多个交易所的代币按最晚上架时间降序排列
    multi_exchange = multi_exchange.sort_values('latest_time', ascending=False)
    
    # 对只有一个交易所的代币按最晚上架时间降序排列
    single_exchange = single_exchange.sort_values('latest_time', ascending=False)
    
    # 移除latest_time列（仅用于排序）
    multi_exchange = multi_exchange.drop('latest_time', axis=1)
    single_exchange = single_exchange.drop('latest_time', axis=1)
    
    return multi_exchange, single_exchange

def run_exchange_comparison():
    """运行交易所对比分析"""
    print("\n" + "=" * 60)
    print("📊 开始交易所对比分析...")
    print("=" * 60)
    
    # 创建对比表格
    multi_exchange_df, single_exchange_df = create_comparison_table()
    
    # 保存多个交易所的代币表格
    multi_output_file = 'data/processed/exchange_comparison.csv'
    multi_exchange_df.to_csv(multi_output_file, index=False, encoding='utf-8-sig')
    
    # 保存单个交易所的代币表格
    single_output_file = 'data/processed/single_exchange_tokens.csv'
    single_exchange_df.to_csv(single_output_file, index=False, encoding='utf-8-sig')
    
    print(f"✅ 多个交易所对比表格已保存到: {multi_output_file}")
    print(f"✅ 单个交易所代币表格已保存到: {single_output_file}")
    print(f"📊 总共发现 {len(multi_exchange_df) + len(single_exchange_df)} 个不同的基础货币")
    
    # 显示统计信息
    print("\n📈 统计信息:")
    print(f"   🏆 在5个交易所都有上架的货币数量: {len(multi_exchange_df[multi_exchange_df['total_exchanges'] == 5])}")
    print(f"   🥇 在4个交易所上架的货币数量: {len(multi_exchange_df[multi_exchange_df['total_exchanges'] == 4])}")
    print(f"   🥈 在3个交易所上架的货币数量: {len(multi_exchange_df[multi_exchange_df['total_exchanges'] == 3])}")
    print(f"   🥉 在2个交易所上架的货币数量: {len(multi_exchange_df[multi_exchange_df['total_exchanges'] == 2])}")
    print(f"   💎 只在1个交易所上架的货币数量: {len(single_exchange_df)}")
    
    # 显示前10个最新上架的货币（多个交易所）
    print("\n🔥 前10个最新上架的货币（多个交易所）:")
    top_10_multi = multi_exchange_df.head(10)
    for _, row in top_10_multi.iterrows():
        exchanges = []
        if row['coinbase_spot'] or row['coinbase_futures']: 
            exchanges.append('Coinbase')
        if row['okx_spot'] or row['okx_futures']: 
            exchanges.append('OKX')
        if row['binance_spot'] or row['binance_futures']: 
            exchanges.append('Binance')
        if row['upbit_spot'] or row['upbit_futures']: 
            exchanges.append('Upbit')
        if row['hyperliquid_spot'] or row['hyperliquid_futures']: 
            exchanges.append('Hyperliquid')
        
        print(f"   {row['baseCurrency']}: {row['total_exchanges']}个交易所 ({', '.join(exchanges)})")
    
    # 显示前10个最新上架的货币（单个交易所）
    print("\n💎 前10个最新上架的货币（单个交易所）:")
    top_10_single = single_exchange_df.head(10)
    for _, row in top_10_single.iterrows():
        exchanges = []
        if row['coinbase_spot'] or row['coinbase_futures']: 
            exchanges.append('Coinbase')
        if row['okx_spot'] or row['okx_futures']: 
            exchanges.append('OKX')
        if row['binance_spot'] or row['binance_futures']: 
            exchanges.append('Binance')
        if row['upbit_spot'] or row['upbit_futures']: 
            exchanges.append('Upbit')
        if row['hyperliquid_spot'] or row['hyperliquid_futures']: 
            exchanges.append('Hyperliquid')
        
        print(f"   {row['baseCurrency']}: {row['total_exchanges']}个交易所 ({', '.join(exchanges)})")

def detect_changes():
    """检测数据文件是否有变化"""
    print("\n" + "=" * 60)
    print("📊 检测数据文件是否有变化...")
    print("=" * 60)

    # 获取当前时间
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"当前时间: {current_time}")

    # 获取上次运行时的文件时间
    last_run_time_file = 'last_run_time.txt'
    if os.path.exists(last_run_time_file):
        with open(last_run_time_file, 'r') as f:
            last_run_time_str = f.read().strip()
        print(f"上次运行时间: {last_run_time_str}")
    else:
        print("未找到上次运行时间文件，将视为首次运行。")

    # 获取所有数据文件的修改时间
    data_files = [
        'data/processed/binance_data.csv',
        'data/processed/okx_data.csv',
        'data/processed/coinbase_data.csv',
        'data/processed/upbit_data.csv',
        'data/processed/hyperliquid_data.csv'
    ]

    print("\n📁 数据文件:")
    for file_path in data_files:
        if os.path.exists(file_path):
            file_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y%m%d_%H%M%S")
            print(f"  - {file_path}: 修改时间 {file_modified_time}")
        else:
            print(f"  - {file_path}: 文件不存在")

    # 比较当前时间与上次运行时间
    if os.path.exists(last_run_time_file):
        with open(last_run_time_file, 'r') as f:
            last_run_time_str = f.read().strip()
        
        if last_run_time_str == current_time:
            print("\n📝 数据文件没有变化。")
        else:
            print("\n📝 数据文件有变化！")
            print(f"  上次运行时间: {last_run_time_str}")
            print(f"  当前时间: {current_time}")
    else:
        print("\n📝 数据文件有变化！")
        print(f"  当前时间: {current_time}")

    # 更新上次运行时间文件
    with open(last_run_time_file, 'w') as f:
        f.write(current_time)
    print(f"✅ 上次运行时间已更新到: {last_run_time_file}")

def compare_token_changes():
    """比较代币变化并打印详细信息"""
    print("\n" + "=" * 60)
    print("🔄 比较代币变化...")
    print("=" * 60)
    
    current_file = 'data/processed/exchange_comparison.csv'
    previous_file = 'data/processed/exchange_comparison_previous.csv'
    
    # 检查当前文件是否存在
    if not os.path.exists(current_file):
        print(f"❌ 当前对比文件不存在: {current_file}")
        return None
    
    # 读取当前数据
    try:
        current_df = pd.read_csv(current_file)
        print(f"✅ 成功读取当前数据，共 {len(current_df)} 个代币")
    except Exception as e:
        print(f"❌ 读取当前数据失败: {e}")
        return None
    
    # 检查是否有之前的数据文件
    if not os.path.exists(previous_file):
        print(f"📝 未找到之前的数据文件，将当前数据保存为基准")
        current_df.to_csv(previous_file, index=False, encoding='utf-8-sig')
        print(f"✅ 当前数据已保存为基准文件: {previous_file}")
        return None
    
    # 读取之前的数据
    try:
        previous_df = pd.read_csv(previous_file)
        print(f"✅ 成功读取之前的数据，共 {len(previous_df)} 个代币")
    except Exception as e:
        print(f"❌ 读取之前数据失败: {e}")
        return None
    
    # 比较变化
    changes = []
    changes_data = {
        'new_tokens': [],
        'removed_tokens': [],
        'status_changes': []
    }
    
    # 获取所有代币的集合
    current_tokens = set(current_df['baseCurrency'])
    previous_tokens = set(previous_df['baseCurrency'])
    
    # 新增的代币
    new_tokens = current_tokens - previous_tokens
    if new_tokens:
        print(f"\n🆕 新增代币 ({len(new_tokens)} 个):")
        for token in sorted(new_tokens):
            token_data = current_df[current_df['baseCurrency'] == token].iloc[0]
            exchanges = []
            if token_data['coinbase_spot'] or token_data['coinbase_futures']: exchanges.append('Coinbase')
            if token_data['okx_spot'] or token_data['okx_futures']: exchanges.append('OKX')
            if token_data['binance_spot'] or token_data['binance_futures']: exchanges.append('Binance')
            if token_data['upbit_spot'] or token_data['upbit_futures']: exchanges.append('Upbit')
            if token_data['hyperliquid_spot'] or token_data['hyperliquid_futures']: exchanges.append('Hyperliquid')
            print(f"   + {token}: {token_data['total_exchanges']}个交易所 ({', '.join(exchanges)})")
            changes.append(f"新增: {token}")
            changes_data['new_tokens'].append({
                'name': token,
                'exchanges': token_data['total_exchanges']
            })
    
    # 删除的代币
    removed_tokens = previous_tokens - current_tokens
    if removed_tokens:
        print(f"\n❌ 删除代币 ({len(removed_tokens)} 个):")
        for token in sorted(removed_tokens):
            # 获取删除代币之前的交易所信息
            previous_token_data = previous_df[previous_df['baseCurrency'] == token].iloc[0]
            exchanges = []
            if previous_token_data['coinbase_spot'] or previous_token_data['coinbase_futures']: exchanges.append('Coinbase')
            if previous_token_data['okx_spot'] or previous_token_data['okx_futures']: exchanges.append('OKX')
            if previous_token_data['binance_spot'] or previous_token_data['binance_futures']: exchanges.append('Binance')
            if previous_token_data['upbit_spot'] or previous_token_data['upbit_futures']: exchanges.append('Upbit')
            if previous_token_data['hyperliquid_spot'] or previous_token_data['hyperliquid_futures']: exchanges.append('Hyperliquid')
            print(f"   - {token}: 之前在 {previous_token_data['total_exchanges']}个交易所 ({', '.join(exchanges)})")
            changes.append(f"删除: {token}")
            changes_data['removed_tokens'].append({
                'name': token,
                'exchanges': previous_token_data['total_exchanges']
            })
    
    # 状态变化的代币
    common_tokens = current_tokens & previous_tokens
    status_changes = []
    
    for token in common_tokens:
        current_row = current_df[current_df['baseCurrency'] == token].iloc[0]
        previous_row = previous_df[previous_df['baseCurrency'] == token].iloc[0]
        
        # 比较各交易所状态
        exchanges = ['coinbase_spot', 'coinbase_futures', 'okx_spot', 'okx_futures', 
                    'binance_spot', 'binance_futures', 'upbit_spot', 'upbit_futures', 
                    'hyperliquid_spot', 'hyperliquid_futures']
        
        changes_detail = []
        exchange_changes = []
        
        for exchange in exchanges:
            if current_row[exchange] != previous_row[exchange]:
                exchange_name = exchange.replace('_spot', '').replace('_futures', '').title()
                type_name = '现货' if 'spot' in exchange else '合约'
                if current_row[exchange] == 1:
                    changes_detail.append(f"{exchange_name}新增{type_name}")
                    exchange_changes.append(f"{exchange_name} (+{type_name})")
                else:
                    changes_detail.append(f"{exchange_name}移除{type_name}")
                    exchange_changes.append(f"{exchange_name} (-{type_name})")
        
        if changes_detail:
            status_changes.append({
                'token': token,
                'changes': changes_detail,
                'exchange_changes': exchange_changes,
                'current_exchanges': current_row['total_exchanges'],
                'previous_exchanges': previous_row['total_exchanges']
            })
            changes_data['status_changes'].append({
                'token': token,
                'details': ', '.join(changes_detail),
                'previous_exchanges': previous_row['total_exchanges'],
                'current_exchanges': current_row['total_exchanges']
            })
    
    if status_changes:
        print(f"\n🔄 状态变化代币 ({len(status_changes)} 个):")
        for change in status_changes:
            print(f"   📊 {change['token']}:")
            print(f"      变化详情: {', '.join(change['changes'])}")
            print(f"      交易所变化: {', '.join(change['exchange_changes'])}")
            print(f"      交易所数量: {change['previous_exchanges']} → {change['current_exchanges']}")
            changes.append(f"变化: {change['token']}")
    
    # 总结
    if not changes:
        print("\n✅ 没有发现任何变化")
    else:
        print(f"\n📊 变化总结:")
        print(f"   新增代币: {len(new_tokens)} 个")
        print(f"   删除代币: {len(removed_tokens)} 个")
        print(f"   状态变化: {len(status_changes)} 个")
        print(f"   总变化数: {len(changes)} 个")
    
    # 保存当前数据作为下次比较的基准
    current_df.to_csv(previous_file, index=False, encoding='utf-8-sig')
    print(f"\n✅ 当前数据已保存为新的基准文件: {previous_file}")
    
    # 返回变化数据
    return changes_data

def get_latest_tokens():
    """获取最新的代币清单"""
    try:
        # 读取当前数据
        current_df = pd.read_csv('data/processed/exchange_comparison.csv')
        
        # 分离多交易所和单交易所代币
        multi_exchange_df = current_df[current_df['total_exchanges'] > 1].copy()
        single_exchange_df = current_df[current_df['total_exchanges'] == 1].copy()
        
        # 按时间排序（假设数据是按时间顺序排列的）
        multi_exchange_df = multi_exchange_df.head(10)  # 取最新的10个
        single_exchange_df = single_exchange_df.head(10)  # 取最新的10个
        
        # 转换为字典格式
        latest_tokens = {
            'multi_exchange': multi_exchange_df.to_dict('records'),
            'single_exchange': single_exchange_df.to_dict('records')
        }
        
        return latest_tokens
        
    except Exception as e:
        print(f"⚠️  获取最新代币清单失败: {e}")
        return None

def main():
    # 初始化Telegram通知器（如果启用）
    notifier = None
    if ENABLE_TELEGRAM_NOTIFICATION and BOT_TOKEN != "YOUR_BOT_TOKEN_HERE" and CHAT_ID != "YOUR_CHAT_ID_HERE":
        try:
            notifier = TelegramNotifier(BOT_TOKEN, CHAT_ID)
            print("✅ Telegram通知器初始化成功")
        except Exception as e:
            print(f"⚠️  Telegram通知器初始化失败: {e}")
            notifier = None
    else:
        print("⚠️  Telegram通知未配置或已禁用")
    
    print("=" * 60)
    print("开始收集所有交易所数据")
    print("=" * 60)
    
    # 发送开始通知
    if notifier:
        try:
            notifier.send_start_notification()
        except Exception as e:
            print(f"⚠️  Telegram通知发送失败: {e}")
    
    # 收集Binance数据
    print("\n🟡 开始收集Binance数据...")
    start_time = time.time()
    binance_main()
    binance_time = time.time() - start_time
    print(f"✅ Binance数据收集完成，耗时: {binance_time:.2f}秒")
    
    # 收集OKX数据
    print("\n🟢 开始收集OKX数据...")
    start_time = time.time()
    okx_main()
    okx_time = time.time() - start_time
    print(f"✅ OKX数据收集完成，耗时: {okx_time:.2f}秒")
    
    # 收集Coinbase数据
    print("\n🔵 开始收集Coinbase数据...")
    start_time = time.time()
    coinbase_main()
    coinbase_time = time.time() - start_time
    print(f"✅ Coinbase数据收集完成，耗时: {coinbase_time:.2f}秒")
    
    # 收集Upbit数据
    print("\n🟣 开始收集Upbit数据...")
    start_time = time.time()
    upbit_main()
    upbit_time = time.time() - start_time
    print(f"✅ Upbit数据收集完成，耗时: {upbit_time:.2f}秒")
    
    # 收集Hyperliquid数据
    print("\n🟠 开始收集Hyperliquid数据...")
    start_time = time.time()
    hyperliquid_main()
    hyperliquid_time = time.time() - start_time
    print(f"✅ Hyperliquid数据收集完成，耗时: {hyperliquid_time:.2f}秒")
    
    # 运行交易所对比分析
    comparison_start_time = time.time()
    run_exchange_comparison()
    comparison_time = time.time() - comparison_start_time
    print(f"\n✅ 交易所对比分析完成，耗时: {comparison_time:.2f}秒")

    # 检测数据文件是否有变化
    detect_changes()
    
    # 比较代币变化
    changes_data = compare_token_changes()
    
    # 总结
    total_time = binance_time + okx_time + coinbase_time + upbit_time + hyperliquid_time + comparison_time
    print("\n" + "=" * 60)
    print("🎉 所有交易所数据收集和分析完成！")
    print(f"📊 总耗时: {total_time:.2f}秒")
    print(f"📈 Binance: {binance_time:.2f}秒")
    print(f"📈 OKX: {okx_time:.2f}秒")
    print(f"📈 Coinbase: {coinbase_time:.2f}秒")
    print(f"📈 Upbit: {upbit_time:.2f}秒")
    print(f"📈 Hyperliquid: {hyperliquid_time:.2f}秒")
    print(f"📈 对比分析: {comparison_time:.2f}秒")
    print("=" * 60)
    
    print("\n📁 生成的文件:")
    print("  - data/processed/binance_data.csv (代币清单)")
    print("  - data/processed/okx_data.csv (代币清单)")
    print("  - data/processed/coinbase_data.csv (代币清单)")
    print("  - data/processed/upbit_data.csv (代币清单)")
    print("  - data/processed/hyperliquid_data.csv (代币清单)")
    print("  - data/processed/exchange_comparison.csv (多交易所对比)")
    print("  - data/processed/single_exchange_tokens.csv (单交易所代币)")
    print("  - data/raw/binance/ (原始JSON数据)")
    print("  - data/raw/okx/ (原始JSON数据)")
    print("  - data/raw/coinbase/ (原始JSON数据)")
    print("  - data/raw/upbit/ (原始JSON数据)")
    print("  - data/raw/hyperliquid/ (原始JSON数据)")
    
    # 准备结果数据
    results = {
        'total_time': total_time,
        'binance_time': binance_time,
        'okx_time': okx_time,
        'coinbase_time': coinbase_time,
        'upbit_time': upbit_time,
        'hyperliquid_time': hyperliquid_time,
        'comparison_time': comparison_time
    }
    
    # 获取数据统计
    try:
        current_df = pd.read_csv('data/processed/exchange_comparison.csv')
        multi_exchange_df = current_df[current_df['total_exchanges'] > 1]
        single_exchange_df = current_df[current_df['total_exchanges'] == 1]
        
        results.update({
            'total_tokens': len(current_df),
            'multi_exchange_tokens': len(multi_exchange_df),
            'single_exchange_tokens': len(single_exchange_df)
        })
    except Exception as e:
        print(f"⚠️  获取数据统计失败: {e}")
        results.update({
            'total_tokens': 0,
            'multi_exchange_tokens': 0,
            'single_exchange_tokens': 0
        })
    
    # 准备变化总结
    changes_summary = None
    if changes_data:
        changes_summary = {
            'new_tokens': len(changes_data.get('new_tokens', [])),
            'removed_tokens': len(changes_data.get('removed_tokens', [])),
            'status_changes': len(changes_data.get('status_changes', [])),
            'total_changes': len(changes_data.get('new_tokens', [])) + len(changes_data.get('removed_tokens', [])) + len(changes_data.get('status_changes', []))
        }
    
    # 获取最新代币清单
    latest_tokens = get_latest_tokens()
    
    # 发送完成通知
    if notifier:
        try:
            notifier.send_completion_notification(results, changes_summary, latest_tokens)
            
            # 发送最新代币清单通知
            if latest_tokens:
                notifier.send_latest_tokens_notification(latest_tokens)
            
            # 如果有变化，发送详细变化通知
            if changes_data and any(changes_data.values()):
                notifier.send_changes_notification(changes_data)
        except Exception as e:
            print(f"⚠️  Telegram通知发送失败: {e}")

if __name__ == "__main__":
    main() 