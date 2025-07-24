import pandas as pd
import json
import os
from datetime import datetime
from data_collectors.coinbase_collector import CoinbaseCollector

class CoinbaseProcessor:
    """
    Coinbase数据处理器
    """
    
    def __init__(self):
        self.data_dir = "data/raw/coinbase"
        self.collector = CoinbaseCollector()
        
    def standardize_symbol(self, symbol):
        """标准化交易对格式，使其与Binance格式一致"""
        # Coinbase的格式通常是 BTC-USD，需要转换为 BTCUSD
        return symbol.replace('-', '')
    
    def load_latest_data(self):
        """加载最新的数据文件"""
        try:
            listings = json.load(open(f"{self.data_dir}/listings.json"))
            
            return {
                'listings': listings
            }
        except FileNotFoundError:
            print("数据文件不存在，请先运行数据收集")
            return None
        except Exception as e:
            print(f"加载数据文件失败: {e}")
            return None
    
    def process_data(self):
        """处理数据并生成CSV"""
        data = self.load_latest_data()
        if not data:
            return None
        
        print("开始处理Coinbase数据...")
        
        # 处理产品数据
        listings_data = []
        for listing in data['listings']:
            listings_data.append({
                'symbol': listing['symbol'],
                'baseCurrency': listing['baseCurrency'],
                'quoteCurrency': listing['quoteCurrency'],
                'status': listing['status'],
                'displayName': listing.get('displayName', ''),
                'fxStablecoin': listing.get('fxStablecoin', False),
                'maxSlippagePercentage': listing.get('maxSlippagePercentage', ''),
                'postOnly': listing.get('postOnly', False),
                'limitOnly': listing.get('limitOnly', False),
                'cancelOnly': listing.get('cancelOnly', False),
                'tradingDisabled': listing.get('tradingDisabled', False),
                'statusMessage': listing.get('statusMessage', ''),
                'auctionMode': listing.get('auctionMode', False),
                'exchange': listing['exchange'],
                'type': listing['type'],
                'trading_type': '现货'
            })
        
        # 创建DataFrame
        df = pd.DataFrame(listings_data)
        
        # 保存到CSV
        output_dir = "data/processed"
        os.makedirs(output_dir, exist_ok=True)
        csv_path = f"{output_dir}/coinbase_data.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        return df, csv_path 