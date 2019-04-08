from moneyapp import db
from moneyapp.models import User, Organization, Task, Receiver_Task


# ====================================================================
# User
# 访客基础信息
def addUser(_username, _email, _hashed_password, _telephone, _image_file):
	user = User(username=_username, email=_email, password=_hashed_password, telephone=_telephone, image_file=_image_file)
	db.session.add(user)
	db.session.commit()


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




# ====================================================================
# Organization
def addOrganization(_name, _image_file, _bio):
	organization = Organization(name=_name, image_file=_image_file, bio=_bio)
	db.session.add(organization)
	db.session.commit()


# ====================================================================
# Task
# no organization
def createTask(_user_id, _money, _tag, _number, _applicapable_user, _title, _description, _status):
	task = Task(user_id=_user_id, money=_money, tag=_tag, number=_number, applicapable_user=_applicapable_user, title=_title, description=_description, status=_status)
	db.session.add(task)
	db.session.commit()


# ======================================================
# Receiver_Task
def receiveTask(_user_id, _task_id):
	receiver_task = Receiver_Task(user_id=_user_id, task_id=_task_id)
	db.session.add(receiver_task)
	db.session.commit()

 
