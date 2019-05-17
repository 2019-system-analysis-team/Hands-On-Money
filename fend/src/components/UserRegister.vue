<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark">
					<div class="layout-head">
						个人注册
					</div>
					<div class="home-button">
						<Button shape="circle" icon="ios-home" @click="handleReturnHomepage()"></Button>
					</div>
				</Menu>
            </Header>
            <Content :style="{padding: '50px 50px'}">
				<Card :bordered="false">
					<p slot="title">请填写下列信息</p>
					<Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80" id="form">
						<FormItem label="电话" prop="phone">
							<Input v-model="formValidate.phone" placeholder="请输入您的电话号码" ></Input>
						</FormItem>
						<FormItem label="E-mail" prop="mail">
							<Input v-model="formValidate.mail" placeholder="请输入您的邮箱" ></Input>
						</FormItem>
						<FormItem label="密码" prop="passwd" >
							<Input type="password" v-model="formValidate.passwd" placeholder="请输入您的密码"></Input>
						</FormItem>
						<FormItem label="确认密码" prop="passwdCheck" >
							<Input type="password" v-model="formValidate.passwdCheck" placeholder="请再次输入您的密码"></Input>
						</FormItem>
						<FormItem label="昵称" prop="nickname">
							<Input v-model="formValidate.nickname" placeholder="请输入您的昵称"></Input>
						</FormItem>
						<FormItem label="真实姓名" prop="name">
							<Input v-model="formValidate.name" placeholder="请输入您的真实姓名"></Input>
						</FormItem>
						<FormItem label="学号" prop="stunumber">
							<Input v-model="formValidate.stunumber" placeholder="请输入您的学号"></Input>
						</FormItem>
						<FormItem label="年级" prop="grade">
							<Select v-model="formValidate.grade">
								<Option value="大一">大一</Option>
								<Option value="大二">大二</Option>
								<Option value="大三">大三</Option>
								<Option value="大四">大四</Option>
								<Option value="研究生">研究生</Option>
								<Option value="博士生">博士生</Option>
							</Select>
						</FormItem>
						<FormItem label="性别" prop="gender">
							<RadioGroup v-model="formValidate.gender">
								<Radio label="女生">女生</Radio>
								<Radio label="男生">男生</Radio>
							</RadioGroup>
						</FormItem>
						<FormItem label="学院" prop="school">
							<Select v-model="formValidate.school">
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
						<FormItem label="年龄" prop="age">
						    <Select v-model="formValidate.age" >
								<Option v-for="item in ageoptionsList" :value="item.value" :key="item.value">{{ item.label }}</Option>
							</Select>						
						</FormItem>
						<FormItem label="自我介绍" prop="desc">
							<Input v-model="formValidate.desc" type="textarea" :autosize="{minRows: 2,maxRows: 5}"></Input>
						</FormItem>
						<FormItem>
							<Button type="primary" @click="handleSubmit('formValidate')">提交</Button>
							<Button @click="handleReset('formValidate')" style="margin-left: 8px">重置</Button>
						</FormItem>
					</Form>
				</Card>
            </Content>
            <Footer class="layout-footer-center">2019-2019 &copy; SYSU</Footer>
        </Layout>
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
                    if (this.formValidate.passwdCheck !== '') {
                        // 对第二个密码框单独验证
                        this.$refs.formValidate.validateField('passwdCheck');
                    }
                    callback();
                }
            };
            const validatePassCheck = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入您的密码'));
                } else if (value !== this.formValidate.passwd) {
                    callback(new Error('两次输入的密码不一致'));
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
			    if (value === '') {
			        callback(new Error('姓名不能为空'));
			    } else if (value.toLocaleString().length > 10) {
			        callback(new Error('姓名不能多于10个字符'));
			    } else {
			        callback();
			    }
			};
			const validateStuNumberCheck = (rule, value, callback) => {
				var numReg = /[^\d]/g;
				var numRe = new RegExp(numReg);
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
				ageoptionsList:[],
                formValidate: {
					nickname: '',
                    name: '',
					stunumber: '',
					grade: '大一',
					school: '中国语言文学系',
					age: '18',
					phone: '',
                    mail: '',
                    gender: '女生',
                    desc: '',
                    passwd: '',
                    passwdCheck: '',
                },
                ruleValidate: {
                    passwd: [
                        { required: true, validator: validatePass, trigger: 'blur' }
                    ],
                    passwdCheck: [
                        { required: true, validator: validatePassCheck, trigger: 'blur' }
                    ],
					nickname: [
                        { required: true, validator: validateNicknameCheck, trigger: 'blur' }
                    ],
					phone:[
						{ required: true, validator: validatePhoneCheck, trigger: 'blur' }				
					],
                    mail: [
                        { required: true, message: '邮箱不能为空', trigger: 'blur' },
                        { type: 'email', message: '错误的邮箱格式', trigger: 'blur' }
                    ]
                }
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
			},
            handleSubmit (name) {
				var _this = this;
                this.$refs[name].validate((valid) => {
                    if (valid) {
						this.$axios({
							 method:"post",
							 url:"/users",
							 data:{
								username: this.$data.formValidate.nickname,
								email: this.$data.formValidate.mail,
								phone_number: this.$data.formValidate.phone,
								password: this.$data.formValidate.passwd,
							 }
							}).then(function (response){
							//------------------------------后面功能未测试--------------
								console.log(response);
								window.localStorage.setItem('token', response.data.access_token);
								window.localStorage.setItem('userID', response.data.user_id);
								var url_all = "/users/" + response.data.user_id;
								var url_id = url_all + "/personality";
								var jwt = "JWT " + response.data.access_token;
								_this.$axios({
									 method:"put",
									 url: url_id,
									 data:{
										nickname: _this.$data.formValidate.nickname,
										bio: _this.$data.formValidate.desc
									 },
									 headers:{
										'Authorization': jwt,
									 }
								});
								var url_school = url_all + "/school";
								_this.$axios({
									 method:"put",
									 url: url_school,
									 data:{
										school: _this.$data.formValidate.school,
										grade: _this.$data.formValidate.grade,
										student_number: _this.$data.formValidate.stunumber
									 },
									 headers:{
										'Authorization': jwt,
									 }
								});
								var url_info = url_all + "/personal_info";
								_this.$axios({
									 method:"put",
									 url: url_info,
									 data:{
										name: _this.$data.formValidate.name,
										age: _this.$data.formValidate.age,
										sex: _this.$data.formValidate.gender
									 },
									 headers:{
										'Authorization': jwt,
									 }
								});		
								_this.$Message.success('注册成功!');
								
								//跳转到主页
								_this.$router.push({
									path: '/', 
									name: 'mainpage'
								});
							})
							.catch(function (error) {
								console.log(error.response.status);
								if(error.response.status == 409){
									_this.$Message.error('注册失败，重复的电子邮件或电话号码或用户名');
								}
							});
                    } else {
                        this.$Message.error('信息填写有误!');
                    }
                })
            },
            handleReset (name) {
                this.$refs[name].resetFields();
            },
			handleReturnHomepage () {
			    // 返回主页
				this.$router.push({
					path: '/', 
					name: 'mainpage',
				});		
			},
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
.layout-head{
    width: 150px;
    height: 30px;
	color: white;
    float: left;
    position: relative;
    left: 45%;
	font-size: 30px;
}
.home-button{
    width: 100px;
    height: 30px;
	color: white;
    float: left;
    position: relative;
    left: 86%;
	font-size: 30px;	
}
.layout-footer-center{
    text-align: center;
}
#form{
	margin:0 auto;
	width: 40%;
}
</style>