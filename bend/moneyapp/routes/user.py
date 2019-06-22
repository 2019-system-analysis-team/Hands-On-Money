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
from .home import token_required , blacklist

##=========== Users ===============================

# 修改密码
@routes.route('/users/<user_id>/password', methods=['PUT'])
@token_required
def modifyPassword(current_user, user_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    try:
        d = request.get_json()
        old_password = d['old_password']
        new_password = d['new_password']
        user = queryUserById(user_id)

    except Exception as e:
        return jsonify({"error_code": "400", "error_msg": "fuck you asshole"}),400

    if user:
        bcrypt = Bcrypt(current_app)
        if bcrypt.check_password_hash(user.password, old_password):
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            try:
                changePassword(user_id, hashed_password)
            except Exception as e:
                return jsonify({"error_code": 500, "error_msg": str(e)}), 500
            else:
                return jsonify({"message": "Modify Successfully!"}), 200
        else:
            return jsonify({"error_code": "404", "error_msg": "account not found/password incorrect"}), 404
    

# RESTful 用户登录
@routes.route('/sessions', methods=['POST'])
def login():
    if request.method != 'POST':
        return jsonify({ "error_code": 405,
                            "error_msg": "fuck you asshole"}),405
    
    try:
        token = request.headers['Authorization']
    except:
        pass
    else:
        blacklist.add(token)


    ##email = request.get_json()['email']
    ##password = request.get_json()['password']
    try:
        d = request.get_json()
        user = queryUser(d)
        password = d['password']
    except Exception as e:
        return jsonify({"error_code": "400", "error_msg": "fuck you asshole"}),400

    if user:
        bcrypt = Bcrypt(current_app)
        if bcrypt.check_password_hash(user.password, password):
            token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(hours=24)}, current_app.config['SECRET_KEY'])
            return jsonify({"user_id":user.id, "access_token": token.decode('UTF-8')}), 200
        else:
            return jsonify({"error_code": "404", "error_msg": "account not found/password incorrect"}), 404
    else:
        return jsonify({"error_code": "404", "error_msg": "account not found/password incorrect"}), 404
    
        #return jsonify(e)

 
# RESTful 查找用户
@routes.route('/users/<user_id>', methods=['GET'])
@token_required
def get_user_info(current_user, user_id):
    if request.method != 'GET':
        return jsonify({ "error_code": 405,
                            "error_msg": "fuck you asshole"}),405



    user = queryUserById(user_id)

    if user:
        if current_user.id == int(user_id):
            return jsonify({'user_id': user.id,
                            'email': user.email,
                            'phone_number': user.phone_number,
                            'profile_photo_path': user.profile_photo_path,
                            'student_id': user.student_id,
                            'name': user.name,
                            'age': user.age,
                            'sex': user.sex,
                            'grade': user.grade,
                            'school': user.school,
                            'nickname':user.nickname,
                            'bio': user.bio,
                            'balance': user.balance,
                            'average_comment': user.average_comment
                            })
        else:
            return jsonify({'user_id': user.id,
                            'student_id': user.student_id,
                            'phone_number': user.phone_number,
                            'profile_photo_path': user.profile_photo_path,
                            'name': user.name,
                            'age': user.age,
                            'sex': user.sex,
                            'grade': user.grade,
                            'school': user.school,
                            'nickname':user.nickname,
                            'bio': user.bio,
                            'average_comment': user.average_comment
                            })
    else:
        return jsonify({'error_code': "404",
                             'error_msg': 'User Not Found'}), 404




        

# RESTful  注册
@routes.route('/users', methods=['POST'])
def creating_user():
    if request.method == 'POST':
        d = request.get_json()
        new_dict = dict()
        items = {'email',
                'phone_number',
                'student_id',
                'name',
                'age',
                'sex',
                'grade',
                'school',
                'bio',
                'nickname',
                'password'}
        if 'email' not in d or 'password' not in d or 'phone_number' not in d:
            return jsonify({"error_code": "500", "error_msg": "Invalid information"}),500
        
        for arg in d:
            if arg in items:
                new_dict[arg] = d[arg]

        # try:
        #     nickname = request.get_json()['nickname']
        #     email = request.get_json()['email']
        #     phone_number = request.get_json()['phone_number']
        #     password = request.get_json()['password']
        # except Exception as e:
        #     return jsonify({"error_code": "400", "error_msg": "fuck you asshole"}),400
       

        bcrypt = Bcrypt(current_app)
        hashed_password = bcrypt.generate_password_hash(d['password']).decode('utf-8')
        d.pop('password', None)

        

        if request.files and request.files['file'] :
            file = request.files['file']
            filename = secure_filename(file.filename)

            # Gen GUUID File Name
            fileExt = filename.split('.')[1]
            autoGenFileName = uuid.uuid4()

            newFileName = str(autoGenFileName) + '.' + fileExt

            target = current_app.config['UPLOAD_FOLDER']   ###################
            print(target)

            if not os.path.isdir(target):
                os.mkdir(target)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], newFileName))

        else:
            filename = 'default.jpg'
            newFileName = 'default.jpg'

        try:
            
            #user_id = addUser(nickname, email, hashed_password, phone_number, newFileName)
            user_id = addUser2(new_dict, hashed_password)
            
            token = jwt.encode({'id': user_id, 'exp': datetime.utcnow() + timedelta(hours=24)}, current_app.config['SECRET_KEY'])


            return jsonify({'user_id': user_id,
                         'access_token': token.decode('UTF-8')}), 201
            

        
        except Exception as e:
            err_msg = re.findall(r"UNIQUE constraint failed: .*", str(e))
            return jsonify({'error_code': '409',
                         'error_msg': str(e)}), 409
    
        else:

            return jsonify({ "error_code": 405,
                                "error_msg": "fuck you asshole"}),405

# RESTful 登录注销
@routes.route('/users/<user_id>/session', methods=['DELETE'])    
@token_required
def logout(current_user, user_id):
    #print(current_user.id)
    #print(user_id)
    if request.method != 'DELETE':
        return jsonify({ "error_code": 405,
                            "error_msg": "fuck you asshole"}),405

    if current_user.id == int(user_id):
        token = request.headers['Authorization']
        # print(token)
        # 加入黑名单 不能再使用该token
        blacklist.add(token)
        return jsonify({"message": current_user.nickname + " logged out successfully."}), 200

    else:
        return jsonify({"err_msg": "Not Found"}), 404

# 修改信息
"""
@routes.route('/users/modify_profile_test', methods=['POST', 'GET'])
def test_modify():
    if request.method == 'POST':
        # 之后下面改成 取页面原本的名字 或session里面的名字进行query
        nickname_ori = 'popiko22'
        email = request.form['email']
        phone_number = request.form['phone_number']
        student_id = request.form['student_id']
        name = request.form['name']
        age = request.form['age']
        sex = request.form['sex']
        grade = request.form['grade']
        school = request.form['school']
        bio = request.form['bio']
        nickname = request.form['nickname']
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
        modify_profile(nickname_ori, nickname, email, phone_number, newFileName, age, sex, grade, school, bio)
        result = jsonify({"result": "add!"})
    return result
"""
#==============================================================
#修改用户个人信息

#修改nickname，bio
#nickname nickname 不能重复
@routes.route('/users/<user_id>/personality', methods=['PUT'])
@token_required
def  modifyUserPersonality(current_user, user_id):
    if request.method == 'PUT':
        if current_user.id == int(user_id):
            try:
                d = request.get_json() 
            except Exception as e:
                return jsonify({"error_code": "400", "error_msg": "fuck you asshole"}),400
            try:
                user = modify_User(user_id,d)
                
            except Exception as e:
                err_msg = re.findall(r"UNIQUE constraint failed: .*", str(e))
                return jsonify({'error_code': '409',
                         'error_msg': str(e)}), 409

            # return jsonify({"nickname":user.nickname,
            #         "bio":user.bio}),200
            return jsonify({'name': user.name,
                            'age': user.age,
                            'sex': user.sex,
                            'grade': user.grade,
                            'school': user.school,
                            'nickname':user.nickname,
                            'bio': user.bio,
                            'average_comment': user.average_comment
                            }),200

        else:
            return jsonify({"err_msg": "user Not Found"}), 404
    
    else:
        return jsonify({ "error_code": 405,
                            "error_msg": "fuck you asshole"}),405
        
#修改school，grade，sid
@routes.route('/users/<user_id>/school', methods=['PUT'])
@token_required
def  modifyUserSchool(current_user, user_id):
    if request.method == 'PUT':
        if current_user.id == int(user_id):
            try:
                d = request.get_json()
            except Exception as e:
                return jsonify({"error_code": "400", "error_msg": "fuck you asshole"}),400  

            user = modify_User(current_user.id,d)   #####

            return jsonify({"school":user.school,
                    "grade":user.grade,
                    "student_number":user.student_id
                    }), 200
        else:
            return jsonify({"err_msg": "user Not Found"}), 404
    else:

        return jsonify({ "error_code": 405,
                            "error_msg": "fuck you asshole"}),405

#修改name，age，sex
@routes.route('/users/<user_id>/personal_info', methods=['PUT'])
@token_required
def  modifyUserPersonalInfo(current_user, user_id):
    if request.method == 'PUT':
        if current_user.id == int(user_id):
            try:
                d = request.get_json() 
            except Exception as e:
                return jsonify({"error_code": "400", "error_msg": "fuck you asshole"}),400       
            user = modify_User(current_user.id,d)
            return jsonify({"name":user.name,
                "age":user.age,
                "sex":user.sex
                }), 200

        else:
            return jsonify({"err_msg": "user Not Found"}), 404
    else:
        return jsonify({ "error_code": 405,
                            "error_msg": "fuck you asshole"}),405
#修改photo
@routes.route('/users/<user_id>/profile_photo', methods=['POST'])
@token_required
def  modifyUserPhoto(current_user, user_id):
    if request.method == 'POST':
        if current_user.id == int(user_id):
            
            if request.files and request.files['file'] :
                file = request.files['file']
                filename = secure_filename(file.filename)
                print(filename)
            
                # Gen GUUID File Name
                fileExt = filename.split('.')[1]


                # 判断是否规定格式
                picExt = ['png', 'jpg', 'jpeg', 'bmp'];
                if fileExt not in picExt:
                    return jsonify({"error_code": 415,
                                    "error_msg": "Unsupported Media Type"}),415
                    # 返回图片不支持



                autoGenFileName = uuid.uuid4()

                newFileName = str(autoGenFileName) + '.' + fileExt



                target = current_app.config['UPLOAD_FOLDER']
                print(target)

                if not os.path.isdir(target):
                    os.mkdir(target)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], newFileName))

            else:

                newFileName = 'default.jpg'

            user = modify_User_Photo(current_user.id,newFileName)
            return jsonify({"message":"update successfully!"}),200
         


        else:
            return jsonify({"err_msg": "user Not Found"}), 404



"""
# TODO 给个人账号充值
@routes.route('/users/charge', methods=['POST'])
def user_charge():
    
 
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
"""