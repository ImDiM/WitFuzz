from flask import jsonify, request, Response
from flask.blueprints import Blueprint
from back_end.database import db, mongo
from back_end.database import Record
from sqlalchemy import asc,desc
import jwt

record = Blueprint('record', __name__)
recordlist = Blueprint('recordlist', __name__)

@recordlist.get('')
def get_record_list():
    token = request.args.get('token')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload.get('id')
    except Exception as e:
        return jsonify({
            'code': 401,
            'message': 'Invalid token'
        })
    if user_id is None:
        return jsonify({
            'code': 401,
            'message': 'Invalid token'
        })

    id = request.args.get('task_id')
    order_by = request.args.get('order_by', default='submitted_at')
    order_type = request.args.get('order_type', default='desc')
    page_size = int(request.args.get('page_size', default=10))
    page_number = int(request.args.get('page_number', default=0))
    offset = page_number * page_size
    order_by_filed = getattr(Record, order_by)
    order_by_filed = asc(order_by_filed) if order_type == 'asc' else desc(order_by_filed)
    record_list = Record.query.filter(Record.task_id == id, Record.user_id == user_id).order_by(order_by_filed).offset(offset).limit(page_size).all()
    total_count = Record.query.filter(Record.task_id == id, Record.user_id == user_id).count()
    if not record_list:
        return jsonify({'code': 404})
    record_list_data = [record.to_json() for record in record_list]
    return jsonify({
        'code': 200,
        'data': {
            'record_list': record_list_data,
            'total_count': total_count
            }
        })


@recordlist.get('public')
def get_public_record_list():
    id = request.args.get('task_id')
    order_by = request.args.get('order_by', default='id')
    order_type = request.args.get('order_type', default='desc')
    page_size = int(request.args.get('page_size', default=10))
    page_number = int(request.args.get('page_number', default=0))
    offset = page_number * page_size
    order_by_filed = getattr(Record, order_by)
    order_by_filed = asc(order_by_filed) if order_type == 'asc' else desc(order_by_filed)
    record_list = Record.query.filter(Record.task_id == id, Record.is_public == True).order_by(order_by_filed).offset(offset).limit(page_size).all()
    total_count = Record.query.filter(Record.task_id == id, Record.is_public == True).count()
    if not record_list:
        return jsonify({'code': 404})
    record_list_data = [record.to_json() for record in record_list]
    return jsonify({
        'code': 200,
        'data': {
            'record_list': record_list_data,
            'total_count': total_count
            }
        })


@record.get('<string:id>')
def get_record(id):
    token = request.args.get('token')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload.get('id')
    except Exception as e:
        return jsonify({
            'code': 401,
            'message': 'Invalid token'
        })
    if user_id is None:
        return jsonify({
            'code': 401,
            'message': 'Invalid token'
        })
    record = Record.query.filter(Record.id == id).first()
    if record is None:
        return jsonify({
            'code': 404,
        })
    return jsonify({
        'code': 200,
        'data': {
            'record': record.to_full_json()
        }
    })


@record.put('<string:id>/public')
def set_record_as_public(id):
    token = request.args.get('token')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload.get('id')
    except Exception as e:
        return jsonify({
            'code': 401,
            'message': 'Invalid token'
        })
    if user_id is None:
        return jsonify({
            'code': 401,
            'message': 'Invalid token'
        })
    res = Record.query.filter(Record.user_id == user_id, Record.id == id).update({'is_public': True})
    db.session.commit()
    if not res:
        return jsonify({
            'code': 404,
            'data': {
                'result': True
            }
        })
    return jsonify({
        'code': 200,
        'data': {
            'result': True
        }
    })


@record.put('<string:id>/private')
def set_record_as_private(id):
    token = request.args.get('token')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload.get('id')
    except Exception as e:
        return jsonify({
            'code': 401,
            'message': 'Invalid token'
        })
    if user_id is None:
        return jsonify({
            'code': 401,
            'message': 'Invalid token'
        })
    res = Record.query.filter(Record.user_id == user_id, Record.id == id).update({'is_public': False})
    db.session.commit()
    if not res:
        return jsonify({
            'code': 404,
            'data': {
                'result': False
            }
        })
    return jsonify({
        'code': 200,
        'data': {
            'result': True
        }
    })


@record.delete('<string:id>')
def delete_record(id):
    token = request.args.get('token')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload.get('id')
    except Exception as e:
        return jsonify({
            'code': 401,
            'message': 'Invalid token'
        })
    if user_id is None:
        return jsonify({
            'code': 401,
            'message': 'Invalid token'
        })
    u = Record.query.filter(Record.user_id == user_id, Record.id == id).first()
    if u is None:
        return jsonify({
            'code': 404,
            'data': {
                'result': False
            }
        })
    mongo.delete_file(u.file_id)
    mongo.delete_file(u.result_file_id)
    db.session.delete(u)
    db.session.commit()
    return jsonify({
        'code': 200,
        'data': {
            'result': True
        }
    })


@record.get('<string:id>/file')
def get_result_file(id):
    token = request.args.get('token')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload.get('id')
    except Exception as e:
        return jsonify({
            'code': 401,
            'message': 'Invalid token'
        })
    if user_id is None:
        return jsonify({
            'code': 401,
            'message': 'Invalid token'
        })
    result_file_id = request.args.get('file_id')
    try:
        file = mongo.get_file(result_file_id)
        response = Response(file, mimetype='application/octet-stream')
        return response
    except Exception as e:
        return jsonify({
            'code': 500,
        })
