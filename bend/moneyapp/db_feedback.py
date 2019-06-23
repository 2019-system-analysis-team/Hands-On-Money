from moneyapp.models import db, User, Organization, Task, Receiver_Task, Organization_Member, Transaction, Feedback_Review, Customer_Review
import json
from flask import jsonify
from datetime import datetime
from moneyapp.db_user import checkBalance, queryUserById
from moneyapp.utils import *

def  createFeedbackReview(d):
    feedback_review = Feedback_Review(**d)
    db.session.add(feedback_review)
    db.session.commit()
    return feedback_review

#这里组织是意味着？
def modifyFeedbackReview(d):
    Feedback_Review.query.filter_by(user_id=d['user_id'],task_id=d['task_id']).update(d)
    db.session.commit()
    feedback_review = Feedback_Review.query.filter_by(user_id=d['user_id'],task_id=d['task_id']).first()
    return feedback_review

def deleteFeedbackReview(_user_id,_task_id):
    feedback_review = Feedback_Review.query.filter_by(user_id=_user_id,task_id=_task_id).first()
    db.session.delete(feedback_review)
    db.session.commit()

def getFeedbackReviewByUser(_user_id):
    user_feedback_review = Feedback_Review.query.filter_by(user_id=_user_id)
    return user_feedback_review