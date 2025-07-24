import requests
import json
import os
from datetime import datetime, timedelta

class BinanceCollector:
    def __init__(self):
        self.spot_base_url = "https://api.binance.com"
        self.futures_base_url = "https://fapi.binance.com"
        self.data_dir = "data/raw/binance"
        
    def get_spot_exchange_info(self):
        """获取现货交易所信息"""
        url = f"{self.spot_base_url}/api/v3/exchangeInfo"
        response = requests.get(url)
        return response.json()
    
    def get_futures_exchange_info(self):
        """获取合约交易所信息"""
        url = f"{self.futures_base_url}/fapi/v1/exchangeInfo"
        response = requests.get(url)
        return response.json()
    
    def extract_spot_listings(self, exchange_info):
        """从现货交易所信息中提取已上架代币清单"""
        listings = []
        if 'symbols' in exchange_info:
            for symbol in exchange_info['symbols']:
                if symbol['status'] == 'TRADING':  # 只获取交易中的代币
                    listing = {
                        'symbol': symbol['symbol'],
                        'baseAsset': symbol['baseAsset'],
                        'quoteAsset': symbol['quoteAsset'],
                        'status': symbol['status'],
                        'permissions': symbol.get('permissions', []),
                        'exchange': 'binance',
                        'type': 'spot'
                    }
                    listings.append(listing)
        return listings
    
    def extract_futures_listings(self, exchange_info):
        """从合约交易所信息中提取已上架代币清单"""
        listings = []
        if 'symbols' in exchange_info:
            for symbol in exchange_info['symbols']:
                if symbol['status'] == 'TRADING':  # 只获取交易中的代币
                    listing = {
                        'symbol': symbol['symbol'],
                        'baseAsset': symbol['baseAsset'],
                        'quoteAsset': symbol['quoteAsset'],
                        'status': symbol['status'],
                        'contractType': symbol.get('contractType', ''),
                        'deliveryDate': symbol.get('deliveryDate', 0),
                        'onboardDate': symbol.get('onboardDate', 0),
                        'exchange': 'binance',
                        'type': 'futures'
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
        print("开始收集Binance数据...")
        
        # 获取现货数据
        print("获取现货交易所信息...")
        spot_exchange_info = self.get_spot_exchange_info()
        spot_listings = self.extract_spot_listings(spot_exchange_info)
        
        # 获取合约数据
        print("获取合约交易所信息...")
        futures_exchange_info = self.get_futures_exchange_info()
        futures_listings = self.extract_futures_listings(futures_exchange_info)
        
        # 保存数据
        self.save_data(spot_listings, "spot_listings.json")
        self.save_data(futures_listings, "futures_listings.json")
        
        print(f"数据收集完成！")
        print(f"现货代币数量: {len(spot_listings)}")
        print(f"合约代币数量: {len(futures_listings)}")
        
        return {
            'spot_listings': spot_listings,
            'futures_listings': futures_listings
        } 