# Flask

**This is the back end of WitFuzz**

- [Flask](https://flask.net.cn/) Restful API
  - with crud examples
- MySQL [Flask-SQLAlchemy — Flask-SQLAlchemy Documentation (3.0.x) (palletsprojects.com)](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)

## dev
- install
```bash
pip install -r requirements.txt
```

- set config
```bash
cp config.py config_dev.py
```
> set mysql user and password in config_dev.py
> 
> create database `witfuzz`

- run
```bash
python app.py
```

- generate requirements.txt
```bash
pip install pipreqs
pipreqs ./ --force --encoding='utf-8'
```

## prod

- gunicorn
- gevent

### cmd

- Linux

```bash
gunicorn app:app -c gunicorn.conf.py
```

### docker

```bash
docker build -t flask_demo .
```

- Linux

```bash
docker run --name=flask_demo --network=host -d --rm flask_demo
```

- others

> docker-desktop doesn't support host network

```bash
docker run --name=flask_demo -p 5000:5000 -d --rm flask_demo
```

