import uuid
import jwt
from werkzeug.utils import secure_filename
from flask import render_template, url_for, request, flash, jsonify
from moneyapp.models import User, Organization, Task, Receiver_Task, Organization_Member, Transaction, Customer_Review, Feedback_Review
from moneyapp.db_user import *
from moneyapp.db_organization import *
from moneyapp.db_task import *
from moneyapp.db_review import *
from moneyapp.utils import *
from flask_jwt import JWT, jwt_required, current_identity
from functools import wraps
from . import routes
from .home import token_required

# 发布者回评

# 用户创建的任务回评
@routes.route('/users/<user_id>/customer/<customer_id>/tasks/<task_id>/feedback',method = ['POST']):
@token_required
def  create_User_Feedback_Review(current_user,user_id,customer_id,task_id):

# 组织创建的任务回评
@routes.route('/users/<user_id>/organization/<organization_id>/customer/<customer_id>/tasks/<task_id>/feedback',method = ['POST']):
@token_required
def create_Organization_Feedback_Review():


# 用户创建的任务修改回评
@routes.route('/users/<user_id>/customer/<customer_id>/tasks/<task_id>/feedback',method = ['POST']):
@token_required
def modify_user_Feedback_Review():


# 组织创建的任务修改回评
@routes.route('/users/<user_id>/organization/<organization_id>/customer/<customer_id>/tasks/<task_id>/feedback',method = ['POST']):
@token_required
def modify_organization_Feedback_Review():

# 用户创建的任务删除回评
@routes.route('/users/<user_id>/customer/<customer_id>/tasks/<task_id>/feedback',method = ['POST']):
@token_required
def delete_user_Feedback_Review():

# 组织创建的任务删除回评
@routes.route('/users/<user_id>/organization/<organization_id>/customer/<customer_id>/tasks/<task_id>/feedback',method = ['POST']):
@token_required
def delete_organization_Feedback_Review():
