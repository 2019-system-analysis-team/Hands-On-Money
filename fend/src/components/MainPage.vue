<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark">
                    <div class="layout-logo"></div>
                    <div class="layout-nav" v-if="!isLogin">
                        <MenuItem name="1">
                            <Icon type="ios-navigate"></Icon>
                            项目 1
                        </MenuItem>
                        <MenuItem name="2" to="/userinfomodify">
                            <Icon type="ios-keypad"></Icon>
                            项目 2
                        </MenuItem>
						<Submenu name="3">
							<template slot="title">
								<Icon type="ios-stats" />
								项目 3
							</template>
							<MenuGroup title="使用">
								<MenuItem name="3-1">子项目1</MenuItem>
								<MenuItem name="3-2">子项目2</MenuItem>
								<MenuItem name="3-3">子项目3</MenuItem>
							</MenuGroup>
							<MenuGroup title="留存">
								<MenuItem name="3-4">子项目4</MenuItem>
								<MenuItem name="3-5">子项目5</MenuItem>
							</MenuGroup>
						</Submenu>
                    </div>
                    <div class="layout-nav" v-if="isLogin">
						<MenuItem name="5">
							<Tooltip content="创建一个新任务">
								<Icon type="md-add-circle" size="45" color="#eee"/>
							</Tooltip>
						</MenuItem>
						<Submenu name="1">
							 <template slot="title">
								<Icon type="ios-ionic"></Icon>
								任务
							 </template>
							<MenuItem name="1-1">我的任务</MenuItem>
							<MenuItem name="1-2">新建任务</MenuItem>
							<MenuItem name="1-3">所有任务</MenuItem>
                        </Submenu>
                        <Submenu name="2">
							<template slot="title">
								<Icon type="ios-contacts"></Icon>
								组织
							</template>
							<MenuItem name="2-1" to="/organization">我的组织</MenuItem>
							<MenuItem name="2-2" to="/organregister">新建组织</MenuItem>
                        </Submenu>
						<Submenu name="3">
							<template slot="title">
								<Icon type="ios-card" />
								钱包
							</template>
							<MenuItem name="3-1" @click.native="GotoTopup()">充值</MenuItem>
							<MenuItem name="3-2">提现</MenuItem>
							<MenuItem name="3-3">账户余额 : {{money}}</MenuItem>
						</Submenu>
                    </div>
					<div class="layout-button" v-if="!isLogin">
						<Button type="default" ghost onclick="document.getElementById('loginFrame').style.display='block';
			document.getElementById('bgColorDiv').style.display='block'">登录</Button>
						<Button type="primary" ghost v-on:click="register">注册</Button>
					</div>
					<div class="layout-button" v-if="isLogin">
						<Submenu name="4">
							<template slot="title">
								<Avatar :src="profilePhotoPath" style="background-color: #87d068"></Avatar>
							</template>
							<MenuItem name="4-1" to="/userinfomodify">个人信息</MenuItem>
							<MenuItem name="4-2" @click.native="logout()">退出</MenuItem>
						</Submenu>
						<Badge :count="messagesNumber" overflow-count="99">
							<a class="demo-badge" v-on:click="showMessage"> 
								<Icon type="md-notifications-outline" size="26" color="#eee"></Icon>
							</a>
						</Badge>
					</div>
                </Menu>
            </Header>
			<Content :style="{padding: '50px 50px'}" v-if="!isLogin">
				<Card>
                    <div style="min-height: 400px;">
                        Content
                    </div>
                </Card>
			</Content>			
            <Content :style="{padding: '50px 50px'}" v-if="isLogin">
				<Row v-if="haveTask">
					<Col span="11" style="margin-left: 30px;">
						<Card>
							<p slot="title">已发布的任务</p>
							<p>							
								<div style="min-height: 300px;">
									<p>Content of card</p>
									<p>Content of card</p>
									<p>Content of card</p>
								</div>
							</p>
						</Card>
					</Col>
					<Col span="11" style="margin-left: 30px;">
						<Card>
							<p slot="title">已接取的任务</p>
							<p>							
								<div style="min-height: 300px;">
									<p>Content of card</p>
									<p>Content of card</p>
									<p>Content of card</p>
								</div>
							</p>
						</Card>
					</Col>
				</Row>
				<Row v-if="!haveTask" style="margin-left: 30px;">
					<Col span="23">
						<Card>
							<p slot="title">开始创建一个新任务吧</p>
							<p>							
								<div style="min-height: 300px;text-align:center;">
									<Button type="primary" ghost shape="circle" icon="md-add" style="width: 30%;height: 63px;margin-top: 8%;">新建任务</Button>
								</div>
							</p>
						</Card>
					</Col>
				</Row>
				<Row style="margin-top: 30px; margin-left: 30px;">
					<Col span="23">
						<Card>
							<p slot="title">任务推荐</p>
							<p>							
								<div style="min-height: 300px;">
									<p>Content of card</p>
									<p>Content of card</p>
									<p>Content of card</p>
								</div>
							</p>
						</Card>
					</Col>
				</Row>
            </Content>
            <Footer class="layout-footer-center">2019-2019 &copy; SYSU</Footer>
        </Layout>
		<Drawer
			title="充值"
			v-model="topup"
			width="400"
			:mask-closable="true"
			:styles="styles"
		>
			<Form :model="topupData">
					<FormItem label="充值金额 : " label-position="top">
					<InputNumber
								:max="10000"
								:min="1"
								 v-model="topupData.value"
								></InputNumber>
					</FormItem>
					<FormItem label="支付方式" label-position="top">
						<Select v-model="topupData.mode">
							<Option value="支付宝">支付宝</Option>
							<Option value="微信支付">微信支付</Option>
							<Option value="信用卡">信用卡</Option>
						</Select>
					</FormItem>
				</Row>
			</Form>
			<div class="demo-drawer-footer">
				<Button style="margin-right: 8px" @click="topup = false">取消</Button>
				<Button type="primary" v-on:click="recharge">充值</Button>
			</div>
		</Drawer>
			
        <div id="bgColorDiv" class="black_overlay">
			<div id="loginFrame" class="white_content">
				<form class="form-horizontal">
					<span class="heading">用户登录</span>
					<div class="form-group">
<<<<<<< HEAD
						<input type="text" class="form-control" v-model = "inputName" placeholder="email">
						<i class="fa fa-user"></i>
					</div>
					<div class="form-group help">
						<input type="password" class="form-control" v-model="inputPassword" placeholder="password">
=======
						<input type="text" class="form-control" id="inputName" placeholder="username">
						<i class="fa fa-user"></i>
					</div>
					<div class="form-group help">
						<input type="password" class="form-control" id="inputPassword" placeholder="password">
>>>>>>> a8843b327cd27c9a0a8d7063bd8a1a847ca429b9
						<i class="fa fa-lock"></i>
						<a href="#" class="fa fa-question-circle"></a>
					</div>
					<div class="form-group">
						<button type="button" class="btn btn-default" @click="clickCancel">取消</button>
						<button  type="button" class="btn btn-default" @click="clickLogin">登录</button>
					</div>
				</form>
			</div>
		</div>

    </div>
</template>
<script>
    export default {
		data() {
			return { 
				userID: '',
				isLogin: false,
				profilePhotoPath: '',
				money: 0,
				topupData: {
				    value: 1,
					mode: '支付宝',
				},
				topup: false,
                styles: {
                    height: 'calc(100% - 55px)',
                    overflow: 'auto',
                    paddingBottom: '53px',
                    position: 'static'
                },
				messagesNumber:100,
				haveTask: false,
				inputName: '',
				inputPassword: '',
			};
		}, 
		created: function () { 
			//在created阶段初始化
			this.getEventData();
		},
		methods: {
			getEventData:function() {
				var _this = this;
				let uID = window.localStorage.getItem('userID')
				if(uID == null || uID == ""){
					this.isLogin = false;
					return;
				}
				var url = "/users/" + uID;
				this.$data.userID = uID;
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$axios({
						 method:"get",
						 url:url,
						 headers:{
							'Authorization': jwt,
						 }
				}).then(function (response){
					console.log(response);
					_this.isLogin = true;
					_this.profilePhotoPath = _this.$profilePath + response.data.profile_photo_path;					

				}).catch(function (error) {
					console.log(error.response.status);
					_this.isLogin = false;
				});
			},
			register: function () {
				this.$router.push({
						path: '/userregister'
				});		
			},
			logout (){
				var _this = this;
				if(this.isLogin){
					var url_all = "/users/" + this.$data.userID + "/session";
					var jwt = "JWT " + window.localStorage.getItem('token');
					this.$axios({
						 method:"delete",
						 url: url_all,
						 headers:{
							'Authorization': jwt,
						 }
					}).then(function (response){
						_this.isLogin = false;
						_this.userID = '';
						window.localStorage.removeItem('token');
						window.localStorage.removeItem('userID');
					}).catch(function (error) {
						console.log(error);
					});
				}
			},
			GotoTopup (){
				this.topup = true;
			},
			recharge(){
				this.$Message.success('充值成功!');
				this.money = this.topupData.value + this.money;
				this.topup = false;
			},
			showMessage(){
				this.messagesNumber = 0;
			},
			displayLogin() {
				document.getElementById('loginFrame').style.display='block';
				document.getElementById('bgColorDiv').style.display='block';
			},
			clickLogin() {
<<<<<<< HEAD
				var _this = this;

				if(this.inputName == "" || this.inputPassword == "") {
					alert("请输入邮箱和密码");
				}
				else {
					document.getElementById('bgColorDiv').style.display='none';
					console.log(this.inputName + " + " + this.inputPassword);
					this.$axios({
						 method:"post",
						 url:"/sessions",
						 data:{
							email: this.inputName,
							password: this.inputPassword,
						 }
						}).then(function (response){
							console.log(response);
							window.localStorage.setItem('token', response.data.access_token);
							window.localStorage.setItem('userID', response.data.user_id);
							
							//跳转到主页
							_this.$router.push({
								path: '/', 
								name: 'mainpage'
							});
						})
						.catch(function (error) {
							console.log(error.response.status);
							if(error.response.status == 404){
								_this.$Message.error('用户不存在或者密码错误');
							}
							_this.inputName = '';
							_this.inputPassword = '';

						});
=======
				var nameData = document.getElementById("inputName").value;
				var passwordData = document.getElementById("inputPassword").value;
				if(nameData == "" || passwordData == "") {
					alert("请输入用户名和密码");
				}
				else {
					document.getElementById('bgColorDiv').style.display='none';
					var nameData = document.getElementById("inputName").value;
					localStorage.setItem("nameData", nameData);
					var passwordData = document.getElementById("inputPassword").value;
					localStorage.setItem("passwordData", passwordData);
>>>>>>> a8843b327cd27c9a0a8d7063bd8a1a847ca429b9
				}
			},
			clickCancel() {
				document.getElementById('bgColorDiv').style.display='none';
<<<<<<< HEAD
				this.inputName = '';
				this.inputPassword = '';
=======
				var storage = window.localStorage;  
				var name = storage["nameData"];  
				var password = storage["passwordData"];
				console.log(name + " " + password);
>>>>>>> a8843b327cd27c9a0a8d7063bd8a1a847ca429b9
			}
		}
    }
</script>
<style scoped>
.layout{
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
}
.layout-logo{
    width: 100px;
    height: 30px;
    background: #5b6270;
    border-radius: 3px;
    float: left;
    position: relative;
    top: 15px;
    left: 20px;
}
.layout-nav{
    width: 600px;
    margin: 0 auto;
    margin-right: 0px;
}
.layout-button{
    width: 200px;
    margin: 0 auto;
	margin-right: 0px;
}
.layout-footer-center{
    text-align: center;
}
.ivu-layout-header{
    padding-right: 25px;
}
.demo-drawer-footer{
	width: 100%;
	position: absolute;
	bottom: 50%;
	left: 0;
	border-top: 1px solid #e8e8e8;
	padding: 10px 16px;
	text-align: right;
	background: #fff;
}
.demo-badge{
	width: 30px;
	height: 30px;
	background: #515a6e;
	border-radius: 6px;
	display: inline-block;
}
.ivu-badge{
	margin-top: 15px;
}
.ivu-icon-md-notifications-outline{
	margin-bottom: 30px;
}
.black_overlay {
	display: none;
	position: absolute;
	top: 0%;
	left: 0%;
	width: 100%;
	height: 100%;
	/*background-color: black;*/
	/*-moz-opacity: 0.8;*/
	background: rgba(0,0,0,0.8);
	z-index: 1001;
	opacity: .80;
	filter: alpha(opacity=80);
}
.white_content {
	border-radius: 20px;
	display: none;
	position: absolute;
	top: 20%;
	left: 30%;
	width: 40%;
	height: 370px;
	padding: 16px;
	//border: 3px solid orange;
	background-color: white;
	z-index: 1002;
	overflow: auto;
}
.form-bg{
	padding: 2em 0;
}
.form-horizontal{
	background: #fff;
	padding-bottom: 40px;
	border-radius: 15px;
	text-align: center;
}
.form-horizontal .heading{
	display: block;
	font-size: 35px;
	font-weight: 700;
	padding: 20px 0;
	border-bottom: 1px solid #f0f0f0;
	margin-bottom: 40px;
}
.form-horizontal .form-group{
	padding: 0 40px;
	margin: 0 0 25px 0;
	position: relative;
}
.form-horizontal .form-control{
	font-size: 15px;
	background: #f0f0f0;
	border: none;
	border-radius: 20px;
	box-shadow: none;
	padding: 0 40px 0 15px;
	height: 40px;
	transition: all 0.3s ease 0s;
}
.form-horizontal .form-control:focus{
	background: #e0e0e0;
	box-shadow: none;
	outline: 0 none;
}
.form-horizontal .form-group i{
	position: absolute;
	top: 12px;
	left: 60px;
	font-size: 17px;
	color: #c8c8c8;
	transition : all 0.5s ease 0s;
}
.form-horizontal .form-control:focus + i{
	color: #00b4ef;
}
.form-horizontal .fa-question-circle{
	display: inline-block;
	position: absolute;
	top: 12px;
	right: 60px;
	font-size: 20px;
	color: #808080;
	transition: all 0.5s ease 0s;
}
.form-horizontal .fa-question-circle:hover{
	color: #000;
}
.form-horizontal .main-checkbox{
	float: left;
	left: 20px;
	width: 20px;
	height: 20px;
	background: #11a3fc;
	border-radius: 50%;
	position: relative;
	margin: 12px 0 0 5px;
	border: 1px solid #11a3fc;
}
.form-horizontal .main-checkbox label{
	width: 20px;
	height: 20px;
	position: absolute;
	top: 0;
	left: 0;
	cursor: pointer;
}
.form-horizontal .main-checkbox label:after{
	content: "";
	width: 10px;
	height: 5px;
	position: absolute;
	top: 5px;
	left: 4px;
	border: 3px solid #fff;
	border-top: none;
	border-right: none;
	background: transparent;
	opacity: 0;
	-webkit-transform: rotate(-45deg);
	transform: rotate(-45deg);
}
.form-horizontal .main-checkbox input[type=checkbox]{
	visibility: hidden;
}
.form-horizontal .main-checkbox input[type=checkbox]:checked + label:after{
	opacity: 1;
}
.form-horizontal .text{
	float: left;
	margin-top: 7px;
	margin-left: 25px;
	line-height: 20px;
	padding-top: 5px;
	text-transform: capitalize;
}
.form-horizontal .btn{
	float: right;
	font-size: 14px;
	color: #fff;
	background: #00b4ef;
	border-radius: 30px;
	padding: 10px 25px;
	margin-left: 10px;
	border: none;
	text-transform: capitalize;
	transition: all 0.5s ease 0s;
}
@media only screen and (max-width: 479px){
	.form-horizontal .form-group{
		padding: 0 25px;
	}
	.form-horizontal .form-group i{
		left: 45px;
	}
	.form-horizontal .btn{
		padding: 10px 20px;
	}
}
</style>