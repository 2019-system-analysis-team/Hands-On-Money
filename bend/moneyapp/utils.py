from moneyapp.models import db, User, Organization, Task, Receiver_Task, Organization_Member, Transaction, Feedback_Review, Customer_Review
import json
from flask import jsonify
from datetime import datetime

def createTransaction(_user_id, _organization_id, _money):
    transaction = Transaction(user_id=_user_id, organization_id=_organization_id, money=_money, time=datetime.now())
    db.session.add(transaction)
    db.session.commit()
    return transaction
     

def queryUserById(_id):
    user = User.query.filter_by(id=_id).first()
    return user


def queryOrganizationByID(_organization_id):
    organization = Organization.query.filter_by(id=_organization_id).first()
    return organization


def checkBalance(_user_id, _organization_id, _money):
    if _organization_id:
        organization = queryOrganizationByID(_organization_id)
        return organization.balance >= _money
    elif _user_id:
        user = queryUserById(_user_id)
        return user.balance >= _money


# 检查用户是否创建了某个任务
def checkUserCreateTask(_user_id, _task_id):
    task = Task.query.filter_by(id=_task_id, user_id=_user_id).first()
    return task

# 检查用户是否以组织成员身份创建了某个任务
def checkUserOrgCreateTask(_organization_id, _task_id):
    task = Task.query.filter_by(id=_task_id, organization_id=_organization_id).first()
    return task


# 检查用户是否接受了某个任务
def checkUserReceiveTask(_user_id, _task_id):
    task_record = Receiver_Task.query.filter_by(user_id=_user_id,task_id=_task_id).first()
    if task_record is None:
        return None
    else:
        return task_record

# 打印任务信息
def printSingleTask(task):
    participant_ids = []
    ongoing_participant_ids = []
    waiting_examine_participant_ids = []
    finished_participant_ids = []

    # 获取creator
    creator = queryUserById(task.user_id)
    org_name = None
    
    if task.organization:
        org_name = task.organization.name

    count = 0

    for par in task.received_tasks:
        count += 1
        par_user_id = par.user_id
        participant_ids.append(par_user_id)
        if par.status == 'on going':
            ongoing_participant_ids.append(par_user_id)
        elif par.status == 'waiting examine':
            waiting_examine_participant_ids.append(par_user_id)
        elif par.status == 'finished':
            finished_participant_ids.append(par_user_id)

        
    task_tag_info = None
    if task.tags is not None:
        task_tag_info = json.loads(task.tags)

    user_limit_info = None
    if task.user_limit is not None:
        user_limit_info = json.loads(task.user_limit)

    steps_info = None
    if task.steps is not None:
        steps_info = json.loads(task.steps)
    return {"task_id": task.id, 
                    "user_id": creator.id, #???
                    "creator_user_email": creator.email,
                    "creator_user_phone_number": creator.phone_number,
                    "creator_user_name": creator.nickname, # ????
                    "creator_organization_name": org_name,
                    "status": task.status,
                    "title": task.title,
                    "description": task.description,
                    "tags": task_tag_info,
                    "current_participant_number": count,
                    "participant_number_limit": task.participant_number_limit,
                    "reward_for_one_participant": task.reward_for_one_participant,
                    "post_time": task.post_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "receive_end_time": task.receive_end_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "finish_deadline_time": task.finish_deadline_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "user_limit": user_limit_info,
                    "steps": steps_info,
                    "participant_ids": participant_ids,
                    "ongoing_participant_ids": ongoing_participant_ids,
                    "waiting_examine_participant_ids": waiting_examine_participant_ids,
                    "finished_participant_ids": finished_participant_ids
                    }

# 打印任务简介
def printTaskBrief(task):
    return {"task_id": task.id,
            "task_name": task.title,
            "task_status": task.status}

# 打印任务简介（包括step）
def printTaskBriefReceive(received_task_record):
    task = received_task_record.task
    return {"task_id": task.id,
            "task_name": task.title,
            "task_status": task.status,
            "current_step": received_task_record.step}

# 打印任务简介（包括step）
def printTaskBriefReceiveStatus(received_task_record):
    task = received_task_record.task
    return {"task_id": task.id,
            "task_name": task.title,
            "task_status": task.status,
            "task_receiver_status": received_task_record.status}



# 打印参与者信息
def printUserInfoOfTask(task):
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
            "participant_ids": participant_ids,
            "ongoing_participant_ids": ongoing_participant_ids,
            "waiting_examine_participant_ids": waiting_examine_participant_ids,
            "finished_participant_ids": finished_participant_ids
            }

# 打印公共任务信息
def printPublicSingleTask(task):
    participant_ids = []
    ongoing_participant_ids = []
    waiting_examine_participant_ids = []
    finished_participant_ids = []

    organization_name = None
    user = queryUserById(task.user.id)
    if task.organization is not None:
        organization = queryOrganizationByID(task.organization.id)
        organization_name = organization.name
    for par in task.received_tasks:
        par_user_id = par.user_id
        participant_ids.append(par_user_id)
        if par.status == 'on going':
            ongoing_participant_ids.append(par_user_id)
        elif par.status == 'waiting examine':
            waiting_examine_participant_ids.append(par_user_id)
        elif par.status == 'finished':
            finished_participant_ids.append(par_user_id)

    return {        "task_id": task.id, 
                    "user_id": user.id, #??
                    "creator_user_email": user.email,
                    "creator_user_phone_number": user.phone_number,
                    "creator_organization_name": organization_name,
                    "creator_user_name": user.nickname, # ???
                    "status": task.status,
                    "title": task.title,
                    "description": task.description,
                    "tags": json.loads(task.tags),

                    "current_participant_number":len(participant_ids),
                    "participant_number_limit": task.participant_number_limit,
                    "reward_for_one_participant": task.reward_for_one_participant,
                    "post_time": task.post_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "receive_end_time": task.receive_end_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "finish_deadline_time": task.finish_deadline_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "user_limit": json.loads(task.user_limit),
                    "steps": json.loads(task.steps)
                    }


# 检查用户是否完成了某个任务
def checkFinishTask(received_task_record):
    
    if received_task_record.status != 'finished':
        return False
    else:
        return True

# 检查用户是否已经写过评论
def checkCommentCreated(_user_id, _task_id):
    record = Customer_Review.query.filter_by(user_id=_user_id, task_id=_task_id).first()
    if record is None:
        return False
    else:
        return True

# 打印一条评论
def printSingleReview(review):
    return {"nickname": review.user.nickname,
            "title": review.title,
            "content": review.content,
            "rate": review.rate}

# 发布者的平均分
def updateAvgComment(_task_id):
    task = Task.query.filter_by(id=_task_id).first()
    if task.organization_id is None:
        # 个人
        user = task.user
        # print('em,,')
        # print(user.nickname)
        # print('end')

        all_tasks = user.tasks
        all_reviews = []
        for task in all_tasks:
            all_reviews.extend(task.customer_reviews)
        #customer_reviews = task.customer_reviews

        count = 0
        total_points = 0

        if len(all_reviews) == 0:
            user.average_comment = 5.0

        else:
            for review in all_reviews:
                count += 1
                total_points += review.rate

            user.average_comment = float(total_points/count)
    else:
        organization = task.organization

        customer_reviews = task.customer_reviews

        all_tasks = organization.tasks
        all_reviews = []
        for task in all_tasks:
            all_reviews.extend(task.customer_reviews)
        #customer_reviews = task.customer_reviews

        count = 0
        total_points = 0

        if len(all_reviews) == 0:
            user.average_comment = 5.0

        else:
            for review in all_reviews:
                count += 1
                total_points += review.rate


            organization.average_comment = float(total_points/count)

    db.session.commit()

# 计算任务的平均分
def calculateTaskAvgComment(_task_id):
    task = Task.query.filter_by(id=_task_id).first()
    print(task.title)
    count = 0
    total_points = 0
    
    for review in task.customer_reviews:
        count += 1
        total_points += review.rate

    if count == 0:
        return 5.0

    else:
        return float(total_points/count)




# 检查用户是否已经写过回评
def checkFeedbackCreated(user_id,task_id,receiver_id):
    record = Feedback_Review.query.filter_by(user_id=_user_id, task_id=_task_id,receiver_id=receiver_id).first()
    if record is None:
        return False
    else:
        return True

'''
# 更新接收者的评分
def updateAvgFeedback(_user_id):
'''  

