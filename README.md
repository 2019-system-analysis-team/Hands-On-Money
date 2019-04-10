## 需要完成的接口

- [ ] 删除个人任务
- [ ] 组织管理员或者群主删除任务
- [X] 群主删除组织
- [ ] 组织信息的录入和修改
- [X] 个人账户充值
- [ ] 群主把成员设置为管理员
- [ ] 任务搜索
- [ ] 更改状态 (1)任务接收者更改自己的任务完成进度 (2)发布者更改任务总的完成进度
- [ ] 根据名字查找组织

在route.py里面已经写好个框架就填进去就好了

搜索TODO可以看到需要完成的部分

## 测试方法

工具：postman+一个sqlite的可视化工具（比如db browser for sqlite）

（1）写好接口

（2）先把之前的site.db删除，然后运行一下db_create.py

[![AIMsH0.png](https://s2.ax1x.com/2019/04/09/AIMsH0.png)](https://imgchr.com/i/AIMsH0)

（3）打开可视化工具，导入site.db

（4）打开postman，测试接口

选择GET/POST -> 输入api -> 选择Body -> form-data -> 填写KEY和VALUE->然后点击Send往下拉可以看到respond

举个栗子

[![AIMhv9.png](https://s2.ax1x.com/2019/04/09/AIMhv9.png)](https://imgchr.com/i/AIMhv9)



然后看看可视化工具里面任务条目有没有增加

[![AIMID1.png](https://s2.ax1x.com/2019/04/09/AIMID1.png)](https://imgchr.com/i/AIMID1)



## 已经写好的表

user -> 储存用户信息

organization -> 储存组织信息

organization_member  -> 储存组织和用户的信息（表示用户加入组织的记录）

task -> 任务（发布的任务）

receiver_task -> 用户接受任务的记录

transaction -> 代币流动记录

具体的key可以看下面的图

[![AIKv7V.png](https://s2.ax1x.com/2019/04/09/AIKv7V.png)](https://imgchr.com/i/AIKv7V)

## 一些已经实现的接口

- 注册用户：

  /users/register_test

  email

  telephone

  username

  password

- 登录：

  /users/login

  username

  password

- 修改用户信息：

  /users/modify_profile_test

  email

  telephone

  student_id

  realname

  age

  sex

  grade

  school

  bio

  username

  file

- 查找用户信息：

  /users/search_use

  username

- 创建任务(user)：

  /task/create_test

  user_id

  money

  tag

  number

  applicapable_user

  titile

  description

  status

- 创建任务(organization)：

  /task/create_organization

  user_id

  organization_id

  money

  tag

  number

  applicapable_user

  titile

  description

  status

- 接受任务：

  /task/receive_task

  user_id

  task_id

- 创建组织：

  /organizations/create_test

  name

  bio

  file

  user_id

- 群主、管理员增加组织成员：

  /organizations/add_member

  user_id

  organization_id

  status

- 群成员给组织充值

  /organizations/charge

  user_id

  organization_id

  money

## 教程

选择、插入、删除

<http://www.pythondoc.com/flask-sqlalchemy/queries.html> 









