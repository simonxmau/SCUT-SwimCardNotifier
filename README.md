# SCUT-SwimCardNotifier

该项目用于解决 **华南理工大学（SCUT）**： `华工道明游泳馆`、`华工东区游泳场` 次卡使用变动通知的问题。

主要通过定时执行任务，爬取东区游泳馆次卡使用情况，当次卡使用次数发生变动时，通过钉钉机器人发送消息通知。

实现技术分别使用了 FastAPI + Celery + Redis：

- FastAPI 实现 Session 帐号添加
- Celery 实现定时任务调度和异步任务执行
- Redis 作为 Celery 的 Broker 和 Backend，还有数据持久化

## 小程序分析

1. 两个游泳馆使用同一套系统，接口也是一样的
2. 数据似乎没有隔离，通过 code 换取 OpenID 和 Session
3. Session 有效期暂确定为 ≤ 1 天，通过每分钟带 Session 请求接口可以保活

## 项目逻辑

- 通过 POST `/add` 接口添加帐号订单信息
- 系统每 15 分钟调用一次帐户的卡数量接口，用于保持 Session 的有效性
- 系统在每天 06-30~8:00 和 18:30~22:00 两个时间段中每 30 秒查询一次卡信息，如果剩余次数有变动，则会通过钉钉机器人发送消息通知

## 运行配置

> 项目所有配置均通过环境变量文件（`.env`）进行配置

参考配置

```yaml
# 基础配置
LOG_LEVEL=info # 日志等级

# Redis 配置
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=3

# Celery 配置
CELERY_BROKER=redis://${REDIS_HOST}:${REDIS_PORT}/4
CELERY_BACKEND=redis://${REDIS_HOST}:${REDIS_PORT}/5

# 钉钉机器人配置
SECRET=SECb499ff7fa...b46caa93ba562f8c157195eb9a
WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=d2ab9a489a9538355ec574a3...b9efaf94ef6a7d34461a
```

## 运行

#### 调试运行

**运行 beat**

```shell
celery -A app.celery.tasks beat --loglevel=debug
```

**运行 worker**

```shell
celery -A app.celery.tasks worker --loglevel=debug
```

**运行 api**

```shell
python main.py

# 开发调试的时候可以加热更新参数 `--reload`
#uvicorn main:app
```

#### Docker 运行

```shell
docker-compose up
```