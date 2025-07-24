# 主运行脚本
# 用于协调数据收集和处理的流程

from data_collectors.binance_collector import BinanceCollector
from data_processors.binance_processor import BinanceProcessor

def binance_main():
    print("开始收集Binance数据...")
    
    # 收集数据
    collector = BinanceCollector()
    data = collector.collect_all_data()
    
    print("Binance数据收集完成！")
    print(f"现货交易对数量: {len(data['spot_listings'])}")
    print(f"合约交易对数量: {len(data['futures_listings'])}")
    
    # 处理数据
    print("开始处理数据...")
    processor = BinanceProcessor()
    result = processor.process_data()
    
    if result:
        df, csv_path = result
        print(f"Binance数据处理完成！")
        print(f"总交易对数量: {len(df)}")
        print(f"CSV文件保存至: {csv_path}")
        print(f"现货交易对: {len(df[df['trading_type'] == '现货'])}")
        print(f"合约交易对: {len(df[df['trading_type'] == '合约'])}")
        print(f"现货+合约交易对: {len(df[df['trading_type'] == '现货+合约'])}")
    else:
        print("Binance数据处理失败！")

if __name__ == "__main__":
    binance_main() 