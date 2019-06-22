from moneyapp.models import db, User, Organization, Task, Receiver_Task, Organization_Member, Transaction, Feedback_Review, Customer_Review
import json
from flask import jsonify
from datetime import datetime
from moneyapp.db_user import checkBalance, queryUserById
from moneyapp.utils import *

def charge(_user_id, _organization_id, _amount):
	user = queryUserById(_user_id)
	print('user balance: ', user.balance)

	# 用户
	if _organization_id is None:
		# 充值
		if _amount >= 0:
			user.balance += _amount

		# 提现
		else:
			balance_flag = checkBalance(_user_id, None, -_amount)
			if balance_flag:
				user.balance += _amount
			else:
				raise ValueError("The balance is not enough!")
		
		transaction = createTransaction(_user_id, _organization_id, _amount)
		db.session.commit()
		print(user.balance)
		return user.balance

	# 组织
	else:
		organization = queryOrganizationByID(_organization_id)
		balance_flag = checkBalance(_user_id, None, _amount)
		if balance_flag:
			user.balance -= _amount
			organization.balance += _amount
			transaction = createTransaction(_user_id, _organization_id, _amount)
			db.session.commit()
			return organization.balance
		else:
			raise ValueError("The balance is not enough!")
	
		








