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
							<MenuItem name="3-2"  @click.native="WithdrawDeposit()">提现</MenuItem>
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
					<TabPane label="基本信息" name="基本信息">
						<Card dis-hover>
							<div slot="extra">
								<Button type="error" shape="circle"  @click="deleteTask()" v-show="!isOngoing && isManager">删除任务</Button>
								<Button type="warning" shape="circle"  @click="toshowWithdrawInfo()" v-show="isOngoing && isManager">撤回任务</Button>
								<Button type="primary" icon="ios-hammer-outline" shape="circle" v-show="!isOngoing && isManager" @click="modifyTask()">修改任务</Button>
							</div>	
							<Modal v-model="showWithdrawInfo">
								<div>
									<p style="text-align:center; font-size: 16px;">
										<span>您真的要撤回该任务吗？</span>
									</p>
								</div>
								<div slot="footer">
									<Button type="text" @click="showWithdrawInfoCancel">取消</Button>
									<Button type="error" @click="withdrawTask">确认撤回</Button>
								</div>
							</Modal>
							<Modal v-model="showdeleteTaskInfo">
								<div>
									<p style="text-align:center; font-size: 16px;">
										<span>您真的要删除该任务吗？删除操作不可逆!</span>
									</p>
								</div>
								<div slot="footer">
									<Button type="text" @click="showdeleteTaskInfoCancel">取消</Button>
									<Button type="error" @click="deleteTaskTrue">确认删除</Button>
								</div>
							</Modal>
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
						    <Collapse simple>
								<Panel name="1">
									用户限制
									<p slot="content">
										年龄下限 : {{showTaskInfomation.user_limit.age_upper}} 年龄上限 : {{showTaskInfomation.user_limit.age_lower}}</br>
										年级 : <tag v-for="item in showTaskInfomation.user_limit.grades" :key="item.grades">{{item}}</tag></br>
										性别 : <tag v-for="item in showTaskInfomation.user_limit.sexes" :key="item.sexes">{{item}}</tag></br>
										学校 : <tag v-for="item in showTaskInfomation.user_limit.schools" :key="item.schools">{{item}}</tag>
									</p>
								</Panel>
								<Panel name="2" v-show="showTaskInfomation.tags !=  '问卷'">
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
								<Panel name="2" v-show="showTaskInfomation.tags ==  '问卷'">
									问卷浏览
									<p slot="content" style="background:#eee;padding: 20px">
										<Card v-for="(item,index) in showTaskInfomation.steps" :key="item.title"  dis-hover>
												问题 {{index+1}} : {{item.title}}
											<p v-show="item.description != '' ">单选选项：</P>
											<RadioGroup v-show="item.description != '' ">
												<Radio v-for="single in item.forsingle" :key="single.label" disabled><span>{{single.label}}</span></Radio>
											</RadioGroup>
										</Card>
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
							<Table border :columns="finishedParticipant" :data="finished_participant_info" v-if="this.participantSelectType == 3"></Table>
						</Card>		
					</TabPane>
				</Tabs>
            </Content>
			<Modal v-model="appraise.isShow">
				<p slot="header" style="text-align:center">
					<span>请评价该成员在此次任务中</span>
				</p>
				<div>
				<Card dis-hover>
					<p >标题：</P> 
					<Input v-model="appraise.title" placeholder="请输入想要评价的方面" ></Input>
					<p >内容：</P> 
					<Input v-model="appraise.content" placeholder="请输入评价的内容" ></Input>
					<p >评分：</P> 
					<Rate show-text allow-half v-model="appraise.rate">
						<span style="color: #f5a623">{{ appraise.rate }}</span>
					</Rate>
				</Card>
				</div>
				<div slot="footer">
					<Button type="primary" @click="sendRate">确认评价</Button>
				</div>
			</Modal>
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
            return {
				appraise:{
					isShow: false,
					title: '',
					content: '',
					rate: 5,
					appId: 0,
				},
				isWithdraw:false,
				showWithdrawInfo: false,
				showdeleteTaskInfo: false,
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
                        title: '电话',
                        key: 'phone_number'
                    },
                    {
                        title: '学号',
                        key: 'student_id'
                    },
					{
					    title: '年级',
					    key: 'grade'
					},
					{
					    title: '学院',
					    key: 'school'
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
                        title: '电话',
                        key: 'phone_number'
                    },
                    {
                        title: '学号',
                        key: 'student_id'
                    },
					{
					    title: '年级',
					    key: 'grade'
					},
					{
					    title: '学院',
					    key: 'school'
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
                        title: '电话',
                        key: 'phone_number'
                    },
                    {
                        title: '学号',
                        key: 'student_id'
                    },
					{
					    title: '年级',
					    key: 'grade'
					},
					{
					    title: '学院',
					    key: 'school'
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
                        title: '电话',
                        key: 'phone_number'
                    },
                    {
                        title: '学号',
                        key: 'student_id'
                    },
					{
					    title: '年级',
					    key: 'grade'
					},
					{
					    title: '学院',
					    key: 'school'
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
				isOngoing:false,
				isManager:false,
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
				
				let organID = window.localStorage.getItem('organID');
				if(organID != null){
					this.isCreateByOrgan = true;
					this.organID = organID;
				}
				

				this.taskID = window.localStorage.getItem('taskID');
				if(this.taskID == null)
				{
					// 返回主页
					this.$router.push({
						path: '/', 
						name: 'mainpage',
					});	
				}
				let uID = window.localStorage.getItem('userID');
				if(uID == null || uID == ""){
					//跳转到主页
					this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				}
				
				this.$data.userID = uID;
				var jwt = "JWT " + window.localStorage.getItem('token');
				var _this = this;
				var url = "/users/" + this.$data.userID;
				if(this.isCreateByOrgan){
					url += "/organizations/" + this.organID + "/my_tasks/" + this.taskID;
					
					var _this = this;
					var url_info = "/users/" + uID + "/organizations/" + this.organID;

					this.$axios({
							 method:"get",
							 url:url_info,
							 headers:{
								'Authorization': jwt,
							 }
					}).then(function (response){
						var allMembersShortInfo = response.data.members;

						for(var i=0; i < allMembersShortInfo.length;i++){

							if(allMembersShortInfo[i].user_id == _this.userID){
								if(allMembersShortInfo[i].status == 'admin'){
									_this.isManager = true;
								}else if(allMembersShortInfo[i].status == 'owner'){
									_this.isManager = true;
								}
							}
						}
					})
				}
				else{
					url += "/my_tasks/" + this.taskID;
					this.isManager = true;
				}						
				this.$axios({
					 method:"get",
					 url: url,
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					console.log("任务信息");
					console.log(response);
					_this.showTaskInfomation = response.data;
					if(_this.showTaskInfomation.status == "pending"){
						_this.isOngoing = false;
					}else{
						_this.isOngoing = true;
					}
					if(_this.showTaskInfomation.tags == '问卷'){
						for(var k = 0; k < _this.showTaskInfomation.steps.length; k++){
							//console.log(_this.showTaskInfomation.steps[k]);
							if(_this.showTaskInfomation.steps[k].description != ''){
								var tempsigle = [];
								var temp = _this.showTaskInfomation.steps[k].description.split('&');
								//console.log(temp);
								for(var g = 1; g<temp.length;g++){
									var test = {};
									_this.$set(test,'label',temp[g]);
									tempsigle.push(test);
								}
								_this.$set(_this.showTaskInfomation.steps[k],'forsingle',tempsigle);
							}
						}
					}
					   if(_this.showTaskInfomation.participant_ids != null)
					   {
						   for(var i = 0 ;i < _this.showTaskInfomation.participant_ids.length;i++){					
								var url = "/users/" + _this.showTaskInfomation.participant_ids[i];
								var jwt = "JWT " + window.localStorage.getItem('token');
								_this.$axios({
									 method:"get",
									 url:url,
									 headers:{
										'Authorization': jwt,
									 }
								}).then(function (response){
									console.log("参与者信息");
									console.log(response);
									var test = {};
									_this.$set(test,'id',response.data.user_id);
									_this.$set(test,'phone_number',response.data.phone_number);
									_this.$set(test,'student_id',response.data.student_id);
									_this.$set(test,'name',response.data.name);
									_this.$set(test,'grade',response.data.grade);
									_this.$set(test,'school',response.data.school);
									_this.participant_info.push(test);
								}).catch(function (error) {
									_this.$Message.error('获取任务参与者的信息失败!');
								});
						   }
						   for(var i = 0 ;i < _this.showTaskInfomation.ongoing_participant_ids.length;i++){
								var url = "/users/" + _this.showTaskInfomation.ongoing_participant_ids[i];
								var jwt = "JWT " + window.localStorage.getItem('token');
								_this.$axios({
									 method:"get",
									 url:url,
									 headers:{
										'Authorization': jwt,
									 }
								}).then(function (response){
									console.log("正在参与任务信息");
									console.log(response);
									var test = {};
									_this.$set(test,'id',response.data.user_id);
									_this.$set(test,'phone_number',response.data.phone_number);
									_this.$set(test,'student_id',response.data.student_id);
									_this.$set(test,'name',response.data.name);
									_this.$set(test,'grade',response.data.grade);
									_this.$set(test,'school',response.data.school);
									_this.ongoing_participant_info.push(test);
								}).catch(function (error) {
									_this.$Message.error('获取任务参与者的信息失败!');
								});
						   }
						   for(var i = 0 ;i < _this.showTaskInfomation.waiting_examine_participant_ids.length;i++){
								var url = "/users/" + _this.showTaskInfomation.waiting_examine_participant_ids[i];
								var jwt = "JWT " + window.localStorage.getItem('token');
								_this.$axios({
									 method:"get",
									 url:url,
									 headers:{
										'Authorization': jwt,
									 }
								}).then(function (response){
									console.log("等待确认信息");
									console.log(response);
									var test = {};
									_this.$set(test,'id',response.data.user_id);
									_this.$set(test,'phone_number',response.data.phone_number);
									_this.$set(test,'student_id',response.data.student_id);
									_this.$set(test,'name',response.data.name);
									_this.$set(test,'grade',response.data.grade);
									_this.$set(test,'school',response.data.school);
									_this.waiting_examine_participant_info.push(test);
								}).catch(function (error) {
									_this.$Message.error('获取任务参与者的信息失败!');
								});
						   }
						   for(var i = 0 ;i < _this.showTaskInfomation.finished_participant_ids.length;i++){
								var url = "/users/" + _this.showTaskInfomation.finished_participant_ids[i];
								var jwt = "JWT " + window.localStorage.getItem('token');
								_this.$axios({
									 method:"get",
									 url:url,
									 headers:{
										'Authorization': jwt,
									 }
								}).then(function (response){
									console.log("完成实验");
									console.log(response);
									var test = {};
									_this.$set(test,'id',response.data.user_id);
									_this.$set(test,'phone_number',response.data.phone_number);
									_this.$set(test,'student_id',response.data.student_id);
									_this.$set(test,'name',response.data.name);
									_this.$set(test,'grade',response.data.grade);
									_this.$set(test,'school',response.data.school);
									_this.finished_participant_info.push(test);
								}).catch(function (error) {
									_this.$Message.error('获取任务参与者的信息失败!');
								});
						   }				   
					   }
				}).catch(function (error) {
					_this.$Message.error('获取任务信息失败!');
						//跳转到主页
						_this.$router.push({
							path: '/', 
							name: 'mainpage'
						});
					console.log(error);
				});	


				this.money = window.localStorage.getItem('money');
			    this.profilePhotoPath = window.localStorage.getItem('MyProfilePhotoPath');
			},
			sendRate(){
				//POST /users/:user_id/tasks/:task_id/feedback/:user_id HTTP/1.1
				// POST /users/:user_id/organizations/:organization_id/tasks/:task_id/feedback/:user_id HTTP/1.1
				var _this = this;
				var url_all = "/users/" + this.$data.userID ;
				if(this.isCreateByOrgan){
					url_all += "/organizations/" + this.organID + "/tasks/" + this.taskID;
				}
				else{
					url_all += "/tasks/" + this.taskID;
				}
				url_all += '/feedback/' + this.appraise.appId;
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$axios({
					 method:"post",
					 url: url_all,
					 data:{
						title:  this.appraise.title,
						content: this.appraise.content,
						rate: this.appraise.rate
					 },
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					_this.$Message.success('评价成功!');
				}).catch(function (error) {
					console.log(error);
				});			
				this.appraise.appId = 0;
				this.appraise.title = '';
				this.appraise.content = '';
				this.appraise.rate = 5;
				this.appraise.isShow = false;
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
				console.log(this.waiting_examine_participant_info[index]);
				var url = "/users/" + this.$data.userID + "/tasks/" + this.taskID+ "/finishers/" + this.waiting_examine_participant_info[index].id;
				var deleteID = this.waiting_examine_participant_info[index].id;
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$axios({
					 method:"put",
					 url: url,
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					_this.$Message.success('完成任务!');
					_this.appraise.isShow = true;
					_this.appraise.appId = deleteID;
					_this.showTaskInfomation.ongoing_participant_ids = response.data.ongoing_participant_ids;
					_this.showTaskInfomation.participant_ids = response.data.participant_ids;
					_this.waiting_examine_participant_info.splice(index,1);
					for(var i=0; i < _this.participant_info.length; i++)
					{
						if(_this.participant_info[i].id == deleteID)
						{
							_this.waiting_examine_participant_info.splice(i,1);
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
			deleteTask(){
				this.showdeleteTaskInfo = true;
			},
			showdeleteTaskInfoCancel(){
				this.showdeleteTaskInfo = false;
			},
			deleteTaskTrue(){
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
					 method:"delete",
					 url: url,
					 data:{
						task_id: this.taskID,
						task_name: this.showTaskInfomation.title,
					 },
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					_this.$Message.info('删除任务成功');
				    window.localStorage.removeItem('taskID');
					_this.$router.back();  
				}).catch(function (error) {
					console.log(error);
				});					
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
					_this.isOngoing = false;
				}).catch(function (error) {
					console.log(error);
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
			modifyTask(){
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