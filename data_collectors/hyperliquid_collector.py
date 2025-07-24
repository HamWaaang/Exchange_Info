import requests
import json
import os
from datetime import datetime, timedelta

class HyperliquidCollector:
    """
    Hyperliquid交易所数据收集器
    """
    
    def __init__(self):
        self.base_url = "https://api.hyperliquid.xyz"
        self.data_dir = "data/raw/hyperliquid"
        
    def get_meta_info(self):
        """
        获取元信息（包含永续合约和现货信息）
        """
        url = f"{self.base_url}/info"
        response = requests.post(url, json={"type": "meta"})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"获取元信息失败: {response.status_code}")
            return None
    
    def get_perpetuals_info(self):
        """
        获取永续合约信息
        """
        url = f"{self.base_url}/info"
        response = requests.post(url, json={"type": "perpetuals"})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"获取永续合约信息失败: {response.status_code}")
            return None
    
    def get_spot_info(self):
        """
        获取现货信息
        """
        url = f"{self.base_url}/info"
        response = requests.post(url, json={"type": "spot"})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"获取现货信息失败: {response.status_code}")
            return None
    
    def extract_perpetual_listings(self, meta_info):
        """从元信息中提取永续合约清单"""
        listings = []
        if meta_info and 'universe' in meta_info:
            for i, asset in enumerate(meta_info['universe']):
                listing = {
                    'symbol': asset.get('name', ''),
                    'baseAsset': asset.get('name', ''),
                    'quoteAsset': 'USD',  # Hyperliquid永续合约通常以USD计价
                    'status': 'TRADING',
                    'exchange': 'hyperliquid',
                    'type': 'perpetual',
                    'asset_id': i,
                    'decimals': asset.get('decimals', 0),
                    'szDecimals': asset.get('szDecimals', 0),
                    'priceDecimals': asset.get('priceDecimals', 0),
                    'isLinear': asset.get('isLinear', True)
                }
                listings.append(listing)
        return listings
    
    def extract_spot_listings(self, spot_meta):
        """从现货元信息中提取现货清单"""
        listings = []
        if spot_meta and 'spotMeta' in spot_meta:
            for i, spot_info in enumerate(spot_meta['spotMeta']):
                listing = {
                    'symbol': f"{spot_info.get('base', '')}/{spot_info.get('quote', '')}",
                    'baseAsset': spot_info.get('base', ''),
                    'quoteAsset': spot_info.get('quote', ''),
                    'status': 'TRADING',
                    'exchange': 'hyperliquid',
                    'type': 'spot',
                    'asset_id': 10000 + i,  # 现货资产ID = 10000 + index
                    'index': i,
                    'baseDecimals': spot_info.get('baseDecimals', 0),
                    'quoteDecimals': spot_info.get('quoteDecimals', 0)
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
        print("开始收集Hyperliquid数据...")
        
        # 获取元信息
        print("获取元信息...")
        meta_info = self.get_meta_info()
        
        # 获取永续合约信息
        print("获取永续合约信息...")
        perpetuals_info = self.get_perpetuals_info()
        
        # 获取现货信息
        print("获取现货信息...")
        spot_info = self.get_spot_info()
        
        # 提取永续合约列表
        perpetual_listings = self.extract_perpetual_listings(meta_info)
        
        # 提取现货列表
        spot_listings = self.extract_spot_listings(spot_info)
        
        # 保存数据
        self.save_data(perpetual_listings, "perpetual_listings.json")
        self.save_data(spot_listings, "spot_listings.json")
        self.save_data(meta_info, "meta_info.json")
        self.save_data(perpetuals_info, "perpetuals_info.json")
        self.save_data(spot_info, "spot_info.json")
        
        print(f"数据收集完成！")
        print(f"永续合约数量: {len(perpetual_listings)}")
        print(f"现货交易对数量: {len(spot_listings)}")
        
        return {
            'perpetual_listings': perpetual_listings,
            'spot_listings': spot_listings,
            'meta_info': meta_info,
            'perpetuals_info': perpetuals_info,
            'spot_info': spot_info
        } 