from moneyapp.models import db, User, Organization, Task, Receiver_Task, Organization_Member, Transaction
import json
from flask import jsonify
from datetime import datetime

# ====================================================================
# Organization
def addOrganization(_name, _image_file, _bio):
    organization = Organization(name=_name, image_file=_image_file, bio=_bio)
    db.session.add(organization)
    db.session.commit()

    all_organizations = Organization.query.all()

    id = organization.id
    return id

def queryOrganizationByID(_organization_id):
    organization = Organization.query.filter_by(id=_organization_id).first()
    return organization

def queryOrganizationByName(_organization_name):
    organization = Organization.query.filter_by(name=_organization_name).first()
    return organization

def modifyOrganization(_organization_id, info):
    organization = Organization.query.filter_by(id = _organization_id).first()

    organization.name = info["name"]
    organization.bio = info["bio"]

    db.session.commit()
    return organization

def modifyOrganization2(organization_id, d):
    
    organization = Organization.query.filter_by(id=organization_id).update(d)
   

    db.session.commit()
    return organization

def modifyOrganizationPhoto(_organization_id, _image_file):
    organization = Organization.query.filter_by(id = _organization_id).first()
    organization.image_file = _image_file
    db.session.commit()
    return organization

#----------------------------------------------
#todo 删除组织信息
#是否需要考虑将组织成员内的组织信息删除
def deleteOrganization(_organization_id):
        organization = Organization.query.filter_by(id=_organization_id).first()
        
        # 删除organization member
        for record in organization.organization_members:
            db.session.delete(record)

        # 删除organization名下的task
        for task in organization.tasks:
            # 删除接受了该组织的任务的记录
            for received_record in task.received_tasks:
                db.session.delete(received_record)

            db.session.delete(task)

        db.session.delete(organization)
        db.session.commit()

    

# ===============================================================
# Organization Member
def addMember(_user_id, _organization_id, _status):
    organization_member = Organization_Member(user_id=_user_id, organization_id=_organization_id, status=_status)
    db.session.add(organization_member)
    db.session.commit()
    return organization_member

# 根据organization_id获取该组织下所有成员
def queryMembers(_organization_id):
    organization_member = Organization_Member.query.filter_by(organization_id = _organization_id)
    return organization_member

# 根据query_id获取该成员参加的所有组织
def queryOrganizations(_user_id):
    organization_member = Organization_Member.query.filter_by(user_id = _user_id)
    return organization_member

# 设置管理员
def changeMemberStatus(_user_id,_organization_id, status):
    organization_member = Organization_Member.query.filter_by(user_id=_user_id , organization_id = _organization_id).first()
    organization_member.status = status
    db.session.commit()
    return organization_member

# 可以用于判断xx用户是否是xx组织成员，有没有权限以组织名义发任务
def queryRecord(_user_id, _organization_id):
    record = Organization_Member.query.filter_by(user_id=_user_id, organization_id=_organization_id).first()
    return record

# 删除组织成员
def deleteRecord(_uesr_id, _organization_id):
    record = Organization_Member.query.filter_by(user_id=_uesr_id, organization_id=_organization_id).first()
    db.session.delete(record)
    db.session.commit()



'''
def chargeForOrganization(_user_id, _organization_id, _money):
    transaction = Transaction(user_id=_user_id, organization_id=_organization_id, money=_money)
    

    organization = Organization.query.filter_by(id=_organization_id).first()
    organization.balance += float(_money)
    
    db.session.add(transaction)
    db.session.commit()




#----------------------------------------------------------
#todo 
#按照user_id和organization 搜索组织成员
def queryMemberById(_user_id,_organization_id):
    organization_member = Organization_Member.query.filter_by(user_id=_user_id , organization_id =_organization_id).first()
    return organization_member
'''
