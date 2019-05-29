* [用户与组织系统](#用户与组织系统)
   * [用户创建](#用户创建)
      * [test case1：创建已经存在的用户](#test-case1创建已经存在的用户)
      * [test case2：创建新的用户](#test-case2创建新的用户)
   * [用户登录](#用户登录)
      * [test case1:用户正确登录](#test-case1用户正确登录)
   * [用户登录注销](#用户登录注销)
      * [test case 1：成功注销](#test-case-1成功注销)
      * [test case 2：注销非登录者（非token记录）的账号](#test-case-2注销非登录者非token记录的账号)
   * [用户信息](#用户信息)
   * [用户修改昵称和简介：](#用户修改昵称和简介)
      * [test case1:正确修改信息](#test-case1正确修改信息)
      * [test case2：想要修改非登录用户信息](#test-case2想要修改非登录用户信息)
   * [用户修改学校、年级、学号信息](#用户修改学校年级学号信息)
   * [用户修改真实姓名、年龄、性别信息](#用户修改真实姓名年龄性别信息)
   * [用户修改头像](#用户修改头像)
   * [组织创建](#组织创建)
      * [test case 1: 成功创建组织](#test-case-1:-成功创建组织)
      * [test case 2: 非登陆用户创建组织](#test-case-2:-非登陆用户创建组织)
      * [test case 3: 组织名重复](#test-case-3:-组织名重复)
   * [组织信息](#组织信息)
      * [test case 1: 正确获得指定组织信息](#test-case-1:-正确获得指定组织信息)
      * [test case 2: 非登陆用户获取信息](#test-case-2:-非登陆用户获取信息)
      * [test case 3: 找不到组织](#test-case-3:-找不到组织)
      * [test case 4: 管理员成功查询组织余额](#test-case-4:-管理员成功查询组织余额)
      * [test case 5: 非管理员查询组织余额](#test-case-5:-非管理员查询组织余额)
   * [组织信息修改 (Todo)](#组织信息修改)
      * [test case 1: 正确修改指定组织信息](#test-case-1:-正确修改指定组织信息)
      * [test case 2: 非管理员修改组织信息](#test-case-2:-非管理员修改组织信息)
      * [test case 3: 找不到组织2](#test-case-3:-找不到组织2)
      * [test case 4: 组织名重复(Todo)](#test-case-4:-组织名重复(Todo))
   * [群主管理员添加成员](#群主管理员添加成员)
      * [test case 1: 使用邮箱成功添加](#test-case-1:-使用邮箱成功添加)
      * [test case 2: 使用电话成功添加](#test-case-2:-使用电话成功添加)
      * [test case 3: 重复添加成员(Todo)](#test-case-3:-重复添加成员(Todo))
   * [组织成员权限变更(Todo)](#组织成员权限变更(Todo))
      * [test case 1: 成功修改权限](#test-case-1:-成功修改权限)
   * [组织成员删除 (Todo)](#组织成员删除-todo)
      * [test case 1: 成功删除成员](#test-case-1:-成功删除成员)
   * [群主删除组织(Todo)](#群主删除组织(Todo))
   * [用户参加的组织](#用户参加的组织)
* [任务系统](#任务系统)
   * [个人创建任务](#个人创建任务)
   * [组织创建任务](#组织创建任务)
   * [用户查询自己创建的任务](#用户查询自己创建的任务)
   * [组织查询自己创建的任务](#组织查询自己创建的任务)
   * [*任务查询](#任务查询)
      * [test case 1：查找给female的任务](#test-case-1查找给female的任务)
      * [test case 2：查找steps不超过1的任务](#test-case-2查找steps不超过1的任务)
      * [test case 3：找到所有task1-org组织创建的任务](#test-case-3找到所有task1-org组织创建的任务)
   * [任务接受](#任务接受)
   * [任务完成](#任务完成)
      * [test case 1：正常改变step](#test-case-1正常改变step)
      * [test case 2：step_id超过任务本身设定的step/step之前已经标记过了](#test-case-2step_id超过任务本身设定的stepstep之前已经标记过了)
      * [test case 3：该用户没有接受该任务](#test-case-3该用户没有接受该任务)
   * [任务审核](#任务审核)
      * [test case 1：正常标记用户完成任务](#test-case-1正常标记用户完成任务)
      * [test case 2：该用户已经被标记完成](#test-case-2该用户已经被标记完成)
   * [撤回任务](#撤回任务)
      * [test case 1：正常撤回](#test-case-1正常撤回)
      * [test case 2：撤回已经处于pending状态的任务](#test-case-2撤回已经处于pending状态的任务)
   * [修改个人未发布任务](#修改个人未发布任务)
   * [修改组织未发布任务](#修改组织未发布任务)
      * [test case 1：修改未经撤回的任务](#test-case-1修改未经撤回的任务)
      * [test case 2：正常修改组织创建任务](#test-case-2正常修改组织创建任务)
   * [删除个人任务](#删除个人任务)
      * [test case 1：正常删除任务](#test-case-1正常删除任务)
      * [test case 2：删除不属于自己的任务](#test-case-2删除不属于自己的任务)
   * [删除组织任务](#删除组织任务)
      * [test case 1：正常删除任务](#test-case-1正常删除任务-1)
* [接收者评价系统](#接收者评价系统)
   * [任务接收者写评价](#任务接收者写评价)
      * [test case 1：正常添加评论](#test-case-1正常添加评论)
      * [test case 3：该用户还未经审核标记为完成该任务](#test-case-3该用户还未经审核标记为完成该任务)
      * [test case 4：该用户已经写过评价](#test-case-4该用户已经写过评价)
   * [任务接收者修改评价](#任务接收者修改评价)
      * [test case 1：正确修改评论](#test-case-1正确修改评论)
      * [test case 2：还未编辑评论](#test-case-2还未编辑评论)
   * [任务接收者删除评论](#任务接收者删除评论)
      * [test case 1：正常删除](#test-case-1正常删除)
      * [test case 2：未找到评论](#test-case-2未找到评论)
   * [获取某个任务的评价（平均分 所有评价）](#获取某个任务的评价平均分所有评价)

[![_Entity Relationship Diagram Example (3).png](https://i.loli.net/2019/05/22/5ce50cf37871046705.png)

#### 用户与组织系统

##### 用户创建

@app.route('/users', methods=\['POST'\])

###### test case1：创建已经存在的用户

```
POST http://localhost:5000/users
```
```
// Request
{
    "password":"test1ll",
    "email": "test1ll",
    "phone_number": "test1ll",
    "nickname": "test1ll"
}
```
```
// Response 409
{
    "error_code": "409",
    
     "error_msg": "create conflicted, duplicate email or phone_number, goto login"
}
```

###### test case2：创建新的用户

```
POST http://localhost:5000/users
```

```
//Request
{
    "password":"test3",
    "email": "test3",
    "phone_number": "test3",
    "username": "test3"
}
```

```
//Response 200 
{
    "user_id": 12,
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTIsImV4cCI6MTU1NzA3NzE1N30.Z_QwVqcVggw-9NDQmGCJfaoRVTv2WubTPeT252dBQlQ"
}
```



##### 用户登录

@app.route('/sessions', methods=\['POST'\])

###### test case1:用户正确登录

```
POST http://localhost:5000/sessions
```
```
// Request
{
    "password":"test3",
    "email": "test3"
}
```
```
// Response 200
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTIsImV4cCI6MTU1NzA3NzMzMH0.44DNTuebntSUx9OimCxySVp089mrczX4aWQV8wN1zbE"
}
```

##### 用户登录注销

@app.route('/users/<user_id>/session', methods=['DELETE'])

###### test case 1：成功注销

```
DELETE http://localhost:5000/users/12/session
```

```
// Request
// ...
```

```
// Response 200 OK
{
    "message": "username logged out successfully."
}
```

###### test case 2：注销非登录者（非token记录）的账号

```
DELETE http://localhost:5000/users/2/session
```

```
// Request
// ...
```

```
// Response 404 NOT FOUND
{
    "err_msg": "Not Found"
}
```

##### 用户信息

@app.route('/users/<user_id>', methods=['GET'])

###### test case1：成功返回当前登录用户的信息

```
GET http://localhost:5000/users/2
```

```
// Request
// ...
```

```
// Response 200 OK
{
    "email": "test1",
    "phone_number": "test1",
    "profile_photo_path": "default.jpg",
    "student_id": null,
    "name": null,
    "age": null,
    "sex": null,
    "grade": null,
    "school": null,
    "nickname": "test1",
    "bio": "this person is very lazy",
    "balance": 0,
    "avg_comment": 5
}
```

###### test case2：查询并不存在的用户信息

```
GET http://localhost:5000/users/11
```

```
// Request
// ...
```

```
// Response 404
{
    "error_code": "404",
    "error_msg": "User Not Found"
}
```

###### test case 3：查询非登录用户的信息

```
http://localhost:5000/users/1
```

```
// Request
// ...
```

```
// Response 200 OK
{
    "profile_photo_path": "default.jpg",
    "name": null,
    "age": null,
    "sex": null,
    "grade": null,
    "school": null,
    "nickname": "test3",
    "bio": "this person is very lazy",
    "avg_comment": 5
}
```



##### 用户修改昵称和简介：

@app.route('/users/<user_id>/personality', methods=['PUT'])

###### test case1:正确修改信息

```
PUT http://localhost:5000/users/12/personality
```

```
//Request
{
    "username":"username",
    "bio": "bio"
}
```

```
//Response 200 
{ "nickname": "username", "bio": "bio" }
```

###### test case2：想要修改非登录用户信息

```
PUT http://localhost:5000/users/11/personality
```

```
//Request
{
    "username":"username",
    "bio": "bio"
}
```

```
//Response 404
{ "err_msg": "user Not Found" }
```

###### test case3：修改后的username已存在

```
PUT http://localhost:5000/users/12/personality
```

```
//Request
{
    "username":"kkk",
    "bio": "test1"
}
```

```
//Response 409
{
    "error_code": "409",
    "error_msg": "conflicted"
}

```



##### 用户修改学校、年级、学号信息

@app.route('/users/<user_id>/school', methods=['PUT'])

```
PUT http://localhost:5000/users/12/school
```

```
//Request
{
    "school":"school",
    "grade": "1",
    "student_id":"1"
}
```

```
//Response 200
{ "school": "school", "grade": "1", "student_number": "1" }
```

##### 用户修改真实姓名、年龄、性别信息

@app.route('/users/<user_id>/personal_info', methods=['PUT'])

```
PUT http://localhost:5000/users/12/personal_info
```

```
//Request
{
    "realname":"name",
    "age": "1",
    "sex":"f"
}
```

```
//Response 200
{ "name": "name", "age": 1, "sex": "f" }
```

##### 用户修改头像

@app.route('/users/<user_id>/personal_info', methods=['PUT'])

```
POST http://localhost:5000/users/12/profile_photo
```

```
//Request
file
```

```
//Reaponse 200
{ "message": "update successfully!" }
```



##### 组织创建

@app.route('/users/<user_id>/organizations', methods=['POST']

###### test case 1: 成功创建组织

```
POST http://localhost:5000/users/1/organizations
```

```
// Request
{
    "name":"org1",
    "bio": "bio1"
}
```

```
// Response 201 CREATED
{
    "organization_id": 1
}
```

###### test case 2: 非登陆用户创建组织

```
POST http://localhost:5000/users/2/organizations
```

```
// Request
{
    "name":"org1",
    "bio": "bio1"
}
```

```
// Response 401 Unauthorized
{
    "error_code": "401",
    "error_msg": "Unauthorized"
}
```

##### test case 3: 组织名重复

```
POST http://localhost:5000/users/1/organizations
```

```
// Request
{
    "name":"org1",
    "bio": "bio1"
}
```

```
// Response 409 Conflict
{
    "error_code": 409,
    "error_msg": "create conflicted, duplicate organization name"
}
```

##### 组织信息

@app.route('/users/<user_id>/organizations/<organization_id>', methods=['GET'])

@app.route('/users/<user_id>/organizations/<organization_id>/balance', methods=['GET'])

###### test case 1: 正确获得指定组织信息

```
GET http://localhost:5000/users/2/organizations/1
```

```
// Response 200 OK
{
    "name": "name11",
    "bio": "bio11",
    "avg_comment": 5,
    "members": [
        {
            "user_id": 2,
            "status": "admin"
        }
    ]
}
```

###### test case 2: 非登陆用户获取信息

```
GET http://localhost:5000/users/1/organizations/1
```

```
// Response 401 Unauthorized
{
    "error_code": "401",
    "error_msg": "Unauthorized"
}
```

###### test case 3: 找不到组织

```
GET http://localhost:5000/users/1/organizations/10
```

```
// Response 404 Not Found
{
    "error_code": "404",
    "error_msg": "Unauthorized"
}
```

###### test case 4: 管理员成功查询组织余额

```
GET http://localhost:5000/users/1/organizations/1/balance
```

```
// Response 200 OK
{
    "balance": 0
}
```

###### test case 5: 非管理员查询组织余额

```
GET http://localhost:5000/users/2/organizations/1/balance
```

```
// Response 401 Unauthorized
{
    "error_code": "401",
    "error_msg": "Unauthorized"
}
```

##### 组织信息修改

@app.route('/users/<user_id>/organizations/<organization_id>', methods=['PUT'])

###### test case 1: 正确修改指定组织信息

```
PUT http://localhost:5000/users/2/organizations/1
```

```
// Request
{
    "name":"org111",
    "bio": "bio111"
}
```

```
// Response 200 OK
{
    "name": "name111",
    "bio": "bio111"
}
```

###### test case 2: 非管理员修改组织信息

```
PUT http://localhost:5000/users/2/organizations/3
```

```
// Request
{
    "name":"org111",
    "bio": "bio111"
}
```

```
// Response 401 Unauthorized
{
    "error_code": "401",
    "error_msg": "Unauthorized"
}
```

###### test case 3: 找不到组织2

```
PUT http://localhost:5000/users/2/organizations/10
```

```
// Request
{
    "name":"org111",
    "bio": "bio111"
}
```

```
// Response 404 Not Found
{
    "error_code": "404",
    "error_msg": "Organization Not Found"
}
```

###### test case 4: 组织名重复(Todo)

```
PUT http://localhost:5000/users/2/organizations/2
```

```
// Request
{
    "name":"org1",
    "bio": "bio1"
}
```

```
// Response 500
{
    "error_code": 500,
    "error_msg": "duplicate organization name"
}
```

##### 群主管理员添加成员(Todo)

@app.route('/users/<user_id>/organizations/<organization_id>/members',
methods=\['POST'\])

###### test case 1: 使用邮箱成功添加

```
POST http://localhost:5000/users/2/organizations/1/members
```

```
// Request 
{
    "email": "test",
    "status": "member"
}
```

```
// Response 201 Created
{
    "msg": "Added successfully."
}
```

###### test case 2: 使用电话成功添加

```
POST http://localhost:5000/users/2/organizations/1/members
```

```
// Request
{
    "phone_number": "test2",
    "status": "member"
}
```

```
// Response 201 Created
{
    "msg": "add successfully."
}
```

###### test case 3: 重复添加成员(Todo)

```
POST http://localhost:5000/users/2/organizations/1/members
```

```
// Request 500
{
    "phone_number": "test1",
    "status": "member"
}
```

```
// Response
{
    "error_code": "500",
    "error_msg": "duplicate member"
}
```

##### 组织成员权限变更(Todo)

@app.route('/users/<user_id>/organizations/<organization_id>/members/<member_id>', methods=['PUT'])

###### test case 1: 成功修改权限

```
POST http://localhost:5000/users/2/organizations/1/members/1
```

```
// Request 
{
    "status": "member"
}
```

```
// Response 200 OK
{
    "msg": "update successfully."
}
```

##### 组织成员删除(Todo)

@app.route('/users/<user_id>/organizations/<organization_id>/members/<member_id>', methods=['DELETE'])

###### test case 1: 成功删除成员

```
DELETE http://localhost:5000/users/2/organizations/2/members/1
```

```
// Response 200 OK
{
    "msg": "delete successfully."
}
```

##### 群主删除组织(Todo)

@app.route('/users/<user_id>/organizations/<organization_id>',
methods=\['DELETE'\])

```
DELETE http://localhost:5000/users/2/organization/1
```

```
// Response
{
    "name": "test4",
    "bio": "test4"
}
```

##### 用户参加的组织

@app.route('/users/<user_id>/organizations', methods=['GET'])

```
//Response
{
    "organizations": [
        {
            "organization_id": 2,
            "organization_name": "name",
            "status": "admin"
        }
    ]
}
```

#### 任务系统

##### 个人创建任务

@app.route('/users/<user_id>/task', methods=\['POST'\])

```
POST http://localhost:5000/users/9/task
```
```
// Request
{
    "title": "task9",
    "description": "task9",
    "tags": ["tag1", "tag2", "tag3"],
    "participant_number_limit": 10,
    "reward_for_one_participant": 0.1,
    "user_limit": {
        "age_upper": 0,
        "age_lower": 1,
        "grades": ["grade1", "grade1"],
        "sexes": ["sex_type1", "sex_type2", "sex_type3"],
        "schools": ["school_name1", "school_name2"]
    },
    "steps": [
        {
            "title": "step1",
            "description": "string"
        },
        {
            "title": "step2",
            "description": "string"
        }
    ]
}
```
```
// Response
{
    "task_id": 5,
    "creator_user_id": 9,
    "creator_organization_id": null,
    "status": "on going",
    "title": "task9",
    "description": "task9",
    "tags": [
        "tag1",
        "tag2",
        "tag3"
    ],
    "participant_number_limit": 10,
    "reward_for_one_participant": 0.1,
    "post_time": "Mon, 22 Apr 2019 11:28:42 GMT",
    "receive_end_time": "Mon, 22 Apr 2019 12:28:42 GMT",
    "finish_deadline_time": "Tue, 23 Apr 2019 11:28:42 GMT",
    "user_limit": {
        "age_upper": 0,
        "age_lower": 1,
        "grades": [
            "grade1",
            "grade1"
        ],
        "sexes": [
            "sex_type1",
            "sex_type2",
            "sex_type3"
        ],
        "schools": [
            "school_name1",
            "school_name2"
        ]
    },
    "steps": [
        {
            "title": "step1",
            "description": "string"
        },
        {
            "title": "step2",
            "description": "string"
        }
    ],
    "participant_ids": [],
    "ongoing_participant_ids": [],
    "waiting_examine_participant_ids": [],
    "finished_participant_ids": []
}
```

##### 组织创建任务

@app.route('/users/<user_id>/organization/<organization_id>/tasks',
methods=\['POST'\])

```
POST http://localhost:5000/users/1/organization/1/tasks
```
```
// Request
{
    "title": "task1",
    "description": "task1",
    "tags": ["tag1", "tag2", "tag3"],
    "participant_number_limit": 10,
    "reward_for_one_participant": 10,
    "user_limit": {
        "age_upper": 0,
        "age_lower": 1,
        "grades": ["grade1", "grade1"],
        "sexes": ["sex_type1", "sex_type2", "sex_type3"],
        "schools": ["school_name1", "school_name2"]
    },
    "steps": [
        {
            "title": "step1",
            "description": "string"
        },
        {
            "title": "step2",
            "description": "string"
        }
    ]
}
```
```
// Response
{
    "task_id": 11,
    "creator_user_id": 1,
    "creator_organization_id": 1,
    "status": "on going",
    "title": "task1",
    "description": "task1",
    "tags": [
        "tag1",
        "tag2",
        "tag3"
    ],
    "participant_number_limit": 10,
    "reward_for_one_participant": 10,
    "post_time": "Mon, 22 Apr 2019 09:01:22 GMT",
    "receive_end_time": "Mon, 22 Apr 2019 10:01:22 GMT",
    "finish_deadline_time": "Tue, 23 Apr 2019 09:01:22 GMT",
    "user_limit": {
        "age_upper": 0,
        "age_lower": 1,
        "grades": [
            "grade1",
            "grade1"
        ],
        "sexes": [
            "sex_type1",
            "sex_type2",
            "sex_type3"
        ],
        "schools": [
            "school_name1",
            "school_name2"
        ]
    },
    "steps": [
        {
            "title": "step1",
            "description": "string"
        },
        {
            "title": "step2",
            "description": "string"
        }
    ],
    "participant_ids": [],
    "ongoing_participant_ids": [],
    "waiting_examine_participant_ids": [],
    "finished_participant_ids": []
}
```

##### 用户查询自己创建的任务

@app.route('/users/<user_id>/tasks', methods=\['GET'\])

```
POST http://localhost:5000/users/9/tasks
```
```
// Request
// ...
```
```
// Response
[
    {
        "task_id": 5,
        "creator_user_id": 9,
        "creator_organization_id": null,
        "status": "on going",
        "title": "task9",
        "description": "task9",
        "tags": [
            "tag1",
            "tag2",
            "tag3"
        ],
        "participant_number_limit": 10,
        "reward_for_one_participant": 0.1,
        "post_time": "Mon, 22 Apr 2019 11:28:42 GMT",
        "receive_end_time": "Mon, 22 Apr 2019 12:28:42 GMT",
        "finish_deadline_time": "Tue, 23 Apr 2019 11:28:42 GMT",
        "user_limit": {
            "age_upper": 0,
            "age_lower": 1,
            "grades": [
                "grade1",
                "grade1"
            ],
            "sexes": [
                "sex_type1",
                "sex_type2",
                "sex_type3"
            ],
            "schools": [
                "school_name1",
                "school_name2"
            ]
        },
        "steps": [
            {
                "title": "step1",
                "description": "string"
            },
            {
                "title": "step2",
                "description": "string"
            }
        ],
        "participant_ids": [],
        "ongoing_participant_ids": [],
        "waiting_examine_participant_ids": [],
        "finished_participant_ids": []
    },
    {
        "task_id": 6,
        "creator_user_id": 9,
        "creator_organization_id": null,
        "status": "on going",
        "title": "task9-2",
        "description": "task9-2",
        "tags": [
            "tag1",
            "tag2",
            "tag3"
        ],
        "participant_number_limit": 10,
        "reward_for_one_participant": 0.1,
        "post_time": "Mon, 22 Apr 2019 11:43:38 GMT",
        "receive_end_time": "Mon, 22 Apr 2019 12:43:38 GMT",
        "finish_deadline_time": "Tue, 23 Apr 2019 11:43:38 GMT",
        "user_limit": {
            "age_upper": 0,
            "age_lower": 1,
            "grades": [
                "grade1",
                "grade1"
            ],
            "sexes": [
                "sex_type1",
                "sex_type2",
                "sex_type3"
            ],
            "schools": [
                "school_name1",
                "school_name2"
            ]
        },
        "steps": [
            {
                "title": "step1",
                "description": "string"
            },
            {
                "title": "step2",
                "description": "string"
            }
        ],
        "participant_ids": [],
        "ongoing_participant_ids": [],
        "waiting_examine_participant_ids": [],
        "finished_participant_ids": []
    },
    {
        "task_id": 7,
        "creator_user_id": 9,
        "creator_organization_id": null,
        "status": "on going",
        "title": "task9-3",
        "description": "task9-3",
        "tags": [
            "tag1",
            "tag2",
            "tag3"
        ],
        "participant_number_limit": 10,
        "reward_for_one_participant": 0.1,
        "post_time": "Mon, 22 Apr 2019 13:13:11 GMT",
        "receive_end_time": "Mon, 22 Apr 2019 14:13:11 GMT",
        "finish_deadline_time": "Tue, 23 Apr 2019 13:13:11 GMT",
        "user_limit": {
            "age_upper": 0,
            "age_lower": 1,
            "grades": [
                "grade1",
                "grade1"
            ],
            "sexes": [
                "sex_type1",
                "sex_type2",
                "sex_type3"
            ],
            "schools": [
                "school_name1",
                "school_name2"
            ]
        },
        "steps": [
            {
                "title": "step1",
                "description": "string"
            },
            {
                "title": "step2",
                "description": "string"
            }
        ],
        "participant_ids": [],
        "ongoing_participant_ids": [],
        "waiting_examine_participant_ids": [],
        "finished_participant_ids": []
    }
]
```

##### 组织查询自己创建的任务

@app.route('/users/<user_id>/organization/<organization_id>/tasks',
methods=\['GET'\])

```
POST http://localhost:5000/users/9/organization/1/tasks
```
```
// Request
// ...
```
```
// Response
[
    {
        "task_id": 8,
        "creator_user_id": 9,
        "creator_organization_id": 1,
        "status": "on going",
        "title": "task9-org",
        "description": "task9-org",
        "tags": [
            "tag1",
            "tag2",
            "tag3"
        ],
        "participant_number_limit": 10,
        "reward_for_one_participant": 10,
        "post_time": "Mon, 22 Apr 2019 13:27:50 GMT",
        "receive_end_time": "Mon, 22 Apr 2019 14:27:50 GMT",
        "finish_deadline_time": "Tue, 23 Apr 2019 13:27:50 GMT",
        "user_limit": {
            "age_upper": 0,
            "age_lower": 1,
            "grades": [
                "grade1",
                "grade1"
            ],
            "sexes": [
                "sex_type1",
                "sex_type2",
                "sex_type3"
            ],
            "schools": [
                "school_name1",
                "school_name2"
            ]
        },
        "steps": [
            {
                "title": "step1",
                "description": "string"
            },
            {
                "title": "step2",
                "description": "string"
            }
        ],
        "participant_ids": [],
        "ongoing_participant_ids": [],
        "waiting_examine_participant_ids": [],
        "finished_participant_ids": []
    }
]
```

##### *任务查询

@app.route('/users/<user_id>/tasks/search', methods=['GET'])

###### test case 1：查找给female的任务

```
GET http://localhost:5000/users/1/tasks/search
```

```
// Request
{
    "user_limit": {
        "sexes": ["female"]
    } 
}
```

```
// Response 200 OK
[
    {
        "task_id": 14,
        "creator_user_id": 1,
        "creator_organization_id": null,
        "status": "on going",
        "title": "task-test-1",
        "description": "task-test-boy & girl",
        "tags": [
            "deliver"
        ],
        "participant_number_limit": 10,
        "reward_for_one_participant": 10,
        "post_time": "Wed, 24 Apr 2019 17:16:35 GMT",
        "receive_end_time": "Wed, 24 Apr 2019 18:16:35 GMT",
        "finish_deadline_time": "Thu, 25 Apr 2019 17:16:35 GMT",
        "user_limit": {
            "age_upper": 20,
            "age_lower": 18,
            "grades": [
                "grade1",
                "grade1"
            ],
            "sexes": [
                "female",
                "male"
            ],
            "schools": [
                "school_name1",
                "school_name2"
            ]
        },
        "steps": [
            {
                "title": "step1-org",
                "description": "string"
            },
            {
                "title": "step2-org",
                "description": "string"
            }
        ],
        "participant_ids": [],
        "ongoing_participant_ids": [],
        "waiting_examine_participant_ids": [],
        "finished_participant_ids": []
    },
    {
        "task_id": 15,
        "creator_user_id": 1,
        "creator_organization_id": null,
        "status": "on going",
        "title": "task-test-2",
        "description": "task-test-only girl",
        "tags": [
            "deliver"
        ],
        "participant_number_limit": 10,
        "reward_for_one_participant": 10,
        "post_time": "Wed, 24 Apr 2019 17:16:35 GMT",
        "receive_end_time": "Wed, 24 Apr 2019 18:16:35 GMT",
        "finish_deadline_time": "Thu, 25 Apr 2019 17:16:35 GMT",
        "user_limit": {
            "age_upper": 20,
            "age_lower": 18,
            "grades": [
                "grade1",
                "grade1"
            ],
            "sexes": [
                "female"
            ],
            "schools": [
                "school_name1",
                "school_name2"
            ]
        },
        "steps": [
            {
                "title": "step1-org",
                "description": "string"
            },
            {
                "title": "step2-org",
                "description": "string"
            }
        ],
        "participant_ids": [],
        "ongoing_participant_ids": [],
        "waiting_examine_participant_ids": [],
        "finished_participant_ids": []
    }
]
```

###### test case 2：查找steps不超过1的任务

```
PUT http://localhost:5000/users/1/tasks/search
```

```
// Request
{
    "steps_number_upper": 1
}
```

```
// Response 200 OK
[
    {
        "task_id": 16,
        "creator_user_id": 1,
        "creator_organization_id": null,
        "status": "on going",
        "title": "task-test-one-step",
        "description": "task-tesk",
        "tags": [
            "deliver"
        ],
        "participant_number_limit": 10,
        "reward_for_one_participant": 10,
        "post_time": "Wed, 24 Apr 2019 17:16:35 GMT",
        "receive_end_time": "Wed, 24 Apr 2019 18:16:35 GMT",
        "finish_deadline_time": "Thu, 25 Apr 2019 17:16:35 GMT",
        "user_limit": {
            "age_upper": 20,
            "age_lower": 18,
            "grades": [
                "grade1",
                "grade1"
            ],
            "sexes": [
                "female",
                "male"
            ],
            "schools": [
                "school_name1",
                "school_name2"
            ]
        },
        "steps": [
            {
                "title": "step1-org",
                "description": "string"
            }
        ],
        "participant_ids": [],
        "ongoing_participant_ids": [],
        "waiting_examine_participant_ids": [],
        "finished_participant_ids": []
    }
]
```

###### test case 3：找到所有task1-org组织创建的任务

```
PUT http://localhost:5000/users/1/tasks/search
```

```
// Request 
{
    "creator_organization_name": "test1-org"
}
```

```
// Response 200 OK
[
    {
        "task_id": 13,
        "creator_user_id": 1,
        "creator_organization_id": 1,
        "status": "pending",
        "title": "task-cccc",
        "description": "task-ccc",
        "tags": [
            "tag1-org-cc"
        ],
        "participant_number_limit": 16,
        "reward_for_one_participant": 10,
        "post_time": "Wed, 24 Apr 2019 14:30:26 GMT",
        "receive_end_time": "Wed, 24 Apr 2019 15:30:26 GMT",
        "finish_deadline_time": "Thu, 25 Apr 2019 14:30:26 GMT",
        "user_limit": {
            "age_upper": 0,
            "age_lower": 1,
            "grades": [
                "grade1",
                "grade1"
            ],
            "sexes": [
                "sex_type1",
                "sex_type2",
                "sex_type3"
            ],
            "schools": [
                "school_name1",
                "school_name2"
            ]
        },
        "steps": [
            {
                "title": "step1-org",
                "description": "string"
            },
            {
                "title": "step2-org",
                "description": "string"
            }
        ],
        "participant_ids": [],
        "ongoing_participant_ids": [],
        "waiting_examine_participant_ids": [],
        "finished_participant_ids": []
    },
    {
        "task_id": 11,
        "creator_user_id": 1,
        "creator_organization_id": 1,
        "status": "pending",
        "title": "task-ccccorg",
        "description": "task-ccc",
        "tags": [
            "tag1-org-cc"
        ],
        "participant_number_limit": 16,
        "reward_for_one_participant": 13,
        "post_time": "Wed, 24 Apr 2019 12:39:29 GMT",
        "receive_end_time": "Wed, 24 Apr 2019 13:39:29 GMT",
        "finish_deadline_time": "Thu, 25 Apr 2019 12:39:29 GMT",
        "user_limit": {
            "age_upper": 0,
            "age_lower": 1,
            "grades": [
                "grade1",
                "grade1"
            ],
            "sexes": [
                "sex_type1",
                "sex_type2",
                "sex_type3"
            ],
            "schools": [
                "school_name1",
                "school_name2"
            ]
        },
        "steps": [
            {
                "title": "step1-org",
                "description": "string"
            },
            {
                "title": "step2-org",
                "description": "string"
            }
        ],
        "participant_ids": [],
        "ongoing_participant_ids": [],
        "waiting_examine_participant_ids": [],
        "finished_participant_ids": []
    }
]
```

##### 任务接受

@app.route('/users/<user_id>/tasks/<task_id>', methods=\['POST'\])

```
POST http://localhost:5000/users/2/tasks/8
```
```
// Request
// ...
```
```
// Response 201 CREARTED
{
    "msg": "Receive task successfully."
}
```

##### 任务完成

@app.route('/users/<user_id>/tasks/<task_id>/steps/<step_id>',
methods=\['PUT'\])

###### test case 1：正常改变step

```
PUT http://localhost:5000/users/2/tasks/1/steps/1
```
```
// Request
// ...
```
```
// Response 200 OK
{
    "user_id": 2,
    "task_id": 1,
    "task_title": "task1",
    "task_status": "On going",
    "task_total_steps": [
        {
            "title": "step1",
            "description": "string"
        },
        {
            "title": "step2",
            "description": "string"
        }
    ],
    "task_finished_steps": 1
}
```

###### test case 2：step\_id超过任务本身设定的step/step之前已经标记过了

```
PUT http://localhost:5000/users/2/tasks/1/steps/1
```
```
// Request
// ...
```
```
// Response 500 INTERNAL SERVER ERROR
{
    "error_code": "500",
    "error_msg": "Step number incorrect"
}
```

###### test case 3：该用户没有接受该任务

```
PUT http://localhost:5000/users/1/tasks/1/steps/1
```
```
// Request
// ...
```
```
// Response 500 INTERNAL SERVER ERROR
{
    "error_code": "500",
    "error_msg": "Insufficient permission"
}
```

##### 任务审核

@app.route('/users/<user_id>/tasks/<task_id>/finisher/<finisher_id>',
methods=\['PUT'\])

###### test case 1：正常标记用户完成任务

```
PUT http://localhost:5000/users/1/tasks/1/finisher/4
```
```
// Request
// ...
```
```
// Response 200 OK
{
    "task_id": 1,
    "creator_user_id": 1,
    "creator_organization_id": null,
    "status": "on going",
    "title": "task1",
    "description": "task1",
    "tags": [
        "tag1",
        "tag2",
        "tag3"
    ],
    "participant_number_limit": 10,
    "reward_for_one_participant": 10,
    "post_time": "Tue, 23 Apr 2019 07:37:52 GMT",
    "receive_end_time": "Tue, 23 Apr 2019 08:37:52 GMT",
    "finish_deadline_time": "Wed, 24 Apr 2019 07:37:52 GMT",
    "user_limit": {
        "age_upper": 0,
        "age_lower": 1,
        "grades": [
            "grade1",
            "grade1"
        ],
        "sexes": [
            "sex_type1",
            "sex_type2",
            "sex_type3"
        ],
        "schools": [
            "school_name1",
            "school_name2"
        ]
    },
    "steps": [
        {
            "title": "step1",
            "description": "string"
        },
        {
            "title": "step2",
            "description": "string"
        }
    ],
    "participant_ids": [
        2,
        3,
        4
    ],
    "ongoing_participant_ids": [
        3
    ],
    "waiting_examine_participant_ids": [],
    "finished_participant_ids": [
        2,
        4
    ]
}

```

###### test case 2：该用户已经被标记完成

```
PUT http://localhost:5000/users/1/tasks/1/finisher/2
```
```
// Request
// ...
```
```
// Response 500 INTERNAL SERVER ERROR
{
    "error_code": "500",
    "error_msg": "Task has already finished!"
}

```

##### 撤回任务

@app.route('/users/<user_id>/tasks/<task_id>', methods=\[‘PUT’\])

###### test case 1：正常撤回

```
PUT http://localhost:5000/users/1/tasks/2
```
```
// Request
{
    "status":"pending"
}
```
```
// Response 200 OK
{
    "task_id": 2,
    "creator_user_id": 1,
    "creator_organization_id": null,
    "status": "pending",
    "title": "task2",
    "description": "task2",
    "tags": [
        "tag1",
        "tag2",
        "tag3"
    ],
    "participant_number_limit": 10,
    "reward_for_one_participant": 10,
    "post_time": null,
    "receive_end_time": null,
    "finish_deadline_time": null,
    "user_limit": {
        "age_upper": 0,
        "age_lower": 1,
        "grades": [
            "grade1",
            "grade1"
        ],
        "sexes": [
            "sex_type1",
            "sex_type2",
            "sex_type3"
        ],
        "schools": [
            "school_name1",
            "school_name2"
        ]
    },
    "steps": [
        {
            "title": "step1",
            "description": "string"
        },
        {
            "title": "step2",
            "description": "string"
        }
    ],
    "participant_ids": [],
    "ongoing_participant_ids": [],
    "waiting_examine_participant_ids": [],
    "finished_participant_ids": []
}

```

###### test case 2：撤回已经处于pending状态的任务

```
PUT http://localhost:5000/users/1/tasks/2
```
```
// Request
{
    "status":"pending"
}
```
```
// Response 500 INTERNAL SERVER ERROR
{
    "error_code": "500",
    "error_msg": "Already pended"
}

```

##### 修改个人未发布任务

@app.route('/users/<user_id>/tasks/<task_id>', methods=\[‘PUT’\])

```
PUT http://localhost:5000/users/1/tasks/1
```
```
// Request
{
    "title": "task1-modify",
    "description": "task1-modify",
    "tags": ["tag1", "tag2", "tag3"],
    "participant_number_limit": 1,
    "reward_for_one_participant": 5,
    "user_limit": {
        "age_upper": 0,
        "age_lower": 1,
        "grades": ["grade1", "grade1"],
        "sexes": ["sex_type1", "sex_type2", "sex_type3"],
        "schools": ["school_name1", "school_name2"]
    },
    "steps": [
        {
            "title": "step1",
            "description": "string"
        },
        {
            "title": "step2",
            "description": "string"
        }
    ]
}
```
```
// Request 200 OK
{
    "task_id": 1,
    "creator_user_id": 1,
    "creator_organization_id": null,
    "status": "pending",
    "title": "task1-modify",
    "description": "task1-modify",
    "tags": [
        "tag1",
        "tag2",
        "tag3"
    ],
    "participant_number_limit": 1,
    "reward_for_one_participant": 5,
    "post_time": null,
    "receive_end_time": null,
    "finish_deadline_time": null,
    "user_limit": {
        "age_upper": 0,
        "age_lower": 1,
        "grades": [
            "grade1",
            "grade1"
        ],
        "sexes": [
            "sex_type1",
            "sex_type2",
            "sex_type3"
        ],
        "schools": [
            "school_name1",
            "school_name2"
        ]
    },
    "steps": [
        {
            "title": "step1",
            "description": "string"
        },
        {
            "title": "step2",
            "description": "string"
        }
    ],
    "participant_ids": [],
    "ongoing_participant_ids": [],
    "waiting_examine_participant_ids": [],
    "finished_participant_ids": []
}

```

##### 修改组织未发布任务

@app.route('/users/<user_id>/organization/<organization_id>/tasks/<task_id>',
methods=\['PUT'\])

###### test case 1：修改未经撤回的任务

```
PUT http://localhost:5000/users/1/organization/1/tasks/3
```
```
// Request
{
    "title": "task-org1-modify",
    "description": "task-org1-modify",
    "tags": ["tag1-org", "tag2-org", "tag3-org"],
    "participant_number_limit": 10,
    "reward_for_one_participant": 10,
    "user_limit": {
        "age_upper": 0,
        "age_lower": 1,
        "grades": ["grade1", "grade1"],
        "sexes": ["sex_type1", "sex_type2", "sex_type3"],
        "schools": ["school_name1", "school_name2"]
    },
    "steps": [
        {
            "title": "step1-org",
            "description": "string"
        },
        {
            "title": "step2-org",
            "description": "string"
        }
    ]
}
```
```
// Response 500 INTERNAL SERVER ERROR
{
    "error_code": "500",
    "error_msg": "The task is not pended, can't be modified."
}

```

###### test case 2：正常修改组织创建任务

```
PUT http://localhost:5000/users/1/organization/1/tasks/3
```
```
// Request
{
    "title": "task-org1-modify",
    "description": "task-org1-modify",
    "tags": ["tag1-org", "tag2-org", "tag3-org"],
    "participant_number_limit": 10,
    "reward_for_one_participant": 10,
    "user_limit": {
        "age_upper": 0,
        "age_lower": 1,
        "grades": ["grade1", "grade1"],
        "sexes": ["sex_type1", "sex_type2", "sex_type3"],
        "schools": ["school_name1", "school_name2"]
    },
    "steps": [
        {
            "title": "step1-org",
            "description": "string"
        },
        {
            "title": "step2-org",
            "description": "string"
        }
    ]
}
```
```
// Response 200 OK
{
    "task_id": 3,
    "creator_user_id": 1,
    "creator_organization_id": 1,
    "status": "pending",
    "title": "task-org1-modify",
    "description": "task-org1-modify",
    "tags": [
        "tag1-org",
        "tag2-org",
        "tag3-org"
    ],
    "participant_number_limit": 10,
    "reward_for_one_participant": 10,
    "post_time": null,
    "receive_end_time": null,
    "finish_deadline_time": null,
    "user_limit": {
        "age_upper": 0,
        "age_lower": 1,
        "grades": [
            "grade1",
            "grade1"
        ],
        "sexes": [
            "sex_type1",
            "sex_type2",
            "sex_type3"
        ],
        "schools": [
            "school_name1",
            "school_name2"
        ]
    },
    "steps": [
        {
            "title": "step1-org",
            "description": "string"
        },
        {
            "title": "step2-org",
            "description": "string"
        }
    ],
    "participant_ids": [],
    "ongoing_participant_ids": [],
    "waiting_examine_participant_ids": [],
    "finished_participant_ids": []
}

```

##### 删除个人任务

@app.route('/users/<user_id>/tasks/<task_id>', methods=\['DELETE'\])

###### test case 1：正常删除任务

```
DELETE http://localhost:5000/users/1/tasks/1
```
```
// Request
// ...
```
```
// Response 200 OK
{
    "msg": "Delete task1-modify successfully."
}

```

###### test case 2：删除不属于自己的任务

```
DELETE http://localhost:5000/users/1/tasks/4
```
```
// Request
// ...
```
```
// Response 404 NOT FOUND
{
    "error_code": "404",
    "error_msg": "task Not Found"
}

```

##### 删除组织任务

@app.route('/users/<user_id>/organization/<organization_id>/tasks/<task_id>',
methods=\['DELETE'\])

###### test case 1：正常删除任务

```
DELETE http://localhost:5000/users/1/organization/1/tasks/3
```
```
// Request
// ...
```
```
// Response 200 OK
{
    "msg": "Delete task1-org successfully."
}

```

#### 接收者评价系统

##### 任务接收者写评价

@routes.route('/users/<user_id>/tasks/<task_id>/review', methods=['POST'])

###### test case 1：正常添加评论

```
POST http://localhost:5000/users/3/tasks/1/review
```

```
// Request
{
    "title":"Good!",
    "content":"It's easy to do. And can earn a lot of money!",
    "rate": 5
}
```

```
// Response
{
    "user_id": 3,
    "task_id": 1,
    "review_title": "Good!",
    "review_content": "It's easy to do. And can earn a lot of money!",
    "review_rate": 5
}
```

表项可以留空（会默认好评）

待添加

######test case 2：该用户没有接收该任务

待添加

###### test case 3：该用户还未经审核标记为完成该任务

待添加

###### test case 4：该用户已经写过评价

```
POST http://localhost:5000/users/3/tasks/1/review
```

```
// Request
{
    "title":"Good! Again",
    "content":"It's easy to do. And can earn a lot of money! Again",
    "rate": 5
}
```

```
// Response
{
    "error_code": "500",
    "error_msg": "You have created a comment"
}
```

##### 任务接收者修改评价

@routes.route('/users/<user_id>/tasks/<task_id>/review', methods=['PUT'])

###### test case 1：正确修改评论

```
PUT http://localhost:5000/users/3/tasks/1/review
```

```
// Request
{
    "title":"Good! Modify",
    "content":"It's easy to do. And can earn a lot of money! Modify",
    "rate": 2
}
```

```
// Response
{
    "user_id": 3,
    "task_id": 1,
    "review_title": "Good! Modify",
    "review_content": "It's easy to do. And can earn a lot of money! Modify",
    "review_rate": 2
}
```

###### test case 2：还未编辑评论

待添加

##### 任务接收者删除评论

@routes.route('/users/<user_id>/tasks/<task_id>/review', methods=['DELETE'])

###### test case 1：正常删除

待添加

###### test case 2：未找到评论

```
DELETE http://localhost:5000/users/3/tasks/1/review
```

```
// Request
{
    "title":"Good! Modify",
    "content":"It's easy to do. And can earn a lot of money! Modify",
    "rate": 2
}
```

```
// Response
{
    "error_code": "500",
    "error_msg": "No comment found"
}
```

##### 获取某个任务的评价（平均分+所有评价）

@routes.route('/tasks/<task_id>/reviews', methods=['GET'])

```
GET http://localhost:5000/tasks/1/reviews
```

```
// Request
//
```

```
// Response
{
    "avg_points": 4.428571428571429,
    "reviews": [
        {
            "username": "test2",
            "title": "ok",
            "content": "ok",
            "rate": 5
        },
        {
            "username": "test2",
            "title": "o k",
            "content": "o k",
            "rate": 5
        },
        {
            "username": "test2",
            "title": "o k",
            "content": "o k",
            "rate": 5
        },
        {
            "username": "test2",
            "title": "kakaka",
            "content": "kakaaaaaaaaakaa",
            "rate": 5
        },
        {
            "username": "test2",
            "title": "kakaka",
            "content": "kakaaaaaaaaakaa",
            "rate": 5
        },
        {
            "username": "test2",
            "title": "kakaka",
            "content": "default good review",
            "rate": 5
        },
        {
            "username": "test-new",
            "title": "Good! Modify",
            "content": "It's easy to do. And can earn a lot of money! Modify",
            "rate": 1
        }
    ]
}
```

