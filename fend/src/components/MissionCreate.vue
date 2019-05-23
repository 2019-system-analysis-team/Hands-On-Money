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
                            <Col span="22">
					            <p>请填写下列信息</p>
                            </Col>
                            <Col span="1">
                                <Button id="addbutton" class="addstepStyle" type="primary" @click="addStepClick()">增加步骤</Button>
                            </Col>
                        </Row>
                    </div>
					<Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80" id="form">
                        <Row>
                            <Col span="10" offset="1">
                                <FormItem label="名称" prop="nickname">
                                    <Input v-model="formValidate.nickname" placeholder="请输入任务的名称" ></Input>
                                </FormItem>
                                <FormItem label="简介" prop="missionbrief">
                                    <Input v-model="formValidate.missionbrief" type="textarea" :autosize="{minRows: 2,maxRows: 5}"></Input>
                                </FormItem>
                                <FormItem label="任务类型" prop="missiontype">
                                    <Select v-model="formValidate.missiontype">
                                        <Option value="问卷">问卷</Option>
                                        <Option value="心理实验">心理实验</Option>
                                        <Option value="其他">其他</Option>
                                    </Select>
                                </FormItem>
                                <FormItem label="人数" prop="memnumber">
                                    <InputNumber v-model="formValidate.memnumber" placeholder="请输入参与任务的最大人数" ></InputNumber>
                                </FormItem>
                                <FormItem label="报酬" prop="reward">
                                    <InputNumber v-model="formValidate.reward" placeholder="请输入任务报酬" ></InputNumber>
                                </FormItem>
                                <FormItem label="时间设置">
                                    <DatePicker type="datetime" placeholder="任务接收截止时间" style="width: 200px"></DatePicker>
                                    <DatePicker type="datetime" placeholder="任务完成截止时间" style="width: 200px"></DatePicker>
                                </FormItem>
                            </Col>
                            <Col span="10" offset="2"z>
                                <!-- <Button id="addbutton" class="addstepStyle" type="primary" @click="addStepClick()">增加步骤</Button> -->
                                <Card style="height: 380px; overflow: auto;">
                                <Card v-for="cardItem in citems" :key="cardItem.id">
                                    步骤{{cardItem.number + 1}}描述:
                                    <div slot="extra">
                                        <Button :size="delButtonSize" type="error" ghost @click="delStepClick(cardItem.number)">删除</Button>
                                    </div>
                                    <Input style="padding-top:5px;" type="textarea" :autosize="{minRows: 2,maxRows: 10}"></Input>
                                </Card>
                                </Card>
                            </Col>
                            <Col span="2" offset="11" style="padding-top: 10px;">
                                <Button type="primary" style="right:0px;">发布</Button>
                            </Col>
                        </Row>
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
                    callback(new Error('任务名称不能为空'));
                } else {
                    callback();
                }
            };
			const validateBriefCheck = (rule, value, callback) => {
			    if (value === '') {
			        callback(new Error('内容不能为空'));
			    } else {
			        callback();
			    }
			};
			const validateNumberCheck = (rule, value, callback) => {
			    if (value < 0) {
			        callback(new Error('人数不能为负数'));
			    } else {
			        callback();
			    }
			};
            return {
                delButtonSize: 'small',
                citemcount: 1,
                citemnum: 0,
                citems:[],
                ageoptionsList:[],
				// isManager: false,
				// isCreater: true,
                formValidate: {
					nickname: '',
					missiontype: '问卷',
                },
                ruleValidate: {
					nickname: [
                        { required: true, validator: validateNameCheck, trigger: 'blur' }
                    ],
                    missionbrief: [
                        { required: true, validator: validateBriefCheck, trigger: 'blur' }
                    ],
                    memnumber: [
                        { required: true, validator: validateNumberCheck, trigger: 'blur' }
                    ]
                }
            }
        },
		created: function () { 
			this.getEventData();
		},
        methods: {
			getEventData:function() {
				for(var i = 10;i<=30;i++){
					this.$data.ageoptionsList.push({label:i.toString(),value:i.toString()});
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
            addStepClick: function() {
                this.citems.push({id: (this.citemcount)++, number: this.citemnum++});
                console.log("length " + this.citems.length);
            },
            delStepClick: function(delItemNum) {
                console.log(delItemNum);
                for(var i = delItemNum + 1; i < this.$data.citems.length; ++i)
                    this.$data.citems[i].number--;
                this.$data.citems.splice(delItemNum, 1);
                --this.$data.citemnum;
            }
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