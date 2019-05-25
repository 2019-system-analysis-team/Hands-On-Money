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
						<Modal v-model="showTaskStepInfo">
							<p slot="header" style="text-align:center">
								<span>已完成步骤</span>
							</p>
							<div>
							<Card dis-hover>
								<Steps :current="current">
									<Step :title="item.title" v-for="item in showTaskInfomation.steps" :key="item.title">
									</Step>
								</Steps>
								<Button type="primary" @click="next" class="finshButton">完成当前步骤</Button>
							</Card>
							</div>
							<div slot="footer">
								<Button type="primary" @click="showTaskCancel">关闭</Button>
							</div>
						</Modal>
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
				showTaskStepInfo: false,
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
                        title: '邮箱',
                        key: 'email'
                    },
                    {
                        title: '电话',
                        key: 'phone_number'
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
                        title: '邮箱',
                        key: 'email'
                    },
                    {
                        title: '电话',
                        key: 'phone_number'
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
                        title: '邮箱',
                        key: 'email'
                    },
                    {
                        title: '电话',
                        key: 'phone_number'
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
                        title: '邮箱',
                        key: 'email'
                    },
                    {
                        title: '电话',
                        key: 'phone_number'
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
					task_id: 123456,
					creator_user_email: "i@sirius.com",
					creator_user_phone_number: "13123456789",
					creator_organization_name: "name",
					title: "一个标题",
					description: "一个描述",
					tags: ["tag1", "tag2", "tag3"],
					current_participant_number: 3,
					participant_number_limit: 10,
					reward_for_one_participant: 2,
					post_time: "date_obj",
					receive_end_time: "date_obj",
					finish_deadline_time: "date_obj",
					steps: [
						{
							title: "下楼",
							description: "下楼"
						},
						{
							title: "拿外卖",
							description: "拿外卖"
						}
					],
					"user_limit": {
						"age_upper": 0,
						"age_lower": 1,
						"grades": ["grade1", "grade1"],
						"sexes": ["sex_type1", "sex_type2", "sex_type3"],
						"schools": ["school_name1", "school_name2"]
					},
					"participant_ids": [123, 124, 125, 126],
					"ongoing_participant_ids": [123, 124],
					"waiting_examine_participant_ids": [125],
					"finished_participant_ids": [126],
				},
				ongoing_participant_info:[
					{
						"id": 123,
						"email": "a@163.com",
						"phone_number": "12345618912",
						"name": "123",
					},
					{
						"id": 124,
						"email": "b@163.com",
						"phone_number": "12345628912",
						"name": "124",
					},
					{
						"id": 125,
						"email": "c@163.com",
						"phone_number": "12345638912",
						"name": "125",
					},
					{
						"id": 126,
						"email": "d@163.com",
						"phone_number": "12345648912",
						"name": "126",
					},
				],
				waiting_examine_participant_info:[
					{
						"id": 125,
						"email": "c@163.com",
						"phone_number": "12345638912",
						"name": "125",
					},					
				],
				ongoing_participant_info:[
					{
						"id": 123,
						"email": "a@163.com",
						"phone_number": "12345618912",
						"name": "123",
					},
					{
						"id": 124,
						"email": "b@163.com",
						"phone_number": "12345628912",
						"name": "124",
					},					
				],
				finished_participant_info:[
					{
						"id": 126,
						"email": "d@163.com",
						"phone_number": "12345648912",
						"name": "126",
					},					
				],
				participant_info:[
					{
						"id": 123,
						"email": "a@163.com",
						"phone_number": "12345618912",
						"name": "123",
					},
					{
						"id": 124,
						"email": "b@163.com",
						"phone_number": "12345628912",
						"name": "124",
					},
					{
						"id": 125,
						"email": "c@163.com",
						"phone_number": "12345638912",
						"name": "125",
					},
					{
						"id": 126,
						"email": "d@163.com",
						"phone_number": "12345648912",
						"name": "126",
					},
				],
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
				current:0,
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
				let routerParams = this.$route.params.taskID;
				
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
				
				this.$data.userID = uID;

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
				var url_all = "/users/:" + this.$data.userID.toString() + "/session";
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
				this.showTaskStepInfo = true;
				/*
                this.$Modal.info({
                    title: '已完成步骤',
                    content: `名字：${this.ongoing_participant_info[index].name}<br>`
                })
				*/
            },
			showTaskCancel(){
				 this.$Message.info('Clicked cancel');
				 this.showTaskStepInfo = false;
			},
			next () {
                if (this.current == this.showTaskInfomation.steps.length - 1) {
                    this.$Message.info("完成任务");
                } else {
                    this.current += 1;
                }
            },
			toshowWithdrawInfo(){
				this.showWithdrawInfo = true;
			},
			showWithdrawInfoCancel(){
				this.showWithdrawInfo = false;
			},
			withdrawTask() {
				this.$Message.info('撤回任务成功');
				this.showWithdrawInfo = false;
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