# Docker部署文件清单

## 📁 必需文件

### 核心程序文件
```
main_all.py                    # 主程序
telegram_notifier.py           # Telegram通知模块
telegram_config.py             # Telegram配置文件
main_binance.py               # Binance数据收集
main_okx.py                   # OKX数据收集
main_coinbase.py              # Coinbase数据收集
main_upbit.py                 # Upbit数据收集
main_hyperliquid.py           # Hyperliquid数据收集
```

### 数据收集器目录
```
data_collectors/
├── __init__.py
├── binance_collector.py
├── okx_collector.py
├── coinbase_collector.py
├── upbit_collector.py
└── hyperliquid_collector.py
```

### 数据处理器目录
```
data_processors/
├── __init__.py
├── binance_processor.py
├── okx_processor.py
├── coinbase_processor.py
├── upbit_processor.py
└── hyperliquid_processor.py
```

### Docker部署文件
```
Dockerfile                    # Docker镜像构建文件
docker-compose.yml           # 容器编排配置
requirements.txt              # Python依赖包
.dockerignore                # Docker构建忽略文件
deploy.sh                    # 一键部署脚本
scheduler.sh                 # 定时运行脚本
monitor.sh                   # 监控脚本
README_DOCKER.md             # 部署说明文档
```

## 🚀 快速部署步骤

### 1. 上传文件到服务器
```bash
# 创建项目目录
mkdir exchange-info
cd exchange-info

# 上传所有必需文件
# (使用scp、rsync或其他方式)
```

### 2. 配置Telegram
```bash
# 编辑配置文件
nano telegram_config.py
```

### 3. 一键部署
```bash
# 添加执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

## 📊 文件大小估算

- 核心程序文件: ~50KB
- 数据收集器: ~30KB
- 数据处理器: ~30KB
- Docker文件: ~5KB
- 总计: ~115KB

## 🔧 最小化部署

如果只需要基本功能，可以进一步精简：

### 最小文件集
```
main_all.py
telegram_notifier.py
telegram_config.py
data_collectors/
data_processors/
Dockerfile
docker-compose.yml
requirements.txt
deploy.sh
```

### 移除的文件
- 文档文件 (*.md)
- 测试文件
- 示例文件
- 临时文件

## 📝 部署检查清单

- [ ] 所有必需文件已上传
- [ ] Telegram配置已设置
- [ ] 数据目录已创建
- [ ] Docker已安装
- [ ] docker-compose已安装
- [ ] 网络连接正常
- [ ] 权限设置正确

## 🎯 部署验证

部署完成后，验证以下功能：

1. **容器状态**
```bash
docker-compose ps
```

2. **日志查看**
```bash
docker-compose logs -f
```

3. **手动运行**
```bash
docker-compose exec exchange-info python main_all.py
```

4. **Telegram通知**
- 检查是否收到开始通知
- 检查是否收到完成通知
- 检查是否收到代币清单

5. **数据文件**
```bash
ls -la data/processed/
``` 