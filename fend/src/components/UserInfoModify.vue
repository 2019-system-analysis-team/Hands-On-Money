<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark" active-name="1">
                    <div class="layout-logo"></div>
                    <div class="layout-nav">
                        <Submenu name="1">
							 <template slot="title">
								<Icon type="ios-navigate"></Icon>
								任务
							 </template>
							<MenuItem name="1-1">我的任务</MenuItem>
							<MenuItem name="1-2">新建任务</MenuItem>
                        </Submenu>
                        <Submenu name="2">
							<template slot="title">
								<Icon type="ios-keypad"></Icon>
								组织
							</template>
							<MenuItem name="2-1">我的组织</MenuItem>
							<MenuItem name="2-2" to="/organregister">新建组织</MenuItem>
                        </Submenu>
						<Submenu name="3">
							<template slot="title">
								<Icon type="ios-stats" />
								余额:{{money}}
							</template>
							<MenuItem name="3-1">充值</MenuItem>
							<MenuItem name="3-2">提现</MenuItem>
						</Submenu>
                    </div>
					<div>
						<Submenu name="4">
							<template slot="title">
								<Avatar src="https://i.loli.net/2017/08/21/599a521472424.jpg" />
							</template>
							<MenuItem name="4-1" to="/">退出</MenuItem>
						</Submenu>
					</div>
                </Menu>
            </Header>
			<Content :style="{padding: '50px 50px'}">
				<Card :bordered="false">
					<p slot="title">您的个人信息如下</p>
					<Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80" id="form">
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
							<Upload
								ref="upload"
								:show-upload-list="false"
								:default-file-list="defaultList"
								:on-success="handleSuccess"
								:format="['jpg','jpeg','png']"
								:max-size="2048"
								:on-format-error="handleFormatError"
								:on-exceeded-size="handleMaxSize"
								:before-upload="handleBeforeUpload"
								multiple
								type="drag"
								action="//jsonplaceholder.typicode.com/posts/"
								style="display: inline-block;width:78px;">
								<div style="width: 78px;height:78px;line-height: 78px;">
									<Icon type="ios-camera" size="40"></Icon>
								</div>
							</Upload>
							<Modal title="浏览头像" v-model="visible">
								<img :src="'https://o5wwk8baw.qnssl.com/' + imgName + '/avatar'" v-if="visible" style="width: 100%">
							</Modal>
						</FormItem>
						<FormItem label="昵称" prop="nickname">
							<Input v-model="formValidate.nickname" placeholder="请输入您的昵称"></Input>
						</FormItem>
						<FormItem label="真实姓名" prop="name">
							<Input disabled v-model="formValidate.name" placeholder="请输入您的真实姓名"></Input>
						</FormItem>
						<FormItem label="学号" prop="stunumber">
							<Input disabled v-model="formValidate.stunumber" placeholder="请输入您的学号"></Input>
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
								<Option value="数据科学与计算机学院">数据科学与计算机学院</Option>
								<Option value="管理学院">管理学院</Option>
								<Option value="法学院">法学院</Option>
							</Select>
						</FormItem>
						<FormItem label="年龄" prop="age">
						    <Select v-model="formValidate.age" >
								<Option v-for="item in ageoptionsList" :value="item.value" :key="item.value">{{ item.label }}</Option>
							</Select>						
						</FormItem>
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
						<FormItem label="自我介绍" prop="desc">
							<Input v-model="formValidate.desc" type="textarea" :autosize="{minRows: 2,maxRows: 5}"></Input>
						</FormItem>
						<FormItem>
							<Button type="primary" @click="handleSubmit('formValidate')">修改</Button>
							<Button @click="handleReturnHomepage()" style="margin-left: 8px">返回主页</Button>
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
				money:'',
				ageoptionsList:[],
                formValidate: {
					nickname: '',
                    name: '',
					stunumber: '',
					grade: '大一',
					school: '数据科学与计算机学院',
					age: '18',
					phone: '',
                    mail: '',
                    gender: '女生',
                    desc: '',
                    passwd: '',
                    passwdCheck: '',
                },
                defaultList: [
                    {
                        'name': 'a42bdcc1178e62b4694c830f028db5c0',
                        'url': 'https://o5wwk8baw.qnssl.com/a42bdcc1178e62b4694c830f028db5c0/avatar'
                    }
                ],
                imgName: '',
                visible: false,
				uploadList: [],
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
                    name: [
                        { required: true, validator: validateNameCheck, trigger: 'blur' }
                    ],
                    stunumber: [
                        { required: true, validator: validateStuNumberCheck, trigger: 'blur' }
                    ],
					grade:[
						{required: true}
					],
					school:[
						{required: true}
					],
					age:[
						{required: true}
					],
					phone:[
						{ required: true, validator: validatePhoneCheck, trigger: 'blur' }				
					],
                    mail: [
                        { required: true, message: '邮箱不能为空', trigger: 'blur' },
                        { type: 'email', message: '错误的邮箱格式', trigger: 'blur' }
                    ],
                    gender: [
                        { required: true}
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
				this.$data.formValidate.nickname = 'pml';
				this.$data.formValidate.name = '潘茂林';
				this.$data.formValidate.stunumber = '12345678';
				this.$data.formValidate.phone = '13013021302';
				this.$data.formValidate.mail = '123@123.com';
				this.$data.formValidate.phone = '13013021302';
				this.$data.formValidate.desc = 'nb';
				this.$data.money = 999;
			},
            handleSubmit (name) {
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        this.$Message.success('修改成功!');
                    } else {
                        this.$Message.error('信息填写有误!');
                    }
                })
            },
            handleReturnHomepage () {
                // 返回主页
				this.$router.push({
						path: '/'
				});		
            },
			handleView (name) {
                this.imgName = name;
                this.visible = true;
            },
            handleSuccess (res, file) {
                file.url = 'https://o5wwk8baw.qnssl.com/a42bdcc1178e62b4694c830f028db5c0/avatar';
                file.name = 'a42bdcc1178e62b4694c830f028db5c0';
            },
            handleFormatError (file) {
                this.$Notice.warning({
                    title: '文件格式不正确',
                    desc: '文件 ' + file.name + ' 的格式不正确, 请选择 jpg 或者 png.'
                });
            },
            handleMaxSize (file) {
                this.$Notice.warning({
                    title: '超出文件大小限制',
                    desc: '文件  ' + file.name + ' 太大, 不能超过 2M.'
                });
            },
            handleBeforeUpload () {
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
    margin-right: 80px;
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
#form{
	margin:0 auto;
	width: 40%;
}
</style>