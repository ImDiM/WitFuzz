FROM python:3.10-alpine
WORKDIR /back_end

# RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install gunicorn pymysql gevent -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone

COPY requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .
CMD ["gunicorn", "app:app", "-c", "gunicorn.conf.py"]
