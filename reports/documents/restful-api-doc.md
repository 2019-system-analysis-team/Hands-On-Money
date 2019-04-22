# RESTful API 设计文档

## 标准

- [What is REST](https://restfulapi.net/)
- [A RESTful Tutorial](https://www.restapitutorial.com/)
- [表现层状态转换](https://zh.wikipedia.org/wiki/%E8%A1%A8%E7%8E%B0%E5%B1%82%E7%8A%B6%E6%80%81%E8%BD%AC%E6%8D%A2)
- [理解RESTful架构](http://www.ruanyifeng.com/blog/2011/09/restful.html)
- [Media Uploading](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types)

## 参考
- [baoleme API doc](https://baoleme.github.io/API-document/#/)
- [Tiny Hippo 点餐系统API文档](https://rookies-sysu.github.io/Dashboard/07-03-API)
> Remember, they are not restful at all.


- [基于 Token 的身份验证：JSON Web Token JWT](https://ninghao.net/blog/2834)
- [Flask-JWT doc](https://pythonhosted.org/Flask-JWT/)


## 目录

- [RESTful API 设计文档](#restful-api-%E8%AE%BE%E8%AE%A1%E6%96%87%E6%A1%A3)
  - [标准](#%E6%A0%87%E5%87%86)
  - [参考](#%E5%8F%82%E8%80%83)
  - [目录](#%E7%9B%AE%E5%BD%95)
  - [API](#api)
    - [用户与组织系统](#%E7%94%A8%E6%88%B7%E4%B8%8E%E7%BB%84%E7%BB%87%E7%B3%BB%E7%BB%9F)
      - [用户创建](#%E7%94%A8%E6%88%B7%E5%88%9B%E5%BB%BA)
      - [用户登陆](#%E7%94%A8%E6%88%B7%E7%99%BB%E9%99%86)
      - [用户登陆注销](#%E7%94%A8%E6%88%B7%E7%99%BB%E9%99%86%E6%B3%A8%E9%94%80)
      - [用户信息](#%E7%94%A8%E6%88%B7%E4%BF%A1%E6%81%AF)
      - [用户信息修改](#%E7%94%A8%E6%88%B7%E4%BF%A1%E6%81%AF%E4%BF%AE%E6%94%B9)
      - [组织创建](#%E7%BB%84%E7%BB%87%E5%88%9B%E5%BB%BA)
      - [组织信息](#%E7%BB%84%E7%BB%87%E4%BF%A1%E6%81%AF)
      - [组织信息修改](#%E7%BB%84%E7%BB%87%E4%BF%A1%E6%81%AF%E4%BF%AE%E6%94%B9)
      - [组织成员添加](#%E7%BB%84%E7%BB%87%E6%88%90%E5%91%98%E6%B7%BB%E5%8A%A0)
      - [组织成员权限变更](#%E7%BB%84%E7%BB%87%E6%88%90%E5%91%98%E6%9D%83%E9%99%90%E5%8F%98%E6%9B%B4)
      - [组织成员删除](#%E7%BB%84%E7%BB%87%E6%88%90%E5%91%98%E5%88%A0%E9%99%A4)
      - [组织删除](#%E7%BB%84%E7%BB%87%E5%88%A0%E9%99%A4)
      - [用户参加的组织](#%E7%94%A8%E6%88%B7%E5%8F%82%E5%8A%A0%E7%9A%84%E7%BB%84%E7%BB%87)
    - [任务系统](#%E4%BB%BB%E5%8A%A1%E7%B3%BB%E7%BB%9F)
      - [用户/组织创建任务](#%E7%94%A8%E6%88%B7%E7%BB%84%E7%BB%87%E5%88%9B%E5%BB%BA%E4%BB%BB%E5%8A%A1)
      - [用户/组织查询自己创建的任务](#%E7%94%A8%E6%88%B7%E7%BB%84%E7%BB%87%E6%9F%A5%E8%AF%A2%E8%87%AA%E5%B7%B1%E5%88%9B%E5%BB%BA%E7%9A%84%E4%BB%BB%E5%8A%A1)
      - [任务查询](#%E4%BB%BB%E5%8A%A1%E6%9F%A5%E8%AF%A2)
      - [任务接受](#%E4%BB%BB%E5%8A%A1%E6%8E%A5%E5%8F%97)
      - [任务完成](#%E4%BB%BB%E5%8A%A1%E5%AE%8C%E6%88%90)
      - [任务审核](#%E4%BB%BB%E5%8A%A1%E5%AE%A1%E6%A0%B8)
      - [撤回任务](#%E6%92%A4%E5%9B%9E%E4%BB%BB%E5%8A%A1)
      - [修改未发布任务](#%E4%BF%AE%E6%94%B9%E6%9C%AA%E5%8F%91%E5%B8%83%E4%BB%BB%E5%8A%A1)
      - [组织/个人删除任务](#%E7%BB%84%E7%BB%87%E4%B8%AA%E4%BA%BA%E5%88%A0%E9%99%A4%E4%BB%BB%E5%8A%A1)

## API

- 数据表结构

![er model db design](https://s2.ax1x.com/2019/04/09/AIKv7V.png)

- 约定
    - 对于每个 request，response 列表的优先级自顶向下递减；
    - `error_msg` 只是我随便写的，你们可以自己改；
    - 对于键值不符合文档要求的 request，一律返回 400 Bad Request
    - 对于不在文档列表中的 request HTTP verb，一律返回 405 Method Not Allowed
    - 除部分注册、登陆可访问的 API 之外，未经正确验证 JWT 的 API 访问一律返回 401 Unauthorized
```json
//response: Bad Request. This post is SOMEHOW WRONG. 
//e.g. key is not correct, or value contain not-allowed characters (just like attacker)
HTTP/1.1 400 Bad Request
Content-Type: application/json
{
    "error_code": 400,
    "error_msg": "fuck you asshole"
}
```
```json
//response: Method Not Allowed
HTTP/1.1 405 Method Not Allowed
Content-Type: application/json
{
    "error_code": 405,
    "error_msg": "fuck you asshole"
}
```
```json
//response: JWT missing/incorrect/timeout, redirect ot login page
HTTP/1.1 401 Unauthorized
Content-Type: application/json
{
    "error_code": 401,
    "error_msg": "Unauthorized"
}
```
### 用户与组织系统
#### 用户创建

```json
//request: creating user 
POST /users HTTP/1.1
Content-Type: application/json
{
    "email": "user@example.com",
    "phone_number": "13123456789",
    "password": "password"
}
```

```json
//response: create successfully
HTTP/1.1 201 Created  //redirect to /
Content-Type: application/json
{
    "user_id":123456,
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNDQ0OTE3NjQwLCJuYmYiOjE0NDQ5MTc2NDAsImV4cCI6MTQ0NDkxNzk0MH0.KPmI6WSjRjlpzecPvs3q_T3cJQvAgJvaQAPtk1abC_E"
}
//about access_token, see Flask-JWT doc(https://pythonhosted.org/Flask-JWT/) for further information.

//response: create conflicted, duplicate email or phone_number
HTTP/1.1 409 Conflict
Content-Type: application/json
{
    "error_code": 409,
    "error_msg": "create conflicted, duplicate email or phone_number, goto login"
}
```

#### 用户登陆

```json
//request: login by email
POST /sessions HTTP/1.1
Content-Type: application/json
{
    "email": "user@example.com",
    "password": "password"
}
//request: or login by phone_number
{
    "phone_number": "13123456789",
    "password": "password"
}
```

```json
//response: login successfully, redirect to homepage
HTTP/1.1 200 OK
Content-Type: application/json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNDQ0OTE3NjQwLCJuYmYiOjE0NDQ5MTc2NDAsImV4cCI6MTQ0NDkxNzk0MH0.KPmI6WSjRjlpzecPvs3q_T3cJQvAgJvaQAPtk1abC_E"
}
//about access_token, see Flask-JWT doc(https://pythonhosted.org/Flask-JWT/) for further information.

//response: login failed, account not found/password incorrect
HTTP/1.1 404 Not Found
Content-Type: application/json
{
    "error_code": 404,
    "error_msg": "account not found/password incorrect"
}
```

#### 用户登陆注销

```json
//request: delete user session
DELETE /users/:user_id/session HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
```

```json
//response: delete session successfully, redirect to login page
HTTP/1.1 200 OK
//response: Unauthorized JWT, do not delete any session and redirect to login page
HTTP/1.1 401 Unauthorized
//response: user Not Found, do not delete any session and redirect to login page
HTTP/1.1 404 Not Found
```


#### 用户信息

```json
//request: get user info
GET /users/:user_id HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
```

```json
//response: get user info successfully
//user profile_photo will be downloaded independently from API
HTTP/1.1 200 OK
Content-Type: application/json
{
    "email": "",
    "phone_number": "",
    "profile_photo_path": "",
    "student_id": "",
    "name": "",
    "age": 0,
    "sex": "",
    "grade": "",
    "school": "",
    "bio": "",
    "balance": 0,
    "avg_comment": 0
}

//response: JWT missing/incorrect/timeout
HTTP/1.1 401 Unauthorized
Content-Type: application/json
{
    "error_code": 401,
    "error_msg": "Unauthorized"
}

//response: no this user:/users/:user_id in table
HTTP/1.1 404 Not Found
Content-Type: application/json
{
    "error_code": 404,
    "error_msg": "user Not Found"
}
```

#### 用户信息修改

分段更新。

```json
//request: update personality
PUT /users/:user_id/personality HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
Content-Type: application/json
{
    "nickname": "nickname",
    "bio": "bio"
}

//request: update school
PUT /users/:user_id/school HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
Content-Type: application/json
{
    "school": "school",
    "grade": "grade",
    "student_number": "sid"
}

//request: update personal_info
PUT /users/:user_id/personal_info HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
Content-Type: application/json
{
    "name": "name",
    "age": 0,
    "sex": "sex"
}

//request: update photo, after update, pull photo to client
POST /users/:user_id/profile_photo HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
Content-Type: image/jpeg
```

```json
//response: update success, NOT FOR update photo
HTTP/1.1 200 OK
Content-Type: application/json
{
    "key1": "value",
    "key2": "value",
    "key3": "value"
}

//response: JWT missing/incorrect/timeout
HTTP/1.1 401 Unauthorized
Content-Type: application/json
{
    "error_code": 401,
    "error_msg": "Unauthorized"
}

//response: no this /users/:user_id in table
HTTP/1.1 404 Not Found
Content-Type: application/json
{
    "error_code": 404,
    "error_msg": "user Not Found"
}
//response: not support img format
HTTP/1.1 415 Unsupported Media Type
Content-Type: application/json
{
    "error_code": 415,
    "error_msg": "Unsupported Media Type"
}
```

#### 组织创建

```json
//request: creating organization 
POST /users/:user_id/organization HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
Content-Type: application/json
{
    "name": "organization_name",
    "bio": "bio",
}
```

```json
//response: create successfully
HTTP/1.1 201 Created  //redirect to /organization/:organization_id
Content-Type: application/json
{
    "organization_id":"123456"
}

//response: JWT missing/incorrect/timeout
HTTP/1.1 401 Unauthorized
Content-Type: application/json
{
    "error_code": 401,
    "error_msg": "Unauthorized"
}

//response: create conflicted, duplicate name
HTTP/1.1 409 Conflict
Content-Type: application/json
{
    "error_code": 409,
    "error_msg": "create conflicted, duplicate organization name"
}
```

#### 组织信息
```json
//request: get organization info. All registered user can see it.
GET /users/:user_id/organization/:organization_id HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI

//request: get organization balance. Only admin can see it.
GET /users/:user_id/organization/:organization_id/balance HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
```

```json
//response: get organization info successfully. 
//user profile_photo will be downloaded independently from API
// NOTE: If you want member list to show more info of members, it will lead to N+1 problem, 
// see also (https://restfulapi.net/rest-api-n-1-problem/). Try server side solutions.
HTTP/1.1 200 OK
Content-Type: application/json
{
    "name": "",
    "bio": "",
    "avg_comment": 0,
    "members":[
        {
            "user_id": 123,
            "status": "status"
        },
        {
            "user_id": 123,
            "status": "status"
        }
    ]
}

//response: get organization balance successfully
HTTP/1.1 200 OK
Content-Type: application/json
{
    "balance": 0
}

//response: JWT missing/incorrect/timeout
HTTP/1.1 401 Unauthorized
Content-Type: application/json
{
    "error_code": 401,
    "error_msg": "Unauthorized"
}

//response: no this organization/:organization_id in table
HTTP/1.1 404 Not Found
Content-Type: application/json
{
    "error_code": 404,
    "error_msg": "organization Not Found"
}
```

#### 组织信息修改

```json
//request: update organization info
PUT /users/:user_id/organization/:organization_id HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
Content-Type: application/json
{
    "name": "name",
    "bio": "bio"
}
//request: update organization photo, after update, pull photo to client
POST /users/:user_id/organization/:organization_id/profile_photo HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
Content-Type: image/jpeg
```

```json
//response: get organization info successfully. 
HTTP/1.1 200 OK
Content-Type: application/json
{
    "name": "",
    "bio": ""
}
//response: JWT missing/incorrect/timeout
HTTP/1.1 401 Unauthorized
Content-Type: application/json
{
    "error_code": 401,
    "error_msg": "Unauthorized",
}
//response: no this organization/:organization_id in table
HTTP/1.1 404 Not Found
Content-Type: application/json
{
    "error_code": 404,
    "error_msg": "organization Not Found"
}
//response: not support img format
HTTP/1.1 415 Unsupported Media Type
Content-Type: application/json
{
    "error_code": 415,
    "error_msg": "Unsupported Media Type"
}
```

#### 组织成员添加
```json
//request: add organization member
POST /users/:user_id/organization/:organization_id/members HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
Content-Type: application/json
{
    "email": "email@mail.com",
    "status": "member"
}
or
{
    "phone_number": "13123456789",
    "status": "member"
}
```
```json
//response: add member successfully. Redirect to organization info
HTTP/1.1 201 Created

//response: JWT missing/incorrect/timeout, redirect to login;
//or you dont have permission to add member to such "status"
HTTP/1.1 401 Unauthorized
Content-Type: application/json
{
    "error_code": 401,
    "error_msg": "Unauthorized"
}
or
{
    "error_code": 401,
    "error_msg": "insufficient permission"
}
//response: no this user/organization in users
HTTP/1.1 404 Not Found
Content-Type: application/json
{
    "error_code": 404,
    "error_msg": "user/organization Not Found"
}
```

#### 组织成员权限变更
```json
//request: modify organization member status
PUT /users/:user_id/organization/:organization_id/members/:user_id HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
Content-Type: application/json
{
    "status": "member"
}
```
```json
//response: modify member successfully. Redirect to organization info
HTTP/1.1 200 OK

//response: JWT missing/incorrect/timeout, redirect to login;
//or you dont have permission to modify member to such "status"
HTTP/1.1 401 Unauthorized
Content-Type: application/json
{
    "error_code": 401,
    "error_msg": "Unauthorized"
}
or
{
    "error_code": 401,
    "error_msg": "insufficient permission"
}
//response: no this user/organization in users
HTTP/1.1 404 Not Found
Content-Type: application/json
{
    "error_code": 404,
    "error_msg": "user/organization Not Found"
}
```

#### 组织成员删除
```json
//request: delete organization member
DELETE /users/:user_id/organization/:organization_id/members/:user_id HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
```
```json
//response: delete member successfully. Redirect to organization info
HTTP/1.1 200 OK

//response: JWT missing/incorrect/timeout, redirect to login;
//or you dont have permission to delete member while he is in such "status"
HTTP/1.1 401 Unauthorized
Content-Type: application/json
{
    "error_code": 401,
    "error_msg": "Unauthorized"
}
or
{
    "error_code": 401,
    "error_msg": "insufficient permission"
}
//response: no this user/organization in users
HTTP/1.1 404 Not Found
Content-Type: application/json
{
    "error_code": 404,
    "error_msg": "user/organization Not Found"
}
```

#### 组织删除
```json
//request: delete organization, only creator
DELETE /users/:user_id/organization/:organization_id HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
```
```json
//response: show deleted organization info. 
HTTP/1.1 200 OK
Content-Type: application/json
{
    "name": "",
    "bio": ""
}
//response: JWT missing/incorrect/timeout
HTTP/1.1 401 Unauthorized
Content-Type: application/json
{
    "error_code": 401,
    "error_msg": "Unauthorized",
}
//response: no this organization/:organization_id in table
HTTP/1.1 404 Not Found
Content-Type: application/json
{
    "error_code": 404,
    "error_msg": "organization Not Found"
}
```
#### 用户参加的组织
```json
//request: get user's organization
GET /users/:user_id/organization HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
```
```json
TODO return organization list
```

### 任务系统

#### 用户/组织创建任务

```json
//request: user creating task 
POST /users/:user_id/tasks HTTP/1.1
//or request: organization creating task 
POST /users/:user_id/organization/:organization_id/tasks HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
Content-Type: application/json
{
    "title": "string",
    "description": "string",
    "tags": ["tag1", "tag2", "tag3"],
    "participant_number_limit": 10,
    "reward_for_one_participant": 0,
    "post_time": "date_obj",
    "receive_end_time": "date_obj",
    "finish_deadline_time": "date_obj",
    "user_limit": {
        "age_upper": 0,
        "age_lower": 1,
        "grades": ["grade1", "grade1"],
        "sexes": ["sex_type1", "sex_type2", "sex_type3"],
        "schools": ["school_name1", "school_name2"]
    },
    "steps": [
        {
            "title": "string",
            "description": "string"
        },
        {
            "title": "string",
            "description": "string"
        }
    ]
}
```
```json
//response: create task successfully, show created task
HTTP/1.1 201 Created
// NOTE would be better if return a list of users' name/nickname to avoid N+1 
// NOTE if create by person, OMIT creator_organization_name problem 
{
    "task_id": 123,
    "creator_user_id": 123,
    "creator_organization_id": 123,
    "status": "ongoing",
    "title": "string",
    "description": "string",
    "tags": ["tag1", "tag2", "tag3"],
    "participant_number_limit": 10,
    "reward_for_one_participant": 0,
    "post_time": "date_obj",
    "receive_end_time": "date_obj",
    "finish_deadline_time": "date_obj",
    "user_limit": {
        "age_upper": 0,
        "age_lower": 1,
        "grades": ["grade1", "grade1"],
        "sexes": ["sex_type1", "sex_type2", "sex_type3"],
        "schools": ["school_name1", "school_name2"]
    },
    "steps": [
        {
            "title": "string",
            "description": "string"
        },
        {
            "title": "string",
            "description": "string"
        }
    ],
    "participant_ids": [123, 124, 125, 126],
    "ongoing_participant_ids": [123, 124],
    "waiting_examine_participant_ids": [125],
    "finished_participant_ids": [126]
}

// NOTE if some necessary thing missing, return 400
// TODO

//response: no this user/organization in users/organizations
HTTP/1.1 404 Not Found
Content-Type: application/json
{
    "error_code": 404,
    "error_msg": "user/organization Not Found"
}
```

#### 用户/组织查询自己创建的任务

```json
//request: get user created tasks 
GET /users/:user_id/tasks HTTP/1.1
//or request: get organization created tasks 
GET /users/:user_id/organization/:organization_id/tasks HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
```

```json
//response: almost the same as 201 in 用户/组织创建任务,
//but may be more information. TODO
```

#### 任务查询

```json
//request: user query tasks
GET /users/:user_id/tasks HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
Content-Type: application/json
{
    "creator_user_email": "i@sirius.com",
    "creator_user_phone_number": "13123456789",
    "creator_organization_name": "name",
    "status": "ongoing",
    "title": "sub_string",
    "tags": ["tag1", "tag2", "tag3"],
    "reward_for_one_participant_upper": 3,
    "reward_for_one_participant_lower": 1,
    "receive_end_time": "date_obj",
    "finish_deadline_time": "date_obj",
    "user_limit": {
        "age_upper": 0,
        "age_lower": 1,
        "grades": ["grade1", "grade1"],
        "sexes": ["sex_type1", "sex_type2", "sex_type3"],
        "schools": ["school_name1", "school_name2"]
    },
    "steps_number_upper": 5,
    "steps_number_lower": 1
}
// NOTE if user do not set a particular value of some key, 
// just OMIT the entire key-value pair, and send the rest.
// Let us see some examples.
// Example 1: query tasks from a org without any limits.
{
    "creator_organization_name": "name"
} 
// should return all tasks created by org with name:"name"  
// AND satisfied user limit of /users/:user_id

// Example 2: query tasks for girls(even if you are a boy(ew~))
{
    "user_limit": {
        "sexes": ["female"]
    } 
}
// should return all tasks with user_limit:sexes:girl
// THAT'S SAY, if query json contain "user_limit", 
// it will OVERRIDE user_limit inherit from /users/:user_id

// Example 3: query task with no more than 3 steps
{
    "steps_number_upper": 3
}
// should return all tasks with tasks:len(tasks)<=3
// THAT'S SAY, all bound(upper/lower) is INCLUDE,
// if only one bound is set, the return will be [-INF, bound] or [bound, +INF]
```

```json
//response: show all queried tasks. 
// NOTE only show some of the json, not all of them.
HTTP/1.1 200 OK
Content-Type: application/json
{
    "tasks":[
        {
            "task_id": 123456,
            "creator_user_email": "i@sirius.com",
            "creator_user_phone_number": "13123456789",
            "creator_organization_name": "name",
            "status": "ongoing",
            "title": "string",
            "description": "string",
            "tags": ["tag1", "tag2", "tag3"],
            "current_participant_number": 3,
            "participant_number_limit": 10,
            "reward_for_one_participant": 2,
            "post_time": "date_obj",
            "receive_end_time": "date_obj",
            "finish_deadline_time": "date_obj",
            "user_limit": {
                "age_upper": 0,
                "age_lower": 1,
                "grades": ["grade1", "grade1"],
                "sexes": ["sex_type1", "sex_type2", "sex_type3"],
                "schools": ["school_name1", "school_name2"]
            },
            "steps": [
                {
                    "title": "string",
                    "description": "string"
                },
                {
                    "title": "string",
                    "description": "string"
                }
            ]
        },
    ]
}
```
#### 任务接受
```json
//request: user accepting task 
POST /users/:user_id/tasks/:task_id HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
```
```json
//response: accept task successfully, show updated task
HTTP/1.1 201 Created
//TODO return a updated task info
```

#### 任务完成
```json
//request: user finishing a step of task 
PUT /users/:user_id/tasks/:task_id/steps/:step_id HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
```
```json
//response: finish step successfully, show updated task
HTTP/1.1 200 OK
//TODO return a updated task info
```

#### 任务审核
```json
//request: user finishing a step of task 
PUT /users/:user_id/tasks/:task_id/finishers/:user_id HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
```
```json
//response: task finish accepted successfully
HTTP/1.1 200 OK
//TODO should return a new doing-er, done-er, finished-er list
```

#### 撤回任务
```json
//request: user change task status into pending
//NOTE only for ongoing tasks 
PUT /users/:user_id/tasks/:task_id HTTP/1.1
//or request: organization creating task 
PUT /users/:user_id/organization/:organization_id/tasks/:task_id HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
Content-Type: application/json
{
    "status": "pending"
}
```

#### 修改未发布任务
```json
//request: user editing task
//NOTE only for not published(waiting/pending) tasks 
PUT /users/:user_id/tasks/:task_id HTTP/1.1
//or request: organization creating task 
PUT /users/:user_id/organization/:organization_id/tasks/:task_id HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
Content-Type: application/json
//TODO the same json as create task
```

#### 组织/个人删除任务

```json
//request: delete tasks
DELETE /users/:user_id/tasks/:task_id HTTP/1.1
DELETE /users/:user_id/organization/:organization_id/tasks/:task_id HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
```
```json
//TODO
```