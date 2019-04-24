import os, datetime
import json
import re
import uuid
import jwt
from werkzeug.utils import secure_filename
from flask import render_template, url_for, request, flash, jsonify
from moneyapp import app, db, bcrypt
from moneyapp.models import User, Organization, Task, Receiver_Task, Organization_Member, Transaction
from moneyapp.db_operations import addUser, queryUser, addUser_detailed, addOrganization, createTask, createTaskOrganization, modify_profile, receiveTask, addMember, queryRecord, chargeForOrganization, checkBalance,queryUserById,chargeForUser,queryOrganizationByID,deleteOrganization, queryUserByEmail, deleteTask, queryUserByTelephone, finishUserTask, changeTaskStatus, searchTask
from moneyapp.db_operations import queryOrganizationByName,addManager,queryTaskByTag,userChangeReceiveTask,queryReceiverTask,queryTaskById, modifyTask
from flask_jwt import JWT, jwt_required, current_identity
from functools import wraps

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/profile_pics')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'thisisansecretkey'
app.config['JSON_SORT_KEYS'] = False

blacklist = set()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token or token in blacklist:
            return jsonify({'message': 'Token is missing!'}), 401
      
        try:
            print(token)
            print(token[4:])  # 去掉前面的JWT
            token = token[4:]
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = queryUserById(data['id']) 
            print(current_user.username)
        except:
            print(token)
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated



@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        if request.form['button'] == 'add':
            if request.form['username'] and request.form['email'] and request.form['password']:
                hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
                addUser(request.form['username'], request.form['email'], hashed_password)
                flash("Successfully added! " + request.form['username'])
        elif request.form['button'] == 'search':
            if request.form['username2']:
                user = queryUser(request.form['username2'])
                if user:
                    flash("username: " + user.username)
                    flash("email: " + user.email)
                    flash("image_file: " + user.image_file)
                else:
                    flash("Can't find this user")
    return render_template('layout.html')

@app.route('/api/users', methods=['GET'])
def get_all_users():
    user = queryUser('zhutou')
    return json.dumps({"username":user.username, "email":user.email})


##=========== Users ===============================
# RESTful 用户登录
@app.route('/sessions', methods=['POST'])
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
        if bcrypt.check_password_hash(user.password, password):
            token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return jsonify({"access_token": token.decode('UTF-8')}), 200
        else:
            return jsonify({"error_code": "404", "error_msg": "account not found/password incorrect"}), 404
    else:
        return jsonify({"error_code": "404", "error_msg": "account not found/password incorrect"}), 404

 
# RESTful 查找用户
@app.route('/users/<user_id>', methods=['GET'])
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
@app.route('/users', methods=['POST'])
def creating_user():
    if request.method == 'POST':
        username = request.get_json()['username']
        email = request.get_json()['email']
        telephone = request.get_json()['phone_number']
        password = request.get_json()['password']
       
  
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], newFileName))

        else:
            filename = 'default.jpg'
            newFileName = 'default.jpg'

        try:

            user_id = addUser(username, email, hashed_password, telephone, newFileName)
            
            token = jwt.encode({'id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])


            return jsonify({'user_id': user_id,
                         'access_token': token.decode('UTF-8')}), 201
            

        
        except Exception as e:
            err_msg = re.findall(r"UNIQUE constraint failed: .*", str(e))
            return jsonify({'error_code': '409',
                         'error_msg': err_msg}), 409
  
# RESTful 登录注销
@app.route('/users/<user_id>/session', methods=['DELETE'])    
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
@app.route('/users/modify_profile_test', methods=['POST', 'GET'])
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], newFileName))

        else:
            #filename = 'default.jpg'
            newFileName = 'default.jpg'

        modify_profile(username_ori, username, email, telephone, newFileName, age, sex, grade, school, bio)

        result = jsonify({"result": "add!"})

    return result

# TODO 给个人账号充值
@app.route('/users/charge', methods=['POST'])
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
 







##=============== Organization =======================
# RESTful 创建组织
@app.route('/users/<user_id>/organization', methods=['POST'])
@token_required
def create_organization(current_user, user_id):
    name = request.get_json()['name']
    bio = request.get_json()['bio']

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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], newFileName))

    else:
        #filename = 'default.jpg'
        newFileName = 'default2.jpg'

    try:
        organization_id = addOrganization(name, newFileName, bio)

        addMember(user_id, organization_id, "owner")

        return jsonify({"organization_id": organization_id}), 201

    except Exception as e:
            err_msg = re.findall(r"UNIQUE constraint failed: .*", str(e))
            return jsonify({'error_code': "409",
                         'error_msg': str(e)}), 409


# RESTful 群主删除组织
@app.route('/users/<user_id>/organization/<organization_id>', methods=['DELETE'])
@token_required
def organization_delete(current_user, user_id, organization_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    organization = queryOrganizationByID(organization_id)

    if not organization:
        return jsonify({"error_code": "404", "error_msg": "organization Not Found"}), 404

    record = queryRecord(current_user.id, int(organization_id))
    
    if not record or record.status != 'owner':
        return jsonify({"error_code": "401",
                        "error_msg": "insufficient permission"}), 401

    deleteOrganization(organization_id)
    return jsonify({"name": organization.name, "bio": organization.bio}), 200
    
# RESTful 群主管理员添加成员
@app.route('/users/<user_id>/organization/<organization_id>/members', methods=['POST'])
@token_required
def add_organization_member(current_user, user_id, organization_id):
    
    status = request.get_json()['status']
    # email, telephone任意有一个就好
    try:
        email = request.get_json()['email']
        user = queryUserByEmail(email)
    except:
        pass

    try:
        telephone = request.get_json()['phone_number']
        user = queryUserByTelephone(telephone)
    except:
        pass
        
        

    user_operator = queryUserById(int(user_id))
    organization = queryOrganizationByID(int(organization_id))

    if not user_operator or not user:
        return jsonify({"error_code": "404",
                        "error_msg": "user Not Found"}), 404
    if not organization:
        return jsonify({"error_code": "404",
                        "error_msg": "organization Not Found"}), 404

    record = queryRecord(current_user.id, organization_id)
    if not record or record.status == 'member':
        return jsonify({"error_code": "401",
                        "error_msg": "insufficient permission"}), 401
    else:
        addMember(user.id, organization_id, "member")
        return jsonify({"msg": "Added successfully."}), 201

# TODO 组织信息的录入和修改
@app.route('/organizations/modify_profile', methods=['POST'])
def organization_modify_profile():
    """
    需要首先在db_operations.py里面实现一个修改函数
    然后在这里调用
    需要判断操作者是否为组织的创建者（owner）或者管理员（manager）
    可以使用queryRecord来获得user和organization的记录
    利用status判断是否为创建者、管理员
    :param request.form['user_id'] 用户id
    :param request.form['organization_id'] 组织id
    :param request.form['name'] 组织名字（用于修改）
    :param request.form['bio'] 组织说明（用于修改）
    :param request.form['file'] 头像修改（具体的可以参考前面用户修改资料的头像部分的修改）
    :rtype: json {"status": "", "message": "", 
                    "organization_name": "", "organization_bio": "", "orgnazation_avatar_path":""}
    """
  
    if request.method == 'POST':
        user_id = request.form['user_id']
        organization_id = request.form['organization_id']
        organization_name = request.form['name']
        organization_bio = request.form['bio']
       
       
        result = {'status':'fail',
                'message':'no permission'}


    else:
        result = {"status": "fail",
                  "message": "no post"}
        
    return jsonify(result)

# 给组织充值
@app.route('/organizations/charge', methods=['POST'])
def organization_charge():
    """
    需要首先在db_operations.py里面实现一个修改函数(chargeForOrganization写好了)
    然后在这里调用
    需要判断操作者是否为组织成员（owner/manager/ordinary member）
    可以使用queryRecord来获得user和organization的记录
    :param request.form['user_id'] 用户id
    :param request.form['organization_id'] 组织id
    :param request.form['money'] 充多少钱
    :rtype: json {"status": "", "message": "", 
                    "organization_id": ""}
    """
    if request.method == 'POST':
        user_id = request.form['user_id']
        organization_id = request.form['organization_id']
        money = request.form['money']

        record = queryRecord(user_id, organization_id)
        if record:
            
            chargeForOrganization(user_id, organization_id, money)
            
            result = {"status": "success", 
                      "message": "Successfully charge",
                      "organization_id": organization_id
                      }
        else:
            result = {"status": "fail",
                      "message": "No Permission"}

        
    else:
        result = {"status": "fail",
                  "message": "no post"}

    return jsonify(result)

# TODO 按名字搜索组织
@app.route('/organizations/filter', methods=['GET'])
def organization_filter():
    """
    需要首先在db_operations.py里面实现一个filter函数，可以参考queryUser
    然后在这里调用
    :param request.form['organization_name'] 用户id
    :rtype: json {"organization_name": {}}
    """
    #返回的信息不定
    if request.method == 'GET':
        organization_name = request.form['organization_name']
        organization = queryOrganizationByName(organization_name)
        if organization:
            result = {"status":"true",
                       "message":"successfully get" }
        else:
            result = {"status":"false",
                      "message":"no such organization"}
    else:
        result = {"status": "false",
                  "message": "no get"}
    return jsonify(result)

# TODO 群主设置成员为管理员
@app.route('/organizations/set_status', methods=['POST'])
def set_member_status():
    """
    需要首先在db_operations.py里面实现一个修改函数
    然后在这里调用
    需要判断操作者是否为群主，且被操作者是否为群内成员
    可以使用queryRecord来获得user和organization的记录
    :param request.form['owner_id'] 群主id
    :param request.form['member_id'] 要被设置为管理员的用户的id
    :param request.form['organization_id'] 组织id
    :rtype: json {"status": "", "message": "", 
                    "organization_id": ""}
    """
    if request.method == 'POST':
        owner_id = request.form['owner_id']
        member_id = request.form['member_id']
        organization_id = request.form['organization_id']
        owner = queryRecord(owner_id,organization_id)
        member = queryRecord(member_id,organization_id)
        if owner and member:
            if owner.status == 'owner' and member.status == 'member':
                addManager(member_id,organization_id)
                result = {'status':'success',
                          'message' : 'change'}
            else:
                result = {'status':'fail'}
        else:
            result = {'status':'fail'}

    else:
        result = {"status": "false", 
                  "message": "no post"}

    return jsonify(result)




##=========== Task =================================
# RESTful 用户创建任务
@app.route('/users/<user_id>/task', methods=['POST'])
@token_required
def user_create_task(current_user, user_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    #if checkBalance(user_id, None, float(reward_for_one_participant) * float(participant_number_limit)):
    d = request.get_json()

    d['user_id'] = int(user_id)


    task = createTask(request.get_json())

   
    return_msg = printSingleTask(task)

    return jsonify(return_msg), 200
    
    

# RESTful 组织创建任务
@app.route('/users/<user_id>/organization/<organization_id>/tasks', methods=['POST'])
@token_required
def organization_create_task(current_user, user_id, organization_id):
    # 检查user, organization是否存在
    user = queryUserById(user_id)
    if not user or int(user_id) != current_user.id:
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    organization = queryOrganizationByID(organization_id)
    if not organization:
        return jsonify({"error_code": "404", "error_msg": "organization Not Found"}), 404


    record = queryRecord(current_user.id, organization_id)
    if not record or record.status == 'member':
        return jsonify({"error_code": "401",
                        "error_msg": "insufficient permission"}), 401

    
    d = request.get_json()
    d['user_id'] = int(user_id)
    d['organization_id'] = int(organization_id)
    
    # !!! balance判断
    #if checkBalance(user_id, None, float(reward_for_one_participant) * float(participant_number_limit)):
    task = createTask(d)

    return_msg = printSingleTask(task)

    return jsonify(return_msg), 200




# RESTful 用户查询自己创建的任务
@app.route('/users/<user_id>/tasks', methods=['GET'])
@token_required
def check_user_tasks(current_user, user_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    task_info = []

    for task in current_user.tasks:
        task_info.append(printSingleTask(task))

    return jsonify(task_info), 200


# RESTful 组织查询自己创建的任务
@app.route('/users/<user_id>/organization/<organization_id>/tasks', methods=['GET'])
@token_required
def check_organization_tasks(current_user, user_id, organization_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    organization = queryOrganizationByID(organization_id)
    if not organization:
        return jsonify({"error_code": "404", "error_msg": "organization Not Found"}), 404

    record = queryRecord(current_user.id, organization_id)
    if not record:
        return jsonify({"error_code": "401",
                        "error_msg": "insufficient permission"}), 401

    task_info = []

    for task in organization.tasks:
        task_info.append(printSingleTask(task))

    return jsonify(task_info), 200


# RESTful 删除个人任务
@app.route('/users/<user_id>/tasks/<task_id>', methods=['DELETE'])
@token_required
def delete_user_task(current_user, user_id, task_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    task = queryTaskById(task_id)
    if not task or task.organization != None:
        return jsonify({"error_code": "404", "error_msg": "task Not Found"}), 404

    
    if not task.user.id == int(current_user.id):
        return jsonify({"error_code":"500", "error_msg": "insufficient permission"}), 500

    deleteTask(user_id, task_id, None)
    return jsonify({"msg": "Delete " + str(task.title) + " successfully."}), 200

# RESTful 删除组织任务
@app.route('/users/<user_id>/organization/<organization_id>/tasks/<task_id>', methods=['DELETE'])
@token_required
def delete_organization_task(current_user, user_id, task_id, organization_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    task = queryTaskById(task_id)
    if not task or task.organization.id != int(organization_id):
        return jsonify({"error_code": "404", "error_msg": "task Not Found"}), 404

    record = queryRecord(user_id, organization_id)
    if not record or record.status == "member":
        return jsonify({"error_code":"500", "error_msg": "insufficient permission"}), 500

    deleteTask(user_id, task_id, organization_id)
    return jsonify({"msg": "Delete " + str(task.title) + " successfully."}), 200

# RESTful 接受任务
@app.route('/users/<user_id>/tasks/<task_id>', methods=['POST'])
@token_required
def receive_task(current_user, user_id, task_id):
    user = queryUserById(user_id)
    if not user or current_user.id != int(user_id):
        return jsonify({"error_code": "404",
                        "error_msg": "user Not Found"}), 404

    task = queryTaskById(task_id)
    if not task:
        return jsonify({"error_code": "404",
                        "error_msg": "task Not Found"}), 404
    try:
        receiveTask(user_id, task_id)
    except Exception as e:
        return jsonify({"error_code": "500", "error_msg": str(e)}), 500
    else:   
        return jsonify({"msg": "Receive task successfully."}), 201

# RESTful 任务完成
@app.route('/users/<user_id>/tasks/<task_id>/steps/<step_id>', methods=['PUT'])
@token_required
def mark_task_step(current_user, user_id, task_id, step_id):
    
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404
    
    task = queryTaskById(task_id)
    
    if not task:
        return jsonify({"error_code": "404", "error_msg": "task Not Found"}), 404
    
    try:
        task_record = userChangeReceiveTask(int(user_id), int(task_id), int(step_id))
    except Exception as e:
        return jsonify({"error_code": "500",
                        "error_msg": str(e)}), 500 
    else:
        return jsonify({"user_id": current_user.id,
                        "task_id": task_record.task.id,
                        "task_title": task_record.task.title,
                        "task_status": task_record.status,
                        "task_total_steps": json.loads(task_record.task.steps),
                        "task_finished_steps": task_record.step}), 200
  

# RESTful 任务审核
@app.route('/users/<user_id>/tasks/<task_id>/finisher/<finisher_id>', methods=['PUT'])
@token_required
def mark_task_finished(current_user, user_id, task_id, finisher_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404
    
    task = queryTaskById(task_id)
    if not task or task.user.id != current_user.id:
        return jsonify({"error_code": "404", "error_msg": "task Not Found"}), 404
    
    try:
        task = finishUserTask(task_id, finisher_id)

    except Exception as e:
        return jsonify({"error_code": "500",
                        "error_msg": str(e)}), 500 
    else:
        result_msg = printSingleTask(task)

        return jsonify(result_msg), 200

        # status = "on going" if (datetime.datetime.utcnow() > task.post_time and datetime.datetime.utcnow() < task.finish_deadline_time) else "not ongoing"
    
        # participant_ids = []
        # ongoing_participant_ids = []
        # waiting_examine_participant_ids = []
        # finished_participant_ids = []

        # for par in task.received_tasks:
        #     par_user_id = par.user_id
        #     participant_ids.append(par_user_id)
        #     if par.status == 'on going':
        #         ongoing_participant_ids.append(par_user_id)
        #     elif par.status == 'waiting examine':
        #         waiting_examine_participant_ids.append(par_user_id)
        #     elif par.status == 'finished':
        #         finished_participant_ids.append(par_user_id)
       
        # return jsonify({"task_id": task.id, 
        #                 "creator_user_id": task.user_id,
        #                 "creator_organization_id": task.organization_id,
        #                 "status": status,
        #                 "title": task.title,
        #                 "description": task.description,
        #                 "tags": json.loads(task.tags),
        #                 "participant_number_limit": task.participant_number_limit,
        #                 "reward_for_one_participant": task.reward_for_one_participant,
        #                 "post_time": task.post_time,
        #                 "receive_end_time": task.receive_end_time,
        #                 "finish_deadline_time": task.finish_deadline_time,
        #                 "user_limit": json.loads(task.user_limit),
        #                 "steps": json.loads(task.steps),
        #                 "participant_ids": participant_ids,
        #                 "ongoing_participant_ids": ongoing_participant_ids,
        #                 "waiting_examine_participant_ids": waiting_examine_participant_ids,
        #                 "finished_participant_ids": finished_participant_ids
        #                 }), 200


# RESTful 个人撤回任务 + 修改任务
@app.route('/users/<user_id>/tasks/<task_id>', methods=['PUT'])
@token_required
def set_user_task_pending(current_user, user_id, task_id):
    # 是否登录者操作
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404
    
    # 是否有该任务
    task = queryTaskById(task_id)
    if not task:
        return jsonify({"error_code": "404", "error_msg": "task Not Found"}), 404
    
    
    d = request.get_json()

    # 撤回任务 有status项即撤回
    if 'status' in d:
        try:
            changeTaskStatus(int(user_id), int(task_id), d['status'], None)
        except Exception as e:
            return jsonify({"error_code": "500", "error_msg": str(e)}), 500
        #changeTaskStatus(int(user_id), int(task_id), d['status'], None)
    
    # 修改
    else:

    
        try:
            # !!! 到后面要把这个注释去掉 为了方便测试先注释掉
            #if checkBalance(user_id, None, float(money) * float(number)):
            modifyTask(int(task_id), int(user_id), None, d)
        
        except Exception as e:
            return jsonify({"error_code": "500", "error_msg": str(e)}), 500


    return_msg = printSingleTask(task)
    return jsonify(return_msg), 200
         

# RESTful 组织撤回任务 + 修改任务
@app.route('/users/<user_id>/organization/<organization_id>/tasks/<task_id>', methods=['PUT'])
@token_required
def set_org_task_pending(current_user, user_id, organization_id, task_id):
    # 是否登录者操作
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404
    
    # 是否有该任务
    task = queryTaskById(task_id)
    if not task:
        return jsonify({"error_code": "404", "error_msg": "task Not Found"}), 404
    
    
    d = request.get_json()

    # 撤回任务 有status项即撤回
    if 'status' in d:
        try:
            changeTaskStatus(int(user_id), int(task_id), d['status'], None)
        except Exception as e:
            return jsonify({"error_code": "500", "error_msg": str(e)}), 500
        #changeTaskStatus(int(user_id), int(task_id), d['status'], None)
    
    # 修改
    else:
        try:
            # !!! 到后面要把这个注释去掉 为了方便测试先注释掉
            #if checkBalance(user_id, None, float(money) * float(number)):
            modifyTask(int(task_id), int(user_id), int(organization_id), d)
        
        except Exception as e:
            return jsonify({"error_code": "500", "error_msg": str(e)}), 500


    return_msg = printSingleTask(task)
    return jsonify(return_msg), 200



# TODO 任务搜索 （对tag进行搜索）
@app.route('/task/filter', methods=['GET'])
def task_filter():
    """
    需要首先在db_operations.py里面实现一个filter函数
    然后在这里调用
    :param request.form['tag'] 标签
    :rtype: json {"status": "", "message": "", "filtered task": {"", ""}}
    """
    if request.method == 'GET':
        tag = request.form['tag']

        
        task = queryTaskByTag(tag)
        if task:
            result = {'status':'success',
                      'message':'search successful'}
        
        else:
            result = {'status':'fail'}
    else:
        result = {'status':'fail',
                  'message':'no get'}
    return jsonify(result)

# TODO 任务接收者修改所接受的任务的状态（mark完成了几步）
#（暂时修改status为传入的request.form['status']的内容）
@app.route('/task/receiver_set_status', methods=['POST'])
def receiver_set_status():
    """
    需要首先在db_operations.py里面实现一个filter函数
    然后在这里调用
    需要先判断user和task是否是接收关系（record） -》需要另外在db_operations.py里写一个函数
    :param request.form['user_id'] 用户id
    :param request.form['task'] 任务id
    :param request.form['status'] 要设置任务为什么状态
    :rtype: json {"status": "", "message": ""}
    """
    if request.method == 'POST':
        user_id = request.form['user_id']
        task_id = request.form['task_id']
        status = request.form['status']
        record = queryReceiverTask(user_id,task_id)
        if record:
           userChangeReceiveTask(user_id,task_id,status)
           result = {'status':'success',
          'message':'change successfully'} 

        else:
            result = {'status':'fail',
           'message':'no suit'}
        
    else:
        result = {'status': 'fail',
        'message':'no post'}

    return jsonify(result)

# TODO 任务发布者修改发布任务的状态（比如设置为已完成...)
@app.route('/task/owner_set_status', methods=['POST'])
def owner_set_status():
    """
    需要首先在db_operations.py里面实现一个filter函数
    然后在这里调用
    需要先判断user和task的关系 -》需要另外在db_operations.py里写一个函数
    :param request.form['user_id'] 用户id
    :param request.form['task'] 任务id
    :param request.form['status'] 要设置任务为什么状态
    :rtype: json {"status": "", "message": ""}
    """
    if request.method == 'POST':
        user_id = request.form['user_id']
        task_id = request.form['task']
        status = request.form['status']
        
        
        task = queryTaskById(user_id,task_id)
        result = {'status':'successfully'}
        
        if task:
            changeTaskStatus(task_id,status)
            result = {'status':'successfully',
            'message':'change!'}
        else:
            result = {
            'status':'fail',
            'message': 'no task'
            }
        
    else:
        result = {'status':'fail'}     
    return jsonify(result)


# RESTful 任务查询
@app.route('/users/<user_id>/tasks/search', methods=['GET'])
@token_required
def search_all_tasks(current_user, user_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    d = request.get_json()

    
    task_diff_set = searchTask(d)

    task_info = []

    for task in task_diff_set:
        task_info.append(printSingleTask(task))
        
    return jsonify(task_info), 200



#############################################################






# util func
def printSingleTask(task):
    participant_ids = []
    ongoing_participant_ids = []
    waiting_examine_participant_ids = []
    finished_participant_ids = []

    for par in task.received_tasks:
        par_user_id = par.user_id
        participant_ids.append(par_user_id)
        if par.status == 'on going':
            ongoing_participant_ids.append(par_user_id)
        elif par.status == 'waiting examine':
            waiting_examine_participant_ids.append(par_user_id)
        elif par.status == 'finished':
            finished_participant_ids.append(par_user_id)

    return {"task_id": task.id, 
                    "creator_user_id": task.user_id,
                    "creator_organization_id": task.organization_id,
                    "status": task.status,
                    "title": task.title,
                    "description": task.description,
                    "tags": json.loads(task.tags),
                    "participant_number_limit": task.participant_number_limit,
                    "reward_for_one_participant": task.reward_for_one_participant,
                    "post_time": task.post_time,
                    "receive_end_time": task.receive_end_time,
                    "finish_deadline_time": task.finish_deadline_time,
                    "user_limit": json.loads(task.user_limit),
                    "steps": json.loads(task.steps),
                    "participant_ids": participant_ids,
                    "ongoing_participant_ids": ongoing_participant_ids,
                    "waiting_examine_participant_ids": waiting_examine_participant_ids,
                    "finished_participant_ids": finished_participant_ids
                    }


@app.route('/users/register', methods=['POST', 'GET'])
def uploadFile():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        telephone = request.form['telephone']
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], newFileName))

        else:
            filename = 'default.jpg'
            newFileName = 'default.jpg'

        addUser(username, email, hashed_password, telephone, newFileName)

        result = {
            'username': username,
            'email': email,
            'password': password,
            'telephone': telephone,
            'image_file': newFileName
        }

        return jsonify({'result': result})



