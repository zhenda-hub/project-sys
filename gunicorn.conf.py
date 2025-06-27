import logging
import os

# 日志配置
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 日志格式
log_format = '%(asctime)s [%(levelname)s] %(message)s'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Gunicorn配置
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
timeout = 300  # 设置worker超时时间为300秒(5分钟)
keepalive = 5
max_requests = 1000
max_requests_jitter = 50

# 日志文件配置
accesslog = "-"  # 同时输出到控制台和文件
errorlog = "-"   # 同时输出到控制台和文件
loglevel = "info"
capture_output = True
logger_class = "gunicorn.glogging.Logger"
disable_redirect_access_to_syslog = True
