from flask import render_template, url_for, request, flash
from moneyapp import app, db, bcrypt
from moneyapp.models import User

@app.route("/", methods=['GET','POST'])
def home():
	if request.method == 'POST':
		if request.form['button'] == 'add':
			if request.form['username'] and request.form['email'] and request.form['password']:
				hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
				user = User(username=request.form['username'], email=request.form['email'], password=hashed_password)
				db.session.add(user)
				db.session.commit()
				flash("Successfully added! " + user.username)
		elif request.form['button'] == 'search':
			if request.form['username2']:
				user = User.query.filter_by(username=request.form['username2']).first()
				if user:
					flash("username: " + user.username)
					flash("email: " + user.email)
				else:
					flash("Can't find this user")
	return render_template('layout.html')
