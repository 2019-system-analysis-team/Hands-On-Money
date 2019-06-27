# 数据库设计文档

## ER 图

![](https://camo.githubusercontent.com/1fff7b325a89cc508e7e60267e344d47869524db/68747470733a2f2f692e6c6f6c692e6e65742f323031392f30352f32322f3563653530636633373837313034363730352e706e67)

## 数据库表

```python
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True, nullable=False)
	phone_number = db.Column(db.String(30), unique=True, nullable=True)
	profile_photo_path = db.Column(db.String(20), nullable=False, default='default.jpg')
	student_id = db.Column(db.String(8), unique=True, nullable=True)
	name = db.Column(db.String(30), nullable=True)
	age = db.Column(db.Integer, nullable=True)
	sex = db.Column(db.String(30), nullable=True)
	grade = db.Column(db.String(100), nullable=True)
	school = db.Column(db.String(100), nullable=True)
	bio = db.Column(db.Text, default='this person is very lazy')
	balance = db.Column(db.Float, default=0.0)
	average_comment = db.Column(db.Float, default=5.0)
	nickname = db.Column(db.String(30))
	password = db.Column(db.String(60), nullable=False)
	
	
class Organization(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True, nullable=False)
	image_file = db.Column(db.String(20), default='default.jpg')
	bio = db.Column(db.Text, default='')
	balance = db.Column(db.Float, default=0.0)
	average_comment = db.Column(db.Float, default=5.0)


class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref=db.backref('tasks', lazy='dynamic'))
	organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=True)
	organization = db.relationship('Organization', backref=db.backref('tasks', lazy='dynamic'))
	reward_for_one_participant = db.Column(db.Float, nullable=False)
	tags = db.Column(db.Text, nullable=True)
	participant_number_limit = db.Column(db.Integer, nullable=False)
	post_time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
	receive_end_time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow() + timedelta(hours=1))
	finish_deadline_time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow() + timedelta(hours=24))
	title = db.Column(db.String(100), nullable=False)
	description = db.Column(db.Text, nullable=True, default='No description')
	user_limit = db.Column(db.Text, nullable=True)
	steps = db.Column(db.Text, nullable=True)
	steps_number = db.Column(db.Integer, nullable=True)
	status = db.Column(db.String(100), nullable=True)

class Receiver_Task(db.Model):
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	user = db.relationship('User', backref=db.backref('received_tasks', lazy='dynamic'))
	task_id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)
	task = db.relationship('Task', backref=db.backref('received_tasks', lazy='dynamic'))
	received_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow()) # 时间以后再修改
	status = db.Column(db.String(50), nullable=False, default='on going') # 自己完成的情况
	step = db.Column(db.Integer, nullable=False, default=0)

class Organization_Member(db.Model):
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	user = db.relationship('User', backref=db.backref('organization_members', lazy='dynamic'))
	organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), primary_key=True)
	organization = db.relationship('Organization', backref=db.backref('organization_members', lazy='dynamic'))
	status = db.Column(db.String(50), nullable=False, default='ordinary member')

class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref=db.backref('transactions', lazy='dynamic'))
	organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
	organization = db.relationship('Organization', backref=db.backref('transactions', lazy='dynamic'))
	money = db.Column(db.Float, nullable=False)
	time = db.Column(db.DateTime, default=datetime.utcnow())

class Feedback_Review(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref=db.backref('feedback_reviews', lazy='dynamic'))
	organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
	organization = db.relationship('Organization', backref=db.backref('feedback_reviews', lazy='dynamic'))
	receiver_id = db.Column(db.Integer, nullable=False)
	task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
	task = db.relationship('Task', backref=db.backref('feedback_reviews', lazy='dynamic'))
	title = db.Column(db.String(100), nullable=False, default='Feedback review')
	content = db.Column(db.Text, nullable=False, default='default good review')
	rate = db.Column(db.Integer, nullable=False, default=5)

class Customer_Review(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref=db.backref('customer_reviews', lazy='dynamic'))
	task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
	task = db.relationship('Task', backref=db.backref('customer_reviews', lazy='dynamic'))
	title = db.Column(db.String(100), nullable=False, default='Customer review')
	content = db.Column(db.Text, nullable=False, default='default good review')
	rate = db.Column(db.Integer, nullable=False, default=5)
```