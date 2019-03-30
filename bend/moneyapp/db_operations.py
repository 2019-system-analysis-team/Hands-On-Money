from moneyapp import db
from moneyapp.models import User

def addUser(_username, _email, _hashed_password, _telephone, _image_file):
	user = User(username=_username, email=_email, password=_hashed_password, telephone=_telephone, image_file=_image_file)
	db.session.add(user)
	db.session.commit()

	# return sth??

def queryUser(_username):
	user = User.query.filter_by(username=_username).first()
	return user