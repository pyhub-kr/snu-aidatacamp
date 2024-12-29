ARG PYTHON_VERSION=3.13-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    pip install gunicorn 'uvicorn[standard]' && \
    rm -rf /root/.cache/
COPY . /code

RUN python manage.py collectstatic --noinput

# 외부 데이터베이스가 설정되면 제거하기
ENV DATABASE_URL sqlite:////code/db.sqlite3
RUN python manage.py migrate && python manage.py load_melon_songs

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "mysite.asgi:application"]
