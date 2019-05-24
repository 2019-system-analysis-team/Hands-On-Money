<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark">
					<div class="layout-head">任务市场</div>
					<div class="home-button">
						<Button shape="circle" icon="ios-home" @click="handleReturnHomepage()"></Button>
					</div>
				</Menu>
            </Header>
            <Content :style="{padding: '50px 50px'}">
				<Card :bordered="false">
					<p slot="title">请填写下列条件信息</p>
					<Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80" id="form">
						<FormItem label="任务名称" prop="title">
							<Input v-model="formValidate.title" placeholder="请输入任务名称"></Input>
						</FormItem>
						<FormItem label="Tag" prop="tag">
							<Input v-model="formValidate.tag" placeholder="请输入任务标签"></Input>
						</FormItem>
                        <FormItem label="发布方" prop="boss">
							<Select v-model="formValidate.boss">
								<Option value="Tencent">Tencent</Option>
								<Option value="Huawei">Huawei</Option>
								<Option value="Xiaomi">Xiaomi</Option>
							</Select>
                        </FormItem>
                        <FormItem label="状态" prop="status">
							<Select v-model="formValidate.status">
                                <Option value="all">全部</Option>
								<Option value="ongoing">正在进行</Option>
								<Option value="finished">已结束</Option>
							</Select>
                        </FormItem>
                        <FormItem label="任务时间">
                            <DatePicker type="datetime" placeholder="任务接收截止时间" style="width: 200px"></DatePicker>
                            <DatePicker type="datetime" placeholder="任务完成截止时间" style="width: 200px"></DatePicker>
                        </FormItem>
						<FormItem>
							<Button type="primary" @click="handleSubmit('formValidate')">查询</Button>
							<Button @click="handleReset('formValidate')" style="margin-left: 8px">重置</Button>
						</FormItem>
					</Form>
				</Card>
                <Card :bordered="false" style="top: 10px;">
                    <p slot="title">查询结果</p>
                    <Table :columns="taskInfoCol" :data="taskInfoData"></Table>
                </Card>
            </Content>



            <Footer class="layout-footer-center">2019-2019 &copy; SYSU</Footer>
        </Layout>
    </div>
</template>
<script>
  export default {
        data () {
			// const validateNicknameCheck = (rule, value, callback) => {
            //     if (value === '') {
            //         callback(new Error('昵称不能为空'));
            //     } else if (value.toLocaleString().length > 15) {
            //         callback(new Error('昵称不能多于15个字符'));
            //     } else {
            //         callback();
            //     }
            // };
			// const validateNameCheck = (rule, value, callback) => {
			//     if (value === '') {
			//         callback(new Error('姓名不能为空'));
			//     } else if (value.toLocaleString().length > 10) {
			//         callback(new Error('姓名不能多于10个字符'));
			//     } else {
			//         callback();
			//     }
			// };
			// const validateStuNumberCheck = (rule, value, callback) => {
			// 	var numReg = /[^\d]/g;
			// 	var numRe = new RegExp(numReg);
			// 	if (!numRe.test(value) && value.length == 8){
			// 		callback();
			// 	}else{
			// 		callback(new Error('学号为8位数字'));
			// 	}
			// };
            return {
				ageoptionsList:[],
                formValidate: {
					title: '',
                    tag: '',
                    boss: 'Tencent',
                    status: 'all'
                },
                // ruleValidate: {
				// 	title: [
                //         { required: true, validator: validateNicknameCheck, trigger: 'blur' }
                //     ],
                // },
                taskInfoCol: [
                    {
                        title: '任务名',
                        key: 'name'
                    },
                    {
                        title: 'tag',
                        key: 'tag'
                    },
                    {
                        title: '发布方',
                        key: 'boss'
                    },
                    {
                        title: '状态',
                        key: 'status'
                    },
                    {
                        title: '发布时间',
                        key: 'reltime'
                    },
                    {
                        title: '截止时间',
                        key: 'ddltime'
                    }
                ],
                taskInfoData: [
                    {
                        name: 'Coding1',
                        tag: 'first',
                        boss: 'Tencent',
                        reltime: '2016-10-03',
                        ddltime: '2016-11-03'
                    },
                    {
                        name: 'Coding2',
                        tag: 'second',
                        boss: 'Huawei',
                        reltime: '2016-11-02',
                        ddltime: '2016-11-04'
                    },
                    {
                        name: 'Coding3',
                        tag: 'third',
                        boss: 'Samsung',
                        reltime: '2016-11-11',
                        ddltime: '2016-11-13'
                    },
                    {
                        name: 'Coding4',
                        tag: 'forth',
                        boss: 'Individual',
                        reltime: '2016-10-29',
                        ddltime: '2016-11-31'
                    },
                ]

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
								username: this.$data.formValidate.title,
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
										title: _this.$data.formValidate.title
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
										name: _this.$data.formValidate.name
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
									_this.$Message.error('注册失败，重复的电子邮件或电话号码');
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