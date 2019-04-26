import uuid
import jwt
from werkzeug.utils import secure_filename
from flask import render_template, url_for, request, flash, jsonify, current_app
from moneyapp.models import User, Organization, Task, Receiver_Task, Organization_Member, Transaction
from moneyapp.db_user import *
from moneyapp.db_organization import *
from moneyapp.db_task import *
from flask_jwt import JWT, jwt_required, current_identity
from functools import wraps
from . import routes
from .home import token_required

##=============== Organization =======================
# RESTful 创建组织
@routes.route('/users/<user_id>/organization', methods=['POST'])
@token_required
def create_organization(current_user, user_id):
    name = request.get_json()['name']
    bio = request.get_json()['bio']

    if request.files and request.files['file'] :
            file = request.files['file']
            filename = secure_filename(file.filename)

            # Gen GUUID File Name
            fileExt = filename.split('.')[1]
            autoGenFileName = uuid.uuid4()

            newFileName = str(autoGenFileName) + '.' + fileExt

            target = UPLOAD_FOLDER
            print(target)

            if not os.path.isdir(target):
                os.mkdir(target)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], newFileName))

    else:
        #filename = 'default.jpg'
        newFileName = 'default2.jpg'

    try:
        organization_id = addOrganization(name, newFileName, bio)

        addMember(user_id, organization_id, "owner")

        return jsonify({"organization_id": organization_id}), 201

    except Exception as e:
            err_msg = re.findall(r"UNIQUE constraint failed: .*", str(e))
            return jsonify({'error_code': "409",
                         'error_msg': str(e)}), 409


# RESTful 群主删除组织
@routes.route('/users/<user_id>/organization/<organization_id>', methods=['DELETE'])
@token_required
def organization_delete(current_user, user_id, organization_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    organization = queryOrganizationByID(organization_id)

    if not organization:
        return jsonify({"error_code": "404", "error_msg": "organization Not Found"}), 404

    record = queryRecord(current_user.id, int(organization_id))
    
    if not record or record.status != 'owner':
        return jsonify({"error_code": "401",
                        "error_msg": "insufficient permission"}), 401

    deleteOrganization(organization_id)
    return jsonify({"name": organization.name, "bio": organization.bio}), 200
    
# RESTful 群主管理员添加成员
@routes.route('/users/<user_id>/organization/<organization_id>/members', methods=['POST'])
@token_required
def add_organization_member(current_user, user_id, organization_id):
    
    status = request.get_json()['status']
    # email, telephone任意有一个就好
    try:
        email = request.get_json()['email']
        user = queryUserByEmail(email)
    except:
        pass

    try:
        telephone = request.get_json()['phone_number']
        user = queryUserByTelephone(telephone)
    except:
        pass
        
        

    user_operator = queryUserById(int(user_id))
    organization = queryOrganizationByID(int(organization_id))

    if not user_operator or not user:
        return jsonify({"error_code": "404",
                        "error_msg": "user Not Found"}), 404
    if not organization:
        return jsonify({"error_code": "404",
                        "error_msg": "organization Not Found"}), 404

    record = queryRecord(current_user.id, organization_id)
    if not record or record.status == 'member':
        return jsonify({"error_code": "401",
                        "error_msg": "insufficient permission"}), 401
    else:
        addMember(user.id, organization_id, "member")
        return jsonify({"msg": "Added successfully."}), 201

# TODO 组织信息的录入和修改
@routes.route('/organizations/modify_profile', methods=['POST'])
def organization_modify_profile():
    """
    需要首先在db_operations.py里面实现一个修改函数
    然后在这里调用
    需要判断操作者是否为组织的创建者（owner）或者管理员（manager）
    可以使用queryRecord来获得user和organization的记录
    利用status判断是否为创建者、管理员
    :param request.form['user_id'] 用户id
    :param request.form['organization_id'] 组织id
    :param request.form['name'] 组织名字（用于修改）
    :param request.form['bio'] 组织说明（用于修改）
    :param request.form['file'] 头像修改（具体的可以参考前面用户修改资料的头像部分的修改）
    :rtype: json {"status": "", "message": "", 
                    "organization_name": "", "organization_bio": "", "orgnazation_avatar_path":""}
    """
  
    if request.method == 'POST':
        user_id = request.form['user_id']
        organization_id = request.form['organization_id']
        organization_name = request.form['name']
        organization_bio = request.form['bio']
       
       
        result = {'status':'fail',
                'message':'no permission'}


    else:
        result = {"status": "fail",
                  "message": "no post"}
        
    return jsonify(result)

# 给组织充值
@routes.route('/organizations/charge', methods=['POST'])
def organization_charge():
    """
    需要首先在db_operations.py里面实现一个修改函数(chargeForOrganization写好了)
    然后在这里调用
    需要判断操作者是否为组织成员（owner/manager/ordinary member）
    可以使用queryRecord来获得user和organization的记录
    :param request.form['user_id'] 用户id
    :param request.form['organization_id'] 组织id
    :param request.form['money'] 充多少钱
    :rtype: json {"status": "", "message": "", 
                    "organization_id": ""}
    """
    if request.method == 'POST':
        user_id = request.form['user_id']
        organization_id = request.form['organization_id']
        money = request.form['money']

        record = queryRecord(user_id, organization_id)
        if record:
            
            chargeForOrganization(user_id, organization_id, money)
            
            result = {"status": "success", 
                      "message": "Successfully charge",
                      "organization_id": organization_id
                      }
        else:
            result = {"status": "fail",
                      "message": "No Permission"}

        
    else:
        result = {"status": "fail",
                  "message": "no post"}

    return jsonify(result)

# TODO 按名字搜索组织
@routes.route('/organizations/filter', methods=['GET'])
def organization_filter():
    """
    需要首先在db_operations.py里面实现一个filter函数，可以参考queryUser
    然后在这里调用
    :param request.form['organization_name'] 用户id
    :rtype: json {"organization_name": {}}
    """
    #返回的信息不定
    if request.method == 'GET':
        organization_name = request.form['organization_name']
        organization = queryOrganizationByName(organization_name)
        if organization:
            result = {"status":"true",
                       "message":"successfully get" }
        else:
            result = {"status":"false",
                      "message":"no such organization"}
    else:
        result = {"status": "false",
                  "message": "no get"}
    return jsonify(result)

# TODO 群主设置成员为管理员
@routes.route('/organizations/set_status', methods=['POST'])
def set_member_status():
    """
    需要首先在db_operations.py里面实现一个修改函数
    然后在这里调用
    需要判断操作者是否为群主，且被操作者是否为群内成员
    可以使用queryRecord来获得user和organization的记录
    :param request.form['owner_id'] 群主id
    :param request.form['member_id'] 要被设置为管理员的用户的id
    :param request.form['organization_id'] 组织id
    :rtype: json {"status": "", "message": "", 
                    "organization_id": ""}
    """
    if request.method == 'POST':
        owner_id = request.form['owner_id']
        member_id = request.form['member_id']
        organization_id = request.form['organization_id']
        owner = queryRecord(owner_id,organization_id)
        member = queryRecord(member_id,organization_id)
        if owner and member:
            if owner.status == 'owner' and member.status == 'member':
                addManager(member_id,organization_id)
                result = {'status':'success',
                          'message' : 'change'}
            else:
                result = {'status':'fail'}
        else:
            result = {'status':'fail'}

    else:
        result = {"status": "false", 
                  "message": "no post"}

    return jsonify(result)
