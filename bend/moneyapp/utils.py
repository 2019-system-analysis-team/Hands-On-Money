from moneyapp.models import db, User, Organization, Task, Receiver_Task, Organization_Member, Transaction, Feedback_Review, Customer_Review
import json
from flask import jsonify
from datetime import datetime

def queryUserById(_id):
    user = User.query.filter_by(id=_id).first()
    return user


def queryOrganizationByID(_organization_id):
    organization = Organization.query.filter_by(id=_organization_id).first()
    return organization


def checkBalance(_user_id, _organization_id, _money):
    if _organization_id:
        organization = queryOrganizationByID(_organization_id)
        return organization.balance >= _money
    elif _user_id:
        user = queryUserById(_user_id)
        return user.balance >= _money
