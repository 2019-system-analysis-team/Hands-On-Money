from moneyapp import db
from moneyapp.models import User, Organization, Task, Receiver_Task, Organization_Member, Transaction
import json
from flask import jsonify

# ====================================================================
# User
# 访客基础信息
def addUser(_username, _email, _hashed_password, _telephone, _image_file):
    user = User(username=_username, email=_email, password=_hashed_password, telephone=_telephone, image_file=_image_file)
    db.session.add(user)
    db.session.commit()
    return user.id


# 一开始就填详细信息成为用户
def addUser_detailed(_username, _email, _hashed_password, _telephone, _image_file, _student_id, _realname, _age, _sex, _grade, _school, _bio):
    user = User(username=_username, email=_email, password=_hashed_password, telephone=_telephone, image_file=_image_file, student_id=_student_id, realname=_realname, age=_age, sex=_sex, grade=_grade, school=_school, bio=_bio)
    db.session.add(user)
    db.session.commit()

# 修改操作(不包括密码修改)
def modify_profile(_username_ori, _username, _email, _telephone, _image_file, _age, _sex, _grade, _school, _bio):
    user = User.query.filter_by(username=_username_ori).first()
    
    user.username = _username
    user.email = _email
    user.telephone = _telephone
    user.image_file = _image_file
    user.age = _age
    user.sex = _sex
    user.grade = _grade
    user.school = _school
    user.bio = _bio

    db.session.commit()


def queryUser(_username):
    user = User.query.filter_by(username=_username).first()
    return user

def queryUserById(_id):
    user = User.query.filter_by(id=_id).first()
    return user

def queryUserByEmail(_email):
    user = User.query.filter_by(email=_email).first()
    return user

def queryUserByTelephone(_telephone):
    user = User.query.filter_by(telephone=_telephone).first()
    return user




# ====================================================================
# Organization
def addOrganization(_name, _image_file, _bio):
    organization = Organization(name=_name, image_file=_image_file, bio=_bio)
    db.session.add(organization)
    db.session.commit()

    all_organizations = Organization.query.all()

    id = len(all_organizations)

    return id



def chargeForOrganization(_user_id, _organization_id, _money):
    transaction = Transaction(user_id=_user_id, organization_id=_organization_id, money=_money)
    

    organization = Organization.query.filter_by(id=_organization_id).first()
    organization.balance += float(_money)
    
    db.session.add(transaction)
    db.session.commit()

def queryOrganizationByID(_organization_id):
    organization = Organization.query.filter_by(id=_organization_id).first()
    return organization
#----------------------------------------------
#todo 删除组织信息
#是否需要考虑将组织成员内的组织信息删除
def deleteOrganization(_organization_id):
        organization = Organization.query.filter_by(id=_organization_id).first()
        
        # 删除organization member
        for record in organization.organization_members:
            db.session.delete(record)

        # 删除organization名下的task
        for task in organization.tasks:
            # 删除接受了该组织的任务的记录
            for received_record in task.received_tasks:
                db.session.delete(received_record)

            db.session.delete(task)

        db.session.delete(organization)
        db.session.commit()

#-----------------------------------------------
#todo 按名字搜索组织
def queryOrganizationByName(_organization_name):
    organization = Organization.query.filter_by(name=_organization_name).first()
    return organization

#--------------------------------------------------
#todo 改变组织信息
def modify_orgfile(_organization_id,_organization_name,_organization_bio, _image_file):

    organization = Organization.query.filter_by(id = _organization_id).first()

    organization.name = _organization_name
    organization.bio = _organization_bio
    organization.image_file = _image_file

    db.session.commit()

# ===============================================================
# Organization Member
def addMember(_user_id, _organization_id, _status):
    organization_member = Organization_Member(user_id=_user_id, organization_id=_organization_id, status=_status)
    db.session.add(organization_member)
    db.session.commit()

# 可以用于判断xx用户是否是xx组织成员，有没有权限以组织名义发任务
def queryRecord(_user_id, _organization_id):
    record = Organization_Member.query.filter_by(user_id=_user_id, organization_id=_organization_id).first()
    if record:
        return record
#--------------------------------------------------------------------
#todo
#判断用户是否接收了该任务
def queryReceiverTask(_user_id,_task_id):
    record = Receiver_Task.query.filter_by(user_id=_user_id,task_id=_task_id).first()
    if record:
        return record
#--------------------------------------------------------

#--------------------------------------------------
#todo
#设置管理员:
def addManager(_user_id,_organization_id):
    organization_member = Organization_Member.query.filter_by(user_id=_user_id , organization_id = _organization_id).first()
    organization_member.status = 'manager'
    db.session.commit()


# ====================================================================
# Task
# no organization
# def createTask(_user_id, _money, _tag, _number, _applicapable_user, _title, _description, _status):
#   task = Task(user_id=_user_id, money=_money, tag=_tag, number=_number, applicapable_user=_applicapable_user, title=_title, description=_description, status=_status)
#   user = User.query.filter_by(id=_user_id).first()
#   user.balance -= float(_money)
#   db.session.add(task)
#   db.session.commit()

def createTask(_user_id, _organization_id, _money, _tags, _number, _post_time, _receive_end_time, _finish_deadline_time, _title, _description, _user_limit, _steps):
    task = Task(user_id=_user_id, organization_id=_organization_id, money=_money, tags=_tags, number=_number, post_time=_post_time, 
            receive_end_time=_receive_end_time, finish_deadline_time=_finish_deadline_time, title=_title, description=_description, 
            user_limit=_user_limit, steps = _steps)
    db.session.add(task)
    db.session.commit()

    return task

def createTaskOrganization(_organization_id, _user_id, _money, _tag, _number, _applicapable_user, _title, _description, _status):
    task = Task(organization_id=_organization_id, user_id=_user_id, money=_money, tag=_tag, number=_number, applicapable_user=_applicapable_user, title=_title, description=_description, status=_status)
    organization = Organization.query.filter_by(id=_organization_id).first()
    organization.balance -= float(_money)
    db.session.add(task)
    db.session.commit()#-----------------------------------------------------------------

#todo 
#delete task user
def deleteTask(_user_id,_task_id):
    task = Task.query.filter_by(id=_task_id).first()
    
    # 删除和任务相关的Receiver_Task里面的记录
    # backref！
    for rec in task.received_tasks:
        db.session.delete(rec)

    money = task.money
    user = User.query.filter_by(id=_user_id).first()
    user.balance += float(money) # 钱返还
    


    db.session.delete(task)
    db.session.commit()

#----------------------------------------------------------------
#todo 
#delete task organization

def deleteTaskOrganization(_organization_id,_task_id):
    task = Task.query.filter_by(id=_task_id).first()
    
    for rec in task.received_tasks:
        db.session.delete(rec)

    money = task.money
    organization = Organization.query.filter_by(id=_organization_id).first()
    organization.balance += float(money)
    db.session.delete(task)
    db.session.commit()

# ======================================================
# Receiver_Task
def receiveTask(_user_id, _task_id):
    task = queryTaskById(_task_id)
    user_number = Receiver_Task.query.filter_by(task_id=_task_id).count()
    
    user_number_limitation = task.number
    #users_number = task.received_tasks
    print("user num",user_number)
    if user_number_limitation <= user_number:
        raise ValueError("The user number has reached the limitation")
    receiver_task = Receiver_Task(user_id=_user_id, task_id=_task_id)
    db.session.add(receiver_task)
    db.session.commit()

# =====================================================
# Money
def checkBalance(_user_id, _organization_id, _money):
    if _organization_id:
        organization = queryOrganizationByID(_organization_id)
        return organization.balance >= _money
    elif _user_id:
        user = queryUserById(_user_id)
        return user.balance >= _money
#---------------------------------------
#todo 给个人账号充值
def chargeForUser(_user_id,_money):
    transaction = Transaction(user_id=_user_id,money=_money)
    user = User.query.filter_by(id = _user_id).first()
    user.balance += float(_money)
    db.session.add(transaction)
    db.session.commit()

#--------------------------------------------
#todo
#按照tag搜索task
def queryTaskByTag(_tag):
    task = Task.query.filter_by(tag=_tag).first()
    return task
#------------------------------------------------------
#todo
#按照user_id和task_id 搜索是否存在该task
def queryTaskById(_id):
    # task = None
    task = Task.query.filter_by(id=_id).first()
    return task
#---------------------------------------------------------
#todo
#改变status
def changTaskStatus(_id,_status):
    task = Task.query.filter_by(id = _id).first()
    task.status = _status
    db.session.commit()
#---------------------------------------------------------
#todo
#用户修改任务完成状态
def userChangeReceiveTask(_user_id,_task_id,_step_id):
    task_record = Receiver_Task.query.filter_by(user_id=_user_id,task_id=_task_id).first()
    
    if not task_record:
        raise AssertionError('Insufficient permission') 

    if task_record.status == 'finished':
        raise AssertionError('Task has already finished!')

    task_steps_json_str = task_record.task.steps
    task_steps = json.loads(task_steps_json_str)
    steps_num = len(task_steps)
    
    # step_id 超过规定的step_num 或者step_id已经标记过了
    if _step_id > steps_num or _step_id <= task_record.step or _step_id != (task_record.step + 1):
        raise ValueError('Step number incorrect')

    task_record.step = _step_id

    # 已经完成最后一步了
    if _step_id == steps_num:
        task_record.status = 'waiting examine'

    db.session.commit()

    return task_record

def finishUserTask(_task_id, _finisher_id):
    task_record = Receiver_Task.query.filter_by(user_id=_finisher_id,task_id=_task_id).first()
    
    if not task_record:
        raise AssertionError("The user hasn't taken this task") 

    if task_record.status == 'finished':
        raise AssertionError('Task has already finished!')

    if task_record.status != 'waiting examine':
        raise AssertionError("The user hasn't finished all the steps")

    task_record.status = 'finished'

    db.session.commit()
    return task_record.task

#----------------------------------------------------------
#todo 
#按照user_id和organization 搜索组织成员
def queryMemberById(_user_id,_organization_id):
    organization_member = Organization_Member.query.filter_by(user_id=_user_id , organization_id =_organization_id).first()
    return organization_member






 