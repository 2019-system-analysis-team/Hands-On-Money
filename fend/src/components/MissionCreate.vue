<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark">
					<div class="layout-head">任务创建</div>
					<div class="home-button">
						<Button shape="circle" icon="ios-home" @click="handleReturnHomepage()"></Button>
					</div>
				</Menu>
            </Header>
            <Content :style="{padding: '50px 50px'}">
				<Card :bordered="false">
                    <div slot="title">
                        <Row>
                            <Col span="20" v-show="isQuestionnaire">
					            <p>请填写下列信息</p>
                            </Col>
							<Col span="22" v-show="!isQuestionnaire">
							    <p>请填写下列信息</p>
							</Col>
                            <Col span="2" v-show="isQuestionnaire">
                                <Button class="addstepStyle" type="primary" @click="addSingleChoice()">添加单选</Button>
                            </Col>
							<Col span="1">
							    <Button class="addstepStyle" type="primary" @click="addStepClick()" v-show="!isQuestionnaire">增加步骤</Button>
								<Button class="addstepStyle" type="primary" @click="addProblem()" v-show="isQuestionnaire">添加问答</Button>
							</Col>
                        </Row>
                    </div>
					<Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80" id="form">
                        <Row>
                            <Col span="10" offset="1">
                                <FormItem label="名称" prop="taskName">
                                    <Input v-model="formValidate.taskName" placeholder="请输入任务的名称" ></Input>
                                </FormItem>
                                <FormItem label="简介" prop="missionbrief">
                                    <Input v-model="formValidate.missionbrief" type="textarea" :autosize="{minRows: 2,maxRows: 5}"></Input>
                                </FormItem>
                                <FormItem label="任务类型" prop="missiontype">
									<Select v-model="teskTag" @on-change="selectChange">
										<Option v-for="item in tagList" :value="item.value" :key="item.value">{{ item.label }}</Option>
									</Select>
                                </FormItem>
                                <FormItem label="人数" prop="memnumber">
                                    <InputNumber v-model="formValidate.memnumber" :max="99999" :min="1" placeholder="请输入参与任务的最大人数" ></InputNumber>
                                </FormItem>
                                <FormItem label="报酬" prop="reward">
                                    <InputNumber v-model="formValidate.reward" :max="99999" :min="1" placeholder="请输入任务报酬" ></InputNumber>
                                </FormItem>
                                <FormItem label="时间设置" prop="time">
                                    <DatePicker type="datetime" :options="beforeDate" :value="formValidate.receive_end_time" confirm   @on-change="receiveTimeChange" placeholder="任务接收截止时间" style="width: 200px"></DatePicker>
                                    <DatePicker type="datetime" :options="beforeDate" :value="formValidate.finish_deadline_time" confirm  @on-change="finishTimeChange"  placeholder="任务完成截止时间" style="width: 200px"></DatePicker>
                                </FormItem>
								 <Checkbox v-model="haveUserLimit"  @on-change="changeUserLimit">用户约束</Checkbox>
								 <FormItem label="年龄下限" prop="age_upper" v-show = "haveUserLimit">
								     <InputNumber v-model="user_limit.age_upper" :max="29" :min="10" placeholder="请输入最小参与者年龄" ></InputNumber>
								 </FormItem>
								 <FormItem label="年龄上限" prop="age_lower" v-show = "haveUserLimit">
								     <InputNumber v-model="user_limit.age_lower" :max="30" :min="11" placeholder="请输入最大参与者年龄" ></InputNumber>
								 </FormItem>
							     <FormItem label="年级" prop="grades" v-show = "haveUserLimit">
								 	<Select v-model="user_limit.grades" multiple :max-tag-count="6">
								 		<Option v-for="item in gradeList" :value="item.value" :key="item.value">{{ item.label }}</Option>
								 	</Select>
								 </FormItem>
							     <FormItem label="性别" prop="sexes" v-show = "haveUserLimit">
								 	<Select v-model="user_limit.sexes" multiple :max-tag-count="2">
								 		<Option v-for="item in sexesList" :value="item.value" :key="item.value">{{ item.label }}</Option>
								 	</Select>
								 </FormItem>
							     <FormItem label="学院" prop="schools" v-show = "haveUserLimit">
								 	<Select v-model="user_limit.schools" multiple :max-tag-count="6" filterable >
								 		<Option v-for="item in schoolsList" :value="item.value" :key="item.value">{{ item.label }}</Option>
								 	</Select>
								 </FormItem>
                            </Col>
                            <Col span="10" offset="2"z>
                                <!-- <Button id="addbutton" class="addstepStyle" type="primary" @click="addStepClick()">增加步骤</Button> -->
                                <Card style="height: 500px; overflow: auto;">
                                <Card v-for="cardItem in citems" :key="cardItem.id">
									<div slot="title" v-show="cardItem.state == '非问卷'">
									    步骤{{cardItem.number + 1}}
									</div>
									<div slot="title" v-show="cardItem.state != '非问卷'">
									    问题{{cardItem.number + 1}}
									</div>
                                    <div slot="extra">
										<Poptip placement="bottom" v-show="cardItem.state == '问卷单选'">
											<Button size="small">添加选项内容</Button>
											<div slot="content">
												<Input v-model="tempSingleText" placeholder="请输入选项内容" ></Input></br>
												<Button @click="addAsingle(tempSingleText,cardItem.id)">添加</Button>
											</div>
										</Poptip>
                                        <Button :size="delButtonSize" type="error" ghost @click="delStepClick(cardItem.number)">删除</Button>
                                    </div>
									<p v-show="cardItem.state == '非问卷'">标题：</P> 
									<p v-show="cardItem.state != '非问卷'">问题：</P> 
									<Input v-show="cardItem.state == '非问卷'" v-model="cardItem.title" placeholder="请输入该步骤的标题" ></Input>
									<Input v-show="cardItem.state == '问卷问题'" v-model="cardItem.title" placeholder="请输入要回答的问题" ></Input>
									<Input v-show="cardItem.state == '问卷单选'" v-model="cardItem.title" placeholder="请输入要进行选择的问题" ></Input>
									<p v-show="cardItem.state == '非问卷'">描述：</P>
									<p v-show="cardItem.state == '问卷单选'">单选选项：</P>
									<RadioGroup v-show="cardItem.state == '问卷单选'">
										<Radio v-for="single in cardItem.forsingle" :key="single.label" disabled><span>{{single.label}}</span></Radio>
									</RadioGroup>
									<Input  v-show="cardItem.state == '非问卷'" v-model="cardItem.description" type="textarea" :autosize="{minRows: 2,maxRows: 10}"></Input>
                                </Card>
                                </Card>
                            </Col>
                            <Col span="5" offset="11" style="padding-top: 10px;">
                                <Button type="success" style="right:0px; width: 50%;"  @click="handleSubmit('formValidate')">发布</Button>
                            </Col>
                        </Row>
                    </Form>
				</Card>
            </Content>
            <Footer class="layout-footer-center">2019-2019 &copy; Hands-On-Money</Footer>
        </Layout>
    </div>
</template>























<script>
  export default {
        data () {
			const validateReceiveDateCheck = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('任务接收截止时间不能为空'));
                } else {
					var local = this.getLocalTime();
					if(value < local){
						 callback(new Error('任务接收截止时间不能早于当前时间'));
					}
                }
				callback();
            };
			const validateAlwaysTrue = (rule, value, callback) => {
				callback();
			};
			const validateFinishTime = (rule, value, callback) => {
			    if (value === '') {
			        callback(new Error('任务完成截止时间不能为空'));
			    } else {
					if(this.formValidate.receive_end_time != '')
					{
						if(value < this.formValidate.receive_end_time)
						{
							callback(new Error('任务完成截止时间不能早于任务接收截止时间'));
						}
					}
			    }
				callback();
			};
            return {
				tempSingleText:'',
                delButtonSize: 'small',
                citemcount: 1,
                citemnum: 0,
                citems:[],

                formValidate: {
					taskName: '',
					missiontype: '问卷',
					memnumber: 1,
					reward: 1,
					receive_end_time: '',
					finish_deadline_time: '',
					missionbrief:'',
                },
                ruleValidate: {
					taskName: [
                        { required: true, message: '任务名称不能为空', trigger: 'blur' }
                    ],
                    missionbrief: [
                        { required: true, message: '内容不能为空',trigger: 'blur' }
                    ],
					memnumber:[
                        { required: true, validator: validateAlwaysTrue,trigger: 'blur' }
                    ],
					reward: [
                        { required: true,validator: validateAlwaysTrue,trigger: 'blur' }
                    ],
					time:[
                        { required: true, validator: validateAlwaysTrue,trigger: 'blur' }
                    ],
					missiontype: [
						{ required: true, message: '任务类型不能为空',trigger: 'blur' }
					],
                },
				teskTag:'心理实验',
				tasktags:['心理实验'],
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
                        value: '代跑腿',
                        label: '代跑腿'
                    }
                ],
				gradeList:[
					{
					    value: '大一',
					    label: '大一'
					},
                    {
                        value: '大二',
                        label: '大二'
                    },
                    {
                        value: '大三',
                        label: '大三'
                    },
                    {
                        value: '大四',
                        label: '大四'
                    },
                    {
                        value: '研究生',
                        label: '研究生'
                    },
					{
						value: '博士生',
						label: '博士生'
					}	
				],
				sexesList:[
                    { value: '男', label: '男'},
					{ value: '女', label: '女'}					
				],
				schoolsList:[
					{ value: '中国语言文学系', label: '中国语言文学系'},
					{ value: '历史学系', label: '历史学系'}	,
					{ value: '哲学系', label: '哲学系'},
					{ value: '社会学与人类学学院', label: '社会学与人类学学院'}		,				
					{ value: '博雅学院', label: '博雅学院'},
					{ value: '岭南学院', label: '岭南学院'}		,				
					{ value: '外国语学院', label: '外国语学院'},
					{ value: '法学院', label: '法学院'}	,
					{ value: '政治与公共事务管理学院', label: '政治与公共事务管理学院'},
					{ value: '管理学院', label: '管理学院'}	,
					{ value: '马克思主义学院', label: '马克思主义学院'},
					{ value: '心理学系', label: '心理学系'}		,				
					{ value: '传播与设计学院', label: '传播与设计学院'},
					{ value: '资讯管理学院', label: '资讯管理学院'}		,				
					{ value: '艺术学院', label: '艺术学院'},
					{ value: '数学学院', label: '数学学院'}		,					
					{ value: '物理学院', label: '物理学院'},
					{ value: '化学学院', label: '化学学院'}	,
					{ value: '地理科学与规划学院', label: '地理科学与规划学院'},
					{ value: '生命科学学院', label: '生命科学学院'}	,					
					{ value: '工学院', label: '工学院'},
					{ value: '材料科学与工程学院', label: '材料科学与工程学院'}	,					
					{ value: '电子与信息工程学院', label: '电子与信息工程学院'},
					{ value: '数据科学与计算机学院', label: '数据科学与计算机学院'}		,					
					{ value: '国家保密学院', label: '国家保密学院'}	,					
					{ value: '网络安全学院', label: '网络安全学院'},
					{ value: '环境科学与工程学院', label: '环境科学与工程学院'}		,				
					{ value: '系统科学与工程学院', label: '系统科学与工程学院'},
					{ value: '中山医学院', label: '中山医学院'}	,
					{ value: '光华口腔医学院', label: '光华口腔医学院'},
					{ value: '公共卫生学院', label: '公共卫生学院'}	,
					{ value: '药学院', label: '药学院'},
					{ value: '护理学院', label: '护理学院'},						
					{ value: '逸仙学院', label: '逸仙学院'},
				],
				post_time: null,
				user_limit: {
				    age_upper: 10,
				    age_lower: 30,
				    grades: [],
				    sexes: [],
				    schools: [],
				},
				haveUserLimit: false,
				beforeDate: {
                    disabledDate (date) {
                        return date && date.valueOf() < Date.now() - 86400000;
                    }
                },
				isOrganCreate: false,
				isTaskChange:false,
				organID:0,
				taskID:0,
				isQuestionnaire: false,
				isfirstEnter: true,
            }
        },
		created: function () { 
			this.getEventData();
		},
        methods: {
			getEventData:function() {
				let routerParams = window.localStorage.getItem("organID");
				//console.log(routerParams);
						
				if(routerParams != null)
				{
					this.isOrganCreate = true;
					this.organID = routerParams;
				}
				let task  = window.localStorage.getItem("taskID");
				if(task != null)
				{
					this.isTaskChange = true;
					this.taskID = task;
				}else
				{
					this.isTaskChange = false;
				}
				
				let uID = window.localStorage.getItem('userID')
				if(uID == null || uID == ""){
					//跳转到主页
					this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				}
				
				
				if(this.isTaskChange){
					var _this = this;
					var url = "/users/" + uID;
					if(this.isOrganCreate){
						url += "/organizations/" + this.organID + "/my_tasks/" + this.taskID;
					}
					else{
						url += "/my_tasks/" + this.taskID;
					}
					var jwt = "JWT " + window.localStorage.getItem('token');	
					this.$axios({
						 method:"get",
						 url: url,
						 headers:{
							'Authorization': jwt,
						 }
					}).then(function (response){
						console.log(response.data);
						_this.formValidate.taskName = response.data.title;
						_this.formValidate.missionbrief = response.data.description;
						_this.formValidate.memnumber = response.data.participant_number_limit;
						_this.formValidate.reward = response.data.reward_for_one_participant;
						_this.formValidate.receive_end_time = response.data.receive_end_time;
						_this.formValidate.finish_deadline_time = response.data.finish_deadline_time;
						_this.haveUserLimit = true;
						_this.user_limit.age_upper = response.data.user_limit.age_upper;
						_this.user_limit.age_lower = response.data.user_limit.age_lower;
						_this.user_limit.grades = response.data.user_limit.grades;
						_this.user_limit.sexes = response.data.user_limit.sexes;
						_this.user_limit.schools = response.data.user_limit.schools;
						_this.teskTag = response.data.tags;
						// 需要根据任务类型来区分 TODO
						if(_this.teskTag != '问卷'){
							for(var i=0; i< response.data.steps.length;i++){
								_this.citems.push({id: (_this.citemcount)++, number: _this.citemnum++,description:response.data.steps[i].description,title:response.data.steps[i].title,state:'非问卷',forsingle:[]});
							}	
						}else{
							for(var i=0; i< response.data.steps.length;i++){
								if(response.data.steps[i].description == ''){
									_this.citems.push({id: (_this.citemcount)++, number: _this.citemnum++,description:response.data.steps[i].description,title:response.data.steps[i].title,state:'问卷问题',forsingle:[]});
								}
								else{
									var tempsigle = [];
									var temp = response.data.steps[i].description.split('&');
									console.log(temp);
									for(var k = 1; k<temp.length;k++){
										var test = {};
										_this.$set(test,'label',temp[k]);
										tempsigle.push(test);
									}
									_this.citems.push({id: (_this.citemcount)++, number: _this.citemnum++,description:response.data.steps[i].description,title:response.data.steps[i].title,state:'问卷单选',forsingle:tempsigle});
								}
							}								
						}

					}).catch(function (error) {
						console.log(error);
					});	
				}
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
			addProblem(){
				this.citems.push({id: (this.citemcount)++, number: this.citemnum++,description:'',title:'',state:'问卷问题',forsingle:[]});
			},
			addSingleChoice(){
				this.citems.push({id: (this.citemcount)++, number: this.citemnum++,description:'',title:'',state:'问卷单选',forsingle:[]});
			},
            addStepClick: function() {
				this.citems.push({id: (this.citemcount)++, number: this.citemnum++,description:'',title:'',state:'非问卷',forsingle:[]});
            },
            delStepClick: function(delItemNum) {
               // console.log(delItemNum);
                for(var i = delItemNum + 1; i < this.$data.citems.length; ++i)
                    this.$data.citems[i].number--;
                this.$data.citems.splice(delItemNum, 1);
                --this.$data.citemnum;
            },
			addAsingle(tempSingleText,id){
				if(tempSingleText == '' || tempSingleText == null)
					return;

				for(var i=0;i<this.citems.length;i++)
				{
					if(this.citems[i].id == id)
					{
						var test = {};
						this.$set(test,'label',tempSingleText);
						this.citems[i].forsingle.push(test);

						this.citems[i].description = this.citems[i].description + "&" + tempSingleText;
						tempSingleText = '';
						
						console.log(this.citems[i].description);
					}
				}
			},
			receiveTimeChange(date){
				this.formValidate.receive_end_time = date;
			},
			finishTimeChange(date){
				this.formValidate.finish_deadline_time = date;
			},
			getLocalTime() {
			  var date = new Date();
			  var seperator1 = "-";
			  var year = date.getFullYear();
			  var month = date.getMonth() + 1;
			  var strDate = date.getDate();
			  var hours = date.getHours();
			  var minutes = date.getMinutes();
			  var seconds = date.getSeconds();
			  var seperator2 = ":";
			  if (month >= 1 && month <= 9) {
				month = "0" + month;
			  }
			  if (strDate >= 0 && strDate <= 9) {
				strDate = "0" + strDate;
			  }
			  if (hours >= 1 && hours <= 9) {
				hours = "0" + hours;
			  }
			  if (minutes >= 1 && minutes <= 9) {
				minutes = "0" + minutes;
			  }
			  if (seconds >= 1 && seconds <= 9) {
				seconds = "0" + seconds;
			  }
			  var currentdate = year + seperator1 + month + seperator1 + strDate + " " + hours + seperator2 + minutes + seperator2 + minutes;
			  //console.log(currentdate);
			  return currentdate;
			},
			handleSubmit (name) {
				 this.$refs[name].validate((valid) => {
					 if (valid){
						console.log("正在检验");
						// 任务类型不能为空
						if(this.tasktags.length == 0){
							 this.$Message.error('请至少选择一个任务类型!');
							 return;
						}
						// 时间的限制
						if (this.formValidate.receive_end_time === '') {
						     this.$Message.error('任务接收截止时间不能为空');
							 return;
						} else {
							var local = this.getLocalTime();
							if(this.formValidate.receive_end_time < local){
								 this.$Message.error('任务接收截止时间不能早于当前时间');
								 return;
							}
						}
						if (this.formValidate.finish_deadline_time === '') {
						     this.$Message.error('任务完成截止时间不能为空');
							  return;
						} else {
							if(this.formValidate.finish_deadline_time < this.formValidate.receive_end_time)
							{
								this.$Message.error('任务完成截止时间不能早于任务接收截止时间');
								 return;
							}
						}
						// 用户约束中的年龄
						if(this.haveUserLimit){
							if(this.user_limit.age_upper >= this.user_limit.age_lower){
								this.$Message.error('年龄下限不能大于等于年龄上限');
								 return;
							}
						}
						var steps = [];
						//console.log(this.citems);
						for(var i =0 ;i < this.citems.length;i++){
							var test={};
							this.$set(test,'title',this.citems[i].title);
							this.$set(test,'description',this.citems[i].description);
							steps.push(test);
						}
						
						if(this.citems.length == 0){
							this.$Message.error('请至少添加一个步骤或问题!');
							return;
						}
						
						/*
						*   POST /users/:user_id/tasks HTTP/1.1
							//or request: organization creating task 
							POST /users/:user_id/organizations/:organization_id/tasks HTTP/1.1
						*/
					   var _this = this;
					   var jwt = "JWT " + window.localStorage.getItem('token');
					   let uID = window.localStorage.getItem('userID');
						var url = "/users/" + uID;
						if(this.isOrganCreate){
							url += "/organizations/"+ this.organID + "/tasks";
						}else{
							url +=  "/tasks";
						}
						if(this.isTaskChange){
							url += "/" + this.taskID;
						}
						if(!this.isTaskChange){
							console.log("创建任务时候传到后端的参数:");
							console.log("任务名:" + this.formValidate.taskName + " 简介:" + this.formValidate.missionbrief);
							console.log(this.tasktags);
							this.tasktags[0] = this.teskTag; 
							console.log("参与者:" + this.formValidate.memnumber + " 报酬:" +this.formValidate.reward);
							console.log("创建任务时间:" +this.getLocalTime()+ "接收截止日期:" +this.formValidate.receive_end_time + "完成截止日期" + this.formValidate.finish_deadline_time);
							console.log(this.user_limit);
							console.log(steps);
							this.$axios({
									 method:"post",
									 url:url,
									 data:{
										title: this.formValidate.taskName,
										description: this.formValidate.missionbrief,
										tags: this.tasktags,
										participant_number_limit: this.formValidate.memnumber,
										reward_for_one_participant: this.formValidate.reward,
										post_time: this.getLocalTime(),
										receive_end_time: this.formValidate.receive_end_time,
										finish_deadline_time:this.formValidate.finish_deadline_time,
										user_limit:this.user_limit,
										steps:steps,
									 },
									 headers:{
										'Authorization': jwt,
									 }
							}).then(function (response){
									//console.log(response);
									var task_id = response.data.task_id;
									if(_this.isOrganCreate){
										window.localStorage.setItem('taskID', task_id);
										window.localStorage.setItem('organID', _this.organID);
										_this.$router.push({
											path: '/', 
											name: 'taskinfoforcreate',
											params: { 
													taskID: task_id,
													organID: _this.organID,
											},
										});	
									}else{
										window.localStorage.setItem('taskID', task_id);
										_this.$router.push({
											path: '/', 
											name: 'taskinfoforcreate',
											params: { 
													taskID: task_id,
											},
										});	
									}
									 _this.$Message.success('创建任务成功!');
							}).catch(function (error) {
								_this.$Message.error('创建任务失败!');
							
							});
						}else{
							this.tasktags[0] = this.teskTag; 
							this.$axios({
									 method:"put",
									 url:url,
									 data:{
										title: this.formValidate.taskName,
										description: this.formValidate.missionbrief,
										tags: this.tasktags,
										participant_number_limit: this.formValidate.memnumber,
										reward_for_one_participant: this.formValidate.reward,
										post_time: this.getLocalTime(),
										receive_end_time: this.formValidate.receive_end_time,
										finish_deadline_time:this.formValidate.finish_deadline_time,
										user_limit:this.user_limit,
										steps:steps,
									 },
									 headers:{
										'Authorization': jwt,
									 }
							}).then(function (response){
									//console.log(response);
									var task_id = response.data.task_id;
									if(_this.isOrganCreate){
										window.localStorage.setItem('taskID', task_id);
										window.localStorage.setItem('organID', _this.organID);
										_this.$router.push({
											path: '/', 
											name: 'taskinfoforcreate',
											params: { 
													taskID: task_id,
													organID: _this.organID,
											},
										});	
									}else{
										window.localStorage.setItem('taskID', task_id);
										_this.$router.push({
											path: '/', 
											name: 'taskinfoforcreate',
											params: { 
													taskID: task_id,
											},
										});	
									}
									 _this.$Message.success('修改任务成功!');
							}).catch(function (error) {
								_this.$Message.error('修改任务失败!');
							
							});							
						}
						
						
						console.log("提交成功");
					 }
					 else
					 {
						 console.log("奇怪的错误");
					 }
				 });
				 console.log("进去");
			},
			changeUserLimit(){
				if(this.haveUserLimit == true)
				{
					this.user_limit.age_upper = 10;
					this.user_limit.age_lower = 30;
					this.user_limit.grades = [];
					this.user_limit.sexes = [];
					this.user_limit.schools = [];
				}
				return !this.haveUserLimit;
			},
			selectChange(value){
				if(this.isfirstEnter && (value == '问卷' || value == '代跑腿')){
					this.isfirstEnter = false;
					if(value == '问卷') this.isQuestionnaire = true;
					return;
				}
				if(value == '问卷'){
					this.isQuestionnaire = true;
				}else{
					this.isQuestionnaire = false;
				}
				this.citems = [];
				this.citemcount = 1;
				this.citemnum = 0;
			},
        }
    }
</script>
























<style scoped>
.addstepStyle {
    text-align: center;
}
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
	width: 100%;
}
</style>