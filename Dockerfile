FROM python:3.8-slim

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建静态文件和媒体文件目录
RUN mkdir -p /app/static /app/media /app/collected_static

# 收集静态文件
RUN python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]