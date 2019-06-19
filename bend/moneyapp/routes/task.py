import uuid
import jwt
from werkzeug.utils import secure_filename
from flask import render_template, url_for, request, flash, jsonify
from moneyapp.models import User, Organization, Task, Receiver_Task, Organization_Member, Transaction
from moneyapp.db_user import *
from moneyapp.db_organization import *
from moneyapp.db_task import *
from flask_jwt import JWT, jwt_required, current_identity
from functools import wraps
from . import routes
from .home import token_required


##=========== Task =================================
# RESTful 用户创建任务
@routes.route('/users/<user_id>/tasks', methods=['POST'])
@token_required
def user_create_task(current_user, user_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    #if checkBalance(user_id, None, float(reward_for_one_participant) * float(participant_number_limit)):
    d = request.get_json()

    d['user_id'] = int(user_id)

    # string -> datetime
    time_item = {'post_time', 'receive_end_time', 'finish_deadline_time'};
    for item in time_item:
        if item in d:
            datetime_str = d[item]
            d[item] = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        
    task = createTask(request.get_json())

   
    return_msg = printSingleTask(task)

    return jsonify(return_msg), 200
    
    

# RESTful 组织创建任务
@routes.route('/users/<user_id>/organizations/<organization_id>/tasks', methods=['POST'])
@token_required
def organization_create_task(current_user, user_id, organization_id):
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

    
    d = request.get_json()
    d['user_id'] = int(user_id)
    d['organization_id'] = int(organization_id)
    
    # string -> datetime
    time_item = {'post_time', 'receive_end_time', 'finish_deadline_time'};
    for item in time_item:
        if item in d:
            datetime_str = d[item]
            d[item] = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
     
    # !!! balance判断
    #if checkBalance(user_id, None, float(reward_for_one_participant) * float(participant_number_limit)):
    task = createTask(d)

    return_msg = printSingleTask(task)

    return jsonify(return_msg), 200




# RESTful 用户查询自己创建的任务
@routes.route('/users/<user_id>/my_tasks', methods=['GET'])
@token_required
def check_user_tasks(current_user, user_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    task_info = []

    for task in current_user.tasks:
        if task.organization is None:
            task_info.append(printTaskBrief(task))

    return jsonify({"task": task_info}), 200


# RESTful 组织查询自己创建的任务
@routes.route('/users/<user_id>/organizations/<organization_id>/my_tasks', methods=['GET'])
@token_required
def check_organization_tasks(current_user, user_id, organization_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    organization = queryOrganizationByID(organization_id)
    if not organization:
        return jsonify({"error_code": "404", "error_msg": "organization Not Found"}), 404

    record = queryRecord(current_user.id, organization_id)
    if not record:
        return jsonify({"error_code": "401",
                        "error_msg": "insufficient permission"}), 401

    task_info = []

    for task in current_user.tasks:
        if task.organization is not None:
            task_info.append(printTaskBrief(task))

    return jsonify({"task": task_info}), 200

# RESRful 个人查询自己创建的任务详情
@routes.route('/users/<user_id>/my_tasks/<task_id>', methods=['GET'])
@token_required
def get_created_task_detail(current_user, user_id, task_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    task = checkUserCreateTask(user_id, task_id)

    if task is None:
        return jsonify({
            "error_code": "401",
            "error_msg": "Insufficient permission, you don't create this task"
            }), 401

    else:
        result_msg = printSingleTask(task)

        return jsonify(result_msg), 200

# RESRful 组织查询创建的任务详情
@routes.route('/users/<user_id>/organizations/<organization_id>/my_tasks/<task_id>', methods=['GET'])
@token_required
def get_created_task_org_detail(current_user, user_id, organization_id, task_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    organization = queryOrganizationByID(organization_id)
    if not organization:
        return jsonify({"error_code": "404", "error_msg": "organization Not Found"}), 404

    record = queryRecord(current_user.id, organization_id)
    if not record:
        return jsonify({"error_code": "401",
                        "error_msg": "insufficient permission"}), 401


    task = checkUserOrgCreateTask(organization_id, task_id)

    if task is None:
        return jsonify({
            "error_code": "401",
            "error_msg": "Insufficient permission, you don't create this task"
            }), 401

    else:
        result_msg = printSingleTask(task)

        return jsonify(result_msg), 200
        




# RESTful 查询自己已接受的任务
@routes.route('/users/<user_id>/received_tasks', methods=['GET'])
@token_required
def get_received_task(current_user, user_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    task_info = []

    for received_task_record in current_user.received_tasks:
        task_info.append(printTaskBrief(received_task_record.task))

    return jsonify(task_info), 200

# RESTful 删除个人任务
@routes.route('/users/<user_id>/tasks/<task_id>', methods=['DELETE'])
@token_required
def delete_user_task(current_user, user_id, task_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    task = queryTaskById(task_id)
    if not task or task.organization != None:
        return jsonify({"error_code": "404", "error_msg": "task Not Found"}), 404

    
    if not task.user.id == int(current_user.id):
        return jsonify({"error_code":"500", "error_msg": "insufficient permission"}), 500

    task_name = task.title
    deleteTask(user_id, task_id, None)
    #return jsonify({"msg": "Delete " + str(task.title) + " successfully."}), 200
    return jsonify({"task_id": task_id,
                    "task_name": task_name}), 200
# RESTful 删除组织任务
@routes.route('/users/<user_id>/organizations/<organization_id>/tasks/<task_id>', methods=['DELETE'])
@token_required
def delete_organization_task(current_user, user_id, task_id, organization_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404

    task = queryTaskById(task_id)
    if not task or task.organization.id != int(organization_id):
        return jsonify({"error_code": "404", "error_msg": "task Not Found"}), 404

    record = queryRecord(user_id, organization_id)
    if not record or record.status == "member":
        return jsonify({"error_code":"500", "error_msg": "insufficient permission"}), 500

    task_name = task.title
    deleteTask(user_id, task_id, organization_id)
    #return jsonify({"msg": "Delete " + str(task.title) + " successfully."}), 200
    return jsonify({"task_id": task_id,
                    "task_name": task_name}), 200
    #return jsonify({"msg": "Delete " + str(task.title) + " successfully."}), 200

# RESTful 接受任务
@routes.route('/users/<user_id>/tasks/<task_id>', methods=['POST'])
@token_required
def receive_task(current_user, user_id, task_id):
    user = queryUserById(user_id)
    if not user or current_user.id != int(user_id):
        return jsonify({"error_code": "404",
                        "error_msg": "user Not Found"}), 404

    task = queryTaskById(task_id)
    if not task:
        return jsonify({"error_code": "404",
                        "error_msg": "task Not Found"}), 404
    try:
        receiveTask(user_id, task_id)
    except Exception as e:
        return jsonify({"error_code": "500", "error_msg": str(e)}), 500
    else:   
        return jsonify({"msg": "Receive task successfully."}), 201

# RESTful 任务完成
@routes.route('/users/<user_id>/tasks/<task_id>/steps/<step_id>', methods=['PUT'])
@token_required
def mark_task_step(current_user, user_id, task_id, step_id):
    
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404
    
    task = queryTaskById(task_id)
    
    if not task:
        return jsonify({"error_code": "404", "error_msg": "task Not Found"}), 404
    
    try:
        task_record = userChangeReceiveTask(int(user_id), int(task_id), int(step_id))
    except Exception as e:
        return jsonify({"error_code": "500",
                        "error_msg": str(e)}), 500 
    else:
        return jsonify({"user_id": current_user.id,
                        "task_id": task_record.task.id,
                        "task_title": task_record.task.title,
                        "task_status": task_record.status,
                        "task_total_steps": json.loads(task_record.task.steps),
                        "task_finished_steps": task_record.step}), 200
  

# RESTful 任务审核
@routes.route('/users/<user_id>/tasks/<task_id>/finisher/<finisher_id>', methods=['PUT'])
@token_required
def mark_task_finished(current_user, user_id, task_id, finisher_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404
    
    task = queryTaskById(task_id)
    if not task or task.user.id != current_user.id:
        return jsonify({"error_code": "404", "error_msg": "task Not Found"}), 404
    
    try:
        task = finishUserTask(task_id, finisher_id)

    except Exception as e:
        return jsonify({"error_code": "500",
                        "error_msg": str(e)}), 500 
    else:
        #result_msg = printSingleTask(task)
        result_msg = printUserInfoOfTask(task)
        return jsonify(result_msg), 200

        # status = "on going" if (datetime.datetime.utcnow() > task.post_time and datetime.datetime.utcnow() < task.finish_deadline_time) else "not ongoing"
    
        # participant_ids = []
        # ongoing_participant_ids = []
        # waiting_examine_participant_ids = []
        # finished_participant_ids = []

        # for par in task.received_tasks:
        #     par_user_id = par.user_id
        #     participant_ids.append(par_user_id)
        #     if par.status == 'on going':
        #         ongoing_participant_ids.append(par_user_id)
        #     elif par.status == 'waiting examine':
        #         waiting_examine_participant_ids.append(par_user_id)
        #     elif par.status == 'finished':
        #         finished_participant_ids.append(par_user_id)
       
        # return jsonify({"task_id": task.id, 
        #                 "creator_user_id": task.user_id,
        #                 "creator_organization_id": task.organization_id,
        #                 "status": status,
        #                 "title": task.title,
        #                 "description": task.description,
        #                 "tags": json.loads(task.tags),
        #                 "participant_number_limit": task.participant_number_limit,
        #                 "reward_for_one_participant": task.reward_for_one_participant,
        #                 "post_time": task.post_time,
        #                 "receive_end_time": task.receive_end_time,
        #                 "finish_deadline_time": task.finish_deadline_time,
        #                 "user_limit": json.loads(task.user_limit),
        #                 "steps": json.loads(task.steps),
        #                 "participant_ids": participant_ids,
        #                 "ongoing_participant_ids": ongoing_participant_ids,
        #                 "waiting_examine_participant_ids": waiting_examine_participant_ids,
        #                 "finished_participant_ids": finished_participant_ids
        #                 }), 200


# RESTful 个人撤回任务 + 修改任务
@routes.route('/users/<user_id>/tasks/<task_id>', methods=['PUT'])
@token_required
def set_user_task_pending(current_user, user_id, task_id):
    # 是否登录者操作
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404
    
    # 是否有该任务
    task = queryTaskById(task_id)
    if not task:
        return jsonify({"error_code": "404", "error_msg": "task Not Found"}), 404
    
    
    d = request.get_json()

    # 撤回任务 有status项即撤回
    if 'status' in d:
        try:
            changeTaskStatus(int(user_id), int(task_id), d['status'], None)
        except Exception as e:
            return jsonify({"error_code": "500", "error_msg": str(e)}), 500
        #changeTaskStatus(int(user_id), int(task_id), d['status'], None)
    
    # 修改
    else:

    
        try:
            # string -> datetime
            time_item = {'post_time', 'receive_end_time', 'finish_deadline_time'};
            for item in time_item:
                if item in d:
                    datetime_str = d[item]
                    d[item] = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
             
            # !!! 到后面要把这个注释去掉 为了方便测试先注释掉
            #if checkBalance(user_id, None, float(money) * float(number)):
            modifyTask(int(task_id), int(user_id), None, d)
        
        except Exception as e:
            return jsonify({"error_code": "500", "error_msg": str(e)}), 500


    return_msg = printSingleTask(task)
    return jsonify(return_msg), 200
         

# RESTful 组织撤回任务 + 修改任务
@routes.route('/users/<user_id>/organization/<organization_id>/tasks/<task_id>', methods=['PUT'])
@token_required
def set_org_task_pending(current_user, user_id, organization_id, task_id):
    # 是否登录者操作
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404
    
    # 是否有该任务
    task = queryTaskById(task_id)
    if not task:
        return jsonify({"error_code": "404", "error_msg": "task Not Found"}), 404
    
    
    d = request.get_json()

    # 撤回任务 有status项即撤回
    if 'status' in d:
        try:
            changeTaskStatus(int(user_id), int(task_id), d['status'], None)
        except Exception as e:
            return jsonify({"error_code": "500", "error_msg": str(e)}), 500
        #changeTaskStatus(int(user_id), int(task_id), d['status'], None)
    
    # 修改
    else:
        try:
            # string -> datetime
            time_item = {'post_time', 'receive_end_time', 'finish_deadline_time'};
            for item in time_item:
                if item in d:
                    datetime_str = d[item]
                    d[item] = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
             
            # !!! 到后面要把这个注释去掉 为了方便测试先注释掉
            #if checkBalance(user_id, None, float(money) * float(number)):
            modifyTask(int(task_id), int(user_id), int(organization_id), d)
        
        except Exception as e:
            return jsonify({"error_code": "500", "error_msg": str(e)}), 500


    return_msg = printSingleTask(task)
    return jsonify(return_msg), 200



# TODO 任务搜索 （对tag进行搜索）
@routes.route('/task/filter', methods=['GET'])
def task_filter():
    """
    需要首先在db_operations.py里面实现一个filter函数
    然后在这里调用
    :param request.form['tag'] 标签
    :rtype: json {"status": "", "message": "", "filtered task": {"", ""}}
    """
    if request.method == 'GET':
        tag = request.form['tag']

        
        task = queryTaskByTag(tag)
        if task:
            result = {'status':'success',
                      'message':'search successful'}
        
        else:
            result = {'status':'fail'}
    else:
        result = {'status':'fail',
                  'message':'no get'}
    return jsonify(result)

# TODO 任务接收者修改所接受的任务的状态（mark完成了几步）
#（暂时修改status为传入的request.form['status']的内容）
@routes.route('/task/receiver_set_status', methods=['POST'])
def receiver_set_status():
    """
    需要首先在db_operations.py里面实现一个filter函数
    然后在这里调用
    需要先判断user和task是否是接收关系（record） -》需要另外在db_operations.py里写一个函数
    :param request.form['user_id'] 用户id
    :param request.form['task'] 任务id
    :param request.form['status'] 要设置任务为什么状态
    :rtype: json {"status": "", "message": ""}
    """
    if request.method == 'POST':
        user_id = request.form['user_id']
        task_id = request.form['task_id']
        status = request.form['status']
        record = queryReceiverTask(user_id,task_id)
        if record:
           userChangeReceiveTask(user_id,task_id,status)
           result = {'status':'success',
          'message':'change successfully'} 

        else:
            result = {'status':'fail',
           'message':'no suit'}
        
    else:
        result = {'status': 'fail',
        'message':'no post'}

    return jsonify(result)

# TODO 任务发布者修改发布任务的状态（比如设置为已完成...)
@routes.route('/task/owner_set_status', methods=['POST'])
def owner_set_status():
    """
    需要首先在db_operations.py里面实现一个filter函数
    然后在这里调用
    需要先判断user和task的关系 -》需要另外在db_operations.py里写一个函数
    :param request.form['user_id'] 用户id
    :param request.form['task'] 任务id
    :param request.form['status'] 要设置任务为什么状态
    :rtype: json {"status": "", "message": ""}
    """
    if request.method == 'POST':
        user_id = request.form['user_id']
        task_id = request.form['task']
        status = request.form['status']
        
        
        task = queryTaskById(user_id,task_id)
        result = {'status':'successfully'}
        
        if task:
            changeTaskStatus(task_id,status)
            result = {'status':'successfully',
            'message':'change!'}
        else:
            result = {
            'status':'fail',
            'message': 'no task'
            }
        
    else:
        result = {'status':'fail'}     
    return jsonify(result)


# RESTful 任务详情 （可以查询任意任务）
@routes.route('/users/<user_id>/tasks/<task_id>', methods=['GET'])
@token_required
def search_public_tasks(current_user, user_id, task_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404
    task = queryTaskById(task_id)
    if task is None:
        return jsonify({"error_code": "404", "error_msg": "Task Not Found"}), 404
    else:
        result = printPublicSingleTask(task)
        return jsonify(result), 200

# RESTful 任务查询
@routes.route('/users/<user_id>/tasks', methods=['GET'])
@token_required
def search_all_tasks(current_user, user_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404
    try:
        d = request.get_json()
        # string -> datetime
        time_item = {'post_time', 'receive_end_time', 'finish_deadline_time'};
        for item in time_item:
            if item in d:
                datetime_str = d[item]
                d[item] = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                
    except Exception as e:
        return jsonify({"error_code": "400", "error_msg": "Please specify some limitations. " + str(e)}), 400


    
    task_diff_set = searchTask(d)

    task_info = []

    for task in task_diff_set:
        task_info.append(printSingleTask(task))
        
    return jsonify(task_info), 200



