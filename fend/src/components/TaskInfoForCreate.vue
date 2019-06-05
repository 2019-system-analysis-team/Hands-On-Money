<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark" active-name="1-1">
                    <div class="layout-logo"></div>
                    <div class="layout-nav">
                        <Submenu name="1">
							 <template slot="title">
								<Icon type="ios-ionic"></Icon>
								任务
							 </template>
							<MenuItem name="1-1" to="/mytasks">我的任务</MenuItem>
							<MenuItem name="1-2" @click.native = "createNewTask()">新建任务</MenuItem>
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
					<div>
						<Submenu name="4">
							<template slot="title">
								<Avatar :src="profilePhotoPath" style="background-color: #87d068"></Avatar>
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
					<TabPane label="基本信息" name="基本信息">
						<Card dis-hover>
							<div slot="extra">
								<Button type="warning" shape="circle"  @click="toshowWithdrawInfo()">撤回任务</Button>
								<Button type="primary" icon="ios-hammer-outline" shape="circle">修改任务</Button>
							</div>	
							<Modal v-model="showWithdrawInfo">
								<div>
									<p style="text-align:center; font-size: 16px;">
										<span>您真的要撤回该任务吗？撤回操作不可逆!</span>
									</p>
								</div>
								<div slot="footer">
									<Button type="text" @click="showWithdrawInfoCancel">取消</Button>
									<Button type="error" @click="withdrawTask">确认撤回</Button>
								</div>
							</Modal>
							<p slot="title" class="info">{{showTaskInfomation.title}}</p>
							标签 : <Tag v-for="item in showTaskInfomation.tags" :key="item" :name="item" color="cyan">{{ item }}</Tag>
							<p class="info">任务描述 : {{showTaskInfomation.description}}</p>
							<p class="info">当前参与者人数 : {{showTaskInfomation.current_participant_number}}</p>
							<p class="info">参与者人数上限 : {{showTaskInfomation.participant_number_limit}}</p>
							<p class="info">完成奖励代币 : {{showTaskInfomation.reward_for_one_participant}}</p>
							<p class="info">创建者名字 : {{showTaskInfomation.creator_organization_name}}</p>
							<p class="info">创建者邮箱 : {{showTaskInfomation.creator_user_email}}</p>
							<p class="info">创建者电话 : {{showTaskInfomation.creator_user_phone_number}}</p>
							<p class="info">任务发布时间 : {{showTaskInfomation.post_time}}</p>
							<p class="info">截止接受任务时间 : {{showTaskInfomation.receive_end_time}}</p>
							<p class="info">最迟完成任务时间 : {{showTaskInfomation.finish_deadline_time}}</p>
						    <Collapse simple>
								<Panel name="1">
									步骤
									<p slot="content">
										<Timeline>
												<TimelineItem v-for="item in showTaskInfomation.steps" :key="item.title">
													<p class="time">{{item.title}}</p>
													<p class="content">{{item.description}}</p>
												</TimelineItem>
										</Timeline>
									</p>
								</Panel>
								<Panel name="2">
									用户限制
									<p slot="content">
										年龄下限 : {{showTaskInfomation.user_limit.age_upper}} 年龄上限 : {{showTaskInfomation.user_limit.age_lower}}</br>
										年级 : <tag v-for="item in showTaskInfomation.user_limit.grades" :key="item.grades">{{item}}</tag></br>
										性别 : <tag v-for="item in showTaskInfomation.user_limit.sexes" :key="item.sexes">{{item}}</tag></br>
										学校 : <tag v-for="item in showTaskInfomation.user_limit.schools" :key="item.schools">{{item}}</tag>
									</p>
								</Panel>
							</Collapse>
						</Card>
					</TabPane>
					<TabPane label="任务审核" name="任务审核">
						<Card dis-hover style="height: 560px">
							<p slot="title" style="height: 38px;">
								<Select v-model="participantclass" style="width:200px" @on-change="selectChange">
									<Option v-for="item in classifications" :value="item.value" :key="item.value">{{ item.label }}</Option>
								</Select>
							</p>
							
							<Table border :columns="allParticipant" :data="participant_info" v-if="this.participantSelectType == 0"></Table>
							<Table border :columns="ongoingParticipant" :data="ongoing_participant_info" v-if="this.participantSelectType == 1"></Table>
							<Table border :columns="waitingExamineParticipant" :data="waiting_examine_participant_info" v-if="this.participantSelectType == 2"></Table>
							<Table border :columns="allParticipant" :data="finished_participant_info" v-if="this.participantSelectType == 3"></Table>
						</Card>		
					</TabPane>
				</Tabs>
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
    </div>
</template>
<script>
  export default {
        data () {
            return {
				showWithdrawInfo: false,
                allParticipant: [
                    {
                        title: '名字',
                        key: 'name',
                        render: (h, params) => {
                            return h('div', [
                                h('Icon', {
                                    props: {
                                        type: 'person'
                                    }
                                }),
                                h('strong', params.row.name)
                            ]);
                        }
                    },
                    {
                        title: '学校',
                        key: 'school'
                    },
                    {
                        title: '年级',
                        key: 'grade'
                    }
                ],
                ongoingParticipant: [
                    {
                        title: '名字',
                        key: 'name',
                        render: (h, params) => {
                            return h('div', [
                                h('Icon', {
                                    props: {
                                        type: 'person'
                                    }
                                }),
                                h('strong', params.row.name)
                            ]);
                        }
                    },
                    {
                        title: '学校',
                        key: 'school'
                    },
                    {
                        title: '年级',
                        key: 'grade'
                    },
                    {
                        title: '设置',
                        key: 'action',
                        width: 150,
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: {
                                        type: 'primary',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
                                            this.show(params.index)
                                        }
                                    }
                                }, '完成任务')
                            ]);
                        }
                    }
                ],
				waitingExamineParticipant: [
                    {
                        title: '名字',
                        key: 'name',
                        render: (h, params) => {
                            return h('div', [
                                h('Icon', {
                                    props: {
                                        type: 'person'
                                    }
                                }),
                                h('strong', params.row.name)
                            ]);
                        }
                    },
                    {
                        title: '学校',
                        key: 'school'
                    },
                    {
                        title: '年级',
                        key: 'grade'
                    },
                    {
                        title: '设置',
                        key: 'action',
                        width: 150,
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: {
                                        type: 'primary',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
											
                                        }
                                    }
                                }, '确认参与')
                            ]);
                        }
                    }
                ],
				finishedParticipant: [
                    {
                        title: '名字',
                        key: 'name',
                        render: (h, params) => {
                            return h('div', [
                                h('Icon', {
                                    props: {
                                        type: 'person'
                                    }
                                }),
                                h('strong', params.row.name)
                            ]);
                        }
                    },
                    {
                        title: '学校',
                        key: 'school'
                    },
                    {
                        title: '年级',
                        key: 'grade'
                    }
                ],
				profilePhotoPath: '',
				taskID: '',
				userID: '',
				tabs: '基本信息',
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
						"age_upper": 8,
						"age_lower": 18,
						"grades": ["grade1", "grade1"],
						"sexes": ["sex_type1", "sex_type2", "sex_type3"],
						"schools": ["school_name1", "school_name2"]
					},
					"steps": [
						{
							"title": "string1",
							"description": "string1"
						},
						{
							"title": "string2",
							"description": "string2"
						}
					],
					"participant_ids": [123, 124, 125, 126],
					"ongoing_participant_ids": [121, 128],
					"waiting_examine_participant_ids": [125],
					"finished_participant_ids": [126]
				},
				waiting_examine_participant_info:[],
				ongoing_participant_info:[],
				finished_participant_info:[],
				participant_info:[],
				participantclass:'全部参与者',
				classifications: [
                    {
                        value: '全部参与者',
                        label: '全部参与者'
                    },
                    {
                        value: '正在完成任务的参与者',
                        label: '正在完成任务的参与者'
                    },
                    {
                        value: '等待确认的参与者',
                        label: '等待确认的参与者'
                    },
                    {
                        value: '完成任务的参与者',
                        label: '完成任务的参与者'
                    }
                ],	
				participantSelectType: 0,
				isCreateByOrgan:false,
				organID:null,
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
				/*
				let routerParams = this.$route.params.taskID;
				let organID = this.$route.params.organID;
				if(organID != null){
					this.isCreateByOrgan = true;
					this.organID = organID;
				}
				
				if(routerParams == null)
				{
					// 返回主页
					this.$router.push({
						path: '/', 
						name: 'mainpage',
					});	
				}
				this.taskID = routerParams;
				let uID = window.localStorage.getItem('userID')
				if(uID == null || uID == ""){
					//跳转到主页
					this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				}
				
				//this.$data.userID = uID;
				
				var _this = this;
				var url = "/users/" + this.$data.userID;
				if(this.isCreateByOrgan){
					url += "/organizations/" + this.organID + "/my_tasks/" + this.taskID;
				}
				else{
					url += "/my_tasks/" + this.taskID;
				}
				var jwt = "JWT " + window.localStorage.getItem('token');
								
				this.$axios({
					 method:"get",
					 url: url,
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					_this.showTaskInfomation = response.data;
				}).catch(function (error) {
					console.log(error);
				});	
				*/
			   var _this = this;
			   for(var i = 0 ;i < this.showTaskInfomation.participant_ids.length;i++){					
					var url = "/users/" + this.showTaskInfomation.participant_ids[i];
					var jwt = "JWT " + window.localStorage.getItem('token');
					this.$axios({
						 method:"get",
						 url:url,
						 headers:{
							'Authorization': jwt,
						 }
					}).then(function (response){
						var test = {};
						_this.$set(test,'id',response.data.id);
						_this.$set(test,'school',response.data.school);
						_this.$set(test,'grade',response.data.grade);
						_this.$set(test,'name',response.data.name);
						_this.participant_info.push(test);
					}).catch(function (error) {

					});
			   }
			   for(var i = 0 ;i < this.showTaskInfomation.ongoing_participant_ids.length;i++){
					var url = "/users/" + this.showTaskInfomation.ongoing_participant_ids[i];
					var jwt = "JWT " + window.localStorage.getItem('token');
					this.$axios({
						 method:"get",
						 url:url,
						 headers:{
							'Authorization': jwt,
						 }
					}).then(function (response){
						var test = {};
						_this.$set(test,'id',response.data.id);
						_this.$set(test,'school',response.data.school);
						_this.$set(test,'grade',response.data.grade);
						_this.$set(test,'name',response.data.name);
						_this.ongoing_participant_info.push(test);
					}).catch(function (error) {
					
					});
			   }
			   for(var i = 0 ;i < this.showTaskInfomation.waiting_examine_participant_ids.length;i++){
					var url = "/users/" + this.showTaskInfomation.waiting_examine_participant_ids[i];
					var jwt = "JWT " + window.localStorage.getItem('token');
					this.$axios({
						 method:"get",
						 url:url,
						 headers:{
							'Authorization': jwt,
						 }
					}).then(function (response){
						var test = {};
						_this.$set(test,'id',response.data.id);
						_this.$set(test,'school',response.data.school);
						_this.$set(test,'grade',response.data.grade);
						_this.$set(test,'name',response.data.name);
						_this.waiting_examine_participant_info.push(test);
					}).catch(function (error) {
					
					});
			   }
			   for(var i = 0 ;i < this.showTaskInfomation.finished_participant_ids.length;i++){
					var url = "/users/" + this.showTaskInfomation.finished_participant_ids[i];
					var jwt = "JWT " + window.localStorage.getItem('token');
					this.$axios({
						 method:"get",
						 url:url,
						 headers:{
							'Authorization': jwt,
						 }
					}).then(function (response){
						var test = {};
						_this.$set(test,'id',response.data.id);
						_this.$set(test,'school',response.data.school);
						_this.$set(test,'grade',response.data.grade);
						_this.$set(test,'name',response.data.name);
						_this.finished_participant_info.push(test);
					}).catch(function (error) {
					
					});
			   }
			    this.profilePhotoPath = window.localStorage.getItem('MyProfilePhotoPath');
			},
			GotoTopup (){
				this.topup = true;
			},
			recharge(){
				this.$Message.success('充值成功!');
				this.money = this.topupData.value + this.money;
				this.topup = false;
			},
			logout (){
				var url_all = "/users/" + this.$data.userID.toString() + "/session";
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$axios({
					 method:"delete",
					 url: url_all,
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					window.localStorage.setItem('token', "");
					window.localStorage.setItem('userID', "");
					this.$router.push({
						path: '/', 
						name: 'mainpage'
					});	
				}).catch(function (error) {
					console.log(error);
				});
			},
			selectChange(value){
				if(value == '全部参与者'){
					this.participantSelectType = 0;
				}else if(value == '正在完成任务的参与者'){
					this.participantSelectType = 1;
				}else if(value == '等待确认的参与者'){
					this.participantSelectType = 2;
				}else if(value == '完成任务的参与者'){
					this.participantSelectType = 3;
				}
			
			},
            show (index) {
				var _this = this;
				var url = "/users/:" + this.$data.userID + "/tasks/" + this.taskID+ "/finishers/" + this.ongoing_participant_info[index].id;
				var deleteID = this.ongoing_participant_info[index].id;
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$axios({
					 method:"put",
					 url: url,
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					_this.$Message.success('完成任务!');
					_this.showTaskInfomation.ongoing_participant_ids = response.data.ongoing_participant_ids;
					_this.showTaskInfomation.participant_ids = response.data.participant_ids;
					_this.ongoing_participant_info.splice(index,1);
					for(var i=0; i < _this.participant_info.length; i++)
					{
						if(_this.participant_info[i].id == deleteID)
						{
							_this.ongoing_participant_info.splice(i,1);
							break;
						}
					}
				}).catch(function (error) {
					console.log(error);
				});
				
            },
			toshowWithdrawInfo(){
				this.showWithdrawInfo = true;
			},
			showWithdrawInfoCancel(){
				this.showWithdrawInfo = false;
			},
			withdrawTask() {
				var _this = this;
				var url = "/users/" + this.$data.userID;
				if(this.isCreateByOrgan){
					url += "/organizations/" + this.organID + "/tasks/" + this.taskID;
				}
				else{
					url += "/tasks/" + this.taskID;
				}
				var jwt = "JWT " + window.localStorage.getItem('token');
				
				this.$axios({
					 method:"put",
					 url: url,
					 data:{
						task_id: this.taskID,
						status: "pending",
					 },
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					_this.$Message.info('撤回任务成功');
					_this.showWithdrawInfo = false;
				}).catch(function (error) {
					console.log(error);
				});	
			},
			createNewTask() {
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
.time{
	font-size: 14px;
	font-weight: bold;
}
.content{
	padding-left: 5px;
}
.info {	
    margin-bottom: 10px;
}
.finshButton{
	margin-top: 25px;
}
</style>