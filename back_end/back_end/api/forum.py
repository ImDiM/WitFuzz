from flask import request, jsonify
from flask.blueprints import Blueprint
from back_end.database import db

from back_end.database import User,Answer,Problem
from datetime import datetime

forum = Blueprint('forum', __name__)




# 获取所有问题
@forum.route("", methods=["POST"])
def GetProblemList():
    problems = Problem.query.all()
    payload = []
    for problem in problems:
        content = {"id": problem.id, "title": problem.title, "description": problem.description
                   , "answer_number": problem.answer_number, "user_id": problem.user_id}
        payload.append(content)
        content = {}
    return jsonify({'code':200,'data':payload, 'msg':True})


# 获取某问题的详细信息
@forum.route("/<problem_id>", methods=["POST"])
def GetProblem(problem_id):
    
    if not problem_id.isdigit() or int(problem_id)<1:
        return jsonify({'code':202,'msg':'Invalid problem id!'})
    problem = Problem.query.filter(Problem.id==problem_id).first()
    if problem is None:
        return jsonify({'code':202,'msg':'The problem is not existed!'})
    
    user = User.query.filter(User.id==problem.user_id).first()
    content = {"id": problem.id, "title": problem.title, "description": problem.description
                   , "answer_number": problem.answer_number, "user_id": problem.user_id}
    content.update({"user":user.name})
    return jsonify({'code':200,'data':content, 'msg':True})



# 查看某问题下所有回答
@forum.route("/<problem_id>/answerList", methods=["POST"])
def GetAnswerList(problem_id):
    if not problem_id.isdigit() or int(problem_id)<1:
        return jsonify({'code':202,'msg':'Invalid problem id!'})
    problem = Problem.query.filter(Problem.id==problem_id).first()
    if problem is None:
        return jsonify({'code':202,'msg':'The problem is not existed!'})
    
    answers = Answer.query.filter_by(problem_id=problem_id)
    payload = []
    for answer in answers:
        content = {"id": answer.id, "content": answer.content, "edit_time": answer.edit_time
                   , "user_id": answer.user_id, "problem_id": answer.problem_id}
        user = User.query.filter(User.id==answer.user_id).first()
        content.update({"user":user.name})
        payload.append(content)
        content = {}
    return jsonify({'code':200,'data':payload,'msg':True})



# 获取我的问题列表
@forum.route("my/<user_id>", methods=["POST"])
def GetMyProblems(user_id):
    if not user_id.isdigit() or int(user_id)<1:
        return jsonify({'code':202,'msg':'Invalid user id!'})
    user = User.query.filter(User.id==user_id).first()
    if user is None:
        return jsonify({'code':202,'msg':'The user is not existed!'})
    
    problems = Problem.query.filter_by(user_id=user_id)
    payload = []
    for problem in problems:
        content = {"id": problem.id, "title": problem.title, "description": problem.description
                   , "answer_number": problem.answer_number, "user_id": problem.user_id}
        payload.append(content)
        content = {}
    return jsonify({'code':200,'data':payload,'msg':True})


# 获取回答
@forum.route("<problem_id>/answer/<answer_id>", methods=["POST"])
def GetAnswer(problem_id, answer_id):
    if not problem_id.isdigit() or int(problem_id)<1:
        return jsonify({'code':202,'msg':'Invalid problem id!'})
    problem = Problem.query.filter(Problem.id==problem_id).first()
    if problem is None:
        return jsonify({'code':202,'msg':'The problem is not existed!'})
    
    if not answer_id.isdigit() or int(answer_id)<1:
        return jsonify({'code':202,'msg':'Invalid answer id!'})
    answer = Answer.query.filter(Answer.id==answer_id).first()
    if answer is None:
        return jsonify({'code':202,'msg':'The answer is not existed!'})
    if answer.problem_id != int(problem_id):
        return jsonify({'code':202,'msg':'The answer and problem is not matched!'})

    content = {"id": answer.id, "content": answer.content, "edit_time": answer.edit_time
                   , "user_id": answer.user_id, "problem_id": answer.problem_id}
    return jsonify({'code':200,'data':content,'msg':True})


# 创建问题
@forum.route("addProblem", methods=["POST"])
def addProblem():
    data = request.json
    title = data["title"]
    description = data["description"]
    if len(title)== 0:
        return jsonify({'code':202,'msg':'The title can not be empty!'})
    if len(title)>= 512:
        return jsonify({'code':202,'msg':'The title is too long!'})
    if len(description)== 0:
        return jsonify({'code':202,'msg':'The description can not be empty!'})

    user_id=data["user_id"]
    if not user_id.isdigit() or int(user_id)<1:
        return jsonify({'code':202,'msg':'Invalid user id!'})
    user = User.query.filter(User.id==user_id).first()
    if user is None:
        return jsonify({'code':202,'msg':'The user is not existed!'})

    problem = Problem(title=data["title"], description=data["description"],user_id=data["user_id"])
    db.session.add(problem)
    db.session.commit()

    return jsonify({'code':200,'msg':True})



# 编辑问题
@forum.route("<problem_id>/edit", methods=["POST"])
def EditProblem(problem_id):
    data = request.json

    if not problem_id.isdigit() or int(problem_id)<1:
        return jsonify({'code':202,'msg':'Invalid problem id!'})
    problem = Problem.query.filter(Problem.id==problem_id).first()
    if problem is None:
        return jsonify({'code':202,'msg':'The problem is not existed!'})
    
    if problem.title == data['title'] and problem.description == data['description']:
        return jsonify({'code':202,'msg':'There is nothing changed!'})
    title = data["title"]
    description = data["description"]
    if len(title)== 0:
        return jsonify({'code':202,'msg':'The title can not be empty!'})
    if len(title)>= 512:
        return jsonify({'code':202,'msg':'The title is too long!'})
    if len(description)== 0:
        return jsonify({'code':202,'msg':'The description can not be empty!'})
    problem.title=data['title']
    problem.description = data['description']

    db.session.commit()

    return jsonify({'code':200,'msg':True})



# 删除问题及其所有回答
@forum.route("<problem_id>/del", methods=["POST"])
def DeleteProblem(problem_id):
    if not problem_id.isdigit() or int(problem_id)<1:
        return jsonify({'code':202,'msg':'Invalid problem id!'})
    problem = Problem.query.filter(Problem.id==problem_id).first()
    if problem is None:
        return jsonify({'code':202,'msg':'The problem is not existed!'})
    
    answers = Answer.query.filter_by(problem_id=problem_id)
    for answer in answers:
        print(answer.content)
        db.session.delete(answer)
    db.session.delete(problem)
    db.session.commit()
    return jsonify({'code':200,'msg':True})





# 添加回答
@forum.route("<problem_id>/addAnswer", methods=["POST"])
def AddAnswer(problem_id):
    if not problem_id.isdigit() or int(problem_id)<1:
        return jsonify({'code':202,'msg':'Invalid problem id!'})
    problem = Problem.query.filter(Problem.id==problem_id).first()
    if problem is None:
        return jsonify({'code':202,'msg':'The problem is not existed!'})
    
    
    data = request.json
    content = data["content"]
    user_id = data["user_id"]

    if len(content)== 0:
        return jsonify({'code':202,'msg':'The content can not be empty!'})

    if not user_id.isdigit() or int(user_id)<1:
        return jsonify({'code':202,'msg':'Invalid user id!'})
    user = User.query.filter(User.id==user_id).first()
    if user is None:
        return jsonify({'code':202,'msg':'The user is not existed!'})




    answer = Answer(content=content, problem_id=problem_id, edit_time=datetime.now(),user_id=user_id)
    
    problem = Problem.query.filter(Problem.id==problem_id).first()
    problem.answer_number += 1
    
    db.session.add(answer)
    db.session.commit()

    return jsonify({'code':200,'msg':True})




# 编辑回答
@forum.route("<problem_id>/edit/<answer_id>", methods=["POST"])
def EditAnswer(problem_id, answer_id):
    data = request.json

    if not answer_id.isdigit() or int(answer_id)<1:
        return jsonify({'code':202,'msg':'Invalid answer id!'})
    answer = Answer.query.filter(Answer.id==answer_id).first()
    if answer is None:
        return jsonify({'code':202,'msg':'The answer is not existed!'})
    
    if answer.content == data['content']:
        return jsonify({'code':202,'msg':'There is nothing changed!'})

    if not problem_id.isdigit() or int(problem_id)<1:
        return jsonify({'code':202,'msg':'Invalid problem id!'})
    problem = Problem.query.filter(Problem.id==problem_id).first()
    if problem is None:
        return jsonify({'code':202,'msg':'The problem is not existed!'})
    
    if answer.problem_id != int(problem_id):
        return jsonify({'code':202,'msg':'The answer and problem is not matched!'})
    if len(data['content'])== 0:
        return jsonify({'code':202,'msg':'The content can not be empty!'})
    answer.content = data['content']
    answer.edit_time = datetime.now()

    db.session.commit()

    return jsonify({'code':200,'msg':True})

# 删除回答
@forum.route("<problem_id>/del/<answer_id>", methods=["POST"])
def DeleteAnswer(problem_id, answer_id):
    if not answer_id.isdigit() or int(answer_id)<1:
        return jsonify({'code':202,'msg':'Invalid answer id!'})
    answer = Answer.query.filter(Answer.id==answer_id).first()
    if answer is None:
        return jsonify({'code':202,'msg':'The answer is not existed!'})
    
    if not problem_id.isdigit() or int(problem_id)<1:
        return jsonify({'code':202,'msg':'Invalid problem id!'})
    problem = Problem.query.filter(Problem.id==problem_id).first()
    if problem is None:
        return jsonify({'code':202,'msg':'The problem is not existed!'})
    
    if answer.problem_id != int(problem_id):
        return jsonify({'code':202,'msg':'The answer and problem is not matched!'})
    db.session.delete(answer)
    db.session.commit()
    problem = Problem.query.filter(Problem.id==problem_id).first()
    problem.answer_number -= 1
    db.session.commit()
    return jsonify({'code':200,'msg':True})