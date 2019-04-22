<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark" active-name="1">
                    <div class="layout-logo"></div>
                    <div class="layout-nav">
                        <MenuItem name="1">
                            <Icon type="ios-navigate"></Icon>
                            项目 1
                        </MenuItem>
                        <MenuItem name="2">
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
					<div class="layout-button" v-if="!isLogin">
						<Button onclick="document.getElementById('loginFrame').style.display='block';
			document.getElementById('bgColorDiv').style.display='block'">登录</Button>
						<Button type="primary" ghost v-on:click="register">注册</Button>
					</div>
					<div>
						<Submenu name="4" v-if="isLogin">
							<template slot="title">
								<Avatar src="https://i.loli.net/2017/08/21/599a521472424.jpg" />
							</template>
							<MenuItem name="4-1" to="/userinfomodify">个人信息</MenuItem>
							<MenuItem name="4-2" @click.native="logout()">退出</MenuItem>
						</Submenu>
					</div>
                </Menu>
            </Header>
            <Content :style="{padding: '0 50px'}">
                <Breadcrumb :style="{margin: '20px 0'}">
                    <BreadcrumbItem>Home</BreadcrumbItem>
                    <BreadcrumbItem>Components</BreadcrumbItem>
                    <BreadcrumbItem>Layout</BreadcrumbItem>
                </Breadcrumb>
                <Card>
                    <div style="min-height: 400px;">
                        Content
                    </div>
                </Card>
            </Content>
            <Footer class="layout-footer-center">2019-2019 &copy; SYSU</Footer>
        </Layout>










        <div id="bgColorDiv" class="black_overlay">
			<div id="loginFrame" class="white_content">
				<form class="form-horizontal">
					<span class="heading">用户登录</span>
					<div class="form-group">
						<input type="email" class="form-control" id="inputEmail3" placeholder="username">
						<i class="fa fa-user"></i>
					</div>
					<div class="form-group help">
						<input type="password" class="form-control" id="inputPassword3" placeholder="password">
						<i class="fa fa-lock"></i>
						<a href="#" class="fa fa-question-circle"></a>
					</div>
					<div class="form-group">
						<div class="main-checkbox">
							<input type="checkbox" value="None" id="checkbox1" name="check">
							<label for="checkbox1"></label>
						</div>
						<span class="text">记住密码</span>
						<button type="submit" class="btn btn-default" onclick="
				document.getElementById('bgColorDiv').style.display='none'">取消</button>
						<button type="submit" class="btn btn-default" onclick="
				document.getElementById('bgColorDiv').style.display='none'">登录</button>
					</div>
				</form>
			</div>
		</div>










    </div>
</template>







<script>
    export default {
		data() {
			return { 
				studentID: '',
				isLogin: false,
			};
		}, 
		created: function () { 
			//在created阶段初始化
			this.getEventData();
		},
		methods: {
			getEventData:function() {
				let routerParamsStudentID = this.$route.params.studentID;
				if(routerParamsStudentID == null){
					this.isLogin = false;
				}else{
					this.studentID = routerParamsStudentID;
					this.isLogin = true;
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
				this.isLogin = false;
				this.studentID = '';
			}
		}
    }
</script>







<style scoped>
.layout{
    border: 1px solid #d7dde4;
    width: 100%;
    height: 100%;
    background: #f5f7f9;
    position: relative;
    border-radius: 10px;
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
    margin-right: 120px;
}
.layout-button{
    width: 200px;
    margin: 0 auto;
	margin-right: 0px;
}
.layout-footer-center{
    text-align: center;
}
.black_overlay {
	display: none;
	position: absolute;
	top: 0%;
	left: 0%;
	width: 100%;
	height: 100%;
	/*background-color: black;*/
	/*-moz-opacity: 0.8;*/
	background: rgba(0,0,0,0.8);
	z-index: 1001;
	opacity: .80;
	filter: alpha(opacity=80);
}
.white_content {
	border-radius: 20px;
	display: none;
	position: absolute;
	top: 20%;
	left: 30%;
	width: 40%;
	height: 370px;
	padding: 16px;
	//border: 3px solid orange;
	background-color: white;
	z-index: 1002;
	overflow: auto;
}












.form-bg{
	padding: 2em 0;
}
.form-horizontal{
	background: #fff;
	padding-bottom: 40px;
	border-radius: 15px;
	text-align: center;
}
.form-horizontal .heading{
	display: block;
	font-size: 35px;
	font-weight: 700;
	padding: 20px 0;
	border-bottom: 1px solid #f0f0f0;
	margin-bottom: 40px;
}
.form-horizontal .form-group{
	padding: 0 40px;
	margin: 0 0 25px 0;
	position: relative;
}
.form-horizontal .form-control{
	font-size: 15px;
	background: #f0f0f0;
	border: none;
	border-radius: 20px;
	box-shadow: none;
	padding: 0 40px 0 15px;
	height: 40px;
	transition: all 0.3s ease 0s;
}
.form-horizontal .form-control:focus{
	background: #e0e0e0;
	box-shadow: none;
	outline: 0 none;
}
.form-horizontal .form-group i{
	position: absolute;
	top: 12px;
	left: 60px;
	font-size: 17px;
	color: #c8c8c8;
	transition : all 0.5s ease 0s;
}
.form-horizontal .form-control:focus + i{
	color: #00b4ef;
}
.form-horizontal .fa-question-circle{
	display: inline-block;
	position: absolute;
	top: 12px;
	right: 60px;
	font-size: 20px;
	color: #808080;
	transition: all 0.5s ease 0s;
}
.form-horizontal .fa-question-circle:hover{
	color: #000;
}
.form-horizontal .main-checkbox{
	float: left;
	left: 20px;
	width: 20px;
	height: 20px;
	background: #11a3fc;
	border-radius: 50%;
	position: relative;
	margin: 12px 0 0 5px;
	border: 1px solid #11a3fc;
}
.form-horizontal .main-checkbox label{
	width: 20px;
	height: 20px;
	position: absolute;
	top: 0;
	left: 0;
	cursor: pointer;
}
.form-horizontal .main-checkbox label:after{
	content: "";
	width: 10px;
	height: 5px;
	position: absolute;
	top: 5px;
	left: 4px;
	border: 3px solid #fff;
	border-top: none;
	border-right: none;
	background: transparent;
	opacity: 0;
	-webkit-transform: rotate(-45deg);
	transform: rotate(-45deg);
}
.form-horizontal .main-checkbox input[type=checkbox]{
	visibility: hidden;
}
.form-horizontal .main-checkbox input[type=checkbox]:checked + label:after{
	opacity: 1;
}
.form-horizontal .text{
	float: left;
	margin-top: 7px;
	margin-left: 25px;
	line-height: 20px;
	padding-top: 5px;
	text-transform: capitalize;
}
.form-horizontal .btn{
	float: right;
	font-size: 14px;
	color: #fff;
	background: #00b4ef;
	border-radius: 30px;
	padding: 10px 25px;
	margin-left: 10px;
	border: none;
	text-transform: capitalize;
	transition: all 0.5s ease 0s;
}
@media only screen and (max-width: 479px){
	.form-horizontal .form-group{
		padding: 0 25px;
	}
	.form-horizontal .form-group i{
		left: 45px;
	}
	.form-horizontal .btn{
		padding: 10px 20px;
	}
}





</style>
