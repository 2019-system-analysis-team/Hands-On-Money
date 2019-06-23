<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark" active-name="1-1">
                    <div class="layout-nav">
                        <Submenu name="1">
							 <template slot="title">
								<Icon type="ios-ionic"></Icon>
								任务
							 </template>
							<MenuItem name="1-1" to="/mytasks">我的任务</MenuItem>
							<MenuItem name="1-2" @click.native = "createNewTask()">新建任务</MenuItem>
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
					<div>
						<Submenu name="4">
							<template slot="title">
								<Avatar :src="profilePhotoPath" style="background-color: #515a6e"></Avatar>
							</template>
							<MenuItem name="4-1" to="/userinfomodify">个人信息</MenuItem>
							<MenuItem name="4-2" @click.native="logout()">退出</MenuItem>
						</Submenu>
					</div>
					<Button shape="circle" icon="ios-home" @click="handleReturnHomepage()"></Button>
                </Menu>
            </Header>
			<Content>
				<Tabs type="card" id="tabs" value="任务" v-model="tabs" :animated="false">
					<TabPane label="我的任务" name="我的任务">
						<Card dis-hover style="height: 500px">
							<p slot="title" style="height: 38px;">
								<Select v-model="taskclass" style="width:200px" @on-change="selectChange">
									<Option v-for="item in classifications" :value="item.value" :key="item.value">{{ item.label }}</Option>
								</Select>
							</p>
							<div slot="extra">
								<Button type="primary" icon="ios-add" shape="circle"  @click = "createNewTask()">创建个人任务</Button>
							</div>	
							<Col span="8" v-for="item in selectTasks" :key="item.task_id" style="padding-left: 30px; padding-top: 50px;" v-show="!TasksIsEmpty">
								<Card>
									<p slot="title">{{item.task_name}}</p>
									<div slot="extra">
										<Button type="primary" ghost @click="LookTaskInfo(item.task_id)">详情</Button>
									</div>	
									<p>{{item.task_status}}</p>
								</Card>
							</Col>
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
						</Card>		
					</TabPane>
				</Tabs>
            </Content>
            <Footer class="layout-footer-center">2019-2019 &copy; Hands-On-Money</Footer>
        </Layout>
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
    </div>
</template>
<script>
  export default {
        data () {
            return {
				isWithdraw:false,
				profilePhotoPath: '',		
				userID: '',
				tabs: '我的任务',
				topup: false,
                styles: {
                    height: 'calc(100% - 55px)',
                    overflow: 'auto',
                    paddingBottom: '53px',
                    position: 'static'
                },
				money:0,
                topupData: {
                    value: 1,
					mode: '支付宝',
                },
				showTaskInfomation:{
				},
				selectTasks:[
					{
						"task_id": 0,
						"task_name": "task1-org",
						"task_status": "on going"
					}
				],
				allTasks:[],
				finishedTasks:[],
				inprogressTasks:[],
				receivedTasks:[],
				createdTasks:[],
				notgoingTasks:[],
				TasksIsEmpty:true,
				taskclass:'全部任务',
				classifications: [
				    {
				        value: '全部任务',
				        label: '全部任务'
				    },
					{
					    value: '我创建的',
					    label: '我创建的'
					},
					{
					    value: '我接收的',
					    label: '我接收的'
					},
				    {
				        value: '进行中',
				        label: '进行中'
				    },
				    {
				        value: '未进行',
				        label: '未进行'
				    },
				    {
				        value: '已结束',
				        label: '已结束'
				    },
				],	
				showTaskInfo: false,
            }
        },
		created: function () { 
			this.getEventData();
		},
        methods: {
            handleReturnHomepage () {
                // 返回主页
				this.$router.push({
					path: '/', 
					name: 'mainpage',
				});		
            },
			getEventData:function() {
				let uID = window.localStorage.getItem('userID');
				
				if(uID == null || uID == ""){
					//跳转到主页
					this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				}
				
				this.$data.userID = uID;
				var _this = this;
				var url = "/users/" + uID + "/my_tasks";
				var jwt = "JWT " + window.localStorage.getItem('token');
				console.log(url);
				this.$axios({
					 method:"get",
					 url:url,
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					console.log("获取所有任务");
					console.log(response);
					_this.createdTasks = response.data.task;
					for(var i=0; i<_this.createdTasks.length;i++){
						_this.createdTasks[i].task_name += ' (创建的任务) ';
						if(_this.createdTasks[i].task_status == "finished"){
							_this.finishedTasks.push(_this.createdTasks[i]);
						}else if(_this.createdTasks[i].task_status == "ongoing"){
							_this.inprogressTasks.push(_this.createdTasks[i]);
						}else if(_this.createdTasks[i].task_status == "pending"){
							_this.notgoingTasks.push(_this.createdTasks[i]);
						}
						_this.allTasks.push(_this.createdTasks[i]);
					}		
					if(_this.allTasks.length != 0)
					{
						_this.selectTasks = _this.allTasks;
						_this.TasksIsEmpty = false;
					}
					else
					{
						_this.TasksIsEmpty = true;
					}
					
				}).catch(function (error) {
					_this.$Message.error('获取我创建的任务失败!');
				});
				var url = "/users/" + uID + "/received_tasks";
				this.$axios({
					 method:"get",
					 url:url,
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					console.log("获取已接收任务");
					console.log(response);
					_this.receivedTasks = response.data;
					for(var i=0; i<_this.receivedTasks.length;i++){
						if(_this.receivedTasks[i].task_status == "finished"  || _this.receivedTasks[i].task_receiver_status == "waiting examine"){
							_this.finishedTasks.push(_this.receivedTasks[i]);
						}else if(_this.receivedTasks[i].task_status == "ongoing"){
							_this.inprogressTasks.push(_this.receivedTasks[i]);
						}else if(_this.receivedTasks[i].task_status == "pending"){
							_this.notgoingTasks.push(_this.receivedTasks[i]);
						}
						_this.allTasks.push(_this.receivedTasks[i]);
					}
					if(_this.allTasks.length != 0)
					{
						_this.selectTasks = _this.allTasks;
						_this.TasksIsEmpty = false;
					}
					else
					{
						_this.TasksIsEmpty = true;
					}
				}).catch(function (error) {
					_this.$Message.error('获取已接收的任务失败!');
				});
				  this.money = window.localStorage.getItem('money');
			    this.profilePhotoPath = window.localStorage.getItem('MyProfilePhotoPath');
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
					_this.topup = false;
					window.localStorage.setItem('money', _this.money);
				}).catch(function (error) {
					console.log(error);
					_this.$Message.error('充值失败');
					_this.topup = false;
				});

			},
			logout (){
				var _this = this;
				var url_all = "/users/" + this.$data.userID.toString() + "/session";
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$axios({
					 method:"delete",
					 url: url_all,
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					window.localStorage.removeItem('token');
					window.localStorage.removeItem('userID');
					window.localStorage.removeItem('organID');
					window.localStorage.removeItem('taskID');
					_this.$router.push({
						path: '/', 
						name: 'mainpage'
					});	
				}).catch(function (error) {
					console.log(error);
				});
			},
			selectChange(value){
				console.log(value);
				if(value == '已结束'){
					if(this.finishedTasks.length != 0)
					{
						this.selectTasks = this.finishedTasks;
						this.TasksIsEmpty = false;
					}
					else
					{
						this.TasksIsEmpty = true;
					}
				}else if(value == '进行中'){
					if(this.inprogressTasks.length != 0)
					{
						this.selectTasks = this.inprogressTasks;
						this.TasksIsEmpty = false;
					}
					else
					{
						this.TasksIsEmpty = true;
					}
				}else if(value == '全部任务'){
					if(this.allTasks.length != 0)
					{
						this.selectTasks = this.allTasks;
						this.TasksIsEmpty = false;
					}
					else
					{
						this.TasksIsEmpty = true;
					}
				}else if(value == '我创建的'){
					if(this.createdTasks.length != 0)
					{
						this.selectTasks = this.createdTasks;
						this.TasksIsEmpty = false;
					}
					else
					{
						this.TasksIsEmpty = true;
					}
				}else if(value == '我接收的'){
					if(this.receivedTasks.length != 0)
					{
						this.selectTasks = this.receivedTasks;
						this.TasksIsEmpty = false;
					}
					else
					{
						this.TasksIsEmpty = true;
					}
				}else if(value == '未进行'){
					if(this.notgoingTasks.length != 0)
					{
						this.selectTasks = this.notgoingTasks;
						this.TasksIsEmpty = false;
					}
					else
					{
						this.TasksIsEmpty = true;
					}					
				}
			},
			LookTaskInfo(taskId){
				this.showTaskInfo = true;				
				var jwt = "JWT " + window.localStorage.getItem('token');
				var _this = this;
				// 需要区分是自己创建的还是自己接收的任务
				var isCreate = false;
				for(var i = 0;i < this.createdTasks.length;i++){
					if(this.createdTasks[i].task_id == taskId){
						isCreate = true;
						break;
					}
				}
				if(isCreate){
					var url = "/users/" + this.$data.userID + "/my_tasks/" + taskId;
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
				}else{
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
				}

			},
			showTaskCancel(){
				 this.$Message.info('Clicked cancel');
				 this.showTaskInfo = false;
			},
			ToTaskInfo(taskID){
				var isCreate = false;
				var current_step = 0;
				for(var i = 0;i < this.createdTasks.length;i++){
					if(this.createdTasks[i].task_id == taskID){
						isCreate = true;
						break;
					}
				}
				for(var i = 0;i < this.receivedTasks.length;i++){
					if(this.receivedTasks[i].task_id == taskID){
						console.log("当前任务:");
						console.log(this.receivedTasks[i]);
						current_step = this.receivedTasks[i].current_step;
						break;
					}
				}
				//如果是自己接收的任务则跳转到接收的任务界面
				if(isCreate){
					window.localStorage.setItem('taskID', taskID);
					window.localStorage.removeItem('organID');
					this.$router.push({
						path: '/', 
						name: 'taskinfoforcreate',
						params: { 
								taskID: taskID
						},
					});
				}else{
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
				}
				
			},
			createNewTask() {
				window.localStorage.removeItem('organID');
				window.localStorage.removeItem('taskID');
				this.$router.push({
					path: '/', 
					name: 'missioncreate'
				});		
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
    width: 420px;
    margin: 0 auto;
    margin-right: 112px;
}
.layout-footer-center{
    text-align: center;
}
.demo-upload-list{
	display: inline-block;
	width: 80px;
	height: 80px;
	text-align: center;
	line-height: 80px;
	border: 1px solid transparent;
	border-radius: 4px;
	overflow: hidden;
	background: #fff;
	position: relative;
	box-shadow: 0 1px 1px rgba(0,0,0,.2);
	margin-right: 4px;
}
.demo-upload-list img{
	width: 100%;
	height: 100%;
}
.demo-upload-list-cover{
	display: none;
	position: absolute;
	top: 0;
	bottom: 0;
	left: 0;
	right: 0;
	background: rgba(0,0,0,.6);
}
.demo-upload-list:hover .demo-upload-list-cover{
	display: block;
}
.demo-upload-list-cover i{
	color: #fff;
	font-size: 20px;
	cursor: pointer;
	margin: 0 2px;
}
.form{
	margin:0 auto;
	width: 40%;
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
#tabs{
	background-color: #FFFFFF;
	margin-top: 5px;
}
.content-head{
	margin: 0 auto;
	width: 100%;
	text-align: center;
	padding-top: 10px;
    padding-bottom: 10px;
}
.info {	
    margin-bottom: 10px;
}
</style>