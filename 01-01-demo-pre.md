# DEMO 展示

在这一部分，我们将展示我们实现的所有用例。主要分为如下几个部分：

- [DEMO 展示](#DEMO-%E5%B1%95%E7%A4%BA)
  - [首页](#%E9%A6%96%E9%A1%B5)
  - [用户系统](#%E7%94%A8%E6%88%B7%E7%B3%BB%E7%BB%9F)
    - [注册](#%E6%B3%A8%E5%86%8C)
    - [界面](#%E7%95%8C%E9%9D%A2)
    - [个人信息](#%E4%B8%AA%E4%BA%BA%E4%BF%A1%E6%81%AF)
  - [组织管理系统](#%E7%BB%84%E7%BB%87%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F)
    - [新建](#%E6%96%B0%E5%BB%BA)
    - [详情](#%E8%AF%A6%E6%83%85)
    - [删除](#%E5%88%A0%E9%99%A4)
    - [成员管理](#%E6%88%90%E5%91%98%E7%AE%A1%E7%90%86)
    - [权限管理](#%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86)

## 首页

首页展示了项目的 LOGO，项目功能简介，以及组员名称。通过页面最上端的导航栏，用户可以前往我们的 Github 源代码页面、项目博客，以及进行本系统的注册和登陆。

<img src="https://s2.ax1x.com/2019/06/24/ZkX7xs.png" alt="ZkX7xs.png" border="0">

## 用户系统

本系统提供用户信息管理功能。用户可以通过本系统查看其他用户的信息，并管理自己的信息。

### 注册

点击首页的注册按钮，即可进入注册页面。在该页面中，你需要格式正确地输入包括电话、Email、真实姓名、昵称、学号等个人信息，此外，你还要填写并且确认一个长度符合要求的密码。

<img src="https://s2.ax1x.com/2019/06/24/ZkXT2j.png" alt="ZkXT2j.png" border="0">

如果你填写的信息不符合要求，输入框下方将会出现提示。

<img src="https://s2.ax1x.com/2019/06/24/ZkXIPg.png" alt="ZkXIPg.png" border="0">

正确填写全部信息，即可完成注册。由于用户已经完成了注册，直接进入系统。

<img src="https://s2.ax1x.com/2019/06/24/ZkXoGQ.png" alt="ZkXoGQ.png" border="0">

### 界面

系统的主页面如下图所示。主界面将会显示你当前的全部任务（建立的/接受的）。由于刚注册的用户没有任务，因此存在一个导航到任务市场的连接。这一部分会在 [任务](##任务) 部分详细描述。

<img src="https://s2.ax1x.com/2019/06/24/ZkjpRJ.png" alt="ZkjpRJ.png" border="0">

系统界面的导航栏分为五个部分，分别是任务，组织，钱包，个人信息，以及提示。当鼠标指针指向时，其子功能会扩展弹出。我们会在接下来的部分逐一说明他们的功能。

<img src="https://s2.ax1x.com/2019/06/24/ZkXbMn.png" alt="ZkXbMn.png" border="0">

### 个人信息

在导航栏中指向头像，点击弹出的个人信息选项卡，即可进入个人信息界面。在这个界面中，你可以查看并修改你的个人信息。包括你的学校信息，详情、头像以及密码。

在个人信息栏中，你会看到你的任务完成综合评分。这是由任务完成者对你的打分的平均值决定的。这一部分将在 [评价](##评价) 中详细说明。

<img src="https://s2.ax1x.com/2019/06/24/ZkjSG4.png" alt="ZkjSG4.png" border="0">

为了修改密码，你需要同时输入旧密码确认，并上传你的新密码。

<img src="https://s2.ax1x.com/2019/06/24/ZkXjaT.png" alt="ZkXjaT.png" border="0">

点击头像右侧的符号，可以通过上传图片修改头像。修改前后的效果如下两图所示。

<img src="https://s2.ax1x.com/2019/06/24/ZkXXZV.png" alt="ZkXXZV.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkXziF.png" alt="ZkXziF.png" border="0" />

## 组织管理系统

### 新建

在导航栏中指向组织，点击弹出的我的组织选项卡，即可进入组织管理界面。如果当前没有加入组织，可以自己新建一个组织。新建组织，请点击新建组织选项卡。输入组织名称和描述即可建立新的组织。

<img src="https://s2.ax1x.com/2019/06/24/Zkjis1.png" alt="Zkjis1.png" border="0">

### 详情

在详情页面，我们可以看到组织发布的任务，组织的信息，成员管理以及删除组织。与用户类似，组织的也具有详情页面和平均评价。Owner 和 Admin 可以修改组织的详情。任务可以以组织的名义发布，点击右侧新建组织任务。

<img src="https://s2.ax1x.com/2019/06/24/ZkjeiD.png" alt="ZkjeiD.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjMQA.png" alt="ZkjMQA.png" border="0">

### 删除

仅有 owner 具有删除组织的权限。输入组织的全名，点击删除即可。

<img src="https://s2.ax1x.com/2019/06/24/ZkjFqx.png" alt="ZkjFqx.png" border="0">

### 成员管理

你需要通过邮箱或者电话来添加组织成员。在添加成员时，仅能赋予成员低于你的权限，而不能赋予相同或者更高的权限。输入正确的信息，添加成员。

<img src="https://s2.ax1x.com/2019/06/24/Zkj9z9.png" alt="Zkj9z9.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjVIO.png" alt="ZkjVIO.png" border="0">

### 权限管理

也可以修改比你权限更低的组织成员的权限。Admin 具有添加和删除成员的权限和创建组织任务的权限，而 member 仅能审核组织任务。

<img src="https://s2.ax1x.com/2019/06/24/ZkjEdK.png" alt="ZkjEdK.png" border="0">



<img src="https://s2.ax1x.com/2019/06/24/Zkj3eP.png" alt="Zkj3eP.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/Zkjwyn.png" alt="Zkjwyn.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjtJg.png" alt="ZkjtJg.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjNWQ.png" alt="ZkjNWQ.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjDe0.png" alt="ZkjDe0.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjrwV.png" alt="ZkjrwV.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjhO1.png" alt="ZkjhO1.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/Zkj0Lq.png" alt="Zkj0Lq.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/Zkj6FU.png" alt="Zkj6FU.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjsoT.png" alt="ZkjsoT.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjRSJ.png" alt="ZkjRSJ.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjgW4.png" alt="ZkjgW4.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjcYF.png" alt="ZkjcYF.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjfyR.png" alt="ZkjfyR.png" border="0">

<img src="https://s2.ax1x.com/2019/06/24/ZkjYFS.png" alt="ZkjYFS.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjGo8.png" alt="ZkjGo8.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/Zkj8df.png" alt="Zkj8df.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjQsI.png" alt="ZkjQsI.png" border="0">
<img src="https://s2.ax1x.com/2019/06/24/ZkjWl9.png" alt="ZkjWl9.png" border="0">