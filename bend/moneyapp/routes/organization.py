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
@routes.route('/users/<user_id>/', methods=['POST'])
@token_required
def create_organization(current_user, user_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "401", "error_msg": "Unauthorized"}), 401
    
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
            ##print(target)

            if not os.path.isdir(target):
                os.mkdir(target)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], newFileName))

    else:
        #filename = 'default.jpg'
        newFileName = 'default2.jpg'
    # 组织名重复
    if queryOrganizationByName(name):
        return jsonify({"error_code": 409,
                        "error_msg": "create conflicted, duplicate organization name"}), 409

    organization_id = addOrganization(name, newFileName, bio)

    addMember(user_id, organization_id, "owner")

    return jsonify({"organization_id": organization_id}), 201


# 组织信息
@routes.route('/users/<user_id>/organizations/<organization_id>', methods=['GET'])
@token_required
def get_organization(current_user, user_id, organization_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "401", "error_msg": "Unauthorized"}), 401
    
    '''
    user = queryUserById(int(user_id))
    # 非注册用户
    if not user:
        return jsonify({"error_code": "401", "error_msg": "Unauthorized"}), 401
    '''
    
    organization = queryOrganizationByID(int(organization_id))
    # 组织不存在
    if not organization:
        return jsonify({"error_code": "404", "error_msg": "Organization Not Found"}), 404

    organization_member = queryMembers(int(organization_id))
    members = []
    for record in organization_member:
        member = dict(user_id=record.user_id, status=record.status)
        members.append(member)

    return jsonify({
        "name": organization.name,
        "bio": organization.bio,
        "avg_comment": organization.average_comment,
        "members": members
    }), 200


# 组织信息之balance
@routes.route('/users/<user_id>/organizations/<organization_id>/balance', methods=['GET'])
@token_required
def get_organization_balance(current_user, user_id, organization_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "401", "error_msg": "Unauthorized"}), 401
    
    # 非admin
    record = queryRecord(int(user_id), int(organization_id))
    if not record or record.status == 'member':
        return jsonify({"error_code": "401", "error_msg": "Unauthorized"}), 401
    
    organization = queryOrganizationByID(int(organization_id))
    # 组织不存在
    if not organization:
        return jsonify({"error_code": "404", "error_msg": "Organization Not Found"}), 404

    return jsonify({
        "balance": organization.balance
    }), 200


# 组织信息修改 # TODO
@routes.route('/users/<user_id>/organizations/<organization_id>', methods=['PUT'])
@token_required
def modify_organization(current_user, user_id, organization_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "401", "error_msg": "Unauthorized"}), 401
    
    '''
    user = queryUserById(int(user_id))
    # 非注册用户
    if not user:
        return jsonify({"error_code": "401", "error_msg": "Unauthorized"}), 401
    '''
        
    organization = queryOrganizationByID(int(organization_id))
    # 组织不存在
    if not organization:
        return jsonify({"error_code": "404", "error_msg": "Organization Not Found"}), 404

    # 非admin
    record = queryRecord(int(user_id), int(organization_id))
    if not record or record.status == 'member':
        return jsonify({"error_code": "401", "error_msg": "Unauthorized"}), 401

    info = request.get_json()
    
    # 组织名重复
    if 'name' in info and queryOrganizationByName(info['name']) and \
                    queryOrganizationByName(info['name']).id != organization.id:
        return jsonify({"error_code": 500,
                        "error_msg": "duplicate organization name"}), 500

    modifyOrganization2(int(organization_id), info)
    return jsonify({
        "name": organization.name,
        "bio": organization.bio
    }), 200
    

# 组织信息修改之照片
@routes.route('/users/<user_i>/organizations/<organization_id>/profile_photo', methods=['POST'])
@token_required
def  modify_organization_photo(current_user, user_id, organization_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "401", "error_msg": "Unauthorized"}), 401
    
    organization = queryOrganizationByID(int(organization_id))
    # 组织不存在
    if not organization:
        return jsonify({"error_code": "404", "error_msg": "Organization Not Found"}), 404

    # 非admin
    record = queryRecord(int(user_id), int(organization_id))
    if not record or record.status == 'member':
        return jsonify({"error_code": "401", "error_msg": "Unauthorized"}), 401

    if request.files and request.files['file'] :
        file = request.files['file']
        filename = secure_filename(file.filename)

        # Gen GUUID File Name
        fileExt = filename.split('.')[1]
        # 是否规定格式
        picExt = ['png', 'jpg', 'jpeg', 'bmp']
        if fileExt not in picExt:
            return jsonify({"error_code": 415,
                            "error_msg": "Unsupported Media Type"}),415
        
        autoGenFileName = uuid.uuid4()
        newFileName = str(autoGenFileName) + '.' + fileExt
        target = current_app.config['UPLOAD_FOLDER']
        print(target)

        if not os.path.isdir(target):
            os.mkdir(target)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], newFileName))
        else:
            newFileName = 'default.jpg'
            organization = modifyOrganizationPhoto(organization.id,newFileName)
            return jsonify({
                "name": organization.name,
                "bio": organization.bio
            }), 200


# RESTful 群主管理员添加成员
@routes.route('/users/<user_id>/organizations/<organization_id>/members', methods=['POST'])
@token_required
def add_organization_member(current_user, user_id, organization_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "401", "error_msg": "Unauthorized"}), 401
    

    status = request.get_json()['status']
    # email, telephone任意有一个就好
    user = None
    info = request.get_json()
    user = queryUser(info)
    # try:
    #     info['telephone'] = info['phone_number']
    #     user = queryUser(info)
    # except:
    #     pass
    # 添加非注册用户
    if not user:
        return jsonify({"error_code": "404",
                        "error_msg": "User Not Found"}), 404

    user_operator = queryUserById(int(user_id))
    organization = queryOrganizationByID(int(organization_id))
    '''
    if not user_operator:
        return jsonify({"error_code": "404",
                        "error_msg": "User Not Found"}), 404
    '''
    # 组织不存在
    if not organization:
        return jsonify({"error_code": "404",
                        "error_msg": "Organization Not Found"}), 404
    # 无权限
    record = queryRecord(current_user.id, int(organization_id))
    if not record or record.status == 'member':
        return jsonify({"error_code": "401",
                        "error_msg": "insufficient permission"}), 401
    # 已加入组织
    record = queryRecord(user.id, int(organization_id))
    if record:
        return jsonify({"error_code": "500",
                        "error_msg": "duplicate member"}), 500
    #addMember(user.id, int(organization_id), "member") # fix
    addMember(user.id, int(organization_id), status)
    
    return jsonify({"msg": "add successfully."}), 201


# 群主设置成员为管理员
@routes.route('/users/<user_id>/organizations/<organization_id>/members/<member_id>', methods=['PUT'])
@token_required
def set_member_status(current_user, user_id, organization_id, member_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "User Not Found"}), 404
    
    user = queryUserById(int(user_id))
    # 非注册用户
    if not user:
        return jsonify({"error_code": "401", "error_msg": "Unauthorized"}), 401
    # 非admin
    record = queryRecord(int(user_id), int(organization_id))
    if not record or record.status == 'member':
        return jsonify({"error_code": "401", "error_msg": "insufficient permission"}), 401
   
    organization = queryOrganizationByID(int(organization_id))
    # 组织不存在
    if not organization:
        return jsonify({"error_code": "404", "error_msg": "Organization Not Found"}), 404

    status = request.get_json()['status']
    # 改为了owner或者别的
    if status == 'owner' or (status != 'member' and status != 'admin'):
        return jsonify({"error_code": "500", "error_msg": "Unknown status"}), 500
    # TODO 改owner的status
    changeMemberStatus(int(member_id), int(organization_id), status)
    return jsonify({"msg": "update successfully."}), 200

"""
@routes.route('/organizations/set_status', methods=['POST'])
def set_member_status():
    需要首先在db_operations.py里面实现一个修改函数
    然后在这里调用
    需要判断操作者是否为群主，且被操作者是否为群内成员
    可以使用queryRecord来获得user和organization的记录
    :param request.form['owner_id'] 群主id
    :param request.form['member_id'] 要被设置为管理员的用户的id
    :param request.form['organization_id'] 组织id
    :rtype: json {"status": "", "message": "", 
                    "organization_id": ""}
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
"""

# 组织成员删除
@routes.route('/users/<user_id>/organizations/<organization_id>/members/<member_id>', methods=['DELETE'])
@token_required
def member_delete(current_user, user_id, organization_id, member_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "User Not Found"}), 404

    user = queryUserById(int(user_id))
    # 非注册用户
    if not user:
        return jsonify({"error_code": "401", "error_msg": "Unauthorized"}), 401
    # 非admin
    record = queryRecord(int(user_id), int(organization_id))
    if not record or record.status == 'member':
        return jsonify({"error_code": "401", "error_msg": "insufficient permission"}), 401
    organization = queryOrganizationByID(int(organization_id))
    # 组织不存在
    if not organization:
        return jsonify({"error_code": "404", "error_msg": "Organization Not Found"}), 404
    # 成员不在组织内
    member_record = queryRecord(int(member_id), int(organization_id))
    if not member_record:
        return jsonify({"error_code": "404", "error_msg": "Member Not Found"}), 404
    
    # 删owner
    record = queryRecord(int(member_id), int(organization_id))
    if record.status == 'owner':
        return jsonify({"error_code": "500", "error_msg": "cannot delete owner"}), 500
    
    deleteRecord(int(member_id), int(organization_id))
    return jsonify({"msg": "delete successfully."}), 200


# RESTful 群主删除组织
@routes.route('/users/<user_id>/organizations/<organization_id>', methods=['DELETE'])
@token_required
def organization_delete(current_user, user_id, organization_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "User Not Found"}), 404

    organization = queryOrganizationByID(organization_id)
    # 组织不存在
    if not organization:
        return jsonify({"error_code": "404", "error_msg": "organization Not Found"}), 404

    record = queryRecord(current_user.id, int(organization_id))
    # 只有owner能删
    if not record or record.status != 'owner':
        return jsonify({"error_code": "401",
                        "error_msg": "insufficient permission"}), 401

    deleteOrganization(organization_id)
    return jsonify({"name": organization.name, "bio": organization.bio}), 200
  

# 用户参加的组织
@routes.route('/users/<user_id>/organizations', methods=['GET'])
@token_required
def get_organizations(current_user, user_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "User Not Found"}), 404

    organization_member = queryOrganizations(int(user_id))
    organizations = []
    for record in organization_member:
        organization_name = queryOrganizationByID(record.organization_id).name
        organization = dict(organization_id=record.organization_id,
                            organization_name=organization_name,
                            status=record.status)
        organizations.append(organization)
    return jsonify({"organizations": organizations}), 200  

'''
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
'''

'''
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
'''