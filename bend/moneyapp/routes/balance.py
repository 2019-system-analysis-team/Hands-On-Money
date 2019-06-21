import os
from datetime import datetime, timedelta
import json
import re
import uuid
import jwt
from werkzeug.utils import secure_filename
from flask import render_template, url_for, request, flash, jsonify, current_app
from flask_bcrypt import Bcrypt
from moneyapp.models import User, Organization, Task, Receiver_Task, Organization_Member, Transaction
from moneyapp.db_user import *
from moneyapp.db_organization import *
from moneyapp.db_task import *
from moneyapp.db_balance import *
from flask_jwt import JWT, jwt_required, current_identity
from functools import wraps
from . import routes
from .home import token_required , blacklist

# 用户充值 / 提现
@routes.route('/users/<user_id>/balance', methods=['PUT'])
@token_required
def chargeForUser(current_user, user_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404
    
    try:
        amount = float(request.get_json()['amount'])
    except Exception as e:
        print(str(e))
        return jsonify({"error_code": "500",
                            "error_msg": str(e)}), 500

    else:
        try:
            balance = charge(user_id, None, amount)
        except Exception as e:
            return jsonify({"error_code": 500, 
                            "error_msg": str(e)}), 500

    return jsonify({"balance": balance}), 200


# 用户给组织充值
@routes.route('/users/<user_id>/organizations/<organization_id>/balance', methods=['PUT'])
@token_required
def chargeForOrganization(current_user, user_id, organization_id):
    # 检查user, organization是否存在
    user = queryUserById(user_id)
    if not user or int(user_id) != current_user.id:
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    organization = queryOrganizationByID(organization_id)
    if not organization:
        return jsonify({"error_code": "404", "error_msg": "organization Not Found"}), 404


    record = queryRecord(current_user.id, organization_id)
    if not record or record.status == 'member':
        return jsonify({"error_code": "401",
                        "error_msg": "insufficient permission"}), 401


    try:
        amount = float(request.get_json()['amount'])
    except Exception as e:
        print(str(e))
        return jsonify({"error_code": "500",
                            "error_msg": str(e)}), 500
    else:
        if amount < 0:
            return jsonify({"error_code": 401,
                            "error_msg": "Can't withdraw the money of the organization"}), 401
        balance = charge(user_id, organization_id, amount)

    return jsonify({"balance": balance}), 200











