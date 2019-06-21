<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark" active-name="4-1">
                    <div class="layout-logo"></div>
                    <div class="layout-nav">
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
				<Tabs type="card" id="tabs" value="信息修改" v-model="tabs" :animated="false">
					<TabPane label="个人信息" name="个人信息">
						<Card dis-hover style="height:380px">
							<p slot="title">您的个人信息如下</p>
							<Form ref="personalValidate" :model="personalValidate" :rules="personalRuleValidate" :label-width="80" class="form">
								<FormItem label="综合评分" prop="rate">
									<Rate show-text allow-half v-model="average_comment" disabled >
										<span style="color: #f5a623">{{ average_comment }}</span>
									</Rate>
								</FormItem>	
								<FormItem label="昵称" prop="nickname">
									<Input v-model="personalValidate.nickname" placeholder="请输入您的昵称" :disabled="disabledPersonal"></Input>
								</FormItem>	
								<FormItem label="自我介绍" prop="desc">
									<Input v-model="personalValidate.desc" type="textarea" :autosize="{minRows: 2,maxRows: 5}" :disabled="disabledPersonal"></Input>
								</FormItem>
								<FormItem>
									<Button type="primary" @click="handleSubmit('personalValidate')" style="margin-left:89%">修改信息</Button>
								</FormItem>
							</Form>
						</Card>		
					</TabPane>
					<TabPane label="学校信息" name="学校信息">
						<Card dis-hover style="height:380px">
							<p slot="title">您的学校信息如下</p>
							<Form ref="schoolValidate" :model="schoolValidate" :rules="schoolRuleValidate" :label-width="80" class="form">
								<FormItem label="学院" prop="school">
									<Select v-model="schoolValidate.school" :disabled="disabledSchool">
										<Option value="中国语言文学系">中国语言文学系</Option>
										<Option value="历史学系">历史学系</Option>
										<Option value="哲学系">哲学系</Option>
										<Option value="社会学与人类学学院">社会学与人类学学院</Option>
										<Option value="博雅学院">博雅学院</Option>
										<Option value="岭南学院">岭南学院</Option>
										<Option value="外国语学院">外国语学院</Option>
										<Option value="法学院">法学院</Option>
										<Option value="政治与公共事务管理学院">政治与公共事务管理学院</Option>
										<Option value="管理学院">管理学院</Option>
										<Option value="马克思主义学院">马克思主义学院</Option>
										<Option value="心理学系">心理学系</Option>
										<Option value="传播与设计学院">传播与设计学院</Option>
										<Option value="资讯管理学院">资讯管理学院</Option>
										<Option value="艺术学院">艺术学院</Option>
										<Option value="数学学院">数学学院</Option>
										<Option value="物理学院">物理学院</Option>
										<Option value="化学学院">化学学院</Option>
										<Option value="地理科学与规划学院">地理科学与规划学院</Option>
										<Option value="生命科学学院">生命科学学院</Option>
										<Option value="工学院">工学院</Option>
										<Option value="材料科学与工程学院">材料科学与工程学院</Option>
										<Option value="电子与信息工程学院">电子与信息工程学院</Option>
										<Option value="数据科学与计算机学院">数据科学与计算机学院</Option>
										<Option value="国家保密学院">国家保密学院</Option>
										<Option value="网络安全学院">网络安全学院</Option>
										<Option value="环境科学与工程学院">环境科学与工程学院</Option>
										<Option value="系统科学与工程学院">系统科学与工程学院</Option>
										<Option value="中山医学院">中山医学院</Option>
										<Option value="光华口腔医学院">光华口腔医学院</Option>
										<Option value="公共卫生学院">公共卫生学院</Option>
										<Option value="药学院">药学院</Option>
										<Option value="护理学院">护理学院</Option>
										<Option value="逸仙学院">逸仙学院</Option>
									</Select>
								</FormItem>
								<FormItem label="年级" prop="grade">
									<Select v-model="schoolValidate.grade" :disabled="disabledSchool">
										<Option value="大一">大一</Option>
										<Option value="大二">大二</Option>
										<Option value="大三">大三</Option>
										<Option value="大四">大四</Option>
										<Option value="研究生">研究生</Option>
										<Option value="博士生">博士生</Option>
									</Select>
								</FormItem>
								<FormItem label="学号" prop="stunumber">
									<Input v-model="schoolValidate.stunumber" placeholder="请输入您的学号" :disabled="disabledSchool"></Input>
								</FormItem>
								<FormItem>
									<Button type="primary" @click="handleSubmit('schoolValidate')" style="margin-left:89%">修改信息</Button>
								</FormItem>
							</Form>
						</Card>		
					</TabPane>
					<TabPane label="详细信息" name="详细信息">
						<Card dis-hover style="height:380px">
							<p slot="title">您的详细信息如下</p>
							<Form ref="infoValidate" :model="infoValidate" :rules="infoRuleValidate" :label-width="80" class="form">
								<FormItem label="真实姓名" prop="name">
									<Input v-model="infoValidate.name" placeholder="请输入您的真实姓名" :disabled="disabledInfo"></Input>
								</FormItem>
								<FormItem label="年龄" prop="age">
									<Select v-model="infoValidate.age" :disabled="disabledInfo">
										<Option v-for="item in ageoptionsList" :value="item.value" :key="item.value">{{ item.label }}</Option>
									</Select>						
								</FormItem>
								<FormItem label="性别" prop="gender">
									<RadioGroup v-model="infoValidate.gender" :disabled="disabledInfo">
										<Radio label="女生">女生</Radio>
										<Radio label="男生">男生</Radio>
									</RadioGroup>
								</FormItem>
								<FormItem>
									<Button type="primary" @click="handleSubmit('infoValidate')" style="margin-left:89%">修改信息</Button>
								</FormItem>
							</Form>
						</Card>						
					</TabPane>
					<TabPane label="头像修改" name="头像修改">
						<Card dis-hover style="height:380px">
							<p slot="title">请上传新的头像</p>
							<Form ref="pwdValidate" :model="pwdValidate" :rules="pwdRuleValidate" :label-width="80" class="form">
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
											:format="['jpeg','jpg','png','bmp']"
											:max-size="2048"
											:on-format-error="handleFormatError"
											:on-exceeded-size="handleMaxSize"
											:before-upload="handleBeforeUpload"
											:on-error="handleError"
											accept="image/jpeg,image/jpg, image/png, image/bmp"
											type="drag"
											:action= "profilePhotoUrl"
											style="display: inline-block;width:78px;">
											<div style="width: 78px;height:78px;line-height: 78px;">
												<Icon type="ios-camera" size="40"></Icon>
											</div>
										</Upload>
									</Tooltip>
									<Modal title="浏览头像" v-model="visible">
										<img :src= "profilePhotoPath" v-if="visible" style="width: 100%">
										<div slot="footer">
											<Button type="info" size="large" long @click="visible = false;">确认</Button>
										</div>
									</Modal>
								</FormItem>
							</Form>
						</Card>
					</TabPane>
					<TabPane label="密码修改" name="密码修改">
						<Card dis-hover style="height:380px">
							<p slot="title">请输入新的密码</p>
							<Form ref="pwdValidate" :model="pwdValidate" :rules="pwdRuleValidate" :label-width="80" class="form">
									<FormItem label="旧密码" prop="oldpasswd" >
										<Input type="password" v-model="pwdValidate.oldpasswd" placeholder="请输入您的旧密码" :disabled="disabledPwd"></Input>
									</FormItem>
									<FormItem label="新密码" prop="passwd" >
										<Input type="password" v-model="pwdValidate.passwd" placeholder="请输入您的新密码" :disabled="disabledPwd"></Input>
									</FormItem>
									<FormItem label="确认密码" prop="passwdCheck" >
										<Input type="password" v-model="pwdValidate.passwdCheck" placeholder="请再次输入您的密码" :disabled="disabledPwd"></Input>
									</FormItem>		
									<FormItem>
										<Button type="primary" @click="handleSubmit('pwdValidate')" style="margin-left:89%">修改密码</Button>
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
            const validatePass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入您的密码'));
                } else if (value.toLocaleString().length < 7) {
					callback(new Error('密码不能小于7位'));
				} else {
                    if (this.pwdValidate.passwdCheck !== '') {
                        // 对第二个密码框单独验证
                        this.$refs.pwdValidate.validateField('passwdCheck');
                    }
                    callback();
                }
            };
            const validatePassCheck = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入您的密码'));
                } else if (value !== this.pwdValidate.passwd) {
                    callback(new Error('两次输入的密码不一致'));
                } else {
                    callback();
                }
            };
            const validateoldPassCheck = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入您的旧密码'));
                } else if (value === this.pwdValidate.passwd) {
                    callback(new Error('新密码和旧密码不能相同'));
                } else {
                    callback();
                }
            };
			const validateNicknameCheck = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('昵称不能为空'));
                } else if (value.toLocaleString().length > 15) {
                    callback(new Error('昵称不能多于15个字符'));
                } else {
                    callback();
                }
            };
			const validateNameCheck = (rule, value, callback) => {
				if (value.toLocaleString().length > 10) {
			        callback(new Error('姓名不能多于10个字符'));
			    } else {
			        callback();
			    }
			};
			const validateStuNumberCheck = (rule, value, callback) => {
				var numReg = /[^\d]/g;
				var numRe = new RegExp(numReg);
				if(value === ''){
					callback();
				}
				if (!numRe.test(value) && value.length == 8){
					callback();
				}else{
					callback(new Error('学号为8位数字'));
				}
			};
			const validatePhoneCheck = (rule, value, callback) => {
				var numReg = /[^\d]/g;
				var numRe = new RegExp(numReg);
				if (!numRe.test(value) && value.length == 11){
					callback();
				}else{
					callback(new Error('电话为11位数字'));
				}
			};
            return {
				isWithdraw:false,
				profilePhotoUrl:'',
				profilePhotoPath: '',
				profilePhotoName: '',
				userID: '',
				tabs: '个人信息',
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
				ageoptionsList:[],
				disabledPersonal: true,
				disabledSchool: true,
				disabledInfo: true,
				disabledPwd: true,
				personalValidate:{
					nickname: '',
					desc: ''
				},
				personalRuleValidate:{
					nickname: [
                        { required: true, validator: validateNicknameCheck, trigger: 'blur' }
                    ]	
				},
				schoolValidate:{
					school: '',
					stunumber: '',
					grade: ''
				},
				schoolRuleValidate:{
                    stunumber: [
                        {validator: validateStuNumberCheck, trigger: 'blur' }
                    ],
				},				
				infoValidate:{
					name: '',
					age: '',
					gender: ''	
				},
                infoRuleValidate: {
                    name: [
                        {validator: validateNameCheck, trigger: 'blur' }
                    ]
                },
				pwdValidate:{
                    passwd: '',
                    passwdCheck: '',
					oldpasswd:'',
				},
                defaultList: [{name:'profile',url:'default.jpg'}],
                imgName: '',
                visible: false,
				uploadList: [],
				jwt:{},
				pwdRuleValidate:{
                    passwd: [
                        { required: true, validator: validatePass, trigger: 'blur' }
                    ],
                    passwdCheck: [
                        { required: true, validator: validatePassCheck, trigger: 'blur' }
                    ],
                    oldpasswd: [
                        { required: true, validator: validateoldPassCheck, trigger: 'blur' }
                    ]	
				},
				average_comment:0,
            }
        },
		created: function () { 
			this.getEventData();
		},
        methods: {
			getEventData:function() {
				var i = 10;
				for(;i<=30;i++){
					this.$data.ageoptionsList.push({label:i.toString(),value:i.toString()});
				}
				this.$data.profilePhotoName = '头像';

				let uID = window.localStorage.getItem('userID');

				if(uID == null || uID == ""){
					_this.$Message.error('请先登录!');
					//跳转到主页
					this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				}

				var url = "/users/" + uID;
				this.$data.userID = uID;
				this.$data.profilePhotoUrl = "/users/" + uID + "/profile_photo";
				var jwt = "JWT " + window.localStorage.getItem('token');
				//设置jwt认证头部
				this.$set(this.jwt,'Authorization',jwt);
				//console.log(this.jwt);
	
				var _this = this;
				this.$axios({
						 method:"get",
						 url:url,
						 headers:{
							'Authorization': jwt,
						 }
				}).then(function (response){
					console.log(response);
					_this.$data.personalValidate.nickname = response.data.nickname;
					_this.$data.personalValidate.desc = response.data.bio;
					_this.$data.schoolValidate.school = response.data.school;
					_this.$data.schoolValidate.stunumber = response.data.student_id;
					_this.$data.schoolValidate.grade = response.data.grade;
					_this.$data.infoValidate.name = response.data.name;
					_this.$data.infoValidate.age = response.data.age.toString();
					_this.$data.infoValidate.gender = response.data.sex;		
					_this.$data.money = response.data.balance;
					_this.$data.profilePhotoPath =  _this.$profilePath + response.data.profile_photo_path;
					_this.average_comment = response.data.average_comment;
					window.localStorage.setItem('money',_this.$data.money);
					window.localStorage.setItem('MyProfilePhotoPath', _this.$data.profilePhotoPath);
					var test = {};
					_this.$set(test,'name',_this.profilePhotoName);
					_this.$set(test,'status','finished');
					_this.$set(test,'url',_this.profilePhotoPath);
					_this.uploadList.push(test);
				}).catch(function (error) {
					_this.$Message.error('获取个人信息失败');
					//跳转到主页
					_this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				});
			},
            handleSubmit (name) {
				if(this.tabs == "个人信息" && this.disabledPersonal == true){
					this.disabledPersonal = false;
					return;
				}
				if(this.tabs == "学校信息" && this.disabledSchool == true){
					this.disabledSchool = false;
					return;
				}
				if(this.tabs == "详细信息" && this.disabledInfo == true){
					this.disabledInfo = false;
					return;
				}
				if(this.tabs == "密码修改" && this.disabledPwd == true){
					this.disabledPwd = false;
					return;
				}
				var _this = this;
                this.$refs[name].validate((valid) => {
					var url_all = "/users/" + this.$data.userID;
					var jwt = "JWT " + window.localStorage.getItem('token');
                    if (valid) {
						if(this.tabs == "个人信息"){
							var url_id = url_all + "/personality";
							this.$axios({
								 method:"put",
								 url: url_id,
								 data:{
									nickname: this.$data.personalValidate.nickname,
									bio: this.$data.personalValidate.desc
								 },
								 headers:{
									'Authorization': jwt,
								 }
							}).then(function (response){
								_this.$Message.success('修改成功!');
								_this.disabledPersonal = true;
							}).catch(function (error) {
								console.log(error);
							});
						}else if(this.tabs == "学校信息"){
							var url_school = url_all + "/school";
							this.$axios({
								 method:"put",
								 url: url_school,
								 data:{
									school: this.$data.schoolValidate.school,
									grade: this.$data.schoolValidate.grade,
									student_id: this.$data.schoolValidate.stunumber
								 },
								 headers:{
									'Authorization': jwt,
								 }
							}).then(function (response){
								_this.$Message.success('修改成功!');
								_this.disabledSchool = true;
							}).catch(function (error) {
								console.log(error);
							});
						}else if(this.tabs == "详细信息"){
							var url_info = url_all + "/personal_info";
							this.$axios({
								 method:"put",
								 url: url_info,
								 data:{
									name: this.$data.infoValidate.name,
									age: this.$data.infoValidate.age,
									sex: this.$data.infoValidate.gender
								 },
								 headers:{
									'Authorization': jwt,
								 }
							}).then(function (response){
								_this.$Message.success('修改成功!');
								_this.disabledInfo = true;
							}).catch(function (error) {
								console.log(error);
							});
						}else if(this.tabs == "密码修改"){
							_this.$Message.success('修改成功!');
							_this.disabledPwd = true;
						}
                    } else {
                        _this.$Message.error('信息填写有误!');
                    }
                })
            },
            handleReturnHomepage () {
                // 返回主页
				this.$router.push({
					path: '/', 
					name: 'mainpage',
				});		
            },
			handleView (name) {
                this.imgName = name;
                this.visible = true;
            },
            handleSuccess (res, file) {

            },
            handleFormatError (file) {
                this.$Notice.warning({
                    title: '文件格式不正确',
                    desc: '文件 ' + file.name + ' 的格式不正确, 请选择 jpeg jpg png bmp.'
                });
            },
            handleMaxSize (file) {
                this.$Notice.warning({
                    title: '超出文件大小限制',
                    desc: '文件  ' + file.name + ' 太大, 不能超过 2M.'
                });
            },
			handleError(error, dom, file){
				//console.log(file);
				var jwt = "JWT " + window.localStorage.getItem('token');
				var _this = this;
				let param = new FormData(); // 创建form对象
				param.append('file', file); // 将文件存入file下面
				this.$axios({
					 method:"post",
					 url: this.profilePhotoUrl,
					 data:param,
					 headers:{
						'Authorization': jwt,
						'Content-Type': 'multipart/form-data',
					 }
				}).then(function (response){
					//console.log(response.data);
					_this.$Message.success('修改头像成功!');
					//_this.$router.go(0);
					var url = "/users/" + _this.$data.userID;
					_this.$axios({
							 method:"get",
							 url:url,
							 headers:{
								'Authorization': jwt,
							 }
					}).then(function (response){
						_this.profilePhotoPath =  _this.$profilePath + response.data.profile_photo_path;
						window.localStorage.setItem('MyProfilePhotoPath', _this.profilePhotoPath);
						var test = {};
						_this.$set(test,'name',_this.profilePhotoName);
						_this.$set(test,'status','finished');
						_this.$set(test,'url',_this.profilePhotoPath);
						const check = _this.uploadList.length == 1;
						
						if (check) {
							_this.uploadList.splice(0, 1);
						}
						_this.uploadList.push(test);
						//console.log(_this.defaultList);
					}).catch(function (error) {
						_this.$Message.error('获取个人信息失败');
					});
				
				}).catch(function (error) {
					console.log(error);
				});
				
			},
            handleBeforeUpload () {
                return true;
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
				var url_all = "/users/" + this.$data.userID+ "/session";
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
			createNewTask() {
				window.localStorage.removeItem('organID');
				window.localStorage.removeItem('taskID');
				this.$router.push({
					path: '/', 
					name: 'missioncreate'
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

</style>