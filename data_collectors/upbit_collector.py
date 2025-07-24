import requests
import json
import os
from datetime import datetime, timedelta

class UpbitCollector:
    """
    Upbit交易所数据收集器
    """
    
    def __init__(self):
        self.base_url = "https://api.upbit.com/v1"
        self.data_dir = "data/raw/upbit"
        
    def get_markets(self):
        """
        获取市场列表（交易对信息）
        """
        url = f"{self.base_url}/market/all"
        response = requests.get(url)
        return response.json()
    
    def get_tickers(self, markets=None):
        """
        获取当前价格信息
        """
        if markets:
            # 如果提供了市场列表，获取指定市场的价格
            url = f"{self.base_url}/ticker"
            params = {'markets': ','.join(markets)}
            response = requests.get(url, params=params)
        else:
            # 获取所有市场的价格
            url = f"{self.base_url}/ticker"
            response = requests.get(url)
        return response.json()
    
    def get_orderbook(self, markets):
        """
        获取订单簿信息
        """
        url = f"{self.base_url}/orderbook"
        params = {'markets': ','.join(markets)}
        response = requests.get(url, params=params)
        return response.json()
    
    def extract_listings(self, markets_data):
        """从市场数据中提取已上架代币清单"""
        listings = []
        for market in markets_data:
            # Upbit的市场格式是 "QUOTE-BASE"，例如 "KRW-BTC", "USDT-ETH"
            market_symbol = market['market']
            if '-' in market_symbol:
                quote_currency, base_currency = market_symbol.split('-', 1)
                
                listing = {
                    'symbol': market_symbol,
                    'baseAsset': base_currency,
                    'quoteAsset': quote_currency,
                    'status': 'TRADING',  # Upbit API没有提供状态字段，默认为交易中
                    'exchange': 'upbit',
                    'type': 'spot',
                    'korean_name': market.get('korean_name', ''),
                    'english_name': market.get('english_name', '')
                }
                listings.append(listing)
        return listings
    
    def save_data(self, data, filename):
        """保存数据到JSON文件"""
        os.makedirs(self.data_dir, exist_ok=True)
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def collect_all_data(self):
        """收集所有已上架代币清单"""
        print("开始收集Upbit数据...")
        
        # 获取市场数据
        print("获取市场列表...")
        markets_data = self.get_markets()
        listings = self.extract_listings(markets_data)
        
        # 获取价格数据
        print("获取价格信息...")
        market_symbols = [market['market'] for market in markets_data]
        tickers_data = self.get_tickers(market_symbols)
        
        # 保存数据
        self.save_data(listings, "listings.json")
        self.save_data(tickers_data, "tickers.json")
        self.save_data(markets_data, "markets.json")
        
        print(f"数据收集完成！")
        print(f"交易对数量: {len(listings)}")
        print(f"价格数据数量: {len(tickers_data)}")
        
        return {
            'listings': listings,
            'tickers': tickers_data,
            'markets': markets_data
        } 