from data_collectors.coinbase_collector import CoinbaseCollector
from data_processors.coinbase_processor import CoinbaseProcessor
import os

def coinbase_main(skip_collection=False):
    if not skip_collection:
        print("开始收集Coinbase数据...")
        
        # 收集数据
        collector = CoinbaseCollector()
        data = collector.collect_all_data()
        
        if not data:
            print("Coinbase数据收集失败！")
            return
        
        print("Coinbase数据收集完成！")
        print(f"已上架产品数: {len(data['listings'])}")
    else:
        print("检测到已有数据，跳过数据收集...")
    
    # 处理数据
    print("开始处理数据...")
    processor = CoinbaseProcessor()
    result = processor.process_data()
    
    if result:
        df, csv_path = result
        print(f"Coinbase数据处理完成！")
        print(f"总产品数量: {len(df)}")
        print(f"CSV文件保存至: {csv_path}")
        
        # 显示一些统计信息
        if len(df) > 0:
            print(f"在线状态产品数: {len(df[df['status'] == 'online'])}")
            print(f"交易禁用产品数: {len(df[df['tradingDisabled'] == True])}")
            print(f"仅限价单产品数: {len(df[df['limitOnly'] == True])}")
        else:
            print("没有有效的数据可以显示")
    else:
        print("Coinbase数据处理失败！")

def check_existing_data():
    """检查是否已有数据文件"""
    listings_file = "data/raw/coinbase/listings.json"
    return os.path.exists(listings_file)

if __name__ == "__main__":
    try:
        # 检查是否已有数据，如果有就直接跳过收集
        if check_existing_data():
            coinbase_main(skip_collection=True)
        else:
            coinbase_main(skip_collection=False)
    except KeyboardInterrupt:
        print("\n用户中断了程序")
    except Exception as e:
        print(f"程序运行出错: {e}") 