import pytest
import json, io
import sys
import requests
sys.path.append('..')
from app import create_app
from werkzeug.datastructures import MultiDict
from werkzeug.test import create_environ


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

@pytest.mark.parametrize('task_id', [1, 2, 3, 4, 1000, 2048])
def test_get_task(client, task_id):
    response = client.get(f'/task/{task_id}')
    data = json.loads(response.data)
    if task_id > 4 :
        assert data['code'] == 404
    else:
        assert response.status_code == 200
        assert data['code'] == 200

@pytest.mark.parametrize('task_id', ['abc','bcd'])
def test_get_task_2(client, task_id):
    response = client.get(f'/task/{task_id}')
    data = json.loads(response.data)
    assert data['code'] == 404

@pytest.mark.parametrize('task_id', [1, 2, 3, 4])
def test_get_task_submit_description(client, task_id):
    response = client.get(f'/task/{task_id}/submit_description')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['code'] == 200

@pytest.mark.parametrize('task_id', [1000, 2000])
def test_get_task_submit_description_2(client, task_id):
    response = client.get(f'/task/{task_id}/submit_description')
    data = json.loads(response.data)
    assert data['code'] == 404

@pytest.mark.parametrize('task_id', ['abc','bcd'])
def test_get_task_submit_description_3(client, task_id):
    response = client.get(f'/task/{task_id}/submit_description')
    data = json.loads(response.data)
    assert data['code'] == 404

def test_get_tasklist(client):

    response = client.get('/tasklist')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['code'] == 200
    assert len(data['data']['task_list']) == 4


@pytest.mark.parametrize('task_id', [1])
def test_submit_job(client, task_id, login):
    token = login
    file_data = b'''
#include <stdio.h>

int main(){
  int a,b;
  a = 10;
  b = 11;
  int c = a + b;
  printf("%d\n",c);
  return 0;
}

    '''
    file = io.BytesIO(file_data)
    file.filename = 'test.c'

    form_data = MultiDict([
        ('task_name', 'Test Task'),
        ('file_name', 'test'),
        ('file_type', 'c'),
        ('description', 'Test Description'),
        ('config_str', '{"option": "value"}'),
        ('is_public', 'true'),
        ('file', (file, file.filename))  # 使用元组表示文件字段
    ])

    environ = create_environ(
        method='POST',
        path=f'/task/{task_id}/submit',
        query_string=f'token={token}',
        data=form_data,
        content_type='multipart/form-data'
    )

    response = client.open(environ, content_type='multipart/form-data')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['code'] == 200
    assert data['data']['result'] is True