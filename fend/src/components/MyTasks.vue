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
					<TabPane label="我的任务" name="我的任务">
						<Card dis-hover style="height: 500px">
							<p slot="title" style="height: 38px;">
								<Select v-model="taskclass" style="width:200px" @on-change="selectChange">
									<Option v-for="item in classifications" :value="item.value" :key="item.value">{{ item.label }}</Option>
								</Select>
							</p>
							<div slot="extra">
								<Button type="primary" icon="ios-add" shape="circle">创建个人任务</Button>
							</div>	
							<Col span="8" v-for="item in selectTasks" :key="item.id" style="padding-left: 30px; padding-top: 50px;">
								<Card>
									<p slot="title">{{item.task_name}}</p>
									<div slot="extra">
										<Button type="primary" ghost @click="LookTaskInfo(item.task_id)">详情</Button>
									</div>	
									<p>{{item.status}}</p>
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
									<p class="info">创建者名字 : {{showTaskInfomation.creator_organization_name}}</p>
									<p class="info">创建者邮箱 : {{showTaskInfomation.creator_user_email}}</p>
									<p class="info">创建者电话 : {{showTaskInfomation.creator_user_phone_number}}</p>
									<p class="info">任务发布时间 : {{showTaskInfomation.post_time}}</p>
									<p class="info">截止接受任务时间 : {{showTaskInfomation.receive_end_time}}</p>
									<p class="info">最迟完成任务时间 : {{showTaskInfomation.finish_deadline_time}}</p>
									<p class="info">步骤 : </p>
									<Steps :current="showTaskInfomation.current">
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
					current: -1
				},
				selectTasks:[],
				allTasks:[
					{
						task_id: 123,
						task_name: "填写问卷",
						status: "进行中"
					},
					{
						task_id: 124,
						task_name: "拿快递",
						status: "已结束"
					}
				],
				finishedTasks:[
					{
						task_id: 124,
						task_name: "拿快递",
						status: "已结束"						
					}
				],
				inprogressTasks:[
					{
						task_id: 123,
						task_name: "填写问卷",
						status: "进行中"
					}
				],
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
				let uID = window.localStorage.getItem('userID')
				if(uID == null || uID == ""){
					//跳转到主页
					this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				}
				this.$data.userID = uID;
				this.selectTasks = this.allTasks;
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
				if(value == '已结束'){
					this.selectTasks = this.finishedTasks;
				}else if(value == '进行中'){
					this.selectTasks = this.inprogressTasks;
				}else if(value == '全部任务'){
					this.selectTasks = this.allTasks;
				}
			},
			LookTaskInfo(taskId){
				this.showTaskInfo = true;
				this.showTaskInfomation.task_id = taskId;
			},
			showTaskOK(){
				 this.$Message.info('Clicked OK');
			},
			showTaskCancel(){
				 this.$Message.info('Clicked cancel');
				 this.showTaskInfo = false;
			},
			ToTaskInfo(taskID){
				this.$router.push({
					path: '/', 
					name: 'taskinfoforcreate',
					params: { 
							taskID: taskID
					},
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
.info {	
    margin-bottom: 10px;
}
</style>