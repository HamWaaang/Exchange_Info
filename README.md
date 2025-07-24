# 加密货币交易所数据分析项目

## 项目简介
本项目用于收集和分析各大加密货币交易所的上币信息，帮助筛选有潜力的项目。

## 项目结构
```
Exchange_Info/
├── data_collectors/          # 数据收集器
│   ├── __init__.py
│   ├── base_collector.py     # 基础收集器类
│   ├── binance_collector.py  # Binance数据收集
│   ├── okx_collector.py      # OKX数据收集
│   ├── coinbase_collector.py # Coinbase数据收集
│   └── upbit_collector.py    # Upbit数据收集
├── data_processors/          # 数据处理器
│   ├── __init__.py
│   ├── base_processor.py     # 基础处理器类
│   ├── binance_processor.py  # Binance数据处理
│   ├── okx_processor.py      # OKX数据处理
│   ├── coinbase_processor.py # Coinbase数据处理
│   └── upbit_processor.py    # Upbit数据处理
├── main.py                   # 主运行脚本
├── config.py                 # 配置文件
├── requirements.txt          # 依赖包
└── README.md                 # 项目说明
```

## 支持的交易所
- Binance
- OKX
- Coinbase
- Upbit

## 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法
1. 配置API密钥（在config.py中）
2. 运行主脚本：
```bash
python main.py
```

## 功能特性
- 多交易所数据收集
- 数据清洗和处理
- 项目筛选算法
- 趋势分析
- 报告生成 