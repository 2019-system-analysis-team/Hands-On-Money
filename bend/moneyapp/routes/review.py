import uuid
import jwt
from werkzeug.utils import secure_filename
from flask import render_template, url_for, request, flash, jsonify
from moneyapp.models import User, Organization, Task, Receiver_Task, Organization_Member, Transaction, Customer_Review, Feedback_Review
from moneyapp.db_user import *
from moneyapp.db_organization import *
from moneyapp.db_task import *
from moneyapp.db_review import *
from moneyapp.utils import *
from flask_jwt import JWT, jwt_required, current_identity
from functools import wraps
from . import routes
from .home import token_required


# RESTful 接受任务者写评论
@routes.route('/users/<user_id>/tasks/<task_id>/comment', methods=['POST'])
@token_required
def create_Customer_Review(current_user, user_id, task_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404
    
    # 检查该用户是否接受了任务
    received_task_record = checkUserReceiveTask(user_id, task_id)
    # 没有接受任务
    if not received_task_record: 
        return jsonify({"error_code": "404", "error_msg": "task Not Found"}), 404
    

    # # 检查该用户是否完成了任务
    # finish_flag = checkFinishTask(received_task_record)

    
    # # 没有完成任务
    # if not finish_flag:
    #     return jsonify({"error_code": "500", "error_msg": "You can't comment before you finish the task"}), 500

    # 检查该用户是否已经写了评论
    if checkCommentCreated(user_id, task_id):
        return jsonify({"error_code": "500", "error_msg": "You have created a comment"}), 500
    # 完成了任务
    else:
        d = request.get_json()
        items = {'title', 'content', 'rate'}
        for item in items:
            if item not in d:
                d[item] = None

        d['user_id'] = int(user_id)
        d['task_id'] = int(task_id)
        print(d['task_id'])
        customer_review = createCustomerReview(d)

        # 更改average_comment
        updateAvgComment(task_id)

        return jsonify({"user_id": current_user.id,
                        "task_id": customer_review.task.id,
                        "review_title": customer_review.title,
                        "review_content": customer_review.content,
                        "review_rate": customer_review.rate}), 201
 

# RESTful 接受任务者修改评论
@routes.route('/users/<user_id>/tasks/<task_id>/review', methods=['PUT'])
@token_required
def modify_Customer_Review(current_user, user_id, task_id):
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404
    
    if not checkCommentCreated(user_id, task_id):
        return jsonify({"error_code": "500", "error_msg": "No comment found"}), 500
    
    else:
        d = request.get_json()
        d['user_id'] = int(user_id)
        d['task_id'] = int(task_id)
        modified_review = modifyCustomerReview(d)

        updateAvgComment(task_id)

        return jsonify({"user_id": current_user.id,
                        "task_id": modified_review.task.id,
                        "review_title": modified_review.title,
                        "review_content": modified_review.content,
                        "review_rate": modified_review.rate}), 200
 

# RESTful 接受任务者删除评论
@routes.route('/users/<user_id>/tasks/<task_id>/review', methods=['DELETE'])
@token_required
def delete_Customer_Review(current_user, user_id, task_id):
    print(checkCommentCreated(user_id, task_id))
    if current_user.id != int(user_id):
        return jsonify({"error_code": "404", "error_msg": "user Not Found"}), 404
    
    if not checkCommentCreated(user_id, task_id):
        return jsonify({"error_code": "500", "error_msg": "No comment found"}), 500
    else:
        try:
            deleteCustomerReview(user_id, task_id)
        except Exception as e:
            return jsonify({"error_code": "500",
                            "error_msg": str(e)}), 500
        else:
            updateAvgComment(task_id)
            return jsonify({"msg": "Delete successfully!"}), 200 


# RESTful 获取某个任务的评价
@routes.route('/tasks/<task_id>/reviews', methods=['GET'])
def get_customer_review_by_task(task_id):
    review_list = getCustomerReviewByTask(task_id)
    review_info = []

    for review in review_list:
        review_info.append(printSingleReview(review))

    average_comment = calculateTaskAvgComment(task_id)

    return jsonify({"avg_points": average_comment, "reviews": review_info})






