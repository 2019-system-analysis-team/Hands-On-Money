下载postman

测试

User登录功能

Postman使用

使用Postman，选择GET/POST -> 输入api -> 选择Body -> form-data -> 填写KEY和VALUE->然后点击Send往下拉可以看到respond



![image-20190408141730696](/Users/a10.11.5/Library/Application Support/typora-user-images/image-20190408141730696.png)

查看返回的内容

![image-20190408141748972](/Users/a10.11.5/Library/Application Support/typora-user-images/image-20190408141748972.png)

(现在先考虑一般的情况，之后再考虑Robustness)

用户

- [ ] 注册（只需要基本信息）/users/register_test    POST
- [ ] 登录（目前是username+password)  /users/login    GET
- [ ] 修改信息    /users/modify_profile_test    POST
- [ ] 用户查找（目前是根据用户名查找，会列出username，bios和发布的任务名）   /users/search_user    GET
- [ ] 



任务

- [ ] 创建任务（暂时使用user_id索引用户）    /task/create_test    POST



![image-20190408144503511](/Users/a10.11.5/Library/Application Support/typora-user-images/image-20190408144503511.png)

user可以通过外键refer到user的task表

```python
>>> python
>>> from moneyapp import db
>>> from moneyapp.models import User
>>> from moneyapp.models import Task
>>> user = User.query.filter_by(username='popiko').first()
<User 2>
>>> user.username
'popiko'
>>> user.email
'popiko@email.com'
>>> user.tasks
<sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x11072c048>
>>> task = user.tasks.first()
>>> task
<Task 1>
>>> task.title
'help popiko fetch deliver'
```

输出user的所有task的title

```python
>>> tasks = user.tasks
>>> for task in tasks:
...     print(task.title)
... 
help popiko fetch deliver
help popiko fetch deliver2
help popiko fetch deliver3
```



测试search user

![image-20190408153442119](/Users/a10.11.5/Library/Application Support/typora-user-images/image-20190408153442119.png)



弄一张接收任务表和发布任务表 ？？？

<https://www.cnblogs.com/shamo89/p/8994055.html>

how to define composite primary key

<https://stackoverflow.com/questions/19129289/how-to-define-composite-primary-key-in-sqlalchemy>

![image-20190408155312878](/Users/a10.11.5/Library/Application Support/typora-user-images/image-20190408155312878.png)

采用中间表

```python
>>> tasks = user.tasks
>>> tasks
<sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x11074be48>
>>> tasks[0]
<Task 1>
>>> tasks[0].user
<User 2>
>>> tasks[0].user.username
```



（1）新建用户

创建popiko和popiko2

![image-20190408163745347](/Users/a10.11.5/Library/Application Support/typora-user-images/image-20190408163745347.png)

![image-20190408163806666](/Users/a10.11.5/Library/Application Support/typora-user-images/image-20190408163806666.png)



（2）创建任务

popiko创建任务task1

![image-20190408164315642](/Users/a10.11.5/Library/Application Support/typora-user-images/image-20190408164315642.png)

```python
>>> user_popiko = User.query.filter_by(username='popiko').first()
>>> user_popiko.username
'popiko'
>>> user_popiko.tasks
<sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x103557ef0>
>>> user_popiko.tasks[0]
<Task 1>
>>> user_popiko.tasks[0].title
'help popiko fetch deliver1'
>>> 
```

使用user.tasks可以获取到该user创建的任务

```python
>>> task.user
<User 1>
>>> task.received_tasks[0].user
<User 2>
```

如果要从task获取创建者，只需要task.user

但是如果要从task获取接受者，则还需要通过中间表Receiver_Task，然后获取到user



popko创建task2

![image-20190408170942338](/Users/a10.11.5/Library/Application Support/typora-user-images/image-20190408170942338.png)

（3）接收任务

popiko2接收popiko创建的任务1（暂时还没设置发布者不能接收自己发布的任务）

![image-20190408164559986](/Users/a10.11.5/Library/Application Support/typora-user-images/image-20190408164559986.png)

![image-20190408164811656](/Users/a10.11.5/Library/Application Support/typora-user-images/image-20190408164811656.png)

```python
>>> from moneyapp.models import User
>>> from moneyapp.models import Task
>>> from moneyapp.models import Organization
>>> from moneyapp.models import Receiver_Task
>>> record = Receiver_Task.query.first()
>>> record
<Receiver_Task 2, 1>
>>> record.user
<User 2>
>>> record.task
<Task 1>
>>> record.task.title
'help popiko fetch deliver1'
>>> record.user.username
'popiko2'
>>> user = User.query.filter_by(username='popiko2').first()
>>> user
<User 2>
>>> user.tasks
<sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x103557da0>
>>> user.received_tasks
<sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x10356e898>
>>> user.received_tasks[0]
<Receiver_Task 2, 1>
```

使用user.received_tasks可以获取到自己接收的任务



popiko2接收popko创建的任务2

![image-20190408171116953](/Users/a10.11.5/Library/Application Support/typora-user-images/image-20190408171116953.png)



![image-20190408171223404](/Users/a10.11.5/Library/Application Support/typora-user-images/image-20190408171223404.png)

```python
>>> user = User.query.filter_by(username='popiko').first()
>>> user
<User 1>
>>> user.username
'popiko'
>>> user.tasks
<sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x1034e6b38>
>>> tasks = user.tasks
>>> for task in tasks:
...   print(task.title)
... 
help popiko fetch deliver1
help popiko fetch deliver2
```

```python
>>> user2 = User.query.filter_by(username='popiko2').first()
>>> user2.received_tasks
<sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x10353e860>
>>> received_tasks = user2.received_tasks
>>> for received_task in received_tasks:
...   task_name = received_task.task.title
...   print(task_name)
... 
help popiko fetch deliver1
help popiko fetch deliver2
```



