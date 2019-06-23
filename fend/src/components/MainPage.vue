<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark">
                    <div class="layout-nav" v-if="!isLogin">

                        <MenuItem name="2">
                            <Icon type="ios-keypad"></Icon>
                            <a href="https://github.com/2019-system-analysis-team/Hands-On-Money" style="color: #BBBFC7">Github</a>
                        </MenuItem>
						<MenuItem name="3">
						   <Icon type="ios-navigate"></Icon>
							<a href="https://2019-system-analysis-team.github.io/Hands-On-Money/" style="color: #BBBFC7">关于我们</a>
						</MenuItem>
                    </div>
                    <div class="layout-nav" v-if="isLogin">
						<Submenu name="1">
							 <template slot="title">
								<Icon type="ios-ionic"></Icon>
								任务
							 </template>
							<MenuItem name="1-1" to="/mytasks">我的任务</MenuItem>
							<MenuItem name="1-2" @click.native="createNewTask()">新建任务</MenuItem>
							<MenuItem name="1-3" to="/taskmarket">任务市场</MenuItem>
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
							<MenuItem name="3-2" @click.native="WithdrawDeposit()">提现</MenuItem>
							<MenuItem name="3-3">账户余额 : {{money}}</MenuItem>
						</Submenu>
                    </div>
					<div class="layout-button" v-if="!isLogin">
						<Button type="default" ghost onclick="document.getElementById('loginFrame').style.display='block';
			document.getElementById('bgColorDiv').style.display='block'" style=" margin-right:15px;">登录</Button>
						<Button type="primary" ghost v-on:click="register">注册</Button>
					</div>
					<div class="layout-button" v-if="isLogin">
						<Submenu name="4">
							<template slot="title">
								<Avatar :src="profilePhotoPath" style="background-color: #515a6e"></Avatar>
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
			<Content v-if="!isLogin">
				<div class="mainDiv">
					<!-- <div class="leftpart"></div> -->
					<!-- <div class="rightpart"></div> -->
                    <div class="logo"></div>
                </div>
                <div class="secondDiv">
        			<div class="secondSubDiv"></div>
        			<div class="secondTextDiv">
        				<p class="introTitle">项目介绍</p>
        				<p class="introPara">2019挣闲钱系统，致力于便利协调各个用户的生活。通过客户发布任务，其他用户以有偿做任务的方式解决客户日常实际问题，并使任务执行者获得相应报酬。主要实现功能如下：</p><br>
        				<li class="funcPara">客户创建和删除任务</li>
        				<li class="funcPara">用户接受和退出任务</li>
        				<li class="funcPara">客户建立和解散组织</li>
        				<li class="funcPara">任务的查询和修改</li>
        				<li class="funcPara">任务完成度的记录</li>
        			</div>
                </div>
                <div class="thirdDiv">
                	<div class="thirdSubDiv"></div>
                	<div class="thirdTextDiv">
                		<p class="memTitle">组员信息</p>
                		<li class="memPara">项目经理：席睿 吴宇祺</li>
                		<li class="memPara">前端开发：杨芮 王友坤</li>
                		<li class="memPara">后端开发：王雁玲 许倚安 孙肖冉</li>
                	</div>
                </div>
			</Content>		
            <Content :style="{padding: '50px 50px'}" v-if="isLogin">
				<Row v-if="haveTask" >
					<Col span="11" style="margin-left: 30px;">
						<Card style="height: 550px; overflow: auto;">
							<p slot="title">正在进行中</p>
							<p>							
								<div style="min-height: 420px;">
									<Col span="11" v-for="item in inprogressTasks" :key="item.task_id" style="padding-left: 20px; padding-top: 10px;">
										<Card>
											<p slot="title">{{item.task_name}}</p>
											<div slot="extra">
												<Button type="primary" ghost @click="LookTaskInfo(item.task_id)">详情</Button>
											</div>	
											<p>{{item.task_status}}</p>
										</Card>
									</Col>
								</div>
							</p>
						</Card>
					</Col>
					<Col span="11" style="margin-left: 30px;">
						<Card style="height: 550px; overflow: auto;">
							<p slot="title">已完成的任务</p>
							<p>							
								<div style="min-height: 420px;">
									<Col span="11" v-for="item in finishedTasks" :key="item.task_id" style="padding-left: 20px; padding-top: 10px;">
										<Card>
											<p slot="title">{{item.task_name}}</p>
											<div slot="extra">
												<Button type="primary" ghost @click="LookTaskInfo(item.task_id)">详情</Button>
											</div>	
											<p>{{item.task_status}}</p>
										</Card>
									</Col>
								</div>
							</p>
						</Card>
					</Col>
				</Row>
				<Row v-if="!haveTask" style="margin-left: 30px;">
					<Col span="23">
						<Card>
							<p slot="title">还没有任务 快去新建一个任务或接受一个任务吧</p>
							<p>							
								<div style="min-height: 420px;text-align:center;">
									<Button @click="toTaskMarket" type="primary" ghost shape="circle" icon="md-add" style="width: 30%;height: 63px;margin-top: 8%;">任务市场</Button>
								</div>
							</p>
						</Card>
					</Col>
				</Row>
            </Content>
            <Footer class="layout-footer-center">2019-2019 &copy; Hands-On-Money</Footer>
        </Layout>
		<Modal v-model="showTaskInfo">
			<p slot="header" style="text-align:center">
				<Icon type="ios-information-circle"></Icon>
				<span>任务详情</span>
			</p>
			<div>
			<Card dis-hover>
				<p slot="title" class="info">{{showTaskInfomation.title}}</p>
				标签 : <Tag v-for="item in showTaskInfomation.tags" :key="item" :name="item" color="cyan">{{ item }}</Tag>
				<p class="info">任务描述 : {{showTaskInfomation.description}}</p>
				<p class="info">当前参与者人数 : {{showTaskInfomation.current_participant_number}}</p>
				<p class="info">参与者人数上限 : {{showTaskInfomation.participant_number_limit}}</p>
				<p class="info">完成奖励代币 : {{showTaskInfomation.reward_for_one_participant}}</p>
				<p class="info">任务所属组织 : {{showTaskInfomation.creator_organization_name}}</p>
				<p class="info">创建者邮箱 : {{showTaskInfomation.creator_user_email}}</p>
				<p class="info">创建者电话 : {{showTaskInfomation.creator_user_phone_number}}</p>
				<p class="info">任务发布时间 : {{showTaskInfomation.post_time}}</p>
				<p class="info">截止接受任务时间 : {{showTaskInfomation.receive_end_time}}</p>
				<p class="info">最迟完成任务时间 : {{showTaskInfomation.finish_deadline_time}}</p>
				<p class="info" v-show="showTaskInfomation.tags !=  '问卷' ">步骤 : </p>
				<Steps :current="showTaskInfomation.current" v-show="showTaskInfomation.tags !=  '问卷'">
					<Step :title="item.title" v-for="item in showTaskInfomation.steps" :key="item.title">
					</Step>
				</Steps>
			</Card>
			</div>
			<div slot="footer">
				<Button type="text" @click="showTaskCancel">确定</Button>
				<Button type="primary" @click="ToTaskInfo(showTaskInfomation.task_id)">编辑</Button>
			</div>
		</Modal>
		<Drawer
			title="钱包操作"
			v-model="topup"
			width="400"
			:mask-closable="true"
			:styles="styles"
		>
			<Form :model="topupData">
					<FormItem label="充值金额 : " label-position="top" v-show="!isWithdraw">
					<InputNumber
								:max="10000"
								:min="1"
								 v-model="topupData.value"
								></InputNumber>
					</FormItem>
					<FormItem label="提现金额 : " label-position="top" v-show="isWithdraw">
					<InputNumber
								:max="10000"
								:min="1"
								 v-model="topupData.value"
								></InputNumber>
					</FormItem>
					<FormItem label="支付方式" label-position="top" v-show="!isWithdraw">
						<Select v-model="topupData.mode">
							<Option value="支付宝">支付宝</Option>
							<Option value="微信支付">微信支付</Option>
							<Option value="信用卡">信用卡</Option>
						</Select>
					</FormItem>
				</Row>
			</Form>
			<div class="demo-drawer-footer">
				<Button style="margin-right: 8px" @click="topup = false;isWithdraw = false;">取消</Button>
				<Button type="primary" v-on:click="recharge" v-show="!isWithdraw">充值</Button>
				<Button type="primary" v-on:click="withdraw" v-show="isWithdraw">提现</Button>
			</div>
		</Drawer>
			
        <div id="bgColorDiv" class="black_overlay">
			<div id="loginFrame" class="white_content">
				<form class="form-horizontal">
					<span class="heading">用户登录</span>
					<div class="form-group">
						<input type="text" class="form-control" v-model = "inputName" placeholder="email / phone">
						<i class="fa fa-user"></i>
					</div>
					<div class="form-group help">
						<input type="password" class="form-control" v-model="inputPassword" placeholder="password">
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
				showTaskInfo: false,
				showTaskInfomation:{
				},
				userID: '',
				isLogin: true,
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
				messagesNumber:0,
				haveTask: false,
				inputName: '',
				inputPassword: '',
				isWithdraw:false,
				inprogressTasks:[],
				finishedTasks:[],
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
					//console.log(response);
					_this.isLogin = true;
					_this.profilePhotoPath = _this.$profilePath + response.data.profile_photo_path;		
					_this.money = response.data.balance;
					window.localStorage.setItem('money', _this.money);
					window.localStorage.setItem('MyProfilePhotoPath', _this.profilePhotoPath);
						var url = "/users/" + uID + "/received_tasks";
						_this.$axios({
							 method:"get",
							 url:url,
							 headers:{
								'Authorization': jwt,
							 }
						}).then(function (response){
							console.log("获取已接收任务");
							console.log(response);
							var receivedTasks = response.data;
							for(var i=0; i< receivedTasks.length;i++){
								if( receivedTasks[i].task_status == "ongoing"){
									_this.inprogressTasks.push(receivedTasks[i]);
								}else if(receivedTasks[i].task_status == "finished"){
									_this.finishedTasks.push(receivedTasks[i]);
								}
								_this.haveTask = true;
							}
						}).catch(function (error) {
							_this.$Message.error('获取已接收的任务失败!');
						});
						
				}).catch(function (error) {
					//console.log(error.response.status);
					_this.isLogin = false;
					window.localStorage.removeItem('token');
					window.localStorage.removeItem('userID');
					window.localStorage.removeItem('organID');
					window.localStorage.removeItem('taskID');
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
						window.localStorage.removeItem('organID');
						window.localStorage.removeItem('taskID');
						_this.$Message.success('退出登录成功');
					}).catch(function (error) {
						console.log(error);
					});
				}
			},
			toTaskMarket(){
				this.$router.push({
						path: '/taskmarket'
				});						
			},
			GotoTopup (){
				this.topup = true;
				this.isWithdraw = false;
			},
			WithdrawDeposit(){
				this.topup = true;
				this.isWithdraw = true;
			},
			withdraw(){
				//PUT /users/:user_id/balance HTTP/1.1
				var _this = this;
				var url_all = "/users/" + this.$data.userID + "/balance";
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$axios({
					 method:"put",
					 url: url_all,
					 data:{
						 amount: -this.topupData.value,
					 },
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					_this.$Message.success('提现成功');
					_this.money = response.data.balance;
					_this.topup = false;
					_this.isWithdraw = false;
					window.localStorage.setItem('money', _this.money);
				}).catch(function (error) {
					console.log(error);
					_this.$Message.error('提现失败,余额不足');
					_this.topup = false;
					_this.isWithdraw = false;
				});				
			},
			recharge(){
				//PUT /users/:user_id/balance HTTP/1.1
				var _this = this;
				var url_all = "/users/" + this.$data.userID + "/balance";
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$axios({
					 method:"put",
					 url: url_all,
					 data:{
						 amount: this.topupData.value,
					 },
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					_this.$Message.success('充值成功');
					_this.money = response.data.balance;
					window.localStorage.setItem('money', _this.money);
					_this.topup = false;
				}).catch(function (error) {
					console.log(error);
					_this.$Message.error('充值失败');
					_this.topup = false;
				});

			},
			showMessage(){
				this.messagesNumber = 0;
			},
			displayLogin() {
				document.getElementById('loginFrame').style.display='block';
				document.getElementById('bgColorDiv').style.display='block';
			},
			clickLogin() {
				var _this = this;

				if(this.inputName == "" || this.inputPassword == "") {
					_this.$Message.error('请输入邮箱和密码');
				}
				else {
					document.getElementById('bgColorDiv').style.display='none';
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
							_this.$Message.success('登录成功');
							//跳转到主页
							_this.$router.go(0);
						})
						.catch(function (error) {
							console.log(error.response.status);
								_this.$axios({
								 method:"post",
								 url:"/sessions",
								 data:{
									phone_number: _this.inputName,
									password: _this.inputPassword,
								 }
								}).then(function (response){
									console.log(response);
									window.localStorage.setItem('token', response.data.access_token);
									window.localStorage.setItem('userID', response.data.user_id);
									_this.$Message.success('登录成功');
									//跳转到主页
									_this.$router.go(0);
								})
								.catch(function (error) {
									console.log(error.response.status);
									if(error.response.status == 404){
										_this.$Message.error('用户不存在或者密码错误');
									}
									if(error.response.status == 400){
										_this.$Message.error('用户不存在或者密码错误');
									}
									_this.inputName = '';
									_this.inputPassword = '';
								});
						});
				}
			},
			clickCancel() {
				document.getElementById('bgColorDiv').style.display='none';
				this.inputName = '';
				this.inputPassword = '';
			},
			createNewTask() {
				window.localStorage.removeItem('organID');
				window.localStorage.removeItem('taskID');
				this.$router.push({
					path: '/', 
					name: 'missioncreate'
				});		
			},
			showTaskCancel(){
				 this.showTaskInfo = false;
			},
			ToTaskInfo(taskID){
					var current_step = 0;
					for(var i = 0;i < this.inprogressTasks.length;i++){
						if(this.inprogressTasks[i].task_id == taskID){
							console.log("当前任务:");
							console.log(this.inprogressTasks[i]);
							current_step = this.inprogressTasks[i].current_step;
							break;
						}
					}
					for(var i = 0;i < this.finishedTasks.length;i++){
						if(this.finishedTasks[i].task_id == taskID){
							console.log("当前任务:");
							console.log(this.finishedTasks[i]);
							current_step = this.finishedTasks[i].current_step;
							break;
						}
					}
					window.localStorage.setItem('taskID', taskID);
					window.localStorage.removeItem('organID');
					this.$router.push({
						path: '/', 
						name: 'taskinfoforreceiver',
						params: { 
								taskID: taskID,
								current_step: current_step
						},
					});					
			},
			LookTaskInfo(taskId){
				this.showTaskInfo = true;				
				var jwt = "JWT " + window.localStorage.getItem('token');
				var _this = this;
				// 需要区分是自己创建的还是自己接收的任务
			
				var url = "/users/" + this.$data.userID + "/tasks/" + taskId;
				this.$axios({
						 method:"get",
						 url:url,
						 headers:{
							'Authorization': jwt,
						 }
				}).then(function (response){
					console.log("任务详情");
					console.log(response);
					_this.showTaskInfomation = response.data;
					_this.$set(_this.showTaskInfomation,'current',-1);
				}).catch(function (error) {
					_this.$Message.error('获取任务详情失败!');
				});	
			
			},
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
    width: 530px;
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
.white_content {
	border-radius: 20px;
	display: none;
	position: absolute;
	top: 10%;
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
	/*opacity: .80;*/
	filter: alpha(opacity=80);
}

.mainDiv {
	/* height: 90%; */
	/* background-image: url("./../assets/bgimg.png"); */
	/*background-repeat: no-repeat;*/
	background-position: center;
	/* border: 3px solid red; */
	background-size: cover;
	height: 770px;
	z-index: 0;
}

.mainDiv-mask {
	/*border: 3px solid green;*/
	margin-right: 20px;
	width: 100px;
	height: 770px;
	width: 100%;
	/*background-color: #FDDFB2;*/
	background-color: rgba(50,100,200,0.8);
	/*opacity: 0.8;*/
	z-index: 1;
}

.mainTitle {
	text-align: center;
	font-size: 70px;
	color: white;
	height: 20%;
	padding-top: 15%;
}

.subTitle {
	text-align: center;
	font-size: 30px;
	color: white;
	padding-top: 8%;
}

.secondDiv {
	/* border: 3px solid red; */
	height: 830px;
	position: relative;
	/*background-color: #FDDFB2;*/
	/* background-color: white; */
}

.thirdDiv {
	height: 830px;
	position: relative;
	/*background-color: #FDDFB2;*/
	/* background-color: white; */
}

.secondSubDiv {
	position: absolute;
	width: 40%;
	height: 830px;
	top: 100px;
	left: 150px;
	background-image: url("./../assets/3.png");
	background-repeat: no-repeat;
	/* border: 3px solid red; */
}

.thirdSubDiv {
	position: absolute;
	left: 60%;
	width: 40%;
	height: 830px;
	background-image: url("./../assets/5.png");
	background-repeat: no-repeat;
	/* border: 3px solid red; */
}

.secondTextDiv {
	position: absolute;
	padding: 50px;
	left: 45%;
	width: 50%;
	height: 830px;
	/* border: 3px solid green; */
}

.thirdTextDiv {
	position: absolute;
	padding: 50px;
	left: 5%;
	width: 50%;
	height: 830px;
	/* border: 3px solid green; */
}

.introTitle {
	text-align: center;
	font-size: 50px;
	/*color: white;*/
	margin-top: 10%;
	margin-bottom: 5%;
	/*padding-top: 15%;*/
}

.introPara {
	font-size: 25px;
	text-indent: 55px;
	letter-spacing: 2px;
}

.funcPara {
	font-size: 25px;
	margin: 2%;
	letter-spacing: 2px;
}

.memTitle {
	text-align: center;
	font-size: 50px;
	/*color: white;*/
	margin-top: 10%;
	margin-bottom: 5%;
}

.memPara {
	font-size: 25px;
	margin: 2%;
	letter-spacing: 2px;
}

.logo {
	/* border: 3px solid red; */
	top: 20%;
	margin-left: 28%;
	height: 700px;
	width: 700px;
	background-image: url("./../assets/logo2.png");
	background-repeat: no-repeat;
	background-size: cover;
}
.leftpart {
	position: absolute;
	left: -30px;
	width: 40%;
	height: 830px;
	top: 100px;
	background-image: url("./../assets/2.png");
	background-repeat: no-repeat;
	/* border: 3px solid red; */
}

.rightpart {
	position: absolute;
	left: 70%;
	width: 40%;
	height: 830px;
	background-image: url("./../assets/1.png");
	background-repeat: no-repeat;
	/* border: 3px solid red; */
}
</style>