import os, datetime
import json
import re
import uuid
import jwt
from werkzeug.utils import secure_filename
from flask import render_template, url_for, request, flash, jsonify, make_response
from moneyapp import app, db, bcrypt
from moneyapp.models import User, Organization, Task, Receiver_Task, Organization_Member, Transaction
from moneyapp.db_operations import addUser, queryUser, addUser_detailed, addOrganization, createTask, createTaskOrganization, modify_profile, receiveTask, addMember, queryRecord, chargeForOrganization, checkBalance,queryUserById,chargeForUser,queryOrganizationByID,deleteOrganization, queryUserByEmail
from moneyapp.db_operations import queryOrganizationByName,addManager,queryTaskByTag,userChangeReceiveTask,queryReceiverTask,changTaskStatus,queryTaskById
from flask_jwt import JWT, jwt_required, current_identity
from functools import wraps

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/profile_pics')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'thisisansecretkey'

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

def authenticate(username, password):
    user = queryUser(username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)



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


##=========== Users ============
# RESTful 用户登录
@app.route('/sessions', methods=['POST'])
def login():
    email = request.get_json()['email']
    password = request.get_json()['password']

    user = queryUser(email)

    if user:
        if bcrypt.check_password_hash(user.password, password):
            token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, app.config['SECRET_KEY'])
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
        to_return = jsonify({'error_code': 404,
                         'error_msg': 'User Not Found'})
        return make_response(to_return, 404)

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
            
            token = jwt.encode({'id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, app.config['SECRET_KEY'])


            to_return = jsonify({'user_id': user_id,
                         'access_token': token.decode('UTF-8')})
            return make_response(to_return, 201)

        
        except Exception as e:
            err_msg = re.findall(r"UNIQUE constraint failed: .*", str(e))
            to_return = jsonify({'error_code': 409,
                         'error_msg': str(e)})
            return make_response(to_return, 409)
  
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




# 注册
@app.route('/users/register_test', methods=['POST', 'GET'])
def test_regis():
    if request.method == 'POST':
        email = request.form['email']
        telephone = request.form['telephone']
        #image_file = request.form['image_file']
        #student_id = request.form['student_id']
        #realname = request.form['realname']
        #age = request.form['age']
        #sex = request.form['sex']
        #grade = request.form['grade']
        #school = request.form['school']
        #bio = request.form['bio']
        username = request.form['username']
        password = request.form['password']
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
    


##============ Organization ============
@app.route('/organizations/create_test', methods=['POST', 'GET'])
def test_org_create():
    if request.method=='POST':
        name = request.form['name']
        bio = request.form['bio']
        user_id = request.form['user_id']
        

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

        organization_id = addOrganization(name, newFileName, bio)

        addMember(user_id, organization_id, "owner")


        result = jsonify({"result": "add!"})

    return result

# TODO owner删除组织
@app.route('/organizations/delete', methods=['POST'])
def delete_organization():
    """
    需要首先在db_operations.py里面实现一个删除函数
    然后在这里调用
    需要判断操作者是否为组织的创建者（owner）
    可以使用queryRecord来获得user和organization的记录
    利用status判断是否为创建者
    :param request.form['user_id'] 用户id
    :param request.form['organization_id'] 组织id
    :rtype: json {"status": "", "message": ""}
    """
    if request.method == 'POST':
        user_id = request.form['user_id']
        organization_id = request.form['organization_id']
        organization = queryOrganizationByID(organization_id)
        if organization:
            #判断是否为组织的创建者
            record = queryRecord(user_id,organization_id)
            if record and record.status == 'owner':
                deleteOrganization(organization_id)
                result = {"status": "success", 
                      "message": "Successfully delete"}
            else:
                result = {"status":"fail",
                        "message":"No Permission"}
        else:
            result = {"status": "fail",
                      "message": "No Organization"}
    else:
        result = {"status": "fail",
                  "message": "no post"}
    return jsonify(result)

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



##=========== Organization Member ==========
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
            if owner.status == 'owner' and member.status == 'ordinary':
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


# 群主管理员添加成员
@app.route('/organizations/add_member', methods=['POST'])
def add_organization_member():
    if request.method == 'POST':
        user_id = request.form['user_id']
        organization_id = request.form['organization_id']
        status = request.form['status']
        
        record = queryRecord(user_id, organization_id)

        if record and record.status != 'ordinary member':

            addMember(user_id, organization_id, "ordinary member")

            result = jsonify({"result": "add!"})

        else:
            result = jsonify({"result": "Permission denied!"})

    else:
        result = jsonify({"result": "not add!"})

    return result


##================ Task =======================
# 用户个人创建
@app.route('/task/create_test', methods=['POST', 'GET'])
def test_task_create():
    if request.method=='POST':
        user_id = request.form['user_id']
        money = request.form['money']
        tag = request.form['tag']
        number = request.form['number']
        applicapable_user = request.form['applicapable_user']
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']

        if checkBalance(user_id, None, float(money)):
            createTask(user_id, money, tag, number, applicapable_user, title, description, status)
            result = jsonify({"result": "add!"})
        else:
            result = jsonify({"status":"fail", "message":"no enough money"})

    return result

# TODO 用户个人删除自己发布的任务
@app.route('/task/delete', methods=['POST'])
def delete_user_task():
    """
    需要首先在db_operations.py里面实现一个删除函数
    然后在这里调用
    :param request.form['user_id'] 用户id
    :param request.form['task_id'] 任务id
    :rtype: json {"status": "", "message": ""}
    """
    if request.method == 'POST':
        user_id = request.form['user_id'];
        task_id = request.form['task_id'];
        deleteTask(user_id,task_id);
        result = {'status':"successfully",
                  'message':'delete!'}

    else:
        result = {'status': 'fail',
                  'message':'no post'}
    
    return jsonify(result)

# 组织创建
@app.route('/task/create_organization', methods=['POST'])
def organization_create_task():
    if request.method == 'POST':
        user_id = request.form['user_id']
        organization_id = request.form['organization_id']
        record = queryRecord(user_id, organization_id)
        
        # 群主或管理员才可以新建任务
        if record and record.status != 'ordinary member':
            money = request.form['money']
            tag = request.form['tag']
            number = request.form['number']
            applicapable_user = request.form['applicapable_user']
            title = request.form['title']
            description = request.form['description']
            status = request.form['status']
            if checkBalance(user_id, organization_id, float(money)):
                createTaskOrganization(organization_id, user_id, money, tag, number, applicapable_user, title, description, status)
                result = jsonify({"result": "add!"})
            else:
                result = jsonify({"status":"fail", "message":"no enough money"})
        else:
            result = jsonify({"result": "Permission denied!"})

    else:
        result = jsonify({"result": "not add!"})

    return result

# TODO 组织管理员删除任务
@app.route('/task/organization_delete', methods=['POST'])
def delete_organization_task():
    """
    需要首先在db_operations.py里面实现一个删除函数
    需要判断操作者是否为组织的管理员
    可以使用queryRecord来获得user和organization的记录
    利用status判断是否为管理员
    :param request.form['user_id'] 用户id
    :param request.form['task_id'] 任务id
    :param request.form['organization_id'] 组织id
    :rtype: json {"status": "", "message": ""}
    """
    if request.method == 'POST':
        user_id = request.form['user_id']
        task_id = request.form['task_id']
        organization_id = request.form['organization_id']
        organization_member = queryMemberById(user_id,organization_id)
        if organization_member.status != 'ordinary':
            deleteTaskOrganization(organization_id,task_id)
            result = {'status':'true',
                      'message':'successfully delete!'}
    return jsonify(result)

# 接收任务
@app.route('/task/receive_task', methods=['POST'])
def receive_task():
    if request.method == 'POST':
        user_id = request.form['user_id']
        task_id = request.form['task_id']

        receiveTask(user_id, task_id)

        result = jsonify({"result": "add!"})

        return result

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
            changTaskStatus(task_id,status)
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



##=================================================


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
