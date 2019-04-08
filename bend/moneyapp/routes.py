import os, datetime
import json
import uuid
from werkzeug.utils import secure_filename
from flask import render_template, url_for, request, flash, jsonify
from moneyapp import app, db, bcrypt
from moneyapp.models import User, Organization, Task, Receiver_Task
from moneyapp.db_operations import addUser, queryUser, addUser_detailed, addOrganization, createTask, modify_profile, receiveTask

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/profile_pics')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



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
@app.route('/users/search', methods=['POST'])
def search():
    username = request.get_json()['username2']

    user = queryUser(username)

    if user:
        result = jsonify({"username": user.username, "email": user.email, "image_file": user.image_file})
    else:
        result = jsonify({"error": "No such user"})

    return result

# 登录
@app.route('/users/login', methods=['POST', 'GET'])
def userLogin():
    if request.method == 'GET':
        # 暂时先考虑只用username进行登录，以后再修改
        username = request.form['username']
        password = request.form['password']
        user = queryUser(username)
        if user:
            if bcrypt.check_password_hash(user.password, password):
                result = jsonify({"status": "success", "message": "Successfully login!"})
            else:
                result = jsonify({"status": "fail", "message": "password incorrect"})
        else:
            result = jsonify({"status": "fail", "message": "no such user"})

        return result


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

# 查找用户信息
@app.route('/users/search_user', methods=['POST', 'GET'])
def search_user():
    if request.method == 'GET':
        username = request.form['username']
        user = queryUser(username)
        if user:
            task_titles = []
            for task in user.tasks:
                task_titles.append(task.title)
            result = {
                'status': 'true',
                'username': user.username,
                'bio': user.bio,
                'tasks': task_titles
            }
        else:
            result = {
                'status': 'false',
                'message': 'no such user'
            }



        return jsonify({'result': result})

#======================================
    


##============ Organization ============
@app.route('/organizations/create_test', methods=['POST', 'GET'])
def test_org_create():
    if request.method=='POST':
        name = request.form['name']
        image_file = request.form['image_file']
        bio = request.form['bio']
        addOrganization(name, image_file, bio)

        result = jsonify({"result": "add!"})

    return result

@app.route('/organizations/')


##================ Task =======================
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

        createTask(user_id, money, tag, number, applicapable_user, title, description, status)

        result = jsonify({"result": "add!"})

    return result

@app.route('/task/receive_task', methods=['POST'])
def receive_task():
    if request.method == 'POST':
        user_id = request.form['user_id']
        task_id = request.form['task_id']

        receiveTask(user_id, task_id)

        result = jsonify({"result": "add!"})

        return result



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
