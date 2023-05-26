import datetime
from datetime import datetime as dt
import random
import string

import jwt
from flask import jsonify, request, current_app
from flask.blueprints import Blueprint
from flask_cors import cross_origin
from flask_mail import Message

from back_end.database import db
from back_end.database import User
from back_end.database.db import redis_db, mail

user = Blueprint('user', __name__)


@user.get('<string:id>')
def get_user(id):
    u = User.query.filter(User.id == id).first()
    if u is None:
        return jsonify({
            'code': 404
        })
    return jsonify({
        'code': 200,
        'data': {
            'user': u.to_json()
        }
    })


@user.post('')
def create_user():
    data = request.json

    if len(User.query.filter(User.id == data['id']).all()) > 0:
        return jsonify({
            'code': 500
        })
    u = User(
        id=data['id'],
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    print(u)
    db.session.add(u)
    db.session.commit()

    return jsonify({
        'code': 200,
        'data': {
            'user': u.to_json()
        }
    })


@user.post('<string:id>/username/<string:username>')
def set_username(id, username):
    u = User.query.filter(User.id == id).first()
    if u is None:
        return jsonify({
            'code': 404
        })
    u.username = username
    db.session.commit()
    return jsonify({
        'code': 200,
        'data': {
            'user': u.to_json()
        }
    })


@user.delete('<string:id>')
def delete_user(id):
    print(id)
    u = User.query.filter(User.id == id).first()
    if u is None:
        return jsonify({
            'code': 404
        })
    db.session.delete(u)
    db.session.commit()

    return jsonify({
        'code': 200,
        'data': {
            'user': u.to_json()
        }
    })


@user.post('login')
def login():
    data = request.json
    loginuser = User.query.filter(User.email == data['email']).first()
    if (loginuser is not None) & (loginuser.password == data['password']):
        headers = {
            "alg": "HS256",
            "typ": "JWT",
        }
        payload = {
            "id": str(loginuser.id)
        }
        token = jwt.encode(payload=payload, key='secret', algorithm='HS256', headers=headers)
        print(token)
        return jsonify({
            'code': 200,
            'data': {
                'token': token,
                'name': loginuser.name,
                'user_id': loginuser.id,
                'result': True
            }
        })
    else:
        return jsonify({
            'code': 403,
            'data': {
                'result': False
            }
        })


@user.route('getinfo', methods=['POST'])
def get_info():
    data = request.json
    if data["token"] is None:
        return jsonify({
            'code': 403,
            'data': {
                'user': None
            }
        })
    try:
        payload = jwt.decode(jwt=data["token"], key='secret', algorithms='HS256')
    except:
        return jsonify({
            'code': 403,
            'data': {
                'user': None
            }
        })
    id = payload["id"]
    if id is not None:
        u = User.query.filter(User.id == id).first()
        if u is not None:
            print(u.birthday)
            return jsonify({
                'code': 200,
                'data': {
                    'user': {
                        "email": u.email,
                        "name": u.name,
                        "job": u.job,
                        "intro": u.intro,
                        "birthday": u.birthday
                    }
                }
            })
    return jsonify({
        'code': 403,
        'data': {
            'user': None
        }
    })


@user.route('getinfo', methods=['OPTIONS'])
def get_info_option():
    data = request.json
    pass


@user.post('modifyinfo')
def modify_info():
    data = request.json
    print(data)
    try:
        payload = jwt.decode(jwt=data["token"], key='secret', algorithms='HS256')
        if payload["id"] is not None:
            id = payload["id"]
            loginuser = User.query.filter(User.id == id).first()
            try:
                birstr = str(data['birthday'])[5:16]
                print(birstr)
                birthday = dt.strptime(birstr, "%d %b %Y")
            except:
                birthday = None
            if data['name'] is None:
                return jsonify({
                    'code': 403,
                    'data': {
                        'result': False,
                        'reason': "name is null"
                    }
                })
            if True:
                loginuser.name = data['name']
                loginuser.job = data['job']
                loginuser.intro = data['intro']
                print(birthday)
                if birthday is not None:
                    loginuser.birthday = birthday
                else:
                    if data['birthday'] is not None:
                        year = int(str(data['birthday'])[0:4])
                        month = int(str(data['birthday'])[5:7])
                        day = int(str(data['birthday'])[8:10])
                        loginuser.birthday = datetime.date(year, month, day)
                    else:
                        loginuser.birthday = None
                db.session.commit()
            return jsonify({
                'code': 200,
                'data': {
                    'result': True
                }
            })
        else:
            return jsonify({
                'code': 403,
                'data': {
                    'result': False,
                    'reason': "invalid token"
                }
            })
    except:
        return jsonify({
            'code': 403,
            'data': {
                'result': False,
                'reason': "fatal error"
            }
        })


@user.post('register')
def register():
    data = request.json
    print(data)
    if User.query.filter(User.email == data['email']).first() is not None:
        return jsonify({
            'code': 403,
            'data': {
                'result': False
            }
        })
    if User.query.filter(User.name == data['name']).first() is not None:
        return jsonify({
            'code': 403,
            'data': {
                'result': False
            }
        })
    try:
        if len(data['name']) == 0 or len(data['email']) == 0 or len(data['password']) == 0:
            return jsonify({
                'code': 403,
                'data': {
                    'result': False
                }
            })
    except:
        return jsonify({
            'code': 403,
            'data': {
                'result': False
            }
        })
    try:
        message = Message(subject="感谢您注册witfuzz账号！", recipients=[data['email']],
                          body="用户" + str(data['name']) + "感谢您注册witfuzz账号！")
        mail.send(message)
        if len(data['birthday']) != 0:
            print("error")
            year = int(str(data['birthday'])[0:4])
            month = int(str(data['birthday'])[5:7])
            day = int(str(data['birthday'])[8:10])
            print(datetime.date(year, month, day))
            newuser = User(
                name=data['name'],
                email=data['email'],
                password=data['password'],
                job=data['job'],
                intro=data['intro'],
                birthday=datetime.date(year, month, day)
            )
        else:
            newuser = User(
                name=data['name'],
                email=data['email'],
                password=data['password'],
                job=data['job'],
                intro=data['intro'],
                birthday=None
            )
        db.session.add(newuser)
        db.session.commit()
    except:
        return jsonify({
            'code': 403,
            'data': {
                'result': False
            }
        })

    return jsonify({
        'code': 200,
        'data': {
            'user': newuser.to_json(),
            'result': True
        }
    })


# @user.post('modifypasswordverify')
# def modifypasswordverify():
#     data = request.json
#     print(data['verifycode'])
#     if data['verifycode'] != '666666':
#         return jsonify({
#             'code': 200,
#             'data': {
#                 'result': False
#             }
#         })
#     return jsonify({
#         'code': 403,
#         'data': {
#             'result': True
#         }
#     })


@user.post('modifypassword')
def modifypassword():
    data = request.json
    print(data)
    try:
        mpuser = User.query.filter(User.email == data['email']).first()
    except:
        payload = jwt.decode(jwt=data["token"], key='secret', algorithms='HS256')
        id = payload["id"]
        mpuser = User.query.filter(User.id == id).first()
    if mpuser is None:
        return jsonify({
            'code': 403,
            'data': {
                'result': False
            }
        })
    if (mpuser.password == data['password']):
        return jsonify({
            'code': 403,
            'data': {
                'result': False
            }
        })
    if data['password'] is None:
        return jsonify({
            'code': 403,
            'data': {
                'result': False
            }
        })
    if len(data['password']) < 6:
        return jsonify({
            'code': 403,
            'data': {
                'result': False
            }
        })
    mpuser.password = data['password']
    db.session.commit()
    return jsonify({
        'code': 200,
        'data': {
            'result': True
        }
    })


@user.post('sendverifyCode')
def sendverifycode():
    data = request.json
    u = User.query.filter(User.email == data['email']).first()
    verifycode = random.randint(100000, 999999)
    try:
        redis_db.set_item(name=data['email'], value=verifycode, ex=180)
        print(redis_db.r.get(data['email']))
        print(redis_db.get_item(data['email']))
        message = Message(subject="验证码", recipients=[data['email']],
                          body="验证码:" + str(verifycode) + "三分钟内有效")
        mail.send(message)
    except:
        if u is None:
            return jsonify({
                'code': 403,
                'data': {
                    'result': False
                }
            })
    return jsonify({
        'code': 200,
        'data': {
            'result': True,
            # 'verifycode': verifycode
        }
    })


@user.post('modifypasswordverify')
def verifymodifypassword():
    data = request.json
    verifycode = redis_db.get_item(data['email'])
    print(data)
    print(verifycode)
    if (verifycode is not None) & (verifycode == data['verifycode']):
        return jsonify({
            'code': 200,
            'data': {
                'result': True
            }
        }
        )
    return jsonify({
        'code': 403,
        'data': {
            'result': False
        }
    })
