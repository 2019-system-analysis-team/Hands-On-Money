# 容器编排
## 基本结构
本系统中的容器编排采用下述结构：
- 使用 docker 部署一个或多个 REST API 服务器实例
- 使用 docker 部署一个 Caddy 实例
- 使用 Caddy 均衡多个 REST API 服务器负载
- 使用 Caddy 作为静态文件服务器
- 使用 docker-compose 作为容器编排工具

## docker compose
```
npm run
```
参见 [frontend dockerfile](https://github.com/2019-system-analysis-team/Hands-On-Money/blob/dev-fend/fend/Dockerfile)

```
python3 run.py
```
参见 [backend dockerfile](https://github.com/2019-system-analysis-team/Hands-On-Money/blob/dev-bend/bend/Dockerfile)


## Caddy 配置
[tbd]