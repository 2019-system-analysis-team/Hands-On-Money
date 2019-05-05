import os
from datetime import datetime, timedelta
import json
import re
import uuid
import jwt
from werkzeug.utils import secure_filename
from flask import render_template, url_for, request, flash, jsonify, current_app
from flask_bcrypt import Bcrypt
from moneyapp.models import User, Organization, Task, Receiver_Task, Organization_Member, Transaction
from moneyapp.db_user import *
from moneyapp.db_organization import *
from moneyapp.db_task import *
from flask_jwt import JWT, jwt_required, current_identity
from functools import wraps
from . import routes
from .home import token_required

##=========== Users ===============================
# RESTful 用户登录
@routes.route('/sessions', methods=['POST'])
def login():
    
    try:
        token = request.headers['Authorization']
    except:
        pass
    else:
        blacklist.add(token)


    email = request.get_json()['email']
    password = request.get_json()['password']

    user = queryUser(email)

    if user:
        bcrypt = Bcrypt(current_app)
        if bcrypt.check_password_hash(user.password, password):
            token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
            return jsonify({"access_token": token.decode('UTF-8')}), 200
        else:
            return jsonify({"error_code": "404", "error_msg": "account not found/password incorrect"}), 404
    else:
        return jsonify({"error_code": "404", "error_msg": "account not found/password incorrect"}), 404

 
# RESTful 查找用户
@routes.route('/users/<user_id>', methods=['GET'])
@token_required
def get_user_info(current_user, user_id):
    user = queryUserById(user_id)
    if user:
        return jsonify({'email': user.email,
                        'phone_number': user.telephone,
                        'profile_photo_path': user.image_file,
                        'student_id': user.student_id,
                        'name': user.username,
                        'age': user.age,
                        'sex': user.sex,
                        'grade': user.grade,
                        'school': user.school,
                        'bio': user.bio,
                        'balance': user.balance,
                        'avg_comment': user.average_comment
                        })
    else:
        return jsonify({'error_code': "404",
                         'error_msg': 'User Not Found'}), 404
        

# RESTful  注册
@routes.route('/users', methods=['POST'])
def creating_user():
    if request.method == 'POST':
        username = request.get_json()['username']
        email = request.get_json()['email']
        telephone = request.get_json()['phone_number']
        password = request.get_json()['password']
       
        bcrypt = Bcrypt(current_app)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
       

        if request.files and request.files['file'] :
            file = request.files['file']
            filename = secure_filename(file.filename)

            # Gen GUUID File Name
            fileExt = filename.split('.')[1]
            autoGenFileName = uuid.uuid4()

            newFileName = str(autoGenFileName) + '.' + fileExt

            target = UPLOAD_FOLDER
            print(target)

            if not os.path.isdir(target):
                os.mkdir(target)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], newFileName))

        else:
            filename = 'default.jpg'
            newFileName = 'default.jpg'

        try:

            user_id = addUser(username, email, hashed_password, telephone, newFileName)
            
            token = jwt.encode({'id': user_id, 'exp': datetime.utcnow() + timedelta(minutes=30)}, current_app.config['SECRET_KEY'])


            return jsonify({'user_id': user_id,
                         'access_token': token.decode('UTF-8')}), 201
            

        
        except Exception as e:
            err_msg = re.findall(r"UNIQUE constraint failed: .*", str(e))
            return jsonify({'error_code': '409',
                         'error_msg': str(e)}), 409
  
# RESTful 登录注销
@routes.route('/users/<user_id>/session', methods=['DELETE'])    
@token_required
def logout(current_user, user_id):
    print(current_user.id)
    print(user_id)

    if current_user.id == int(user_id):
        token = request.headers['Authorization']
        # print(token)
        # 加入黑名单 不能再使用该token
        blacklist.add(token)
        return jsonify({"message": current_user.username + " logged out successfully."}), 200

    else:
        return jsonify({"err_msg": "Not Found"}), 404

# 修改信息
@routes.route('/users/modify_profile_test', methods=['POST', 'GET'])
def test_modify():
    if request.method == 'POST':
        # 之后下面改成 取页面原本的名字 或session里面的名字进行query
        username_ori = 'popiko22'

        email = request.form['email']
        telephone = request.form['telephone']
        student_id = request.form['student_id']
        realname = request.form['realname']
        age = request.form['age']
        sex = request.form['sex']
        grade = request.form['grade']
        school = request.form['school']
        bio = request.form['bio']
        username = request.form['username']


        if request.files and request.files['file'] :
            file = request.files['file']
            filename = secure_filename(file.filename)

            # Gen GUUID File Name
            fileExt = filename.split('.')[1]
            autoGenFileName = uuid.uuid4()

            newFileName = str(autoGenFileName) + '.' + fileExt

            target = UPLOAD_FOLDER
            print(target)

            if not os.path.isdir(target):
                os.mkdir(target)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], newFileName))

        else:
            #filename = 'default.jpg'
            newFileName = 'default.jpg'

        modify_profile(username_ori, username, email, telephone, newFileName, age, sex, grade, school, bio)

        result = jsonify({"result": "add!"})

    return result

# TODO 给个人账号充值
@routes.route('/users/charge', methods=['POST'])
def user_charge():
    """
    需要首先在db_operations.py里面实现一个修改函数(类似chargeForOrganization)
    然后在这里调用
    :param request.form['user_id'] 用户id
    :param request.form['money'] 充多少钱
    :rtype: json {"status": "", "message": "", 
                    "organization_id": ""}
    """

    #只能通过user_id进行充值

    if request.method == 'POST':
        user_id = request.form['user_id']
        money = request.form['money']
        user = queryUserById(user_id)
        if user:
            chargeForUser(user_id,money)
            result = {
                'status': 'success',
                
                'message':"Successfully charge"
            }
        else:
            result = {
                'status': 'fail',
                'message': 'no such user'
            }
    else:
        result = {"status": "fail",
                  "message": "no post"}  
    return jsonify(result)
 
