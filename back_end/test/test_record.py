import sys
sys.path.append('..')
from app import create_app
from back_end.database import Record
import pytest
import json, requests


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="function")
def login():
    data = {
            "email": "XXXXXXXXXXXXXX",
            "password": "e10adc3949ba59abbe56e057f20f883e"
    }
    login_info = requests.post(url='http://20.187.85.73:5000/user/login',json=data).json()
    return login_info['data']['token']

@pytest.mark.parametrize('task_id', [1, 1000, 2048])
def test_get_record_list(client, login, task_id):
    params = {
        'order_by': 'submitted_at',
        'order_type': 'desc',
        'token': login,
        'task_id': task_id,
        'page_size': 10,
        'page_number': 0
    }
    response = client.get('/recordlist', query_string=params)
    data = json.loads(response.data)
    if task_id < 5:
        assert data['code'] == 200
    else:
        assert data['code'] == 404


@pytest.mark.parametrize('task_id', [1])
def test_get_record_list_2(client, task_id):
    params = {
        'token': 'invalid_token',
        'task_id': task_id,
        'page_size': 10,
        'page_number': 1
    }
    response = client.get('/recordlist', query_string=params)
    data = json.loads(response.data)
    assert data['code'] == 401

@pytest.mark.parametrize('task_id', ['abc','bcd'])
def test_get_record_list_3(client, task_id, login):
    params = {
        'token': login,
        'task_id': task_id,
        'page_size': 10,
        'page_number': 1
    }
    response = client.get('/recordlist', query_string=params)
    data = json.loads(response.data)
    assert data['code'] == 404


@pytest.mark.parametrize('task_id', [1, 1000, 2048])
def test_get_public_record_list(client, task_id):
    params = {
        'order_by': 'submitted_at',
        'order_type': 'desc',
        'task_id': task_id,
        'page_size': 10,
        'page_number': 0
    }
    response = client.get('/recordlist/public', query_string=params)
    data = json.loads(response.data)
    if task_id < 5:
        assert data['code'] == 200
    else:
        assert data['code'] == 404


@pytest.mark.parametrize('task_id', ['abc','bcd'])
def test_get_public_record_list_3(client, task_id):
    params = {
        'task_id': task_id,
        'page_size': 10,
        'page_number': 1
    }
    response = client.get('/recordlist/public', query_string=params)
    data = json.loads(response.data)
    assert data['code'] == 404

@pytest.mark.parametrize('record_id', [258, 259, 260, 261 , 9999])
def test_get_record(client, record_id , login):
    params = {
        'token': login,
        'record_id': record_id,
        'page_size': 10,
        'page_number': 1
    }
    response = client.get(f'/record/{record_id}', query_string=params)
    data = json.loads(response.data)
    if record_id < 1000:
        assert data['code'] == 200
    else:
        assert data['code'] == 404

@pytest.mark.parametrize('record_id', [258, 259, 260, 261])
def test_get_record_2(client, record_id):
    params = {
        'token': 'invalid_token',
        'record_id': record_id,
        'page_size': 10,
        'page_number': 1
    }
    response = client.get(f'/record/{record_id}', query_string=params)
    data = json.loads(response.data)
    assert data['code'] == 401

@pytest.mark.parametrize('record_id', [281, 283])
def test_set_record_as_public(client, record_id , login):
    params = {
        'token': login,
        'record_id': record_id,
    }
    response = client.put(f'/record/{record_id}/public', query_string=params)
    data = json.loads(response.data)
    assert data['code'] == 200

@pytest.mark.parametrize('record_id', [281, 283])
def test_set_record_as_public_2(client, record_id ):
    params = {
        'token': 'invalid_token',
        'record_id': record_id,
    }
    response = client.put(f'/record/{record_id}/public', query_string=params)
    data = json.loads(response.data)
    assert data['code'] == 401

@pytest.mark.parametrize('record_id', [281, 283])
def test_set_record_as_private(client, record_id , login):
    params = {
        'token': login,
        'record_id': record_id,
    }
    response = client.put(f'/record/{record_id}/private', query_string=params)
    data = json.loads(response.data)
    assert data['code'] == 200

@pytest.mark.parametrize('record_id', [281, 283])
def test_set_record_as_private_2(client, record_id ):
    params = {
        'token': 'invalid_token',
        'record_id': record_id,
    }
    response = client.put(f'/record/{record_id}/private', query_string=params)
    data = json.loads(response.data)
    assert data['code'] == 401


@pytest.mark.parametrize('record_id', [])
def test_delete_record(client, record_id ):
    params = {
        'token': 'invalid_token',
        'record_id': record_id,
    }
    response = client.delete(f'/record/{record_id}', query_string=params)
    data = json.loads(response.data)
    assert data['code'] == 401

@pytest.mark.parametrize('record_id', [])
def test_delete_record_2(client, record_id , login):
    params = {
        'token': login,
        'record_id': record_id,
    }
    response = client.delete(f'/record/{record_id}', query_string=params)
    data = json.loads(response.data)
    assert data['code'] == 200

@pytest.mark.parametrize('record_id', [281])
def test_get_file(client, record_id):
    params = {
        'token': login,
        'file_id': '645f19b2fb10f0b0aed87f30'
    }
    response = client.get(f'/record/{record_id}/file', query_string=params)


@pytest.mark.parametrize('record_id', [281])
def test_get_file(client, record_id):
    params = {
        'token': 'invalid_token',
        'file_id': '645f19b2fb10f0b0aed87f30'
    }
    response = client.get(f'/record/{record_id}/file', query_string=params)
    data = json.loads(response.data)
    assert data['code'] == 401