from moneyapp import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True, nullable=False)
	telephone = db.Column(db.String(30), unique=True, nullable=True)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	student_id = db.Column(db.String(8), unique=True, nullable=True)
	realname = db.Column(db.String(30), nullable=True)
	age = db.Column(db.Integer, nullable=True)
	sex = db.Column(db.String(30), nullable=True)
	grade = db.Column(db.String(100), nullable=True)
	school = db.Column(db.String(100), nullable=True)
	bio = db.Column(db.Text, default='this person is very lazy')
	balance = db.Column(db.Float, default=0.0)
	average_comment = db.Column(db.Float, default=5.0)
	username = db.Column(db.String(30), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	
	
class Organization(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True, nullable=False)
	image_file = db.Column(db.String(20), unique=True, default='default.jpg')
	bio = db.Column(db.Text, default='')
	balance = db.Column(db.Float, default=0.0)
	average_comment = db.Column(db.Float, default=5.0)


class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref=db.backref('tasks', lazy='dynamic'))
	organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=True)
	organization = db.relationship('Organization', backref=db.backref('tasks', lazy='dynamic'))
	money = db.Column(db.Float, nullable=False)
	tag = db.Column(db.String(30), nullable=True)
	number = db.Column(db.Integer, nullable=False)
	applicapable_user = db.Column(db.String(100), nullable=True)
	post_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
	deadline = db.Column(db.DateTime, nullable=True, default=datetime.utcnow()) # 日期怎么传
	title = db.Column(db.String(100), nullable=False)
	description = db.Column(db.Text, nullable=True, default='No description')
	status = db.Column(db.String(50), nullable=False, default='On going')

class Receiver_Task(db.Model):
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	user = db.relationship('User', backref=db.backref('received_tasks', lazy='dynamic'))
	task_id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)
	task = db.relationship('Task', backref=db.backref('received_tasks', lazy='dynamic'))
	received_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow()) # 时间以后再修改
	status = db.Column(db.String(50), nullable=False, default='On going') # 自己完成的情况
	# def __repr__(self):
	# 	return f"User('{self.username}', '{self.email}', '{self.password}')"

# class User(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(30), unique=True, nullable=False)
# 	password = db.Column(db.String(60), nullable=False)
# 	email = db.Column(db.String(100), unique=True, nullable=False)
# 	telephone = db.Column(db.String(30), unique=True, nullable=False)
# 	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

