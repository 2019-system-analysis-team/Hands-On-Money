# RESTful API 设计文档

## 标准

- [What is REST](https://restfulapi.net/)
- [A RESTful Tutorial](https://www.restapitutorial.com/)
- [表现层状态转换](https://zh.wikipedia.org/wiki/%E8%A1%A8%E7%8E%B0%E5%B1%82%E7%8A%B6%E6%80%81%E8%BD%AC%E6%8D%A2)
- [理解RESTful架构](http://www.ruanyifeng.com/blog/2011/09/restful.html)

## 参考
- [baoleme API doc](https://baoleme.github.io/API-document/#/)
- [Tiny Hippo 点餐系统API文档](https://rookies-sysu.github.io/Dashboard/07-03-API)
> Remember, they are not restful at all.


- [基于 Token 的身份验证：JSON Web Token JWT](https://ninghao.net/blog/2834)
- [Flask-JWT doc](https://pythonhosted.org/Flask-JWT/)


## 目录

pass

## API

- 数据表结构

![er model db design](https://s2.ax1x.com/2019/04/09/AIKv7V.png)

- 约定
    - 对于每个 request，response 列表的优先级自顶向下递减；
    - `error_msg` 只是我随便写的，你们可以自己改；
    - 对于键值不符合文档要求的 request，一律返回 400 Bad Request
    - 对于不在文档列表中的 request HTTP verb，一律返回 405 Method Not Allowed
```json
//response: Bad Request. This post is SOMEHOW WRONG. e.g. key is not correct, or value contain not-allowed characters (just like attacker)
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

### 用户创建

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
HTTP/1.1 201 Created  //link to /
Content-Type: application/json
{
    "user_id":"123456",
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

### 用户登陆

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
//response: login successfully
HTTP/1.1 200 OK //link to /
Content-Type: application/json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNDQ0OTE3NjQwLCJuYmYiOjE0NDQ5MTc2NDAsImV4cCI6MTQ0NDkxNzk0MH0.KPmI6WSjRjlpzecPvs3q_T3cJQvAgJvaQAPtk1abC_E"
}
//about access_token, see Flask-JWT doc(https://pythonhosted.org/Flask-JWT/) for further information.

//response: login failed, account not found/password incorrect
HTTP/1.1 404 Not Found //link to /
Content-Type: application/json
{
    "error_code": 404,
    "error_msg": "account not found/password incorrect"
}
```

### 用户信息

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
    "age": "",
    "sex": "",
    "grade": "",
    "school": "",
    "bio": "",
    "age": "",
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

### 用户信息修改

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
    "age": "age",
    "sex": "sex"
}

//request: update photo, after update, download photo again
PUT /users/:user_id/profile_photo HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI
Content-Type: application/json
{
    "profile_photo": "image_obj"
}
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
```

