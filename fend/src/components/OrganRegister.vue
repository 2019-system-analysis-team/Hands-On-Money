<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark">
					<div class="layout-head">
						组织创建
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
						<FormItem label="组织名称" prop="name">
							<Input v-model="formValidate.name" placeholder="请输入组织名称"></Input>
						</FormItem>
						<FormItem label="组织介绍" prop="desc">
							<Input v-model="formValidate.desc" type="textarea" :autosize="{minRows: 2,maxRows: 8}" ></Input>
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
		 return {
			 userID:"",
			 formValidate: {
				 name: '',
				 desc: ''
			 },
			 ruleValidate: {
				 name: [
					 { required: true, validator: validateNameCheck, trigger: 'blur' }
				 ],
				 desc: [
					 {required: true, validator: validateDescCheck, trigger: 'blur' }
				 ]
			 }
		 }
		}, 
		created: function () { 
			this.getEventData();
		},
		methods: {
            handleSubmit (name) {
				var _this = this;
                this.$refs[name].validate((valid) => {
                    if (valid) {
						var jwt = "JWT " + window.localStorage.getItem('token');
						var url = "/users/"+ this.$data.userID +"/organization";
						this.$axios({
							 method:"post",
							 url: url,
							 data:{
								name: this.$data.formValidate.name,
								bio: this.$data.formValidate.desc
							 },
							 headers:{
								'Authorization': jwt,
							 }
						}).then(function (response){
							_this.$Message.success('组织注册成功!');
							console.log(response);
							// 去组织的详情页面
							this.$router.push({
								path: '/', 
								name: 'organizationInfo',
								params: { 
										organID: response.data.organization_id
								},
							});	
						}).catch(function (error) {
							console.log(error);
						});
                        
                    } else {
                        this.$Message.error('信息填写有误!');
                    }
                })
            },
            handleReset (name) {
                this.$refs[name].resetFields();
            },
			getEventData:function() {
				var _this = this;
				let uID = window.localStorage.getItem('userID');
				if(uID == null || uID == ""){
					//跳转到主页
					this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				}
				this.$data.userID = uID;
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