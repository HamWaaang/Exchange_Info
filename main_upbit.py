from data_collectors.upbit_collector import UpbitCollector
from data_processors.upbit_processor import UpbitProcessor

def upbit_main():
    print("开始收集Upbit数据...")
    
    # 收集数据
    collector = UpbitCollector()
    data = collector.collect_all_data()
    
    print("Upbit数据收集完成！")
    print(f"交易对数量: {len(data['listings'])}")
    print(f"价格数据数量: {len(data['tickers'])}")
    print(f"市场数据数量: {len(data['markets'])}")
    
    # 处理数据
    print("开始处理数据...")
    processor = UpbitProcessor()
    result = processor.process_data()
    
    if result:
        df, csv_path = result
        print(f"Upbit数据处理完成！")
        print(f"总交易对数量: {len(df)}")
        print(f"CSV文件保存至: {csv_path}")
        
        # 显示报价货币分布
        quote_currency_counts = df['quoteAsset'].value_counts()
        print(f"报价货币分布:")
        for currency, count in quote_currency_counts.items():
            print(f"  {currency}: {count} 个交易对")
    else:
        print("Upbit数据处理失败！")

if __name__ == "__main__":
    upbit_main() 