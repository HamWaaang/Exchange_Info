from data_collectors.hyperliquid_collector import HyperliquidCollector
from data_processors.hyperliquid_processor import HyperliquidProcessor

def hyperliquid_main():
    print("开始收集Hyperliquid数据...")
    
    # 收集数据
    collector = HyperliquidCollector()
    data = collector.collect_all_data()
    
    print("Hyperliquid数据收集完成！")
    print(f"永续合约数量: {len(data['perpetual_listings'])}")
    print(f"现货交易对数量: {len(data['spot_listings'])}")
    print(f"总交易对数量: {len(data['perpetual_listings']) + len(data['spot_listings'])}")
    
    # 处理数据
    print("开始处理数据...")
    processor = HyperliquidProcessor()
    result = processor.process_data()
    
    if result:
        df, csv_path = result
        print(f"Hyperliquid数据处理完成！")
        print(f"总交易对数量: {len(df)}")
        print(f"CSV文件保存至: {csv_path}")
        
        # 显示类型分布
        type_counts = df['trading_type'].value_counts()
        print(f"交易类型分布:")
        for trading_type, count in type_counts.items():
            print(f"  {trading_type}: {count} 个")
        
        # 显示报价货币分布
        quote_currency_counts = df['quoteAsset'].value_counts()
        print(f"报价货币分布:")
        for currency, count in quote_currency_counts.items():
            print(f"  {currency}: {count} 个交易对")
    else:
        print("Hyperliquid数据处理失败！")

if __name__ == "__main__":
    hyperliquid_main() 