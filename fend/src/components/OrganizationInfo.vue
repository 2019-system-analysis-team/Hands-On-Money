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
				<div class="content-head">
					<Avatar :src="organProfilePhotoPath" style="background-color: #87d068;" size="large">{{formValidate.name}}</Avatar>
					<span style="font-size: 30px;vertical-align: middle;margin-left: 10px;">{{formValidate.name}}</span>
				</div>
				<Tabs type="card" id="tabs" value="组织" v-model="tabs" :animated="false">
					<TabPane label="组织任务" name="组织任务">
						<Card dis-hover style="height: 500px">
							<p slot="title" style="height: 38px;">
								<Select v-model="taskclass" style="width:200px" @on-change="selectChange">
									<Option v-for="item in classifications" :value="item.value" :key="item.value">{{ item.label }}</Option>
								</Select>
							</p>
							<div slot="extra" v-if="isManager || isCreater">
								<Button type="primary" icon="ios-add" shape="circle">新建组织任务</Button>
							</div>	
							<Col span="8" v-for="item in selectTasks" :key="item.id" style="padding-left: 30px; padding-top: 50px;">
								<Card>
									<p slot="title">{{item.title}}</p>
									<div slot="extra">
										<Button type="primary" ghost>编辑</Button>
									</div>	
									<p>{{item.label}}</p>
									 
								</Card>
							</Col>
						</Card>		
					</TabPane>
					<TabPane label="组织信息" name="组织信息">
						<Card dis-hover style="height:380px">
							<p slot="title">组织信息如下</p>
							<Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80" class="form">
								<FormItem label="组织名称" prop="name">
									<Input v-model="formValidate.name" placeholder="请输入组织名称"></Input>
								</FormItem>
								<FormItem label="组织介绍" prop="desc">
									<Input v-model="formValidate.desc" type="textarea" :autosize="{minRows: 2,maxRows: 8}" ></Input>
								</FormItem>
								<FormItem>
									<Button type="primary" @click="handleSubmit('ruleValidate')" style="margin-left:89%">修改信息</Button>
								</FormItem>
							</Form>
						</Card>					
					</TabPane>
					<TabPane label="头像修改" name="头像修改">
						<Card dis-hover style="height:380px">
							<p slot="title">请上传新的头像</p>
							<Form ref="photo" :label-width="80" class="form">
								<FormItem label="头像" prop="photo">
									<div class="demo-upload-list" v-for="item in uploadList">
										<template v-if="item.status === 'finished'">
											<img :src="item.url">
											<div class="demo-upload-list-cover">
												<Icon type="ios-eye-outline" @click.native="handleView(item.name)"></Icon>
											</div>
										</template>
										<template v-else>
											<Progress v-if="item.showProgress" :percent="item.percentage" hide-info></Progress>
										</template>
									</div>
									<Tooltip content="点击上传头像">
										<Upload
											ref="upload"
											:headers ="jwt"
											:show-upload-list="false"
											:default-file-list="defaultList"
											:on-success="handleSuccess"
											:format="['jpeg']"
											:max-size="2048"
											:on-format-error="handleFormatError"
											:on-exceeded-size="handleMaxSize"
											:before-upload="handleBeforeUpload"
											:on-error="handleError"
											accept="image/jpeg"
											type="drag"
											:action= "organProfilePhotoUrl"
											style="display: inline-block;width:78px;">
											<div style="width: 78px;height:78px;line-height: 78px;">
												<Icon type="ios-camera" size="40"></Icon>
											</div>
										</Upload>
									</Tooltip>
									<Modal title="浏览头像" v-model="visible">
										<img :src="'https://o5wwk8baw.qnssl.com/' + imgName + '/avatar'" v-if="visible" style="width: 100%">
									</Modal>
								</FormItem>
							</Form>
						</Card>
					</TabPane>
					<TabPane label="管理成员" name="管理成员">
						<Card dis-hover style="height: 500px">
							<p slot="title" style="height: 38px;">
								全部成员
							</p>
							<div slot="extra" v-if="isManager || isCreater">
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
											<Option value="管理员">管理员</Option>
											<Option value="成员">成员</Option>
										</Select>	
									</FormItem>
								</Form>
							</Modal>
							<Col span="5" v-for="item in allMembers" :key="item.id" style="padding-left: 30px; padding-top: 30px;">
								<Card>
									<p slot="title">成员信息</p>
									<div slot="extra" v-if="isManager || isCreater">
										<Button type="error" ghost @click="deleteMember(item.userID)">删除</Button>
									</div>	
									<div style="width: 70%;float: left;">
										<p style="margin-bottom: 5px;">真实姓名 : {{item.name}}</p>
										<p style="margin-bottom: 5px;">昵称 : {{item.nickname}}</p>
										<p v-if="!(isManager || isCreater)">身份 : {{item.status}}</p>
										<div v-if="isManager || isCreater">
											身份 : 
											<Select v-model="item.status" style="width:70px" v-if="(item.status != '创建者')" @on-change="changeStatus(item)">
												<Option value="管理员">管理员</Option>
												<Option value="成员">成员</Option>
											</Select>
											<Select v-model="item.status" style="width:70px" disabled v-if="(item.status == '创建者')">
												<Option value="创建者" disabled>创建者</Option>
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
					<TabPane label="删除组织" name="删除组织" v-if="isCreater">
						<Card dis-hover style="height:380px">
							<p slot="title">请确认要删除组织</p>
							<Form ref="deleteValidate" :model="deleteValidate" :rules="deleteRuleValidate" :label-width="120" class="form">
								<FormItem label="该组织名称" prop="name">
									<Input v-model="deleteValidate.name" placeholder="请输入即将删除的组织名称"></Input>
								</FormItem>
								<FormItem>
									<Button type="error" @click="handleSubmit('deleteRuleValidate')" style="margin-left:89%">确认删除</Button>
								</FormItem>
							</Form>
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
				profilePhotoUrl:'',
				profilePhotoPath: '',
				profilePhotoName: '',
				
				organProfilePhotoUrl:'',
				organProfilePhotoPath: '',
				organProfilePhotoName: '',
								
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
                topupData: {
                    value: 1,
					mode: '支付宝',
                },
				
				taskclass:'进行中',
				classifications: [
				    {
				        value: '进行中',
				        label: '进行中'
				    },
				    {
				        value: '已结束',
				        label: '已结束'
				    },
				    {
				        value: '全部任务',
				        label: '全部任务'
				    }
				],		
				
                defaultList: [],
                imgName: '',
                visible: false,
				uploadList: [],
				jwt:{},
				organID:0,
				
				allTasks:[
					{
						title:'找绿帽子',
						label:'假装有标签',
						id:1,
					},
					{
						title:'找红帽子',
						label:'假装有标签',
						id:2,
					},
					{
						title:'找黄帽子',
						label:'假装有标签',
						id:3,
					},
					{
						title:'找蓝帽子',
						label:'假装有标签',
						id:4,
					},
				],
				inprogressTasks:[
					{
						title:'找绿帽子',
						label:'假装有标签',
						id:1,
					},
					{
						title:'找红帽子',
						label:'假装有标签',
						id:2,
					},
					{
						title:'找黄帽子',
						label:'假装有标签',
						id:3,
					},
				],
				finishedTasks:[
					{
						title:'找蓝帽子',
						label:'假装有标签',
						id:4,
					},
				],
				selectTasks:[],
				deleteValidate: {
					name: ''
				},
				deleteRuleValidate:{
                    name: [
                        { required: true, validator: validateDeleteNameCheck, trigger: 'blur' }
                    ],					
				},
			    formValidate: {
					 name: '红太阳',
					 desc: ''
				},
				ruleValidate: {
					 name: [
						 { required: true, validator: validateNameCheck, trigger: 'blur' }
					 ],
					 desc: [
						 {required: true, validator: validateDescCheck, trigger: 'blur' }
					 ]
				},
				allMembers:[
					{
						userID:1,
						nickname:'无敌',
						name:'潘茂林',
						status:'创建者',
						headPhotoPath:'',
						statusChanged:false
					},
					{
						userID:2,
						nickname:'雾霭',
						name:'潘茂森',
						status:'管理员',
						headPhotoPath:'',
						statusChanged:false
					},
					{
						userID:3,
						nickname:'爱迪生',
						name:'潘茂木',
						status:'成员',
						headPhotoPath:'',
						statusChanged:false
					}
				],
				isManager: false,
				isCreater: true,
				
				addMember:false,
				addMemberValidate:{
					addMemberType:'电话',
					addMemberInfo:'',
					addMemberStatus:'成员',
				},
				addMemberRuleValidate:{
					 addMemberInfo: [
						 { required: true, message: '该字段不能为空', trigger: 'blur' }
					 ],					
				}
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
				let routerParams = this.$route.params.organID;
				if(routerParams == null)
				{
					// 返回主页
					this.$router.push({
						path: '/', 
						name: 'mainpage',
					});	
				}
				//console.log("routerParams"+routerParams); 
				this.organID = routerParams;

				this.$data.profilePhotoName = '头像';
				//要用完全的路径
				this.$data.profilePhotoUrl = "/users/:"  + "profile_photo_path";


				let uID = window.localStorage.getItem('userID')
				if(uID == null || uID == ""){
					//跳转到主页
					this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				}
				var _this = this;
				var url = "/users/" + uID.toString() + "/organizations/" + organID.toString();
				this.$data.userID = uID;
				this.$data.profilePhotoUrl = "/users/:" + uID.toString() + "profile_photo_path";
				this.organProfilePhotoUrl = "/users/"+uID.toString()+"/organizations/"+  organID.toString() +"/profile_photo";
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$set(this.jwt,'Authorization',jwt);
				/*
				this.$axios({
						 method:"get",
						 url:url,
						 headers:{
							'Authorization': jwt,
						 }
				}).then(function (response){
					console.log(response);	
					//----------------------
					"name": "",
					"bio": "",
					"avg_comment": 0,
					"members":[
						{
							"user_id": 123,
							"status": "status"
						},
						{
							"user_id": 123,
							"status": "status"
						}
					]
					//---------------------
				}).catch(function (error) {
					_this.$Message.error('请先登录!');
					//跳转到主页
					_this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				});
				*/
			},
			handleView (name) {
                this.imgName = name;
                this.visible = true;
            },
            handleSuccess (res, file) {
				//从服务器获得图片路径，更改组织头像
				var url = "/users/:" + this.$data.userID.toString();
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$axios({
						 method:"get",
						 url:url,
						 headers:{
							'Authorization': jwt,
						 }
				}).then(function (response){
					console.log(response);
					this.$data.profilePhotoPath =  response.data.profile_photo_path;
					file.url = response.data.profile_photo_path;
					file.name = '头像';
				}).catch(function (error) {

				});
				this.$Message.success('修改头像成功!');
            },
            handleFormatError (file) {
                this.$Notice.warning({
                    title: '文件格式不正确',
                    desc: '文件 ' + file.name + ' 的格式不正确, 请选择 jpeg .'
                });
            },
            handleMaxSize (file) {
                this.$Notice.warning({
                    title: '超出文件大小限制',
                    desc: '文件  ' + file.name + ' 太大, 不能超过 2M.'
                });
            },
			handleError(error, file){
				if(this.$data.organProfilePhotoPath != ""){
					file.url = this.$data.organProfilePhotoPath;
					file.name = '头像';
				}
				this.$Message.error('修改头像失败!');
			},
            handleBeforeUpload () {
				// 如果之前上传过则删除
                const check = this.uploadList.length == 1;
                if (check) {
					this.$refs.upload.fileList.splice(0, 1);
                }
				else
				{
					return !check;
				}
                return check;
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
            handleSubmit (name) {
                this.$refs[name].validate((valid) => {
					//应该改为修改信息
                    if (valid) {
						var jwt = "JWT " + window.localStorage.getItem('token');
						var url = "/users/"+ this.$data.userID.toString() +"/organizations" + this.organID.toString();
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
							this.$Message.success('组织注册成功!');
							console.log(response);
							// 跳转到组织页面
						}).catch(function (error) {
							console.log(error);
						});
                        
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

					var jwt = "JWT " + window.localStorage.getItem('token');
					var url = "/users/"+ this.$data.userID.toString() +"/organizations" + this.organID.toString() + "/members";
					if (valid) {
						this.$Message.info('Clicked ok');
						if(this.addMemberValidate.addMemberType == '邮件'){
							this.$axios({
								 method:"post",
								 url: url,
								 data:{
									email: this.$data.addMemberValidate.addMemberInfo,
									statue: this.$data.addMemberValidate.addMemberStatus
								 },
								 headers:{
									'Authorization': jwt,
								 }
							}).then(function (response){
								console.log(response);
							}).catch(function (error) {
								console.log(error);
							});						
						}else{
							this.$axios({
								 method:"post",
								 url: url,
								 data:{
									phone_number: this.$data.addMemberValidate.addMemberInfo,
									statue: this.$data.addMemberValidate.addMemberStatus
								 },
								 headers:{
									'Authorization': jwt,
								 }
							}).then(function (response){
								console.log(response);
							}).catch(function (error) {
								console.log(error);
							});								
						}
					}
				});
            },
            addMembercancel () {
                this.$Message.info('Clicked cancel');
            },
			deleteMember(deleteUserID){
				var _this = this;
				var url_all = "/users/"+this.userID.toString()+"/organizations/"+this.organID.toString()+"/members/"+deleteUserID.toString();
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$axios({
					 method:"delete",
					 url: url_all,
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){

				}).catch(function (error) {
					console.log(error);
				});
			
			},
			modifyMemberStatus(item){
				var url_all = "/users/"+this.userID.toString()+"/organizations/"+this.organID.toString()+"/members/"+item.userID.toString();
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$axios({
					 method:"put",
					 url: url_all,
					 data:{
						statue: item.status
					 },
					 headers:{
						'Authorization': jwt,
					 }
				}).then(function (response){
					console.log(response);
				}).catch(function (error) {
					console.log(error);
				});		
				item.statusChanged = false;
			},
        },
        mounted () {
            this.uploadList = this.$refs.upload.fileList;
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
</style>