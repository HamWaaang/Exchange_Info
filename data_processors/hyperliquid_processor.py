import pandas as pd
import json
import os
from datetime import datetime
from data_collectors.hyperliquid_collector import HyperliquidCollector

class HyperliquidProcessor:
    """
    Hyperliquid数据处理器
    """
    
    def __init__(self):
        self.data_dir = "data/raw/hyperliquid"
        self.collector = HyperliquidCollector()
        self.listing_cache_file = "data/hyperliquid_listing_cache.json"
        
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
        try:
            perpetual_listings = json.load(open(f"{self.data_dir}/perpetual_listings.json"))
            spot_listings = json.load(open(f"{self.data_dir}/spot_listings.json"))
            meta_info = json.load(open(f"{self.data_dir}/meta_info.json"))
            perpetuals_info = json.load(open(f"{self.data_dir}/perpetuals_info.json"))
            spot_info = json.load(open(f"{self.data_dir}/spot_info.json"))
            
            return {
                'perpetual_listings': perpetual_listings,
                'spot_listings': spot_listings,
                'meta_info': meta_info,
                'perpetuals_info': perpetuals_info,
                'spot_info': spot_info
            }
        except FileNotFoundError:
            print("数据文件不存在，请先运行数据收集")
            return None
    
    def process_data(self):
        """处理数据并生成CSV"""
        data = self.load_latest_data()
        if not data:
            return None
        
        print("开始处理Hyperliquid数据...")
        
        # 处理永续合约数据
        perpetual_data = []
        for listing in data['perpetual_listings']:
            perpetual_item = {
                'symbol': listing['symbol'],
                'baseAsset': listing['baseAsset'],
                'quoteAsset': listing['quoteAsset'],
                'status': listing['status'],
                'exchange': listing['exchange'],
                'type': listing['type'],
                'trading_type': '永续合约',
                'asset_id': listing['asset_id'],
                'decimals': listing['decimals'],
                'szDecimals': listing['szDecimals'],
                'priceDecimals': listing['priceDecimals'],
                'isLinear': listing['isLinear']
            }
            perpetual_data.append(perpetual_item)
        
        # 处理现货数据
        spot_data = []
        for listing in data['spot_listings']:
            spot_item = {
                'symbol': listing['symbol'],
                'baseAsset': listing['baseAsset'],
                'quoteAsset': listing['quoteAsset'],
                'status': listing['status'],
                'exchange': listing['exchange'],
                'type': listing['type'],
                'trading_type': '现货',
                'asset_id': listing['asset_id'],
                'index': listing['index'],
                'baseDecimals': listing['baseDecimals'],
                'quoteDecimals': listing['quoteDecimals']
            }
            spot_data.append(spot_item)
        
        # 合并数据
        all_data = perpetual_data + spot_data
        
        # 创建DataFrame
        df = pd.DataFrame(all_data)
        
        # 保存到CSV
        output_dir = "data/processed"
        os.makedirs(output_dir, exist_ok=True)
        csv_path = f"{output_dir}/hyperliquid_data.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        print(f"数据处理完成！共处理 {len(all_data)} 个交易对")
        print(f"永续合约: {len(perpetual_data)} 个")
        print(f"现货交易对: {len(spot_data)} 个")
        print(f"CSV文件保存至: {csv_path}")
        
        return df, csv_path
    
    def analyze_listing_trends(self, data):
        """
        分析上币趋势
        """
        if not data:
            return None
        
        # 合并永续合约和现货数据
        all_listings = data['perpetual_listings'] + data['spot_listings']
        df = pd.DataFrame(all_listings)
        
        # 按基础货币统计
        base_currency_counts = df['baseAsset'].value_counts()
        
        # 按报价货币统计
        quote_currency_counts = df['quoteAsset'].value_counts()
        
        # 按类型统计
        type_counts = df['type'].value_counts()
        
        return {
            'base_currency_counts': base_currency_counts.to_dict(),
            'quote_currency_counts': quote_currency_counts.to_dict(),
            'type_counts': type_counts.to_dict(),
            'total_listings': len(df)
        }
    
    def filter_promising_coins(self, data, criteria):
        """
        根据条件筛选有潜力的币种
        """
        if not data:
            return None
        
        # 合并永续合约和现货数据
        all_listings = data['perpetual_listings'] + data['spot_listings']
        df = pd.DataFrame(all_listings)
        
        # 应用筛选条件
        filtered_df = df.copy()
        
        if 'status' in criteria:
            filtered_df = filtered_df[filtered_df['status'] == criteria['status']]
        
        if 'type' in criteria:
            filtered_df = filtered_df[filtered_df['type'] == criteria['type']]
        
        if 'quote_currency' in criteria:
            filtered_df = filtered_df[filtered_df['quoteAsset'] == criteria['quote_currency']]
        
        return filtered_df.to_dict('records') 