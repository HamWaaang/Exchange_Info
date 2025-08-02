# Docker 部署指南

## 🚀 快速部署

### 1. 准备文件

确保以下文件在项目根目录：
- `main_all.py` - 主程序
- `telegram_notifier.py` - Telegram通知模块
- `telegram_config.py` - Telegram配置文件
- `main_*.py` - 各交易所数据收集模块
- `data_collectors/` - 数据收集器目录
- `data_processors/` - 数据处理器目录

### 2. 配置Telegram

编辑 `telegram_config.py`：
```python
BOT_TOKEN = "你的Bot Token"
CHAT_ID = "你的Chat ID"
ENABLE_TELEGRAM_NOTIFICATION = True
```

### 3. 一键部署

```bash
./deploy.sh
```

## 📋 部署文件说明

### 核心文件
- `Dockerfile` - Docker镜像构建文件
- `docker-compose.yml` - 容器编排配置
- `requirements.txt` - Python依赖包
- `.dockerignore` - Docker构建忽略文件
- `deploy.sh` - 一键部署脚本

### 数据持久化
- `./data/` 目录挂载到容器内
- 数据文件在宿主机和容器间同步
- 重启容器数据不会丢失

## 🔧 常用命令

### 启动服务
```bash
docker-compose up -d
```

### 查看日志
```bash
docker-compose logs -f
```

### 停止服务
```bash
docker-compose down
```

### 重启服务
```bash
docker-compose restart
```

### 进入容器
```bash
docker-compose exec exchange-info bash
```

### 手动运行
```bash
docker-compose exec exchange-info python main_all.py
```

## ⏰ 定时运行

项目已配置为自动定时运行：

### 运行模式
- **启动时立即运行一次** - 部署后立即开始数据收集
- **每24小时自动运行一次** - 每天定时执行数据收集
- **每次运行都发送Telegram通知** - 包含开始、完成、代币清单等通知

### 调度配置
```yaml
# docker-compose.yml 中的配置
command: ["./scheduler.sh"]
```

### 监控运行状态
```bash
# 查看调度器日志
tail -f data/scheduler.log

# 使用监控脚本
./monitor.sh

# 查看容器日志
docker-compose logs -f
```

## 📊 数据文件

部署后，数据文件保存在：
- `./data/processed/` - 处理后的CSV文件
- `./data/raw/` - 原始JSON数据
- `./data/processed/exchange_comparison.csv` - 主要对比文件

## 🔍 故障排除

### 1. 容器启动失败
```bash
# 查看详细错误信息
docker-compose logs

# 重新构建镜像
docker-compose build --no-cache
```

### 2. 网络连接问题
```bash
# 检查容器网络
docker-compose exec exchange-info ping google.com
```

### 3. 权限问题
```bash
# 确保数据目录权限正确
chmod -R 755 data/
```

### 4. Telegram通知失败
- 检查 `telegram_config.py` 配置
- 确认Bot Token和Chat ID正确
- 检查网络连接

## 📱 监控

### 查看运行状态
```bash
docker-compose ps
```

### 查看资源使用
```bash
docker stats exchange-info-collector
```

### 查看数据文件
```bash
ls -la data/processed/
```

## 🔄 更新部署

### 1. 停止服务
```bash
docker-compose down
```

### 2. 重新构建
```bash
docker-compose build --no-cache
```

### 3. 启动服务
```bash
docker-compose up -d
```

## 📝 注意事项

1. **数据备份**: 定期备份 `./data/` 目录
2. **配置安全**: 不要将 `telegram_config.py` 提交到Git
3. **资源监控**: 注意容器内存和CPU使用情况
4. **网络稳定**: 确保服务器网络连接稳定
5. **日志管理**: 定期清理日志文件

## 🎯 最佳实践

1. **定时运行**: 建议每小时运行一次
2. **数据备份**: 每天备份重要数据文件
3. **监控告警**: 设置容器状态监控
4. **日志轮转**: 配置日志文件轮转
5. **安全更新**: 定期更新Docker镜像 