import pytest
import json
import sys
import logging
sys.path.append('..')
from app import create_app
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# UT3-1
def test_GetProblemList(client):
    response = client.post(f'/forum')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 200

# UT3-2
def test_GetProblem(client):
    response = client.post(f'/forum/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 200

@pytest.mark.parametrize('problem_id_3_2', [-1, 3.14, 'invalid','invalid-2',3726])
def test_GetProblem_invalid(client, problem_id_3_2):
    response = client.post(f'/forum/{problem_id_3_2}')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

# UT3-3
def test_GetAnswerList(client):
    response = client.post(f'/forum/2/answerList')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 200

@pytest.mark.parametrize('problem_id_3_3', [-2, 2.71, 'wrong','maybe-wrong',523409])
def test_GetAnswerList_invalid(client, problem_id_3_3):
    response = client.post(f'/forum/{problem_id_3_3}/answerList')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

# UT3-4
def test_GetMyProblems(client):
    response = client.post(f'/forum/my/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 200

@pytest.mark.parametrize('user_id_3_4', [-127, 5.23, 'stranger','who?',6627])
def test_GetMyProblems_invalid(client, user_id_3_4):
    response = client.post(f'/forum/my/{user_id_3_4}')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

# UT3-5
def test_GetAnswer(client):
    response = client.post(f'/forum/1/answer/6')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 200

@pytest.mark.parametrize('answer_id_3_5', [-1023, 4.29, 'chatGPT','New.Bing',9622])
def test_GetAnswer_invalid(client, answer_id_3_5):
    response = client.post(f'/forum/1/answer/{answer_id_3_5}')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

# UT3-6
def test_addProblem(client):
    data = {
        'user_id':'4',
        'title':'AFL-FUZZ and ASAN Stuck at dup',
        'description':'I’m a beginner in fuzzing, thanks for the awesome AFL to guide me into fuzzing. but, when I read the source of AFL, I can’t understand the operation described as the issue title (the source is https://github.com/google/AFL/blob/master/afl-fuzz.c#L5523). According to my understanding, if it is to perform arithmetic addition and subtraction, then directly reduce the price, why still do xor operation'
    }
    response = client.post(f'/forum/addProblem',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 200

@pytest.mark.parametrize('ex_3_6', [0,1,2])
def test_addProblem_invalid_prob(client, ex_3_6):
    title = ['','ex_3_6','1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111']
    description = ['ex_3_6','','ex_3_6']
    data={
        'user_id':'4',
        'title':title[ex_3_6],
        'description':description[ex_3_6]
    }
    response = client.post(f'/forum/addProblem',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

@pytest.mark.parametrize('user_id_3_6', ['-127', '5.23', 'stranger','who?','6627'])
def test_addProblem_invalid_user(client, user_id_3_6):
    data={
        'user_id':user_id_3_6,
        'title':'ex_3_6',
        'description':'ex_3_6'
    }
    response = client.post(f'/forum/addProblem',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

# UT3-7
def test_editProblem(client):
    data = {
        'title':'UT-3-7',
        'description':'This is a test'
    }
    response = client.post(f'/forum/38/edit',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 200

@pytest.mark.parametrize('problem_id_3_7', [-1, 3.14, 'invalid','invalid-2',3726])
def test_editProblem_invalid_id(client, problem_id_3_7):
    data = {
        'title':'UT-3-7',
        'description':'This is a testaaaaa'
    }
    response = client.post(f'/forum/{problem_id_3_7}/edit',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

@pytest.mark.parametrize('ex_3_7', [0,1,2])
def test_editProblem_invalid_prob(client, ex_3_7):
    title = ['','ex_3_7','1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111']
    description = ['ex_3_7','','ex_3_7']
    data={
        'user_id':'4',
        'title':title[ex_3_7],
        'description':description[ex_3_7]
    }
    response = client.post(f'/forum/1/edit',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

# UT3-8
def test_deleteProblem(client):
    response = client.post(f'/forum/38/del')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 200

@pytest.mark.parametrize('problem_id_3_8', [-1, 3.14, 'invalid','invalid-2',3726])
def test_deleteProblem_invalid(client, problem_id_3_8):
    response = client.post(f'/forum/{problem_id_3_8}/del')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

# UT3-9
def test_addAnswer(client):
    data = {
        'user_id':'4',
        'content':'This is a test'
    }
    response = client.post(f'/forum/1/addAnswer',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 200

@pytest.mark.parametrize('problem_id_3_9', [-1, 3.14, 'invalid','invalid-2',3726])
def test_addAnswer_invalid_pid(client, problem_id_3_9):
    data = {
        'user_id':'4',
        'content':'This is a test'
    }
    response = client.post(f'/forum/{problem_id_3_9}/addAnswer',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

@pytest.mark.parametrize('user_id_3_9', ['-127', '5.23', 'stranger','who?','6627'])
def test_addAnswer_invalid_uid(client, user_id_3_9):
    data = {
        'user_id':user_id_3_9,
        'content':'This is a test'
    }
    response = client.post(f'/forum/1/addAnswer',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

def test_addAnswer_invalid_detail(client):
    data = {
        'user_id':'4',
        'content':''
    }
    response = client.post(f'/forum/1/addAnswer',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

# UT3-10
def test_editAnswer(client):
    data = {
        'content':'This is edit test'
    }
    response = client.post(f'/forum/1/edit/18',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 200

def test_editAnswer_invalid_detail(client):
    data = {
        'content':''
    }
    response = client.post(f'/forum/1/edit/6',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

def test_editAnswer_invalid_match(client):
    data = {
        'content':''
    }
    response = client.post(f'/forum/1/edit/2',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

@pytest.mark.parametrize('problem_id_3_10', [-1, 3.14, 'invalid','invalid-2',3726])
def test_editAnswer_invalid_pid(client,problem_id_3_10):
    data = {
        'content':'This is an edit test'
    }
    response = client.post(f'/forum/{problem_id_3_10}/edit/2',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

@pytest.mark.parametrize('answer_id_3_10', ['-127', '5.23', 'stranger','who?','6627'])
def test_editAnswer_invalid_aid(client,answer_id_3_10):
    data = {
        'content':'This is an edit test'
    }
    response = client.post(f'/forum/1/edit/{answer_id_3_10}',json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

# UT3-11
def test_deleteAnswer(client):
    response = client.post(f'/forum/1/del/18')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 200

def test_deleteAnswer_match(client):
    response = client.post(f'/forum/1/del/2')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

@pytest.mark.parametrize('problem_id_3_11', [-1, 3.14, 'invalid','invalid-2',3726])
def test_deleteAnswer_invalid_pid(client, problem_id_3_11):
    response = client.post(f'/forum/{problem_id_3_11}/del/6')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202

@pytest.mark.parametrize('answer_id_3_11', ['-127', '5.23', 'stranger','who?','6627'])
def test_deleteAnswer_invalid_aid(client,answer_id_3_11):
    response = client.post(f'/forum/1/del/{answer_id_3_11}')
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data['msg'])
    assert data['code'] == 202