from moneyapp.models import db, User, Organization, Task, Receiver_Task, Organization_Member, Transaction
import json
from flask import jsonify
from datetime import datetime

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
def checkBalance(_user_id, _organization_id, _money):
    if _organization_id:
        organization = queryOrganizationByID(_organization_id)
        return organization.balance >= _money
    elif _user_id:
        user = queryUserById(_user_id)
        return user.balance >= _money
