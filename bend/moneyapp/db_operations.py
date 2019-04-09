from moneyapp import db
from moneyapp.models import User, Organization, Task, Receiver_Task, Organization_Member, Transaction


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

def queryUserById(_user_id):
	user = User.query.filter_by(id=_user_id).first()
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


# ====================================================================
# Task
# no organization
def createTask(_user_id, _money, _tag, _number, _applicapable_user, _title, _description, _status):
	task = Task(user_id=_user_id, money=_money, tag=_tag, number=_number, applicapable_user=_applicapable_user, title=_title, description=_description, status=_status)
	user = User.query.filter_by(id=_user_id).first()
	user.balance -= float(_money)
	db.session.add(task)
	db.session.commit()

def createTaskOrganization(_organization_id, _user_id, _money, _tag, _number, _applicapable_user, _title, _description, _status):
	task = Task(organization_id=_organization_id, user_id=_user_id, money=_money, tag=_tag, number=_number, applicapable_user=_applicapable_user, title=_title, description=_description, status=_status)
	organization = Organization.query.filter_by(id=_organization_id).first()
	organization.balance -= float(_money)
	db.session.add(task)
	db.session.commit()


# ======================================================
# Receiver_Task
def receiveTask(_user_id, _task_id):
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









 
