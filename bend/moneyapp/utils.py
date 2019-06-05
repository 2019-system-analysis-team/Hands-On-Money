from moneyapp.models import db, User, Organization, Task, Receiver_Task, Organization_Member, Transaction, Feedback_Review, Customer_Review
import json
from flask import jsonify
from datetime import datetime

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

# 检查用户是否接受了某个任务
def checkUserReceiveTask(_user_id, _task_id):
    task_record = Receiver_Task.query.filter_by(user_id=_user_id,task_id=_task_id).first()
    if task_record is None:
        return None
    else:
        return task_record

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








