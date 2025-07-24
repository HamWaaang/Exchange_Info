from data_collectors.okx_collector import OKXCollector
from data_processors.okx_processor import OKXProcessor

def okx_main():
    print("开始收集OKX数据...")
    
    # 收集数据
    collector = OKXCollector()
    data = collector.collect_all_data()
    
    print("OKX数据收集完成！")
    print(f"现货交易对数量: {len(data['spot_listings'])}")
    print(f"合约交易对数量: {len(data['futures_listings'])}")
    print(f"永续合约数量: {len(data['swap_listings'])}")
    
    # 处理数据
    print("开始处理数据...")
    processor = OKXProcessor()
    result = processor.process_data()
    
    if result:
        df, csv_path = result
        print(f"OKX数据处理完成！")
        print(f"总交易对数量: {len(df)}")
        print(f"CSV文件保存至: {csv_path}")
        print(f"现货交易对: {len(df[df['trading_type'] == '现货'])}")
        print(f"永续合约交易对: {len(df[df['trading_type'] == '永续合约'])}")
        print(f"现货+永续交易对: {len(df[df['trading_type'] == '现货+永续'])}")
        print(f"现货+合约交易对: {len(df[df['trading_type'] == '现货+合约'])}")
        print(f"合约+永续交易对: {len(df[df['trading_type'] == '合约+永续'])}")
        print(f"现货+合约+永续交易对: {len(df[df['trading_type'] == '现货+合约+永续'])}")
    else:
        print("OKX数据处理失败！")

if __name__ == "__main__":
    okx_main() 