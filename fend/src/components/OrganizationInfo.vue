<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark" active-name="2-1">
                    <div class="layout-logo"></div>
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
				<div class="content-head">
					<Avatar :src="organProfilePhotoPath" style="background-color: #567dab;" size="large">{{organName}}</Avatar>
					<span style="font-size: 30px;vertical-align: middle;margin-left: 10px;">{{organName}}</span>
				</div>
				<Tabs type="card" id="tabs" value="组织" v-model="tabs" :animated="false">
					<TabPane label="组织任务" name="组织任务">
						<Card dis-hover style="height: 500px">
							<p slot="title" style="height: 38px;">
								<Select v-model="taskclass" style="width:200px" @on-change="selectChange">
									<Option v-for="item in classifications" :value="item.value" :key="item.value">{{ item.label }}</Option>
								</Select>
							</p>
							<div slot="extra" v-show="isManager || isCreater">
								<Button type="primary" icon="ios-add" shape="circle" @click="createOrganTask">新建组织任务</Button>
							</div>	
							<Col  v-show="!TasksIsEmpty" span="5" v-for="item in selectTasks" :key="item.task_id" style="padding-left: 30px; padding-top: 50px;">
								<Card>
									<p slot="title">{{item.task_name}}</p>
									<div slot="extra">
										<Button type="primary" ghost @click="LookTaskInfo(item.task_id)">详情</Button>
									</div>	
									<p>{{item.task_status}}</p>
									 
								</Card>
							</Col>
						</Card>		
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
									<p class="info" v-show="showTaskInfomation.tags !=  '问卷'">步骤 : </p>
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
					</TabPane>
					<TabPane label="组织信息" name="组织信息">
						<Card dis-hover style="height:380px">
							<p slot="title">组织信息如下</p>
							<Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80" class="form">
								<FormItem label="综合评分" prop="rate">
									<Rate show-text allow-half v-model="average_comment" disabled >
										<span style="color: #f5a623">{{ average_comment }}</span>
									</Rate>
								</FormItem>	
								<FormItem label="组织名称" prop="name">
									<Input v-model="formValidate.name" placeholder="请输入组织名称" :disabled="organInfodisabled"></Input>
								</FormItem>
								<FormItem label="组织介绍" prop="desc">
									<Input v-model="formValidate.desc" type="textarea" :autosize="{minRows: 2,maxRows: 8}" :disabled="organInfodisabled"></Input>
								</FormItem>
								<FormItem>
									<Button v-show="isCreater" type="primary" @click="handleSubmit('formValidate')" style="margin-left:89%">修改信息</Button>
								</FormItem>
							</Form>
						</Card>					
					</TabPane>
					<TabPane label="管理成员" name="管理成员">
						<Card dis-hover>
							<p slot="title" style="height: 38px;">
								全部成员
							</p>
							<div slot="extra" v-show="isManager || isCreater">
								<Button type="primary" icon="ios-add" shape="circle" @click="addMember = true">添加成员</Button>
							</div>	
							<Modal
								v-model="addMember"
								title="添加成员"
								@on-ok="addMemberok('addMemberValidate')"
								@on-cancel="addMembercancel">
								
								<Form ref="addMemberValidate" :model="addMemberValidate" :rules="addMemberRuleValidate" :label-width="80">
									<FormItem label="添加方式" prop="type">
										<Select v-model="addMemberValidate.addMemberType" style="width:100px">
											<Option value="电话">电话</Option>
											<Option value="邮箱">邮箱</Option>
										</Select>										
									</FormItem>
									<FormItem :label="addMemberValidate.addMemberType" prop="addMemberInfo">
										<Input v-model="addMemberValidate.addMemberInfo" placeholder="请输入" style="width: 300px" />
									</FormItem>
									<FormItem label="身份" >
										<Select v-model="addMemberValidate.addMemberStatus" style="width:100px">
											<Option value="admin">admin</Option>
											<Option value="member">member</Option>
										</Select>	
									</FormItem>
								</Form>
							</Modal>
							<Col span="6" v-for="item in allMembers" :key="item.id" style="padding-left: 20px; padding-top: 30px;">
								<Card style="height: 185px;">
									<p slot="title">成员信息</p>
									<div slot="extra" v-show="(isManager || isCreater) && (item.status != 'owner')">
										<Button type="error" ghost @click="deleteMember(item.userID)">删除</Button>
									</div>	
									<div style="width: 83%;float: left;">
										<p style="margin-bottom: 5px;">真实姓名 : {{item.name}}</p>
										<p style="margin-bottom: 5px;">昵称 : {{item.nickname}}</p>
										<p style="margin-bottom: 5px;">学号 : {{item.student_id}}</p>
										<p v-show="!(isManager || isCreater)">身份 : {{item.status}}</p>
										<div v-show="isManager || isCreater">
											身份 : 
											<Select v-model="item.status" style="width:100px" v-if="(item.status != 'owner')" @on-change="changeStatus(item)">
												<Option value="admin">admin</Option>
												<Option value="member">member</Option>
											</Select>
											<Select v-model="item.status" style="width:100px" disabled v-if="(item.status == 'owner')">
												<Option value="owner" disabled>owner</Option>
											</Select>
											<Tooltip content="点击确认更改" theme="light" v-if="item.statusChanged">
												<Button type="success" @click="modifyMemberStatus(item)" ghost shape="circle" icon="md-checkmark" size="small"></Button>
											</Tooltip>
										</div>
									</div>
									<div style="height: 75px;">
										<Avatar shape="square" size="large" :src="item.headPhotoPath">{{item.nickname}}</Avatar>
									</div>
								</Card>
							</Col>
						</Card>		
					</TabPane>
					<TabPane label="组织钱包" name="组织钱包">
						<Card dis-hover style="height:380px">
							<p slot="title">组织账户信息如下</p>
							<Form  :model="organtopupData" :label-width="80" class="form">
								<FormItem label="组织余额" prop="yue">
									{{organMoney}}
								</FormItem>
								<FormItem label="充值金额" label-position="top">
								<InputNumber
											:max="10000"
											:min="1"
											 v-model="organtopupData.value"
											></InputNumber>
								</FormItem>
								<FormItem label="支付方式" label-position="top">
									<Select v-model="organtopupData.mode">
										<Option value="支付宝">支付宝</Option>
										<Option value="微信支付">微信支付</Option>
										<Option value="信用卡">信用卡</Option>
									</Select>
								</FormItem>
								<FormItem>
									<Button type="primary" @click="chargeForOrgan" style="margin-left:89%">充值</Button>
								</FormItem>
							</Form>
						</Card>					
					</TabPane>
					<TabPane label="删除组织" name="删除组织" v-show="isCreater">
						<Card dis-hover style="height:380px">
							<p slot="title">请确认要删除组织</p>
							<Form ref="deleteValidate" :model="deleteValidate" :rules="deleteRuleValidate" :label-width="120" class="form">
								<FormItem label="该组织名称" prop="name">
									<Input v-model="deleteValidate.name" placeholder="请输入即将删除的组织名称"></Input>
								</FormItem>
								<FormItem>
									<Button type="error" @click="handleSubmit('deleteValidate')" style="margin-left:89%">确认删除</Button>
								</FormItem>
							</Form>
						</Card>	
					</TabPane>
				</Tabs>
            </Content>
            <Footer class="layout-footer-center">2019-2019 &copy; SYSU</Footer>
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
			const validateNameCheck = (rule, value, callback) => {
				if (value === '') {
					callback(new Error('组织名称不能为空'));
				} else if (value.toLocaleString().length > 20) {
					callback(new Error('组织名不能多于20个字符'));
				} else {
					callback();
				}
			};
			const validateDescCheck = (rule, value, callback) => {
			    if (value === '') {
			        callback(new Error('组织介绍不能为空'));
			    } else if (value.toLocaleString().length < 15) {
			        callback(new Error('组织介绍不能少于15个字符'));
			    } else {
			        callback();
			    }
			};
            const validateDeleteNameCheck = (rule, value, callback) => {
				if (value !== this.formValidate.name) {
                    callback(new Error('组织名称不正确'));
                } else {
                    callback();
                }
            };
            return {
				isWithdraw:false,
				profilePhotoPath: '',		
				organProfilePhotoUrl:'',
				organProfilePhotoPath: '',
				organProfilePhotoName: '',
				
				organInfodisabled: true,
				average_comment:0,
				userID: '',
				tabs: '组织任务',
				topup: false,
                styles: {
                    height: 'calc(100% - 55px)',
                    overflow: 'auto',
                    paddingBottom: '53px',
                    position: 'static'
                },
				money:0,
				organMoney:0,
                topupData: {
                    value: 1,
					mode: '支付宝',
                },
				organtopupData: {
				    value: 1,
					mode: '支付宝',
				},
				taskclass:'全部任务',
				classifications: [
					{
					    value: '全部任务',
					    label: '全部任务'
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
				
                defaultList: [],
                imgName: '',
                visible: false,
				uploadList: [],
				jwt:{},
				organID:0,
				
				allTasks:[

				],
				inprogressTasks:[

				],
				finishedTasks:[

				],
				notgoingTasks:[],
				selectTasks:[],
				TasksIsEmpty:true,
				deleteValidate: {
					name: ''
				},
				deleteRuleValidate:{
                    name: [
                        { required: true, validator: validateDeleteNameCheck, trigger: 'blur' }
                    ],					
				},
			    formValidate: {
					 name: '',
					 desc: ''
				},
				organName:'',
				ruleValidate: {
					 name: [
						 { required: true, validator: validateNameCheck, trigger: 'blur' }
					 ],
					 desc: [
						 {required: true, validator: validateDescCheck, trigger: 'blur' }
					 ]
				},
				allMembers:[

				],
				allMembersShortInfo:[
				],
				isManager: false,
				isCreater: false,
				
				addMember:false,
				addMemberValidate:{
					addMemberType:'电话',
					addMemberInfo:'',
					addMemberStatus:'member',
				},
				addMemberRuleValidate:{
					 addMemberInfo: [
						 { required: true, message: '该字段不能为空', trigger: 'blur' }
					 ],					
				},
				showTaskInfomation:{

				},
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
				this.selectTasks = this.allTasks;
	
				let orID = window.localStorage.getItem('organID');
				if(orID == null)
				{
					this.$Message.error('未知组织');
					// 返回主页
					this.$router.push({
						path: '/', 
						name: 'mainpage',
					});	
				}

				this.organID = orID;
				let uID = window.localStorage.getItem('userID');
			
				if(uID == null || uID == ""){
					//跳转到主页
					this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				}
			
				var _this = this;
				var url = "/users/" + uID + "/organizations/" + this.organID;
				this.$data.userID = uID;
				this.organProfilePhotoUrl = "/users/"+uID+"/organizations/"+  this.organID +"/profile_photo";
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$set(this.jwt,'Authorization',jwt);
		
				this.$axios({
						 method:"get",
						 url:url,
						 headers:{
							'Authorization': jwt,
						 }
				}).then(function (response){
					console.log(response);	
					_this.organName = response.data.name;
					_this.formValidate.name = response.data.name;
					_this.formValidate.desc = response.data.bio;
					 _this.allMembersShortInfo = response.data.members;
					 _this.organMoney = response.data.balance;
					 _this.average_comment = response.data.avg_comment;
					for(var i=0; i < _this.allMembersShortInfo.length;i++){
						var url = "/users/" + _this.allMembersShortInfo[i].user_id;
						if(_this.allMembersShortInfo[i].user_id == _this.userID){
							if(_this.allMembersShortInfo[i].status == 'admin'){
								_this.isManager = true;
							}else if(_this.allMembersShortInfo[i].status == 'owner'){
								_this.isCreater = true;
							}
						}
	
						var jwt = "JWT " + window.localStorage.getItem('token');
						_this.$axios({
								 method:"get",
								 url:url,
								 headers:{
									'Authorization': jwt,
								 }
						}).then(function (response){
							console.log("获取成员的信息");
							console.log(response);
							var nickname = response.data.nickname;
							var name = response.data.name;
							var headPhotoPath =  _this.$profilePath + response.data.profile_photo_path;
							var statusChanged = false;
							var test = {};
							_this.$set(test,'userID',response.data.user_id);
							_this.$set(test,'nickname',nickname);
							_this.$set(test,'name',name);
							
							for(var j=0; j < _this.allMembersShortInfo.length;j++){
								if(_this.allMembersShortInfo[j].user_id == response.data.user_id){
									_this.$set(test,'status',_this.allMembersShortInfo[j].status);
								}
							}
							//_this.$set(test,'status',_this.allMembersShortInfo[i].status);
							_this.$set(test,'statusChanged',statusChanged);
							_this.$set(test,'headPhotoPath',_this.$profilePath + response.data.profile_photo_path);
							_this.$set(test,'student_id',response.data.student_id);
							
							console.log("新成员:");
							console.log(test);
							_this.allMembers.push(test);
						}).catch(function (error) {
							console.log(error);
						});
					}
				}).catch(function (error) {
					console.log(error);
					_this.$Message.error('获取组织信息失败!');
				});
							
			    var url = "/users/" + uID + "/organizations/" + this.organID + "/my_tasks";

				this.$axios({
						 method:"get",
						 url:url,
						 headers:{
							'Authorization': jwt,
						 }
				}).then(function (response){
					console.log("所有任务");	
					console.log(url);
					console.log(response);	
					_this.allTasks = response.data.task;
					for(var i=0; i < _this.allTasks.length;i++){
						if(_this.allTasks[i].task_status == "ongoing"){
							_this.inprogressTasks.push(_this.allTasks[i]);
						}else if(_this.allTasks[i].task_status == "finished"){
							_this.finishedTasks.push(_this.allTasks[i]);
						}else if(_this.allTasks[i].task_status == "pending"){
							_this.notgoingTasks.push(_this.allTasks[i]);
						}
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
					
					_this.$Message.error('获取组织任务失败!');
					//跳转到主页
					
					
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
					_this.$Message.error('提现失败，余额不足');
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
			chargeForOrgan(){
				//PUT /users/:user_id/organizations/:organization_id/balance
				var _this = this;
				var url_all = "/users/" + this.$data.userID + "/organizations/" + this.organID + "/balance";
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$axios({
					 method:"put",
					 url: url_all,
					 data:{
						 amount: this.organtopupData.value,
					 },
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
				_this.$Message.success('为组织充值成功!');
				_this.organMoney = _this.organtopupData.value + _this.organMoney;

				_this.money = _this.money - _this.organtopupData.value;
				window.localStorage.setItem('money', _this.money);
				}).catch(function (error) {
					console.log(error);
					_this.$Message.error('为组织充值失败,请检查自己的余额是否充足');
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
				}
			},
            handleSubmit (name) {
				if(name == "formValidate" && this.organInfodisabled == true){
					this.organInfodisabled = false;
					return;
				}
				var _this = this;
                this.$refs[name].validate((valid) => {
                    if (valid) {
						var jwt = "JWT " + window.localStorage.getItem('token');
						var url = "/users/"+ this.$data.userID +"/organizations/" + this.organID;
						console.log("修改内容:" + this.$data.formValidate.name + "简介:" + this.$data.formValidate.desc);
						if(name == "formValidate"){
							this.$axios({
								 method:"put",
								 url: url,
								 data:{
									name: this.$data.formValidate.name,
									bio: this.$data.formValidate.desc
								 },
								 headers:{
									'Authorization': jwt,
								 }
							}).then(function (response){
								_this.$Message.success('修改成功!');
								_this.organInfodisabled = true;
							}).catch(function (error) {
								console.log(error);
							});							
						}else{
							this.$axios({
								 method:"delete",
								 url: url,
								 headers:{
									'Authorization': jwt,
								 }
							}).then(function (response){
								_this.$Message.success('删除成功!');
								window.localStorage.removeItem('organID');
								//跳转到我的组织
								_this.$router.push({
									path: '/', 
									name: 'organization'
								});
							}).catch(function (error) {
								console.log(error);
								_this.$Message.error('权限不够，删除失败');
							});								
						}
                    } else {
                        this.$Message.error('信息填写有误!');
                    }
                })
            },
			changeStatus(item){
				item.statusChanged = true;
			},
            addMemberok (name) {
			   this.$refs[name].validate((valid) => {
					var _this = this;
					var jwt = "JWT " + window.localStorage.getItem('token');
					var url = "/users/"+ this.$data.userID.toString() +"/organizations/" + this.organID.toString() + "/members";
					if (valid) {
						
						if(this.addMemberValidate.addMemberType == '邮箱'){
							console.log('通过邮件添加' + this.$data.addMemberValidate.addMemberInfo + " " +  this.$data.addMemberValidate.addMemberStatus);
							this.$axios({
								 method:"post",
								 url: url,
								 data:{
									email: this.$data.addMemberValidate.addMemberInfo,
									status: this.$data.addMemberValidate.addMemberStatus
								 },
								 headers:{
									'Authorization': jwt,
								 }
							}).then(function (response){
								console.log(response);
								_this.$Message.success('添加成功!');
								_this.$router.go(0);
							}).catch(function (error) {
								console.log(error);
								_this.$Message.error('添加信息填写错误或重复添加!');
							});						
						}else{
							console.log('通过电话添加' + this.$data.addMemberValidate.addMemberInfo + " " +  this.$data.addMemberValidate.addMemberStatus);
							this.$axios({
								 method:"post",
								 url: url,
								 data:{
									phone_number: this.$data.addMemberValidate.addMemberInfo,
									status: this.$data.addMemberValidate.addMemberStatus
								 },
								 headers:{
									'Authorization': jwt,
								 }
							}).then(function (response){
								console.log(response);
								_this.$Message.success('添加成功!');
								_this.$router.go(0);
							}).catch(function (error) {
								console.log(error);
								_this.$Message.error('添加信息填写错误或重复添加!');
							});								
						}
					}
					else
					{
						this.$Message.error('添加信息填写错误或重复添加!');
					}
				});
            },
            addMembercancel () {
                this.$Message.info('取消添加成员');
            },
			deleteMember(deleteUserID){
				var _this = this;
				var url_all = "/users/"+this.userID+"/organizations/"+this.organID+"/members/"+deleteUserID;
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$axios({
					 method:"delete",
					 url: url_all,
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					_this.$Message.success('删除成员成功!');
					_this.$router.go(0);
				}).catch(function (error) {
					console.log(error);
				});
			
			},
			modifyMemberStatus(item){
				var url_all = "/users/"+this.userID+"/organizations/"+this.organID+"/members/"+item.userID;
				var jwt = "JWT " + window.localStorage.getItem('token');
				console.log("修改的权限:" + item.status);
				var _this = this;
				this.$axios({
					 method:"put",
					 url: url_all,
					 data:{
						status: item.status
					 },
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					console.log(response);
					item.statusChanged = false;
					_this.$Message.success('权限更改成功!');
				}).catch(function (error) {
					console.log(error);
				});		
			},
			LookTaskInfo(taskID){
				//console.log("taskID" + taskID);
				this.showTaskInfo = true;				
				var url = "/users/" + this.userID + "/organizations/" + this.organID + "/my_tasks/" + taskID;
				var jwt = "JWT " + window.localStorage.getItem('token');
				var _this = this;
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
					_this.$set(this.showTaskInfomation,'current',-1);
				}).catch(function (error) {

				});
			},
			showTaskOK(){
				 this.$Message.info('Clicked OK');
			},
			showTaskCancel(){
				 this.$Message.info('Clicked cancel');
				 this.showTaskInfo = false;
			},
			ToTaskInfo(taskID){
				//console.log("taskID" + taskID);
				window.localStorage.setItem('taskID', taskID);
				window.localStorage.setItem('organID', this.organID);
				this.$router.push({
					path: '/', 
					name: 'taskinfoforcreate',
					params: { 
							taskID: taskID,
							organID: this.organID,
					},
				});			
			},
			createNewTask() {
				window.localStorage.removeItem('taskID');
				window.localStorage.removeItem('organID');
				this.$router.push({
					path: '/', 
					name: 'missioncreate'
				});		
			},
			createOrganTask(){
				window.localStorage.removeItem('taskID');
				window.localStorage.setItem('organID', this.organID);
				this.$router.push({
					path: '/', 
					name: 'missioncreate',
					params: { 
							organID: this.organID,
					},
				});					
			}
        },
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
.ivu-layout-header{
    padding-right: 25px;
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