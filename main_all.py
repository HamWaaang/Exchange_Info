from main_binance import binance_main
from main_okx import okx_main
from main_coinbase import coinbase_main
from main_upbit import upbit_main
from main_hyperliquid import hyperliquid_main
import pandas as pd
import time

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
    print("\n�� 前10个最新上架的货币（多个交易所）:")
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

def main():
    print("=" * 60)
    print("开始收集所有交易所数据")
    print("=" * 60)
    
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

if __name__ == "__main__":
    main() 