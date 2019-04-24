- [用户与组织系统](#用户与组织系统)
- [用户创建](#用户创建)
- [用户登录](#用户登录)
- [用户登录注销](#用户登录注销)
  - [test case 1：成功注销](#test-case-1成功注销)
  - [test case 2：注销非登录者（非token记录）的账号](#test-case-2注销非登录者非token记录的账号)
- [用户信息](#用户信息)
- [用户信息修改 (Todo)](#用户信息修改-todo)
- [组织创建](#组织创建)
- [组织信息 (Todo)](#组织信息-todo)
- [组织信息修改 (Todo)](#组织信息修改-todo)
- [群主管理员添加成员](#群主管理员添加成员)
- [组织成员权限变更 (Todo)](#组织成员权限变更-todo)
- [组织成员删除 (Todo)](#组织成员删除-todo)
- [群主删除组织](#群主删除组织)
- [用户参加的组织 (Todo)](#用户参加的组织-todo)
- [任务系统](#任务系统)
- [个人创建任务](#个人创建任务)
- [组织创建任务](#组织创建任务)
- [用户查询自己创建的任务](#用户查询自己创建的任务)
- [组织查询自己创建的任务](#组织查询自己创建的任务)
- [*任务查询](#任务查询)
  - [test case 1：查找给female的任务](#test-case-1查找给female的任务)
  - [test case 2：查找steps不超过1的任务](#test-case-2查找steps不超过1的任务)
  - [test case 3：找到所有task1-org组织创建的任务](#test-case-3找到所有task1-org组织创建的任务)
- [任务接受](#任务接受)
- [任务完成](#任务完成)
  - [test case 1：正常改变step](#test-case-1正常改变step)
  - [test case 2：step_id超过任务本身设定的step/step之前已经标记过了](#test-case-2step_id超过任务本身设定的stepstep之前已经标记过了)
  - [test case 3：该用户没有接受该任务](#test-case-3该用户没有接受该任务)
- [任务审核](#任务审核)
  - [test case 1：正常标记用户完成任务](#test-case-1正常标记用户完成任务)
  - [test case 2：该用户已经被标记完成](#test-case-2该用户已经被标记完成)
- [撤回任务](#撤回任务)
  - [test case 1：正常撤回](#test-case-1正常撤回)
  - [test case 2：撤回已经处于pending状态的任务](#test-case-2撤回已经处于pending状态的任务)
- [修改个人未发布任务](#修改个人未发布任务)
- [修改组织未发布任务](#修改组织未发布任务)
  - [test case 1：修改未经撤回的任务](#test-case-1修改未经撤回的任务)
  - [test case 2：正常修改组织创建任务](#test-case-2正常修改组织创建任务)
- [删除个人任务](#删除个人任务)
  - [test case 1：正常删除任务](#test-case-1正常删除任务)
  - [test case 2：删除不属于自己的任务](#test-case-2删除不属于自己的任务)
- [删除组织任务](#删除组织任务)
  - [test case 1：正常删除任务](#test-case-1正常删除任务-1)

#### 用户与组织系统

##### 用户创建

@app.route('/users', methods=\['POST'\])

```
POST http://localhost:5000/users

// Request
{
    "password":"test6",
    "email": "test6",
    "phone_number": "test6",
    "username": "test6"
}

// Response
{
    "user_id": 6,
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NiwiZXhwIjoxNTU1OTI2NDc0fQ.DbbZWZ2feBmRbgYpPMPy8elIN2egFv84NAOGJcKQ040"
}
```

##### 用户登录

@app.route('/sessions', methods=\['POST'\])

```
POST http://localhost:5000/sessions

// Request
{
    "password":"test1",
    "email": "test1"
}

// Response
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTU1OTI2NjM5fQ.FZcD0-iLJITyaqllxNh45oCGS1N0fKl-33YDNaJEsyg"
}
```

##### 用户登录注销

@app.route('/users/<user_id>/session', methods=['DELETE'])

###### test case 1：成功注销

```
DELETE http://localhost:5000/users/1/session
```

```
// Request
// ...
```

```
// Response 200 OK
{
    "message": "test1 logged out successfully."
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
    "email": "test2",
    "phone_number": "test2",
    "profile_photo_path": "default.jpg",
    "student_id": null,
    "name": "test2",
    "age": null,
    "sex": null,
    "grade": null,
    "school": null,
    "bio": "this person is very lazy",
    "balance": 0,
    "avg_comment": 5
}
```

##### 用户信息修改 (Todo)

##### 组织创建

@app.route('/users/<user_id>/organization', methods=\['POST'\])

```
POST http://localhost:5000/users/1/organization

// Request
{
    "name":"test1-org",
    "bio": "test1"
}

// Response 201 CREATED
{
    "organization_id": 1
}
```

##### 组织信息 (Todo)

##### 组织信息修改 (Todo)

##### 群主管理员添加成员

@app.route('/users/<user_id>/organization/<organization_id>/members',
methods=\['POST'\])

test 1 使用email

```
POST http://localhost:5000/users/1/organization/1/members

// Request
{
    "email": "test2",
    "status": "member"
}

// Response
{
    "msg": "Added successfully."
}
```

test2 使用phone\_number

```
POST http://localhost:5000/users/1/organization/1/members

// Request
{
    "phone_number": "test4",
    "status": "member"
}

// Response
{
    "msg": "Added successfully."
}
```



##### 组织成员权限变更 (Todo)

##### 组织成员删除 (Todo)

##### 群主删除组织

@app.route('/users/<user_id>/organization/<organization_id>',
methods=\['DELETE'\])

```
DELETE http://localhost:5000/users/1/organization/1

// Request
// Token required
// ...

// Response
{
    "name": "test1-org",
    "bio": "test1"
}
```

##### 用户参加的组织 (Todo)

#### 任务系统

##### 个人创建任务

@app.route('/users/<user_id>/task', methods=\['POST'\])

```
POST http://localhost:5000/users/9/task

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

// Request
// ...

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

// Request
// ...

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

// Request
// ...

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

// Request
// ...

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

// Request
// ...

// Response 500 INTERNAL SERVER ERROR
{
    "error_code": "500",
    "error_msg": "Step number incorrect"
}
```

###### test case 3：该用户没有接受该任务

```
PUT http://localhost:5000/users/1/tasks/1/steps/1

// Request
// ...

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

// Request
// ...

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

// Request
// ...

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

// Request
{
    "status":"pending"
}

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

// Request
{
    "status":"pending"
}

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

// Response 500 INTERNAL SERVER ERROR
{
    "error_code": "500",
    "error_msg": "The task is not pended, can't be modified."
}

```

###### test case 2：正常修改组织创建任务

```
PUT http://localhost:5000/users/1/organization/1/tasks/3

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

// Request
// ...

// Response 200 OK
{
    "msg": "Delete task1-modify successfully."
}

```

###### test case 2：删除不属于自己的任务

```
DELETE http://localhost:5000/users/1/tasks/4

// Request
// ...

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

// Request
// ...

// Response 200 OK
{
    "msg": "Delete task1-org successfully."
}

```