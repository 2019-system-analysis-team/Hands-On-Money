from moneyapp.models import db, User, Organization, Task, Receiver_Task, Organization_Member, Transaction, Feedback_Review, Customer_Review
import json
from flask import jsonify
from datetime import datetime
from moneyapp.db_user import checkBalance, queryUserById
from moneyapp.utils import *

# 接受任务者写评论
def createCustomerReview(d):
	customer_review = Customer_Review(**d)
	db.session.add(customer_review)
	db.session.commit()

	return customer_review

# 接受任务者修改评论
def modifyCustomerReview(d):
	Customer_Review.query.filter_by(user_id = d['user_id'], task_id=d['task_id']).update(d)
	db.session.commit()

	customer_review = Customer_Review.query.filter_by(user_id = d['user_id'], task_id=d['task_id']).first()

	return customer_review

# 接受任务者删除评论
def deleteCustomerReview(_user_id, _task_id):
	customer_review = Customer_Review.query.filter_by(user_id = _user_id, task_id=_task_id).first()
	db.session.delete(customer_review)
	db.session.commit()

# 获取某个任务的评价
def getCustomerReviewByTask(_task_id):
	return Customer_Review.query.filter_by(task_id=_task_id)

