from moneyapp.models import db, User, Organization, Task, Receiver_Task, Organization_Member, Transaction, Customer_Review, Feedback_Review
import json
from flask import jsonify
from datetime import datetime
from moneyapp.utils import *

# ====================================================================
# User
# 访客基础信息

def addUser(_nickname, _email, _hashed_password, _phone_number, _profile_photo_path):
    user = User(nickname=_nickname, email=_email, password=_hashed_password, phone_number=_phone_number, profile_photo_path=_profile_photo_path)
    db.session.add(user)
    db.session.commit()
    return user.id

def addUser2(d, _hashed_password):
    user = User(**d)
    user.password = _hashed_password
    db.session.add(user)
    db.session.commit()
    return user.id


"""
# 一开始就填详细信息成为用户
def addUser_detailed(_nickname, _email, _hashed_password, _phone_number, _profile_photo_path, _student_id, _name, _age, _sex, _grade, _school, _bio):
    user = User(nickname=_nickname, email=_email, password=_hashed_password, phone_number=_phone_number, profile_photo_path=_profile_photo_path, student_id=_student_id, name=_name, age=_age, sex=_sex, grade=_grade, school=_school, bio=_bio)
    db.session.add(user)
    db.session.commit()
"""

"""
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
"""
#修改用户信息(不包括修改图片)
def modify_User(_id_ori,d):
    
    #items = {"student_id","name","age","sex","grade","school","bio","nickname"}
    User.query.filter_by(id=_id_ori).update(d)
    user = User.query.filter_by(id=_id_ori).first()
    db.session.commit()
    return user

#修改用户图片信息
def modify_User_Photo(_id_ori,_new_filename):
    user = user = User.query.filter_by(id=_id_ori).first()
    user.profile_photo_path = _new_filename
    db.session.commit()
    return user



# def queryUserById(_id):
#     user = User.query.filter_by(id=_id).first()
#     return user


def queryUser(d):
    items ={'email','phone_number'}
    
    if "email" in d:
        user = User.query.filter_by(email = d['email']).first()
    elif "phone_number" in d:
        user = User.query.filter_by(phone_number=d['phone_number']).first()
    return user

"""
def queryUser(_nickname):
    user = User.query.filter_by(nickname=_nickname).first()
    return user

def queryUserByEmail(_email):
    user = User.query.filter_by(email=_email).first()
    return user

def queryUserByphone_number(_phone_number):
    user = User.query.filter_by(phone_number=_phone_number).first()
    return user
"""
#---------------------------------------
#todo 给个人账号充值
def chargeForUser(_user_id,_money):
    transaction = Transaction(user_id=_user_id,money=_money)
    user = User.query.filter_by(id = _user_id).first()
    user.balance += float(_money)
    db.session.add(transaction)
    db.session.commit()


# =====================================================
# Money
# def checkBalance(_user_id, _organization_id, _money):
#     if _organization_id:
#         organization = queryOrganizationByID(_organization_id)
#         return organization.balance >= _money
#     elif _user_id:
#         user = queryUserById(_user_id)
#         return user.balance >= _money
