from moneyapp import db
from moneyapp.models import User, Organization, Task, Receiver_Task, Organization_Member, Transaction
import json
from flask import jsonify
from datetime import datetime
# ====================================================================
# User
# 访客基础信息
def addUser(_nickname, _email, _hashed_password, _phone_number, _profile_photo_path):
    user = User(nickname=_nickname, email=_email, password=_hashed_password, phone_number=_phone_number, profile_photo_path=_profile_photo_path)
    db.session.add(user)
    db.session.commit()
    return user.id


# 一开始就填详细信息成为用户
def addUser_detailed(_nickname, _email, _hashed_password, _phone_number, _profile_photo_path, _student_id, _name, _age, _sex, _grade, _school, _bio):
    user = User(nickname=_nickname, email=_email, password=_hashed_password, phone_number=_phone_number, profile_photo_path=_profile_photo_path, student_id=_student_id, name=_name, age=_age, sex=_sex, grade=_grade, school=_school, bio=_bio)
    db.session.add(user)
    db.session.commit()

# 修改操作(不包括密码修改)
def modify_profile(_nickname_ori, _nickname, _email, _phone_number, _profile_photo_path, _age, _sex, _grade, _school, _bio):
    user = User.query.filter_by(nickname=_nickname_ori).first()
    
    user.nickname = _nickname
    user.email = _email
    user.phone_number = _phone_number
    user.profile_photo_path = _profile_photo_path
    user.age = _age
    user.sex = _sex
    user.grade = _grade
    user.school = _school
    user.bio = _bio

    db.session.commit()


def queryUser(_nickname):
    user = User.query.filter_by(nickname=_nickname).first()
    return user

def queryUserById(_id):
    user = User.query.filter_by(id=_id).first()
    return user

def queryUserByEmail(_email):
    user = User.query.filter_by(email=_email).first()
    return user

def queryUserByphone_number(_phone_number):
    user = User.query.filter_by(phone_number=_phone_number).first()
    return user




# ====================================================================
# Organization
def addOrganization(_name, _profile_photo_path, _bio):
    organization = Organization(name=_name, profile_photo_path=_profile_photo_path, bio=_bio)
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
def modify_orgfile(_organization_id,_organization_name,_organization_bio, _profile_photo_path):

    organization = Organization.query.filter_by(id = _organization_id).first()

    organization.name = _organization_name
    organization.bio = _organization_bio
    organization.profile_photo_path = _profile_photo_path

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




def createTask(d):
    items = {'user_id', 'organization_id', 'title', 'description', 'tags', 'participant_number_limit',\
            'reward_for_one_participant', 'post_time', 'receive_end_time',\
            'finish_deadline_time', 'user_limit', 'steps'}
    for arg in items:
        if arg not in d and arg not in {'post_time', 'receive_end_time', 'finish_deadline_time'}:
            d[arg] = None
        elif arg == 'tags' or arg == 'steps' or arg == 'user_limit':
            d[arg] = json.dumps(d[arg])

    task = Task(**d)
    db.session.add(task)
    db.session.commit()

    status = None
    steps_number = None
    if task.post_time and task.receive_end_time and task.finish_deadline_time:
        status = "on going" if (datetime.utcnow() > task.post_time and datetime.utcnow() < task.finish_deadline_time) else "not ongoing"
    else:
        status = 'not onging'

    if 'steps' in d:
        steps_number = len(json.loads(d['steps']))
    
    task.status = status
    task.steps_number = steps_number
   
    
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
def deleteTask(_user_id,_task_id, _organization_id):
    task = Task.query.filter_by(id=_task_id).first()
    
    # 删除和任务相关的Receiver_Task里面的记录
    # backref！
    for rec in task.received_tasks:
        db.session.delete(rec)

    money = task.reward_for_one_participant * task.participant_number_limit

    if _organization_id == None:
        user = User.query.filter_by(id=_user_id).first()
        user.balance += float(money) # 钱返还
    else:
        organization = queryOrganizationByID(_organization_id)
        organization.balance += float(money)
    


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
    
    user_number_limitation = task.participant_number_limit
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


 
def searchTask(d):
    # 先用status title finish_deadline_time 找一波
    #if d['']
    for arg in d:
        print(arg)
    task_2 = queryTaskById(2)
    task_2_limitation = json.loads(task_2.user_limit)
    print(task_2_limitation['schools'])

    task_temp = Task.query

    if 'title' in d:
        task_temp = task_temp.filter(Task.title.like('%' + d['title'] + '%'))

    # 时间筛选还要再思考一下
    if 'receive_end_time' in d:
        task_temp = task_temp.filter(Task.receive_end_time == d['receive_end_time'])

    if 'finish_deadline_time' in d:
        task_temp = task_temp.filter(Task.finish_deadline_time == d['finish_deadline_time'])

    if 'reward_for_one_participant_upper' in d:
        task_temp = task_temp.filter(Task.reward_for_one_participant <= d['reward_for_one_participant_upper'])

    if 'reward_for_one_participant_lower' in d:
        task_temp = task_temp.filter(Task.reward_for_one_participant >= d['reward_for_one_participant_lower'])

    task_temp = set(task_temp)
    task_temp_difference_set = set()
    task_not_satisfy = set()
    
    for task in task_temp:
        steps_number_of_task = len(json.loads(task.steps))
        if 'steps_number_lower' in d:
            if not steps_number_of_task >= d['steps_number_lower']:
                task_not_satisfy.add(task)
                continue
        if 'steps_number_upper' in d:
            if not steps_number_of_task <= d['steps_number_upper']:
                task_not_satisfy.add(task)
                continue
        if 'tags' in d:
            if not set(d['tags']).issubset(set(json.loads(task.tags))):
                task_not_satisfy.add(task)
                continue
        
        creator_user = task.user
        if 'creator_user_email' in d:
            if not d['creator_user_email'] == creator_user.email:
                task_not_satisfy.add(task)
                continue

        if 'creator_user_phone_number' in d:
            if not d['creator_user_phone_number'] == creator_user.phone_number:
                task_not_satisfy.add(task)
                continue

        # 模糊匹配还没有设置
        if 'creator_organization_name' in d:
            creator_organization = task.organization
            if not creator_organization or not d['creator_organization_name'] == creator_organization.name:
                task_not_satisfy.add(task)
                continue

        if 'user_limit' in d:
            user_limit_task = json.loads(task.user_limit)
            for arg in d['user_limit']:
                try:
                    limit_temp = user_limit_task[arg]
                except:
                    task_not_satisfy.add(task)
                    break
                else:
                    if arg == 'age_upper':
                        if not limit_temp <= d['user_limit'][arg]:
                            task_not_satisfy.add(task)
                            break
                    elif arg == 'age_lower':
                        if not limit_temp >= d['user_limit'][arg]:
                            task_not_satisfy.add(task)
                            break
                    elif arg == 'grades' or arg == 'sexes' or arg == 'schools':
                        set_task = set(limit_temp)
                        set_search = set(d['user_limit'][arg])
                        if not set_search.issubset(set_task):
                            task_not_satisfy.add(task)
                            break
            continue

    task_temp_difference_set = task_temp - task_not_satisfy
    # for task in task_temp_difference_set:
    #     print(task.title)
    return task_temp_difference_set

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
# 可能之后要考虑别人任务列表里面删除任务
def changeTaskStatus(_user_id, _task_id, _status, _organization_id):
    task = Task.query.filter_by(id = _task_id).first()
    if not _organization_id:
        if task.user.id != _user_id:
            raise AssertionError("Insufficient permission")
        elif task.status == 'pending':
            raise AssertionError("Already pended")
        else:
            task.status = 'pending'
    else:
        if task.organization.id != _organization_id:
            raise AssertionError("Insufficient permission")
        else:
            record = queryRecord(_user_id, _organization_id)
            if record.status == 'member':
                raise AssertionError("Insufficient permission")
            else:
                # task.post_time = None
                # task.receive_end_time = None
                # task.finish_deadline_time = None
                task.status = 'pending'
    
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


# 修改任务信息

def modifyTask(_task_id, _user_id, _organization_id, d):
    task = Task.query.filter_by(id = _task_id).first()
    
    if not _organization_id:
        if task.user.id != _user_id:
            print("task user id", task.user.id)
            print("_user_id", _user_id)
            raise AssertionError("Insufficient permission")
        
    else:
        if task.organization.id != _organization_id:
            raise AssertionError("Insufficient permission")
        else:
            record = queryRecord(_user_id, _organization_id)
            if record.status == 'member':
                raise AssertionError("Insufficient permission")

    if task.status != 'pending':
        raise AssertionError("The task is not pended")

    items = {'title', 'description', 'tags', 'participant_number_limit',\
            'reward_for_one_participant', 'post_time', 'receive_end_time',\
            'finish_deadline_time', 'user_limit', 'steps'}
    
    before_cost = None
    
    if task.participant_number_limit != None and task.reward_for_one_participant != None:
        before_cost = task.reward_for_one_participant * task.participant_number_limit

    for arg in items:
        if arg == 'tags' or arg == 'steps' or arg == 'user_limit':
            d[arg] = json.dumps(d[arg])
        
    Task.query.filter_by(id=_task_id).update(d)
    
    if 'participant_number_limit' in d and 'reward_for_one_participant' in d and before_cost != None:
        after_cost = d['participant_number_limit'] * d['reward_for_one_participant']
        delta = after_cost - before_cost

    # check balance
    if checkBalance(_user_id, _organization_id, delta):
        if not _organization_id:
            user = queryUserById(_user_id)
            user.balance -= delta
        else:
            print("hhhhh")
            organization = queryOrganizationByID(_organization_id)
            organization.balance -= delta
    else:
        raise ValueError("Not enough money")
    
    db.session.commit()



    #task = Task.query.filter_by(id = _task_id).first()

    # status = None
    # steps_number = None
    # if task.post_time and task.receive_end_time and task.finish_deadline_time:
    #     status = "on going" if (datetime.utcnow() > task.post_time and datetime.utcnow() < task.finish_deadline_time) else "not ongoing"
    # else:
    #     status = 'not onging'

    # if 'steps' in d:
    #     steps_number = len(json.loads(d['steps']))
    
    # task.status = status
    # task.steps_number = steps_number
   
    
    #db.session.commit()

    return task
    
    
    # task.reward_for_one_participant = _money
    # task.tag = _tags
    # task.participant_number_limit = _number
    # task.post_time = _post_time
    # task.receive_end_time = _receive_end_time
    # task.finish_deadline_time = _finish_deadline_time
    # task.title = _title
    # task.description = _description
    # task.user_limit = _user_limit
    # task.steps = _steps

    # db.session.commit()



 
