from moneyapp import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
<<<<<<< HEAD

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.password}')"
=======
#	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	
	# def __repr__(self):
	# 	return f"User('{self.username}', '{self.email}', '{self.password}')"

>>>>>>> a4d987957e36ec7e3ab39334ce4193bff60c8ff5
