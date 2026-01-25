FROM python:3.8-slim

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_CACHE_DIR=/tmp/uv-cache

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 复制依赖文件
COPY pyproject.toml README.md ./

# 使用 uv 安装依赖
RUN uv sync --no-dev

# 复制项目文件
COPY . .

# 创建静态文件和媒体文件目录
RUN mkdir -p /app/static /app/media /app/collected_static

# 收集静态文件
RUN uv run python manage.py collectstatic --noinput

CMD ["sh", "-c", "uv run python manage.py runserver 0.0.0.0:8000"]