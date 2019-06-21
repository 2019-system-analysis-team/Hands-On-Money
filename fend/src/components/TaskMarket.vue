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

                <Modal v-model="showTaskInfo">
                    <p slot="header" style="text-align:center">
                        <Icon type="ios-information-circle"></Icon>
                        <span>任务详情</span>
                    </p>
                    <div>
                    <Card dis-hover>
                        <p slot="title" class="info">{{displayData.title}}{{ownerMessage}}</p>
                        标签 : <Tag v-for="item in displayData.tags" :key="item" :name="item" color="cyan">{{ item }}</Tag>
                        <p class="info">任务描述 : {{displayData.description}}</p>
                        <p class="info">当前参与者人数 : {{displayData.current_participant_number}}</p>
                        <p class="info">参与者人数上限 : {{displayData.participant_number_limit}}</p>
                        <p class="info">完成奖励代币 : {{displayData.reward_for_one_participant}}</p>
                        <p class="info">创建者名字 : {{displayData.creator_organization_name}}</p>
                        <p class="info">创建者邮箱 : {{displayData.creator_user_email}}</p>
                        <p class="info">创建者电话 : {{displayData.creator_user_phone_number}}</p>
                        <p class="info">任务发布时间 : {{displayData.post_time}}</p>
                        <p class="info">截止接受任务时间 : {{displayData.receive_end_time}}</p>
                        <p class="info">最迟完成任务时间 : {{displayData.finish_deadline_time}}</p>
                        <p class="info">步骤 : </p>
                        <Steps :current="displayData.current">
                            <Step :title="item.title" v-for="item in displayData.steps" :key="item.title">
                            </Step>
                        </Steps>
                    </Card>
                    </div>
                    <div slot="footer">
                        <Button type="primary" ghost @click="showTaskCancel">确定</Button>
                        <Button type="primary" @click="ToTaskInfo(displayData.task_id)" v-if="!isAcceptableTask">编辑</Button>
                        <Button type="success" @click="confirmAccept = true;" v-if="isAcceptableTask">接受</Button>
                    </div>
                </Modal>

                <Modal v-model="confirmAccept"
                    title="确认"
                    @on-ok="acceptMission()"
                    width='400'
                    :styles="{top: '300px'}">
                    <p style="font-size: 15px">您确定要接受这个任务吗？</p>
                </Modal>

				<Card :bordered="false">
					<p slot="title">请填写下列条件信息</p>

                    <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="110" id="form" @keydown.native.enter.prevent ="handleSubmit('formValidate')">

                        <FormItem prop="title">
                            <div class="mainInputDivStyle">
                                <input id="mainInput" 
                                    type="text" 
                                    name="text" 
                                    class="mainInputStyle" 
                                    placeholder="输入任务名称"
                                    v-model="formValidate.title"
                                    >
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
                                            <label style="right: 0px; width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">返回任务最大数量</label>
                                        </Col>
                                        <Col span="6">
                                            <InputNumber v-model="formValidate.size" :min="0" empty></InputNumber>
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
                                                <!-- <Option value="all">全部</Option> -->
                                                <Option value="ongoing">正在进行</Option>
                                                <Option value="not ongoing">未进行</Option>
                                            </Select>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="tags">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">Tag</label>
                                        </Col>
                                        <Col span="6">
                                            <Select v-model="formValidate.tags" multiple :max-tag-count="2" style="width: 230px;">
                                                <Option v-for="item in tagList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                            </Select>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="reward_for_one_participant_lower">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">单人最低报酬</label>
                                        </Col>
                                        <Col span="6">
                                            <InputNumber v-model="formValidate.reward_for_one_participant_lower" :min="0"></InputNumber>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="reward_for_one_participant_upper">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">单人最高报酬</label>
                                        </Col>
                                        <Col span="6">
                                            <InputNumber v-model="formValidate.reward_for_one_participant_upper" :min="0"></InputNumber>
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
                                            <InputNumber v-model="formValidate.age_upper" :min="0"></InputNumber>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="grades">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">年级</label>
                                        </Col>
                                        <Col span="6">
                                            <Select v-model="formValidate.grades" multiple style="width: 230px;">
                                                <Option value="grade1">大一</Option>
                                                <Option value="grade2">大二</Option>
                                                <Option value="grade3">大三</Option>
                                                <Option value="grade4">大四</Option>
                                            </Select>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="sexes">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">性别</label>
                                        </Col>
                                        <Col span="6">
                                            <Select v-model="formValidate.sexes" multiple style="width: 230px;">
                                                <Option value="sex_type1">男</Option>
                                                <Option value="sex_type2">女</Option>
                                            </Select>
                                        </Col>
                                    </FormItem>

                                    <FormItem prop="schools">
                                        <Col span="5">
                                            <label style="width: 100px; margin-left: -100px; padding-right: 50px; font-size: 14px;">学院</label>
                                        </Col>
                                        <Col span="6">
                                            <Select v-model="formValidate.schools" multiple style="width: 230px;">
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
                    <Table :columns="taskInfoCol" :data="taskInfoData" width="1314"></Table>
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
                chosenTaskId: 0,
                confirmAccept: false,
                ownerMessage: '',
                isAcceptableTask: true,
                showTaskInfo: false,
                showdrawer: false,
                displayData: {},
				ageoptionsList:[],
                formValidate: {
                    size: 100,
                    creator_user_email: '',
                    creator_user_phone_number: '',
                    creator_organization_name: '',
                    status: '',
                    title: '',
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
                returnData: {},
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
                        width: 150,
                        align: 'center',
                        key: 'name',

                        render: (h, params) => {
                            return h('div', {
                                // props: {
                                //     type: 'warning',
                                //     size: 'small'
                                // },
                                style: {
                                    // marginRight: '5px'
                                    // border: '1px solid red',
                                    textAlign: 'center',
                                    padding: '15px 23px',
                                    marginLeft: '-18px',
                                    width: '150px',
                                    height: '47px',
                                    cursor: 'pointer'
                                },
                                on: {
                                    click: () => {
                                        this.showTaskAllInfo(this.$data.returnData.data[this.taskInfoData[params.index].num]);
                                        // console.log(params.index);
                                    }
                                }
                            }, this.taskInfoData[params.index].name)
                        }

                    },
                    {
                        title: 'tag',
                        width: 200,
                        align: 'center',
                        key: 'tag',
                        render: (h, params) => {
                            return h('div', {
                                style: {
                                    // marginRight: '5px'
                                    // border: '1px solid red',
                                    textAlign: 'center',
                                    padding: '15px 23px',
                                    marginLeft: '-18px',
                                    width: '200px',
                                    height: '47px',
                                    cursor: 'pointer'
                                },
                                on: {
                                    click: () => {
                                        // console.log(params.index);
                                        this.showTaskAllInfo(this.$data.returnData.data[this.taskInfoData[params.index].num]);
                                    }
                                }
                            }, this.taskInfoData[params.index].tag)
                        }                        
                    },
                    {
                        title: '发布方',
                        width: 200,
                        align: 'center',
                        key: 'boss',
                        render: (h, params) => {
                            return h('div', {
                                style: {
                                    // marginRight: '5px'
                                    // border: '1px solid red',
                                    textAlign: 'center',
                                    padding: '15px 23px',
                                    marginLeft: '-18px',
                                    width: '200px',
                                    height: '47px',
                                    cursor: 'pointer'
                                },
                                on: {
                                    click: () => {
                                        // console.log(params.index);
                                        this.showTaskAllInfo(this.$data.returnData.data[this.taskInfoData[params.index].num]);
                                    }
                                }
                            }, this.taskInfoData[params.index].boss)
                        }                        
                    },
                    {
                        title: '状态',
                        width: 200,
                        align: 'center',
                        key: 'status',
                        render: (h, params) => {
                            return h('div', {
                                style: {
                                    // marginRight: '5px'
                                    // border: '1px solid red',
                                    textAlign: 'center',
                                    padding: '15px 23px',
                                    marginLeft: '-18px',
                                    width: '200px',
                                    height: '47px',
                                    cursor: 'pointer'
                                },
                                on: {
                                    click: () => {
                                        // console.log(params.index);
                                        this.showTaskAllInfo(this.$data.returnData.data[this.taskInfoData[params.index].num]);
                                    }
                                }
                            }, this.taskInfoData[params.index].status)
                        }                          
                    },
                    {
                        title: '发布时间',
                        width: 230,
                        align: 'center',
                        key: 'reltime',
                        render: (h, params) => {
                            return h('div', {
                                style: {
                                    // marginRight: '5px'
                                    // border: '1px solid red',
                                    textAlign: 'center',
                                    padding: '15px 23px',
                                    marginLeft: '-18px',
                                    width: '230px',
                                    height: '47px',
                                    cursor: 'pointer'
                                },
                                on: {
                                    click: () => {
                                        // console.log(params.index);
                                        this.showTaskAllInfo(this.$data.returnData.data[this.taskInfoData[params.index].num]);
                                    }
                                }
                            }, this.taskInfoData[params.index].reltime)
                        }                        
                    },
                    {
                        title: '截止时间',
                        width: 230,
                        align: 'center',
                        key: 'ddltime',
                        render: (h, params) => {
                            return h('div', {
                                style: {
                                    // marginRight: '5px'
                                    // fontSize: '15px',
                                    // border: '1px solid red',
                                    padding: '15px 23px',
                                    marginLeft: '-18px',
                                    width: '230px',
                                    height: '47px',
                                    cursor: 'pointer'
                                },
                                on: {
                                    click: () => {
                                        // console.log(params.index);
                                        this.showTaskAllInfo(this.$data.returnData.data[this.taskInfoData[params.index].num]);
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
                                        // marginRight: '5px',
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
                    // {
                    //     name: 'Coding1',
                    //     tag: [],
                    //     boss: 'Tencent',
                    //     status: 'ongoing',
                    //     reltime: '2016-10-03',
                    //     ddltime: '2016-11-03',
                    //     status: 'ongong',
                    //     num: 1
                    // }
                ]

            }
        },
        
		created: function () { 
            this.getEventData();
		},
        methods: {






























            acceptMission() {
                var jwt = "JWT " + window.localStorage.getItem('token');
                var uID = window.localStorage.getItem('userID');
                if(uID == null || uID == ""){
                    this.$router.push({
                        path: '/', 
                        name: 'mainpage'
                    });
                }
                var url = "/users/" + uID + "/tasks/" + this.$data.chosenTaskId;
                var _this = this;
                this.$axios({
                    method:"post",
                    url:url,
                    headers:{
                        'Authorization': jwt,
                    }
                }).then(function (response){
                    _this.$Message.success('接受任务成功!');
                }).catch(function (error) {
                    _this.$Message.error('接受任务失败!');
                    console.log(error);
                });
            },













































            showTaskAllInfo(paraDisData) {
                this.$data.chosenTaskId = paraDisData.task_id;
                // console.log(this.$data.chosenTaskId);
                this.$data.showTaskInfo = true;
                this.$data.displayData = paraDisData;
                if(paraDisData.creator_organization_name == null)
                    this.$data.displayData.creator_organization_name = paraDisData.creator_user_name;
                var tempUID = window.localStorage.getItem('userID');
                if(tempUID == paraDisData.user_id) {
                    this.$data.isAcceptableTask = false;
                    this.$data.ownerMessage = ' (由本用户创建)';
                }
                else {
                    this.$data.isAcceptableTask = true;
                    this.$data.ownerMessage = '';
                }
            },


			showTaskCancel(){
				 this.showTaskInfo = false;
			},

			ToTaskInfo(taskID){
                window.localStorage.setItem('taskID', taskID);
                window.localStorage.removeItem('organID');
                this.$router.push({
                    path: '/', 
                    name: 'taskinfoforcreate',
                    params: { 
                        taskID: taskID
                    },
                });
			},


			getEventData:function() {
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
                    params: {},
                    headers:{
                        'Authorization': jwt,
                    },
                }).then(function (response){
                    _this.$data.returnData = response;
                    // console.log(_this.$data.returnData);
                    for(var i = 0; i < response.data.length; ++i) {
                        var temptags = "";
                        var tempboss = response.data[i].creator_organization_name;
                        if(tempboss == null)
                            tempboss = response.data[i].creator_user_name;
                        for(var j = 0; j < response.data[i].tags.length; ++j)
                            temptags += response.data[i].tags[j] + " ";
                        var tempdata = {
                            name: response.data[i].title,
                            boss: tempboss,
                            reltime: response.data[i].post_time,
                            ddltime: response.data[i].receive_end_time,
                            status: response.data[i].status,
                            taskid: response.data[i].task_id,
                            tag:  temptags,
                            num: i
                        };
                        _this.$data.taskInfoData.push(tempdata);
                    }
                }).catch(function (error) {
                    _this.$Message.error('请先登录');
                    console.log(error);
                });
			},




            getConditions() {
                var returnConditions = {
                    user_limit: {}
                };
                if(this.$data.formValidate.status != '')
                    returnConditions["status"] = this.$data.formValidate.status;
                if(this.$data.formValidate.creator_user_email != "")
                    returnConditions["creator_user_email"] = this.$data.formValidate.creator_user_email;
                if(this.$data.formValidate.size != null)
                    returnConditions["size"] = this.$data.formValidate.size;
                if(this.$data.formValidate.creator_user_phone_number != "")
                    returnConditions["creator_user_phone_number"] = this.$data.formValidate.creator_user_phone_number;
                if(this.$data.formValidate.creator_organization_name != "")
                    returnConditions["creator_organization_name"] = this.$data.formValidate.creator_organization_name;
                if(this.$data.formValidate.title != "")
                    returnConditions["title"] = this.$data.formValidate.title;
                if(this.$data.formValidate.receive_end_time != "")
                    returnConditions["receive_end_time"] = this.$data.formValidate.receive_end_time;
                if(this.$data.formValidate.finish_deadline_time != "")
                    returnConditions["finish_deadline_time"] = this.$data.formValidate.finish_deadline_time;
                if(this.$data.formValidate.tags.length != 0)
                    returnConditions["tags"] = this.$data.formValidate.tags;
                if(this.$data.formValidate.reward_for_one_participant_upper != null)
                    returnConditions["reward_for_one_participant_upper"] = this.$data.formValidate.reward_for_one_participant_upper;
                if(this.$data.formValidate.reward_for_one_participant_lower != null)
                    returnConditions["reward_for_one_participant_lower"] = this.$data.formValidate.reward_for_one_participant_lower;
                if(this.$data.formValidate.age_upper != null)
                    returnConditions["user_limit"]["age_upper"] = this.$data.formValidate.age_upper;
                if(this.$data.formValidate.age_lower != null)
                    returnConditions["user_limit"]["age_lower"] = this.$data.formValidate.age_lower;
                if(this.$data.formValidate.steps_number_upper != null)
                    returnConditions["steps_number_upper"] = this.$data.formValidate.steps_number_upper;
                if(this.$data.formValidate.steps_number_lower != null)
                    returnConditions["steps_number_lower"] = this.$data.formValidate.steps_number_lower;
                if(this.$data.formValidate.age_upper != null)
                    returnConditions["user_limit"]["age_upper"] = this.$data.formValidate.age_upper;
                if(this.$data.formValidate.age_lower != null)
                    returnConditions["user_limit"]["age_lower"] = this.$data.formValidate.age_lower;
                if(this.$data.formValidate.grades.length != 0)
                    returnConditions["user_limit"]["grades"] = this.$data.formValidate.grades;
                if(this.$data.formValidate.sexes.length != 0)
                    returnConditions["user_limit"]["sexes"] = this.$data.formValidate.sexes;
                if(this.$data.formValidate.schools.length != 0)
                    returnConditions["user_limit"]["schools"] = this.$data.formValidate.schools;


                // console.log(returnConditions);
                return returnConditions;
            },



			handleSubmit (name) {
                 this.$data.taskInfoData = [];
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
                            params: this.getConditions(),
                            headers:{
                                'Authorization': jwt,
                            },
                        }).then(function (response){
                            // _this.$Message.success('success');
                            _this.$data.returnData = response;
                            // console.log(response);
                            for(var i = 0; i < response.data.length; ++i) {
                                var temptags = "";
                                var tempboss = response.data[i].creator_organization_name;
                                if(tempboss == null)
                                    tempboss = response.data[i].creator_user_name;
                                for(var j = 0; j < response.data[i].tags.length; ++j)
                                    temptags += response.data[i].tags[j] + " ";
                                var tempdata = {
                                    name: response.data[i].title,
                                    boss: tempboss,
                                    reltime: response.data[i].post_time,
                                    ddltime: response.data[i].receive_end_time,
                                    status: response.data[i].status,
                                    tag:  temptags,
                                    num: i
                                };
                                _this.$data.taskInfoData.push(tempdata);
                            }
                        }).catch(function (error) {
                            _this.$Message.error('failure');
                            console.log(error)
                        });
					 }
                })
			},

            handleReset (name) {
                this.$refs[name].resetFields();
                this.formValidate.tags = [];
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

.info {	
    margin-bottom: 10px;
}   
</style>