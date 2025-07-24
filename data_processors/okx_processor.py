import pandas as pd
import json
import os
from datetime import datetime
from data_collectors.okx_collector import OKXCollector

class OKXProcessor:
    def __init__(self):
        self.data_dir = "data/raw/okx"
        self.collector = OKXCollector()
        
    def standardize_symbol(self, symbol):
        """标准化交易对格式，移除'-'和'SWAP'等字样，使其与Binance格式一致"""
        # 移除'-'字符
        symbol = symbol.replace('-', '')
        
        # 移除'SWAP'字样（永续合约）
        symbol = symbol.replace('SWAP', '')
        
        # 移除'USDT'后面的'-'（如果有的话）
        if symbol.endswith('USDT-'):
            symbol = symbol[:-1]
        
        # 移除'USDC'后面的'-'（如果有的话）
        if symbol.endswith('USDC-'):
            symbol = symbol[:-1]
        
        # 移除'BTC'后面的'-'（如果有的话）
        if symbol.endswith('BTC-'):
            symbol = symbol[:-1]
        
        # 移除'ETH'后面的'-'（如果有的话）
        if symbol.endswith('ETH-'):
            symbol = symbol[:-1]
        
        return symbol
    
    def load_latest_data(self):
        """加载最新的数据文件"""
        try:
            spot_listings = json.load(open(f"{self.data_dir}/spot_listings.json"))
            futures_listings = json.load(open(f"{self.data_dir}/futures_listings.json"))
            swap_listings = json.load(open(f"{self.data_dir}/swap_listings.json"))
            
            return {
                'spot_listings': spot_listings,
                'futures_listings': futures_listings,
                'swap_listings': swap_listings
            }
        except FileNotFoundError:
            print("数据文件不存在，请先运行数据收集")
            return None
    
    def process_data(self):
        """处理数据并生成CSV"""
        data = self.load_latest_data()
        if not data:
            return None
        
        print("开始处理OKX数据...")
        
        # 处理现货数据
        spot_data = []
        for listing in data['spot_listings']:
            spot_data.append({
                'symbol': listing['symbol'],
                'baseCurrency': listing['baseCurrency'],
                'quoteCurrency': listing['quoteCurrency'],
                'state': listing['state'],
                'category': listing['category'],
                'listTime': listing['listTime'],
                'exchange': listing['exchange'],
                'type': listing['type'],
                'trading_type': '现货'
            })
        
        # 处理合约数据
        futures_data = []
        for listing in data['futures_listings']:
            futures_data.append({
                'symbol': listing['symbol'],
                'baseCurrency': listing['baseCurrency'],
                'quoteCurrency': listing['quoteCurrency'],
                'state': listing['state'],
                'category': listing['category'],
                'contractType': listing.get('contractType', ''),
                'listTime': listing['listTime'],
                'expTime': listing.get('expTime', ''),
                'exchange': listing['exchange'],
                'type': listing['type'],
                'trading_type': '合约'
            })
        
        # 处理永续合约数据
        swap_data = []
        for listing in data['swap_listings']:
            swap_data.append({
                'symbol': listing['symbol'],
                'baseCurrency': listing['baseCurrency'],
                'quoteCurrency': listing['quoteCurrency'],
                'state': listing['state'],
                'category': listing['category'],
                'listTime': listing['listTime'],
                'exchange': listing['exchange'],
                'type': listing['type'],
                'trading_type': '永续合约'
            })
        
        # 合并数据
        all_data = spot_data + futures_data + swap_data
        
        # 创建DataFrame
        df = pd.DataFrame(all_data)
        
        # 保存到CSV
        output_dir = "data/processed"
        os.makedirs(output_dir, exist_ok=True)
        csv_path = f"{output_dir}/okx_data.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        return df, csv_path 