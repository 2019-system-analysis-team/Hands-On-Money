<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark" active-name="1">
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
							<MenuItem name="2-1">我的组织</MenuItem>
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
						<Button type="default" ghost v-on:click="login">登录</Button>
						<Button type="primary" ghost v-on:click="register">注册</Button>
					</div>
					<div class="layout-button" v-if="isLogin">
						<Submenu name="4">
							<template slot="title">
								<Avatar :src="profilePhotoPath" style="background-color: #87d068">{{shownickname}}</Avatar>
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
                    <div style="min-height: 200px;">
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
				profilePhotoPath: '',
				shownickname:'',
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
				haveTask: false
			};
		}, 
		created: function () { 
			//在created阶段初始化
			this.getEventData();
		},
		methods: {
			getEventData:function() {
				this.$data.shownickname = 'hhhh';
				/*
				let uID = window.localStorage.getItem('userID')
				if(uID == null || uID == ""){
					this.isLogin = false;
				}
				var url = "/users/:" + uID.toString();
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
					this.userID = uID;
					this.isLogin = true;
					this.profilePhotoPath = response.data.profile_photo_path;
				}).catch(function (error) {
					console.log(error.data.error_msg);
					this.isLogin = false;
				});
				*/
			   if(this.profilePhotoPath == ''){
				   
			   }
			},
			login: function () {
				this.$router.push({
						path: '/userlogin'
				});			
			},
			register: function () {
				this.$router.push({
						path: '/userregister'
				});		
			},
			logout (){
				if(this.isLogin){
					var url_all = "/users/:" + this.$data.userID.toString() + "/session";
					var jwt = "JWT " + window.localStorage.getItem('token');
					this.$axios({
						 method:"delete",
						 url: url_all,
						 headers:{
							'Authorization': jwt,
						 }
					}).then(function (response){
						this.isLogin = false;
						this.userID = '';
						window.localStorage.setItem('token', "");
						window.localStorage.setItem('userID', "");
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
</style>
