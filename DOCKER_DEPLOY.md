# Docker 部署指南

## 🚀 快速部署

### 1. 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 2GB 可用内存
- 至少 10GB 可用磁盘空间

### 2. 一键部署

```bash
# 克隆项目（如果还没有）
git clone <your-repo-url>
cd Exchange_Info

# 给脚本执行权限
chmod +x deploy.sh manage.sh

# 一键部署
./deploy.sh
```

### 3. 手动部署

```bash
# 1. 创建必要目录
mkdir -p data/processed data/raw/binance data/raw/okx data/raw/coinbase data/raw/upbit data/raw/hyperliquid logs

# 2. 配置Telegram（可选）
# 编辑 telegram_config.py 文件

# 3. 构建并启动
docker-compose up -d

# 4. 查看状态
docker-compose ps
```

## 📋 管理命令

使用管理脚本：

```bash
# 启动服务
./manage.sh start

# 停止服务
./manage.sh stop

# 重启服务
./manage.sh restart

# 查看日志
./manage.sh logs

# 手动运行数据收集
./manage.sh run

# 查看服务状态
./manage.sh status

# 重新构建镜像
./manage.sh build

# 清理数据
./manage.sh clean

# 编辑配置
./manage.sh config

# 查看帮助
./manage.sh help
```

## 🔧 配置说明

### Telegram 配置

编辑 `telegram_config.py` 文件：

```python
# Bot Token - 从 @BotFather 获取
BOT_TOKEN = "你的BOT_TOKEN"

# Chat ID - 你的用户ID或群组ID
CHAT_ID = "你的CHAT_ID"

# 是否启用Telegram通知
ENABLE_TELEGRAM_NOTIFICATION = True
```

### 定时任务配置

编辑 `crontab` 文件：

```bash
# 每6小时运行一次
0 */6 * * * docker exec exchange-info-collector python3 main_all.py >> /app/logs/cron.log 2>&1

# 每天凌晨2点运行一次
0 2 * * * docker exec exchange-info-collector python3 main_all.py >> /app/logs/daily.log 2>&1
```

## 📊 数据持久化

数据存储在以下目录：

- `data/processed/` - 处理后的CSV文件
- `data/raw/` - 原始JSON数据
- `logs/` - 日志文件

这些目录会自动挂载到容器中，确保数据不会丢失。

## 🔍 监控和日志

### 查看实时日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f exchange-info
```

### 查看数据文件

```bash
# 查看处理后的数据
ls -la data/processed/

# 查看原始数据
ls -la data/raw/
```

## 🛠️ 故障排除

### 常见问题

1. **容器启动失败**
   ```bash
   # 查看详细错误信息
   docker-compose logs exchange-info
   
   # 重新构建镜像
   ./manage.sh build
   ```

2. **网络连接问题**
   ```bash
   # 检查网络连接
   docker-compose exec exchange-info ping google.com
   
   # 重启网络
   docker-compose restart
   ```

3. **权限问题**
   ```bash
   # 修复权限
   sudo chown -R $USER:$USER data/ logs/
   chmod 755 data/ logs/
   ```

4. **磁盘空间不足**
   ```bash
   # 清理Docker缓存
   docker system prune -a
   
   # 清理数据
   ./manage.sh clean
   ```

### 性能优化

1. **增加内存限制**
   在 `docker-compose.yml` 中添加：
   ```yaml
   services:
     exchange-info:
       deploy:
         resources:
           limits:
             memory: 4G
   ```

2. **使用SSD存储**
   确保数据目录在SSD上以获得更好的I/O性能。

## 🔄 更新部署

### 更新代码

```bash
# 拉取最新代码
git pull

# 重新构建镜像
./manage.sh build

# 重启服务
./manage.sh restart
```

### 备份数据

```bash
# 备份数据
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz data/ logs/

# 恢复数据
tar -xzf backup_YYYYMMDD_HHMMSS.tar.gz
```

## 📈 生产环境建议

1. **使用Docker Swarm或Kubernetes**进行容器编排
2. **配置监控系统**（如Prometheus + Grafana）
3. **设置日志聚合**（如ELK Stack）
4. **配置自动备份**策略
5. **使用负载均衡器**（如果需要多个实例）

## 🔒 安全建议

1. **使用非root用户**运行容器
2. **定期更新基础镜像**
3. **限制容器资源使用**
4. **配置防火墙规则**
5. **使用私有镜像仓库**

## 📞 支持

如果遇到问题，请：

1. 查看日志：`./manage.sh logs`
2. 检查状态：`./manage.sh status`
3. 重新构建：`./manage.sh build`
4. 提交Issue到项目仓库 