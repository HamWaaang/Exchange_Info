import pandas as pd
import json
import os
from datetime import datetime
from data_collectors.upbit_collector import UpbitCollector

class UpbitProcessor:
    """
    Upbit数据处理器
    """
    
    def __init__(self):
        self.data_dir = "data/raw/upbit"
        self.collector = UpbitCollector()
        self.listing_cache_file = "data/upbit_listing_cache.json"
        
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
            listings = json.load(open(f"{self.data_dir}/listings.json"))
            tickers = json.load(open(f"{self.data_dir}/tickers.json"))
            markets = json.load(open(f"{self.data_dir}/markets.json"))
            
            return {
                'listings': listings,
                'tickers': tickers,
                'markets': markets
            }
        except FileNotFoundError:
            print("数据文件不存在，请先运行数据收集")
            return None
    
    def process_data(self):
        """处理数据并生成CSV"""
        data = self.load_latest_data()
        if not data:
            return None
        
        print("开始处理Upbit数据...")
        
        # 创建ticker数据的字典，方便查找
        tickers_dict = {ticker['market']: ticker for ticker in data['tickers']}
        
        # 处理列表数据
        processed_data = []
        for listing in data['listings']:
            ticker_info = tickers_dict.get(listing['symbol'], {})
            
            processed_item = {
                'symbol': listing['symbol'],
                'baseAsset': listing['baseAsset'],
                'quoteAsset': listing['quoteAsset'],
                'status': listing['status'],
                'exchange': listing['exchange'],
                'type': listing['type'],
                'trading_type': '现货',
                'korean_name': listing.get('korean_name', ''),
                'english_name': listing.get('english_name', ''),
                'trade_price': ticker_info.get('trade_price', 0),
                'change': ticker_info.get('change', ''),
                'change_rate': ticker_info.get('change_rate', 0),
                'high_price': ticker_info.get('high_price', 0),
                'low_price': ticker_info.get('low_price', 0),
                'acc_trade_volume_24h': ticker_info.get('acc_trade_volume_24h', 0),
                'acc_trade_price_24h': ticker_info.get('acc_trade_price_24h', 0),
                'timestamp': ticker_info.get('timestamp', 0)
            }
            processed_data.append(processed_item)
        
        # 创建DataFrame
        df = pd.DataFrame(processed_data)
        
        # 保存到CSV
        output_dir = "data/processed"
        os.makedirs(output_dir, exist_ok=True)
        csv_path = f"{output_dir}/upbit_data.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        print(f"数据处理完成！共处理 {len(processed_data)} 个交易对")
        print(f"CSV文件保存至: {csv_path}")
        
        return df, csv_path
    
    def analyze_listing_trends(self, data):
        """
        分析上币趋势
        """
        if not data or not data['listings']:
            return None
        
        df = pd.DataFrame(data['listings'])
        
        # 按基础货币统计
        base_currency_counts = df['baseAsset'].value_counts()
        
        # 按报价货币统计
        quote_currency_counts = df['quoteAsset'].value_counts()
        
        # 按状态统计
        status_counts = df['status'].value_counts()
        
        return {
            'base_currency_counts': base_currency_counts.to_dict(),
            'quote_currency_counts': quote_currency_counts.to_dict(),
            'status_counts': status_counts.to_dict(),
            'total_listings': len(df)
        }
    
    def filter_promising_coins(self, data, criteria):
        """
        根据条件筛选有潜力的币种
        """
        if not data:
            return None
        
        df = pd.DataFrame(data['listings'])
        
        # 应用筛选条件
        filtered_df = df.copy()
        
        if 'min_volume' in criteria:
            # 这里需要结合ticker数据来筛选交易量
            pass
        
        if 'status' in criteria:
            filtered_df = filtered_df[filtered_df['status'] == criteria['status']]
        
        if 'quote_currency' in criteria:
            filtered_df = filtered_df[filtered_df['quoteAsset'] == criteria['quote_currency']]
        
        return filtered_df.to_dict('records') 