import requests
import json
import os
from datetime import datetime

class OKXCollector:
    def __init__(self):
        self.base_url = "https://www.okx.com"
        self.data_dir = "data/raw/okx"
        
    def get_spot_instruments(self):
        """获取现货交易产品信息"""
        url = f"{self.base_url}/api/v5/public/instruments"
        params = {'instType': 'SPOT'}
        response = requests.get(url, params=params)
        return response.json()
    
    def get_futures_instruments(self):
        """获取合约交易产品信息"""
        url = f"{self.base_url}/api/v5/public/instruments"
        params = {'instType': 'FUTURES'}
        response = requests.get(url, params=params)
        return response.json()
    
    def get_swap_instruments(self):
        """获取永续合约交易产品信息"""
        url = f"{self.base_url}/api/v5/public/instruments"
        params = {'instType': 'SWAP'}
        response = requests.get(url, params=params)
        return response.json()
    
    def extract_spot_listings(self, instruments_data):
        """从现货产品信息中提取已上架代币清单"""
        listings = []
        if 'data' in instruments_data:
            for instrument in instruments_data['data']:
                if instrument['state'] == 'live':  # 只获取活跃的代币
                    listing = {
                        'symbol': instrument['instId'],
                        'baseCurrency': instrument['baseCcy'],
                        'quoteCurrency': instrument['quoteCcy'],
                        'state': instrument['state'],
                        'category': instrument['category'],
                        'listTime': instrument['listTime'],
                        'exchange': 'okx',
                        'type': 'spot'
                    }
                    listings.append(listing)
        return listings
    
    def extract_futures_listings(self, instruments_data):
        """从合约产品信息中提取已上架代币清单"""
        listings = []
        if 'data' in instruments_data:
            for instrument in instruments_data['data']:
                if instrument['state'] == 'live':  # 只获取活跃的代币
                    listing = {
                        'symbol': instrument['instId'],
                        'baseCurrency': instrument['baseCcy'],
                        'quoteCurrency': instrument['quoteCcy'],
                        'state': instrument['state'],
                        'category': instrument['category'],
                        'contractType': instrument.get('ctType', ''),
                        'listTime': instrument['listTime'],
                        'expTime': instrument.get('expTime', ''),
                        'exchange': 'okx',
                        'type': 'futures'
                    }
                    listings.append(listing)
        return listings
    
    def extract_swap_listings(self, instruments_data):
        """从永续合约产品信息中提取已上架代币清单"""
        listings = []
        if 'data' in instruments_data:
            for instrument in instruments_data['data']:
                if instrument['state'] == 'live':  # 只获取活跃的代币
                    listing = {
                        'symbol': instrument['instId'],
                        'baseCurrency': instrument['baseCcy'],
                        'quoteCurrency': instrument['quoteCcy'],
                        'state': instrument['state'],
                        'category': instrument['category'],
                        'listTime': instrument['listTime'],
                        'exchange': 'okx',
                        'type': 'swap'
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
        print("开始收集OKX数据...")
        
        # 获取现货数据
        print("获取现货产品信息...")
        spot_instruments = self.get_spot_instruments()
        spot_listings = self.extract_spot_listings(spot_instruments)
        
        # 获取合约数据
        print("获取合约产品信息...")
        futures_instruments = self.get_futures_instruments()
        futures_listings = self.extract_futures_listings(futures_instruments)
        
        # 获取永续合约数据
        print("获取永续合约产品信息...")
        swap_instruments = self.get_swap_instruments()
        swap_listings = self.extract_swap_listings(swap_instruments)
        
        # 保存数据
        self.save_data(spot_listings, "spot_listings.json")
        self.save_data(futures_listings, "futures_listings.json")
        self.save_data(swap_listings, "swap_listings.json")
        
        print(f"数据收集完成！")
        print(f"现货代币数量: {len(spot_listings)}")
        print(f"合约代币数量: {len(futures_listings)}")
        print(f"永续合约代币数量: {len(swap_listings)}")
        
        return {
            'spot_listings': spot_listings,
            'futures_listings': futures_listings,
            'swap_listings': swap_listings
        } 