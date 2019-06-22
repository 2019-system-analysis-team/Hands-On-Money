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
								<Button type="success" shape="circle"  @click="show()" v-show="this.showTaskInfomation.tags != '问卷'">完成任务</Button>
								<Button type="success" shape="circle"  @click="show()" v-show="this.showTaskInfomation.tags == '问卷'">填写问卷</Button>
							</div>	
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
						<Modal v-model="showQuestionList">
							<p slot="header" style="text-align:center">
								<span>请填写以下问卷</span>
							</p>
							<div>
						
									<p style="background:#eee;padding: 20px;height: 500px; overflow: auto;" >
										<Card v-for="(item,index) in showTaskInfomation.steps" :key="item.title"  dis-hover>
											<p>问题 {{index+1}} : {{item.title}}</P> 
											<Input v-model="item.description" placeholder="请输入问题回答" v-show="item.forsingle == null || item.forsingle.length == 0"></Input>
											<p v-show="item.forsingle != null && item.forsingle.length != 0">单选选项：</P>
											<RadioGroup v-show="item.forsingle != null && item.forsingle.length != 0" v-model = "choiceList[index]" @on-change="selectChange(value,index)">
												<Radio v-for="single in item.forsingle" :key="single.label" :label="single.label"></Radio>
											</RadioGroup>
										</Card>
									</p>
					
							</div>
							<div slot="footer">
								<Button type="primary" @click="showQuestionListCancel">关闭</Button>
								<Button type="primary" @click="FinishQuestionList">完成问卷</Button>
							</div>
						</Modal>
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
								<Button type="primary" @click="next" class="finshButton" v-show="!isNullStep">完成当前步骤</Button>
								<Button type="primary" @click="next" class="finshButton" v-show="isNullStep">确认已完成任务</Button>
							</Card>
							</div>
							<div slot="footer">
								<Button type="primary" @click="showTaskCancel">关闭</Button>
							</div>
						</Modal>
						<Modal v-model="appraise.isShow">
							<p slot="header" style="text-align:center">
								<span>请评价此次任务</span>
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
				appraise:{
					isShow: false,
					title: '',
					content: '',
					rate: 5,
				},
				isWithdraw:false,
				showTaskStepInfo: false,
                showQuestionList: false,
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
			
				current:0,
				isCreateByOrgan:false,
				organID:null,
				isNullStep:false,
				choiceList:[],
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
				let routerParams = window.localStorage.getItem('taskID');
				let organID = window.localStorage.getItem('organID');
				this.current = this.$route.params.current_step;
				console.log("现在步骤:" + this.current);
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
				
				this.$data.userID = uID;
				
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
					 method:"get",
					 url: url,
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					console.log("任务信息");
					console.log(response);
					_this.showTaskInfomation = response.data;
					if(_this.showTaskInfomation.steps.length == 0)
					{
						_this.isNullStep = true;
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
								_this.choiceList.push(tempsigle[0].label);
								_this.$set(_this.showTaskInfomation.steps[k],'forsingle',tempsigle);
							}else{
								_this.choiceList.push('');
							}
						}
						console.log(_this.choiceList);
					}
				}).catch(function (error) {
					_this.$Message.error('获取任务信息失败!');
					console.log(error);
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
			logout (){
				var _this = this;
				var url_all = "/users/" + this.$data.userID + "/session";
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
			selectChange(value,index){
				console.log("选择:"+this.choiceList[index]);
			},
			sendRate(){
				//POST /users/:user_id/tasks/:task_id/comment
				var _this = this;
				var url_all = "/users/" + this.$data.userID + "/tasks/" + this.taskID + "/comment";
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
				this.appraise.isShow = false;
				this.showTaskStepInfo = false;
				this.showQuestionList = false;
			},
            show (index) {
				if(this.showTaskInfomation.tags == '问卷'){
					this.showQuestionList = true;
				}else{
					this.showTaskStepInfo = true;
				}
            },
			showTaskCancel(){
				 //this.$Message.info('Clicked cancel');
				 this.showTaskStepInfo = false;
			},
			showQuestionListCancel(){
			    //this.$Message.info('Clicked cancel');
				this.showQuestionList = false;
			},
			FinishQuestionList(){
				for(var i=0; i < this.choiceList.length;i++){
					if(this.choiceList[i] != ''){
						this.showTaskInfomation.steps[i].description = this.choiceList[i];
					}
				}
				for(var i=0;i < this.showTaskInfomation.steps.length;i++){
					if(this.showTaskInfomation.steps[i].description == ''){
						 this.$Message.info("请将问卷填写完整");
						 return;
					}
					console.log(this.showTaskInfomation.steps[i].description );
				}
					// PUT /users/:user_id/tasks/:task_id/steps/:step_id
					var _this = this;
					var url_all = "/users/" + this.$data.userID + "/tasks/" + this.taskID + "/steps/" + 0;
					var jwt = "JWT " + window.localStorage.getItem('token');
					this.$axios({
						 method:"put",
						 url: url_all,
						 data:{
							task_id:  this.taskID,
							task_finished_steps: 0
						 },
						 headers:{
							'Authorization': jwt,
						 }
					}).then(function (response){
						_this.$Message.success('填写问卷成功!');
					    //_this.current += 1;
						 _this.appraise.isShow = true;
					}).catch(function (error) {
						console.log(error);
						_this.$Message.error('已问卷，请勿重复点击!');
					});		
			},
			next () {
				if(this.isNullStep){
					 this.$Message.info("成功完成任务,等待对方确认");
					 this.appraise.isShow = true;
					 return;
				}
				if(this.showTaskInfomation.tags == '问卷')
				{
					// PUT /users/:user_id/tasks/:task_id/steps/:step_id
					var _this = this;
					var url_all = "/users/" + this.$data.userID + "/tasks/" + this.taskID + "/steps/" + 0;
					var jwt = "JWT " + window.localStorage.getItem('token');
					this.$axios({
						 method:"put",
						 url: url_all,
						 data:{
							task_id:  this.taskID,
							task_finished_steps: 0
						 },
						 headers:{
							'Authorization': jwt,
						 }
					}).then(function (response){
						_this.$Message.success('填写问卷成功!');
					    //_this.current += 1;
						 _this.appraise.isShow = true;
					}).catch(function (error) {
						console.log(error);
						_this.$Message.error('已问卷，请勿重复点击!');
					});					
				}
				else
				{
					// PUT /users/:user_id/tasks/:task_id/steps/:step_id
					var _this = this;
					var url_all = "/users/" + this.$data.userID + "/tasks/" + this.taskID + "/steps/" + (this.current+1);
					var jwt = "JWT " + window.localStorage.getItem('token');
					this.$axios({
						 method:"put",
						 url: url_all,
						 data:{
							task_id:  this.taskID,
							task_finished_steps: this.current+1
						 },
						 headers:{
							'Authorization': jwt,
						 }
					}).then(function (response){
						_this.$Message.success('完成一个步骤成功!');
						if(_this.showTaskInfomation.steps.length == _this.current+1)
						{
							_this.appraise.isShow = true;
						}
					    _this.current += 1;
					}).catch(function (error) {
						console.log(error);
						_this.$Message.error('已完成任务，请勿重复点击!');
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