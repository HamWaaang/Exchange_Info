from data_collectors.binance_collector import BinanceCollector
from data_processors.binance_processor import BinanceProcessor

def test_cache():
    print("测试缓存机制...")
    
    # 测试收集器
    collector = BinanceCollector()
    
    # 测试获取几个交易对的上架时间
    test_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
    
    for symbol in test_symbols:
        print(f"获取 {symbol} 现货上架时间...")
        listing_time = collector.get_listing_time_from_klines(symbol, is_spot=True)
        print(f"{symbol} 现货上架时间: {listing_time}")
    
    # 测试处理器
    processor = BinanceProcessor()
    
    # 测试缓存加载
    cache = processor.load_listing_cache()
    print(f"当前缓存数量: {len(cache)}")
    
    # 测试缓存保存
    test_cache = {'BTCUSDT_spot': '2020-01-01', 'ETHUSDT_spot': '2020-01-02'}
    processor.save_listing_cache(test_cache)
    print("测试缓存已保存")

if __name__ == "__main__":
    test_cache() 