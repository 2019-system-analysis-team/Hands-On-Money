# 使用 flaskJWT 轻松实现 flask 后端与鉴权层分离的架构

JSON Web Tokens (or JWTs) 提供了一种从客户端到服务端传递信息的方法。

在服务端，JWTs 是由登陆用户的信息加预设密钥产生的一串字符，并被保存在客户端上。这种加密方式可以很好地运用在现在的单页应用上。如果你们像了解更多的认证方式，大可以参考以下博客：

- [到底使用 cookie 还是 token 呢？](https://auth0.com/blog/cookies-vs-tokens-definitive-guide/)
- [Token 验证方式与 cookie 之间的对比](http://stackoverflow.com/questions/17000835/token-authentication-vs-cookies)
- [session 在 flask 中是如何运作的](https://www.reddit.com/r/flask/comments/5l2gmf/af_eli5_how_sessions_work_in_flask/)

Flask 是 python 下一个轻量、易学的 Web 后端架构，但是由于其轻量的特性，我们在使用它的时候，发现自己手工实现的鉴权模块难以像其他模块一样区分开来，换言之，鉴权模块的耦合度在我们的架构中过分高了。因此，经过一番查找，我们找到了 FlaskJWT 模块。借由这个模块，我们能够轻松地将鉴权和其他模块区分开来，真正的实现“低内聚，高耦合”的梦想架构。

说的够多了，坑也够多了，不如来看看我为你们准备的最简单的示例代码。

## 安装

如同所有 python 模块，你只需要一行简单的命令就可以实现这个过程：
```
pip install Flask-JWT
```
当然，前提是你得装好 Flask 本体。由于这不是一个 Flask 教程（如果想看的话也可以在 issue 里面催我写），我就不赘述了。

## 路由模块

在这个模块里面，我们将实现一个最简单的 Flask 路由功能。

```py
# in route.py

from flask import Flask
app = Flask(__name__)
app.debug = True

@app.route('/open')
def open():
    return 'hello, world!'

@app.route('/protected')
def open():
    return 'top secret!'

if __name__ == '__main__':
    app.run()
```

十分简单：我们在这个模块里面写入了一个路由，当我们访问 `http://localhost:5000/open` 的时候，就会得到一个 `hello, world!` 字符串的返回。

```
GET /open HTTP/1.1
`hello, world!`
```

然而，我们的服务器上存储着一些不为人知秘密，只有指定的用户才能通过访问 `http://localhost:5000/protected` 获取到这些秘密。可惜，像我们这样写的话，所有用户就都知道我们的秘密了！IT WAS BAD!

```
GET /protected HTTP/1.1
'top secret!'
```

## 增加一点鉴定权限的玩意

我们来写一个新的模块。在这个模块里，我们实现了一个函数，它可以判断用户是不是在我们的指定用户列表里。

```py
# in auth.py

from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'joe', 'password1'),
    User(2, 'bob', 'password2'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)
```

虽然它有点长，但是完全挡不住诸位程序员的目光。

1. 首先，这串代码定义了用户类，它有一个用户名和密码，并且这个用户可以作为字符串打出来；
2. 然后，在 `authenticate(username, password)` 里面，它判断了用户名和密码是否一致；
3. 最后，在 `identity(payload)` 里面，它判断了用户是否存在。

解决了用户名存在性/用户名和密码的一致性之后，我们鉴权的基本任务就已经解决了，现在让我们给路由模块加一点佐料。

## 新的路由模块

佐料不用很多，三行就够了。

```py
# in route.py

from flask import Flask
from auth import * #add line 1
app = Flask(__name__)
app.debug = True
jwt = JWT(app, authenticate, identity) #add line 2
app.config['SECRET_KEY'] = 'super-secret'

@app.route('/open')
def open():
    return 'hello, world!'

@app.route('/protected')
@jwt_required() # #add line 3
def open():
    return 'user %s, top secret!' % current_identity

if __name__ == '__main__':
    app.run()
```

啥？这就好了？没错，这就好了。

- 在 `add line 1` 里面，我们把刚才添加的 `auth.py` 模块全部导入了路由模块中（这不是一个优雅的实践，但是在示例里面无伤大雅）
- 在 `add line 2`，我们实例化了一个 `JWT()` 对象，为我们提供鉴权服务。
- 在 `add line 3`，我们为想要鉴权的路由简单增加一个 `@jwt_required()` 就好了。

现在，如果我们再来直接访问 `http://localhost:5000/protected`

```
GET /protected HTTP/1.1
'error!'
```

很抱歉，你没有通过 `@jwt_required()` 的检验，因此你就会被挡在大门外面。但是，如果我是合法的用户，有用户名和密码的话……

```
POST /auth HTTP/1.1
Content-Type: application/json
{
    "username": "joe",
    "password": "password1"
}
```

那我将得到这么一串（类似的） JWT 字符:

```
HTTP/1.1 200 OK
Content-Type: application/json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNDQ0OTE3NjQwLCJuYmYiOjE0NDQ5MTc2NDAsImV4cCI6MTQ0NDkxNzk0MH0.KPmI6WSjRjlpzecPvs3q_T3cJQvAgJvaQAPtk1abC_E"
}
```

然后再让我们带着这一串字符作为鉴权的“身份识别卡”的话……

```
GET /protected HTTP/1.1
Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNDQ0OTE3NjQwLCJuYmYiOjE0NDQ5MTc2NDAsImV4cCI6MTQ0NDkxNzk0MH0.KPmI6WSjRjlpzecPvs3q_T3cJQvAgJvaQAPtk1abC_E
```

我们离秘密的距离就只有一个 `GET` 啦！

```
'user joe, top secret!'
```

## 更多的思考

在我刚才的例子里，我只举出了一个 `JWT()` 实例的情况。如果我们想要实现更加复杂的权限控制，我们是不是可以实例化更多的 `JWT()` 实例呢？这又是一个有趣的思考和工程实践。

还有，细心的读者可能已经留意到了，懒惰的我在例子中把用户 model 模块一股脑的塞进了 `auth.py` 里面，这是一种很不好的行为！如果这一个好好学习了 OOA/D 的同学，他应该会……