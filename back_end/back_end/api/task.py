from flask import jsonify, request
from flask.blueprints import Blueprint
from back_end.database import Task
from back_end.database import Record
from back_end.database import db, mongo, redis_db
from datetime import datetime
import json, jwt
task = Blueprint('task', __name__)
tasklist = Blueprint('tasklist', __name__)


@task.get('<string:id>')
def get_task(id):
    print(id)
    t = Task.query.filter(Task.id == id).first()
    if t is None:
        return jsonify({
            'code': 404
        })
    return jsonify({
        'code': 200,
        'data': {
            'task': t.to_full_json()
        }
    })


@task.get('<string:id>/submit_description')
def get_task_submit_description(id):
    t = Task.query.filter(Task.id == id).first()
    if t is None:
        return jsonify({
            'code': 404
        })
    return jsonify({
        'code': 200,
        'data': {
            'task_name': t.name,
            'submit_description': t.submit_description,
            'default_config': t.default_config,
            'allowed_file_types': t.allowed_file_types
        }
    })


@tasklist.get('')
def get_tasklist():
    task_list = Task.query.all()
    if task_list is None:
        return jsonify({
            'code': 404
        })
    task_list_data = [task.to_json() for task in task_list]
    return jsonify({
        'code': 200,
        'data': {
            'task_list': task_list_data
        }
    })


@task.post('<string:id>/submit')
def submit_job(id):
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
    file = request.files['file']
    if not file:
        return jsonify({
            'code': 400,
            'message': 'File not found'
        }), 400
    task_name = request.form.get('task_name')
    file_name = request.form.get('file_name')
    file_type = request.form.get('file_type')
    description = request.form.get('description')
    config_str = request.form.get('config_str')
    is_public = request.form.get('is_public') == 'true'
    file_id = mongo.save_file(file)

    record = Record(
        user_id=user_id,
        submitted_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        task_id=id,
        file_id=file_id,
        file_name=f'{file_name}.{file_type}',
        config_str=config_str,
        description=description,
        status='waiting',
        is_public=is_public
    )
    db.session.add(record)
    db.session.commit()

    try:
        message = {
            'task_name': task_name,
            'data': {
                'record_id': record.id,
                'file_id': file_id,
                'file_name': file_name,
                'file_type': file_type,
                'config_str': config_str
            }
        }
        redis_db.xadd({'message': json.dumps(message)})
    except Exception as e:
        db.session.delete(record)
        db.session.commit()
        return jsonify({
            'code': 500,
            'message': 'Internal Server Error'
        })

    return jsonify({
        'code': 200,
        'data': {
            'result': True
        }
    })
