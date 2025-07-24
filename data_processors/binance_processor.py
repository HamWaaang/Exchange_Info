import pandas as pd
import json
import os
from datetime import datetime
from data_collectors.binance_collector import BinanceCollector

class BinanceProcessor:
    def __init__(self):
        self.data_dir = "data/raw/binance"
        self.collector = BinanceCollector()
        self.listing_cache_file = "data/listing_cache.json"
        
    def load_listing_cache(self):
        """加载上架时间缓存"""
        if os.path.exists(self.listing_cache_file):
            with open(self.listing_cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_listing_cache(self, cache):
        """保存上架时间缓存"""
        os.makedirs(os.path.dirname(self.listing_cache_file), exist_ok=True)
        with open(self.listing_cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
    
    def load_latest_data(self):
        """加载最新的数据文件"""
        # 直接加载固定文件名的数据
        try:
            spot_listings = json.load(open(f"{self.data_dir}/spot_listings.json"))
            futures_listings = json.load(open(f"{self.data_dir}/futures_listings.json"))
            
            return {
                'spot_listings': spot_listings,
                'futures_listings': futures_listings
            }
        except FileNotFoundError:
            print("数据文件不存在，请先运行数据收集")
            return None
    
    def process_data(self):
        """处理数据并生成CSV"""
        data = self.load_latest_data()
        if not data:
            return None
        
        print("开始处理Binance数据...")
        
        # 处理现货数据
        spot_data = []
        for listing in data['spot_listings']:
            spot_data.append({
                'symbol': listing['symbol'],
                'baseAsset': listing['baseAsset'],
                'quoteAsset': listing['quoteAsset'],
                'status': listing['status'],
                'exchange': listing['exchange'],
                'type': listing['type'],
                'trading_type': '现货'
            })
        
        # 处理合约数据
        futures_data = []
        for listing in data['futures_listings']:
            futures_data.append({
                'symbol': listing['symbol'],
                'baseAsset': listing['baseAsset'],
                'quoteAsset': listing['quoteAsset'],
                'status': listing['status'],
                'contractType': listing.get('contractType', ''),
                'exchange': listing['exchange'],
                'type': listing['type'],
                'trading_type': '合约'
            })
        
        # 合并数据
        all_data = spot_data + futures_data
        
        # 创建DataFrame
        df = pd.DataFrame(all_data)
        
        # 保存到CSV
        output_dir = "data/processed"
        os.makedirs(output_dir, exist_ok=True)
        csv_path = f"{output_dir}/binance_data.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        return df, csv_path 