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

                    <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="110" id="form">

                        <FormItem prop="title">
                            <div class="mainInputDivStyle">
                                <input id="mainInput" 
                                    type="text" 
                                    name="text" 
                                    class="mainInputStyle" 
                                    placeholder="输入任务名称"
                                    v-model="formValidate.title">
                                <button type="button" id="searchButton" class="searchButtonStyle" @click="handleSubmit('formValidate')">
                                    <span>搜索</span>
                                </button>
                                <button type="button" id="moreinfoButton" class="moreinfoButtonStyle" @click="showdrawer = true">
                                    <span>更多条件</span>
                                </button>
                            </div>
                        </FormItem>





                <Drawer title="更多信息 (不填项默认为该条件不作限制)" 
                        placement="right"
                        width="500" 
                        :closable="true"
                        :mask-closable="true" 
                        v-model="showdrawer">

                        <Row>
                            <Card>
                                <p slot="title" style="text-align: center;">任务信息条件</p>

                                    <FormItem prop="size">
                                        <Col span="5">
                                            <label style="right: 0px; width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">返回任务数量</label>
                                        </Col>
                                        <Col span="6">
                                            <InputNumber v-model="formValidate.size" ::min="0" empty></InputNumber>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="creator_user_email">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">创建者邮箱</label>
                                        </Col>
                                        <Col span="6">
                                            <Input v-model="formValidate.creator_user_email" placeholder="请输入创建者邮箱" style="width: 230px;"/>
                                        </Col>
                                    </FormItem>




                                    <FormItem prop="creator_user_phone_number">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">创建者联系方式</label>
                                        </Col>
                                        <Col span="6">
                                            <Input v-model="formValidate.creator_user_phone_number" placeholder="请输入创建者联系方式" style="width: 230px;"/>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="creator_organization_name">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">创建组织名字</label>
                                        </Col>
                                        <Col span="6">
                                            <Input v-model="formValidate.creator_organization_name" placeholder="请输入创建组织名字" style="width: 230px;"/>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="status">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">状态</label>
                                        </Col>
                                        <Col span="6">
                                            <Select v-model="formValidate.status" style="width: 230px;">
                                                <Option value="all">全部</Option>
                                                <Option value="ongoing">正在进行</Option>
                                                <Option value="finished">已结束</Option>
                                            </Select>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="tags">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">Tag</label>
                                        </Col>
                                        <Col span="6">
                                            <Select v-model="tasktags" multiple :max-tag-count="2" style="width: 230px;">
                                                <Option v-for="item in tagList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                            </Select>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="reward_for_one_participant_lower">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">单人最低报酬</label>
                                        </Col>
                                        <Col span="6">
                                            <InputNumber v-model="formValidate.reward_for_one_participant_lower" ::min="0"></InputNumber>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="reward_for_one_participant_upper">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">单人最高报酬</label>
                                        </Col>
                                        <Col span="6">
                                            <InputNumber v-model="formValidate.reward_for_one_participant_upper" ::min="0"></InputNumber>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="receive_end_time">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">任务接收截止时间</label>
                                        </Col>
                                        <Col span="6">
                                            <DatePicker v-model="formValidate.receive_end_time" type="datetime" placeholder="任务接收截止时间" style="width: 230px"></DatePicker>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="finish_deadline_time">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">任务完成截止时间</label>
                                        </Col>
                                        <Col span="6">
                                            <DatePicker v-model="formValidate.finish_deadline_time" type="datetime" placeholder="任务完成截止时间" style="width: 230px"></DatePicker>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="steps_number_lower">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">最小步骤数</label>
                                        </Col>
                                        <Col span="6">
                                            <InputNumber v-model="formValidate.steps_number_lower" :min="0"></InputNumber>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="steps_number_upper">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">最大步骤数</label>
                                        </Col> 
                                        <Col span="6">
                                            <InputNumber v-model="formValidate.steps_number_upper" :min="0"></InputNumber>
                                        </Col>
                                    </FormItem>
                            </Card>



                            <Card style="margin-top: 20px;">
                                <p slot="title" style="text-align: center;">参加任务者信息条件</p>
                                
                                    <FormItem prop="age_lower">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">参与者最小年龄</label>
                                        </Col>
                                        <Col span="6">
                                            <InputNumber v-model="formValidate.age_lower" :min="0"></InputNumber>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="age_upper">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">参与者最大年龄</label>
                                        </Col>
                                        <Col span="6">
                                            <InputNumber v-model="formValidate.age_upper" ::min="0"></InputNumber>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="grades">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">年级</label>
                                        </Col>
                                        <Col span="6">
                                            <Select v-model="formValidate.grades" style="width: 230px;">
                                                <Option value="grade1">大一</Option>
                                                <Option value="grade2">大二</Option>
                                                <Option value="grade3">大三</Option>
                                                <Option value="grade4">大四</Option>
                                                <Option value="grade0">其他</Option>
                                            </Select>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="sexes">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">性别</label>
                                        </Col>
                                        <Col span="6">
                                            <Select v-model="formValidate.sexes" style="width: 230px;">
                                                <Option value="sex_type1">男</Option>
                                                <Option value="sex_type2">女</Option>
                                                <Option value="sex_type3">其他</Option>
                                            </Select>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="schools">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">学校</label>
                                        </Col>
                                        <Col span="6">
                                            <Select v-model="formValidate.schools" style="width: 230px;">
                                                <Option value="school_name1">中山大学</Option>
                                                <Option value="school_name2">广东外语外贸大学</Option>
                                                <Option value="school_name3">华南理工大学</Option>
                                                <Option value="school_name4">广东药科大学</Option>
                                                <Option value="school_name5">广州中医药大学</Option>
                                                <Option value="school_name6">广州美术学院</Option>
                                                <Option value="school_name7">广州大学</Option>
                                                <Option value="school_name8">广州工业大学</Option>
                                                <Option value="school_name9">星海音乐学院</Option>
                                                <Option value="school_name10">华南师范大学</Option>
                                                <Option value="school_name0">其他</Option>
                                            </Select>
                                        </Col>
                                    </FormItem>
                            </Card>
 
                            <!-- <Col span="4" offset="3"> -->
                                <FormItem style="margin-top: 30px;">
                                    <Button type="primary" @click="showdrawer = false;" style="margin-left: 70px;">确定</Button>
                                    <Button @click="handleReset('formValidate')" style="margin-left: 15px;">重置</Button>
                                </FormItem>
                            <!-- </Col> -->


                        </Row>


                    </Drawer>


                    </Form>

				</Card>

                <Card :bordered="false" style="top: 20px;">
                    <p slot="title">查询结果 (点击任务所在行查看详细信息)</p>
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
            return {
                showdrawer: false,
				ageoptionsList:[],
                formValidate: {
                    size: 100,
                    creator_user_email: 'qq@qq.com',
                    creator_user_phone_number: '13123456789',
                    creator_organization_name: 'none',
                    status: 'ongoing',
                    title: 'first',
                    tags: [],
                    reward_for_one_participant_lower: 0,
                    reward_for_one_participant_upper: 999,
                    receive_end_time: '',
                    finish_deadline_time: '',
                    age_upper: 30,
                    age_lower: 10,
                    grades: [],
                    sexes: [],
                    schools: [],
                    steps_number_upper: 100,
                    steps_number_lower: 0
                },

                ruleValidate: {},
                tasktags: [],
				tagList: [
                    {
                        value: '心理实验',
                        label: '心理实验'
                    },
                    {
                        value: '问卷',
                        label: '问卷'
                    },
                    {
                        value: '拿外卖',
                        label: '拿外卖'
                    },
                    {
                        value: '其他',
                        label: '其他'
                    }
                ],

                taskInfoCol: [
                    {
                        title: '任务名',
                        key: 'name',

                        render: (h, params) => {
                            return h('div', {
                                // props: {
                                //     type: 'warning',
                                //     size: 'small'
                                // },
                                style: {
                                    // marginRight: '5px'
                                    padding: '15px 23px',
                                    marginLeft: '-18px',
                                    width: '300px',
                                    height: '47px',
                                    cursor: 'pointer'
                                },
                                on: {
                                    click: () => {
                                        // window.open("https://www.baidu.com");
                                        //this.$Message.error('' + params.index);
                                        //console.log(params.index);
                                        this.$router.push({
                                            path: '/', 
                                            name: 'taskinfoforcreate',
                                        });	
                                    }
                                }
                            }, this.taskInfoData[params.index].name)
                        }

                    },
                    {
                        title: 'tag',
                        key: 'tag',
                        render: (h, params) => {
                            return h('div', {
                                style: {
                                    // marginRight: '5px'
                                    padding: '15px 23px',
                                    marginLeft: '-18px',
                                    width: '300px',
                                    height: '47px',
                                    cursor: 'pointer'
                                },
                                on: {
                                    click: () => {
                                        //this.$Message.error('' + params.index);
                                        //console.log(params.index);
                                        this.$router.push({
                                            path: '/', 
                                            name: 'taskinfoforcreate',
                                        });	                                        
                                    }
                                }
                            }, this.taskInfoData[params.index].tag)
                        }                        
                    },
                    {
                        title: '发布方',
                        key: 'boss',
                        render: (h, params) => {
                            return h('div', {
                                style: {
                                    // marginRight: '5px'
                                    padding: '15px 23px',
                                    marginLeft: '-18px',
                                    width: '300px',
                                    height: '47px',
                                    cursor: 'pointer'
                                },
                                on: {
                                    click: () => {
                                        //this.$Message.error('' + params.index);
                                        //console.log(params.index);
                                        this.$router.push({
                                            path: '/', 
                                            name: 'taskinfoforcreate',
                                        });	                                        
                                    }
                                }
                            }, this.taskInfoData[params.index].boss)
                        }                        
                    },
                    {
                        title: '状态',
                        key: 'status',
                        render: (h, params) => {
                            return h('div', {
                                style: {
                                    // marginRight: '5px'
                                    padding: '15px 23px',
                                    marginLeft: '-18px',
                                    width: '300px',
                                    height: '47px',
                                    cursor: 'pointer'
                                },
                                on: {
                                    click: () => {
                                        //this.$Message.error('' + params.index);
                                        //console.log(params.index);
                                        this.$router.push({
                                            path: '/', 
                                            name: 'taskinfoforcreate',
                                        });	                                        
                                    }
                                }
                            }, this.taskInfoData[params.index].status)
                        }                          
                    },
                    {
                        title: '发布时间',
                        key: 'reltime',
                        render: (h, params) => {
                            return h('div', {
                                style: {
                                    // marginRight: '5px'
                                    padding: '15px 23px',
                                    marginLeft: '-18px',
                                    width: '300px',
                                    height: '47px',
                                    cursor: 'pointer'
                                },
                                on: {
                                    click: () => {
                                        //this.$Message.error('' + params.index);
                                        //console.log(params.index);
                                        this.$router.push({
                                            path: '/', 
                                            name: 'taskinfoforcreate',
                                        });	                                        
                                    }
                                }
                            }, this.taskInfoData[params.index].reltime)
                        }                        
                    },
                    {
                        title: '截止时间',
                        key: 'ddltime',
                        render: (h, params) => {
                            return h('div', {
                                style: {
                                    // marginRight: '5px'
                                    padding: '15px 23px',
                                    marginLeft: '-18px',
                                    width: '300px',
                                    height: '47px',
                                    cursor: 'pointer'
                                },
                                on: {
                                    click: () => {
                                        //this.$Message.error('' + params.index);
                                        //console.log(params.index);
                                        this.$router.push({
                                            path: '/', 
                                            name: 'taskinfoforcreate',
                                        });	                                        
                                    }
                                }
                            }, this.taskInfoData[params.index].ddltime)
                        }                        
                    },
                    {
                        title: '设置',
                        key: 'action',
                        width: 100,
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: {
                                        type: 'warning',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px',
                                        // display: (params.row.status == "1")?"inline-block":"none"
                                    },
                                    on: {
                                        click: () => {
                                            this.taskInfoData.splice(params.index, 1);
                                        }
                                    }
                                }, '隐藏显示')
                            ]);
                        }

                    }
                ],
                taskInfoData: [
                    {
                        name: 'Coding1',
                        tag: 'first',
                        boss: 'Tencent',
                        reltime: '2016-10-03',
                        ddltime: '2016-11-03'
                    }
                ]

            }
        },
        
		created: function () { 
			this.getEventData();
		},
        methods: {

































































			getEventData:function() {
				// let uID = window.localStorage.getItem('userID')
			
				// // if(uID == null || uID == ""){
				// // 	//跳转到主页
				// // 	this.$router.push({
				// // 		path: '/', 
				// // 		name: 'mainpage'
				// // 	});
				// // }
		
				// var url = "/users/" + uID + "/organizations";
				// this.$data.userID = uID;
				// var jwt = "JWT " + window.localStorage.getItem('token');
		
				// var _this = this;
				// this.$axios({
				// 		 method:"get",
				// 		 url:url,
				// 		 headers:{
				// 			'Authorization': jwt,
				// 		 }
				// }).then(function (response){
                //     var tempOrganizations = response.data.organizations;
                //     for(var i = 0; i < tempOrganizations)
				// }).catch(function (error) {
                //     _this.$Message.error('error');
                //     console.log(error);
				// 	//跳转到主页
				// 	_this.$router.push({
				// 		path: '/', 
				// 		name: 'mainpage'
				// 	});
				// });
			},


			handleSubmit (name) {
				 this.$refs[name].validate((valid) => {
					 if (valid){
                        if(this.formValidate.age_upper < this.formValidate.age_lower){
                            this.$Message.error('年龄下限不能大于等于年龄上限');
                                return;
                        }
                        if(this.formValidate.steps_number_upper < this.formValidate.steps_number_lower){
                            this.$Message.error('最小步骤数不能大于最大步骤数');
                                return;
                        }
                        if(this.formValidate.reward_for_one_participant_upper < this.formValidate.reward_for_one_participant_lower){
                            this.$Message.error('个人最低报酬不能大于个人最高报酬');
                                return;
                        }

                        let uID = window.localStorage.getItem('userID');
                        if(uID == null || uID == ""){
                            this.$router.push({
                                path: '/', 
                                name: 'mainpage'
                            });
                        }
                        var url = "/users/" + uID + "/tasks";
                        this.$data.userID = uID;
                        var jwt = "JWT " + window.localStorage.getItem('token');
                        var _this = this;
                        this.$axios({
                            method:"get",
                            url:url,
                            headers:{
                                'Authorization': jwt,
                            },
                            data: {
                                "size": 20,
                                // creator_user_email: "i@sirius.com",
                                // creator_user_phone_number: "13123456789",
                                // creator_organization_name: "name",
                                // status: "ongoing",
                                // title: "sub_string",
                                // tags: ["tag1", "tag2", "tag3"],
                                // reward_for_one_participant_upper: 3,
                                // reward_for_one_participant_lower: 1,
                                // receive_end_time: "2014-2-12 13:23:22",
                                // finish_deadline_time: "2015-2-1 23:22:21",
                                // user_limit: {
                                //     age_upper: 0,
                                //     age_lower: 1,
                                //     grades: ["grade1", "grade1"],
                                //     sexes: ["sex_type1", "sex_type2", "sex_type3"],
                                //     schools: ["school_name1", "school_name2"]
                                // },
                                // steps_number_upper: 5,
                                // steps_number_lower: 1
                            }
                        }).then(function (response){
                            _this.$Message.success('success');
                        }).catch(function (error) {
                            _this.$Message.error('failure');
                        });
                        // console.log(this.$data.formValidate.creator_user_email);
                        // console.log(this.$data.formValidate.creator_user_phone_number);
                        // console.log(this.$data.formValidate.creator_organization_name);
                        // console.log(this.$data.formValidate.status);
                        // console.log(this.$data.formValidate.title);
                        // console.log(this.$data.formValidate.reward_for_one_participant_upper);
                        // console.log(this.$data.formValidate.reward_for_one_participant_lower);
                        // console.log(this.$data.formValidate.receive_end_time);
                        // console.log(this.$data.formValidate.finish_deadline_time);
                        // console.log(this.$data.formValidate.age_upper);
                        // console.log(this.$data.formValidate.age_lower);
                        // console.log(this.$data.formValidate.steps_number_upper);
                        // console.log(this.$data.formValidate.steps_number_lower);
					 }
				})
			},





















































            handleReset (name) {
                this.$refs[name].resetFields();
                this.tasktags = [];
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
    /* width: 45%; */
	width: 100%;
}

.mainInputDivStyle {
	width: 100%;
	height: 20%;
}

.mainInputStyle {
	width: 50%;
	height: 45px;
	/* font-size: 26px; */
    font-size: 24px;
    border: solid 1px blue;
	margin-left: 12%;
	margin-top: 1%;
	border-radius: 4px;
	text-align: center;
}

#mainInput::-webkit-input-placeholder {
	color: rgba(0, 0, 0, 0.2);
	/*text-align: center;*/
}

.searchButtonStyle {
	display: inline-block;
	border-radius: 4px;
	background-color: rgba(60,70,200,0.8);
	border: 1px solid rgba(60,70,200,0.8);
	color: rgba(255,255,255,1);
	text-align: center;
	font-size: 18px;
	padding: 9px;
	width: 10%;
    height: 43px;
    top: 2px;
	transition: all 0.5s;
	cursor: pointer;
	position: relative;
    /*background-color: #4CAF50;*/
    -webkit-transition-duration: 0.4s; /* Safari */
    transition-duration: 0.4s;
    overflow: hidden;
}

.moreinfoButtonStyle {
	display: inline-block;
	border-radius: 4px;
	background-color: rgba(60,70,200,0.8);
	border: 1px solid rgba(60,70,200,0.8);
	color: rgba(255,255,255,1);
	text-align: center;
	font-size: 18px;
	padding: 9px;
	width: 12%;
    height: 43px;
    top: 2px;
	transition: all 0.5s;
	cursor: pointer;
	position: relative;
    /*background-color: #4CAF50;*/
    -webkit-transition-duration: 0.4s; /* Safari */
    transition-duration: 0.4s;
    overflow: hidden;
}

.searchButtonStyle span, .moreinfoButtonStyle span {
    top: -4px;
	cursor: pointer;
	display: inline-block;
	position: relative;
	transition: 0.5s;
}

.searchButtonStyle span:after, .moreinfoButtonStyle span:after {
	content: '»';
	position: absolute;
	opacity: 0;
	top: 0;
	right: -20px;
	transition: 0.5s;
}

.searchButtonStyle:hover span, .moreinfoButtonStyle:hover span {
 	padding-right: 25px;
}

.searchButtonStyle:hover span:after, .moreinfoButtonStyle:hover span:after {
	opacity: 1;
	right: 0;
}

.searchButtonStyle:after, .moreinfoButtonStyle:after {
    content: "";
    background: rgba(0,0,255,0.8);
    display: block;
    position: absolute;
    padding-top: 300%;
    padding-left: 350%;
    margin-left: -20px!important;
    margin-top: -120%;
    opacity: 0;
    transition: all 0.8s
}

.searchButtonStyle:active:after, .moreinfoButtonStyle:active:after {
    padding: 0;
    margin: 0;
    opacity: 1;
    transition: 0s
}

a:link {
	color: white;
	text-decoration: none;
	transition: font-size 0.2s;
}	/*The content can be used to change anything.*/

a:visited {color: white;}

a:hover {
	color: rgba(50,50,50,1);
	font-size: 44px;
	text-decoration: underline;
}

a:active {color: lightgray;}

.linkproperty
{
	padding-top: 2%;
	font-size: 38px;
	text-align: center;
	line-height: 50px;
}
</style>