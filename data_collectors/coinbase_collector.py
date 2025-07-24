import requests
import json
import os
from datetime import datetime

class CoinbaseCollector:
    """
    Coinbase Exchange公共API数据收集器
    """
    
    def __init__(self):
        self.base_url = "https://api.exchange.coinbase.com"
        self.data_dir = "data/raw/coinbase"
        
    def get_products(self):
        """获取产品列表"""
        url = f"{self.base_url}/products"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取产品列表失败: {e}")
            return None
    
    def extract_listings(self, products_data):
        """从产品信息中提取已上架代币清单"""
        listings = []
        if products_data:
            for product in products_data:
                if product.get('status') == 'online':  # 只获取在线状态的产品
                    listing = {
                        'symbol': product['id'],
                        'baseCurrency': product['base_currency'],
                        'quoteCurrency': product['quote_currency'],
                        'status': product['status'],
                        'displayName': product.get('display_name', ''),
                        'fxStablecoin': product.get('fx_stablecoin', False),
                        'maxSlippagePercentage': product.get('max_slippage_percentage', ''),
                        'postOnly': product.get('post_only', False),
                        'limitOnly': product.get('limit_only', False),
                        'cancelOnly': product.get('cancel_only', False),
                        'tradingDisabled': product.get('trading_disabled', False),
                        'statusMessage': product.get('status_message', ''),
                        'auctionMode': product.get('auction_mode', False),
                        'exchange': 'coinbase',
                        'type': 'spot'
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
        print("开始收集Coinbase数据...")
        
        # 获取产品列表
        print("获取产品列表...")
        products_data = self.get_products()
        if products_data:
            listings = self.extract_listings(products_data)
            self.save_data(listings, "listings.json")
            print(f"数据收集完成！共收集到 {len(listings)} 个已上架产品")
        else:
            print("获取产品列表失败")
            return None
        
        return {
            'listings': listings
        } 