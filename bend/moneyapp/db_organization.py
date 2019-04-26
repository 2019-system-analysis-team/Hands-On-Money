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

    id = len(all_organizations)

    return id



def chargeForOrganization(_user_id, _organization_id, _money):
    transaction = Transaction(user_id=_user_id, organization_id=_organization_id, money=_money)
    

    organization = Organization.query.filter_by(id=_organization_id).first()
    organization.balance += float(_money)
    
    db.session.add(transaction)
    db.session.commit()

def queryOrganizationByID(_organization_id):
    organization = Organization.query.filter_by(id=_organization_id).first()
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

#-----------------------------------------------
#todo 按名字搜索组织
def queryOrganizationByName(_organization_name):
    organization = Organization.query.filter_by(name=_organization_name).first()
    return organization

#--------------------------------------------------
#todo 改变组织信息
def modify_orgfile(_organization_id,_organization_name,_organization_bio, _image_file):

    organization = Organization.query.filter_by(id = _organization_id).first()

    organization.name = _organization_name
    organization.bio = _organization_bio
    organization.image_file = _image_file

    db.session.commit()

# ===============================================================
# Organization Member
def addMember(_user_id, _organization_id, _status):
    organization_member = Organization_Member(user_id=_user_id, organization_id=_organization_id, status=_status)
    db.session.add(organization_member)
    db.session.commit()

# 可以用于判断xx用户是否是xx组织成员，有没有权限以组织名义发任务
def queryRecord(_user_id, _organization_id):
    record = Organization_Member.query.filter_by(user_id=_user_id, organization_id=_organization_id).first()
    if record:
        return record
#--------------------------------------------------------------------
#todo
#判断用户是否接收了该任务
def queryReceiverTask(_user_id,_task_id):
    record = Receiver_Task.query.filter_by(user_id=_user_id,task_id=_task_id).first()
    if record:
        return record
#--------------------------------------------------------

#--------------------------------------------------
#todo
#设置管理员:
def addManager(_user_id,_organization_id):
    organization_member = Organization_Member.query.filter_by(user_id=_user_id , organization_id = _organization_id).first()
    organization_member.status = 'manager'
    db.session.commit()


#----------------------------------------------------------
#todo 
#按照user_id和organization 搜索组织成员
def queryMemberById(_user_id,_organization_id):
    organization_member = Organization_Member.query.filter_by(user_id=_user_id , organization_id =_organization_id).first()
    return organization_member
