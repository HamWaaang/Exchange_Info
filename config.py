# 配置文件
# 存储API密钥、配置参数等

# 交易所API配置
EXCHANGE_CONFIGS = {
    'binance': {
        'api_key': '',
        'api_secret': '',
        'base_url': 'https://api.binance.com',
        'testnet': False
    },
    'okx': {
        'api_key': '',
        'api_secret': '',
        'passphrase': '',
        'base_url': 'https://www.okx.com',
        'testnet': False
    },
    'coinbase': {
        'api_key': '',
        'api_secret': '',
        'base_url': 'https://api.coinbase.com',
        'testnet': False
    },
    'upbit': {
        'api_key': '',
        'api_secret': '',
        'base_url': 'https://api.upbit.com',
        'testnet': False
    }
}

# 数据存储配置
DATA_CONFIG = {
    'raw_data_dir': 'data/raw',
    'processed_data_dir': 'data/processed',
    'reports_dir': 'data/reports'
}

# 筛选条件配置
FILTER_CRITERIA = {
    'min_volume_24h': 1000000,  # 最小24小时交易量
    'min_market_cap': 10000000,  # 最小市值
    'max_price_change_24h': 50,  # 最大24小时价格变化百分比
    'min_listing_age_days': 7    # 最小上线天数
} 