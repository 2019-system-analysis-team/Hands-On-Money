<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu active-name="organization" mode="horizontal" theme="dark" ref="menu">
                    <div class="layout-logo"></div>
                    <div class="layout-nav">
                        <Submenu name="1">
							 <template slot="title">
								<Icon type="ios-ionic"></Icon>
								任务
							 </template>
							<MenuItem name="1-1" to="/mytasks">我的任务</MenuItem>
							<MenuItem name="1-2" @click.native ="createNewTask()">新建任务</MenuItem>
							<MenuItem name="1-3" to="/taskmarket">任务市场</MenuItem>
                        </Submenu>
                        <Submenu name="2">
							<template slot="title">
								<Icon type="ios-contacts"></Icon>
								组织
							</template>
							<MenuItem name="organization" to="/organization">我的组织</MenuItem>
							<MenuItem name="organregister" to="/organregister">新建组织</MenuItem>
                        </Submenu>
						<Submenu name="3">
							<template slot="title">
								<Icon type="ios-card" />
								钱包
							</template>
							<MenuItem name="3-1" @click.native="GotoTopup()">充值</MenuItem>
							<MenuItem name="3-2">提现</MenuItem>
							<MenuItem name="3-3">账户余额 : {{money}}</MenuItem>
						</Submenu>
                    </div>
					<div>
						<Submenu name="4">
							<template slot="title">
								<Avatar :src="profilePhotoPath" style="background-color: #87d068"></Avatar>
							</template>
							<MenuItem name="4-1" to="/userinfomodify">个人信息</MenuItem>
							<MenuItem name="4-2" @click.native="logout()">退出</MenuItem>
						</Submenu>
					</div>
					<Button shape="circle" icon="ios-home" @click="handleReturnHomepage()"></Button>
                </Menu>
            </Header>
			<Content :style="{padding: '24px', minHeight: '280px', background: '#fff'}">
				<Card dis-hover style="height: 560px">
					<p slot="title" style="height: 38px;">
						<Select v-model="organclass" style="width:200px" @on-change="selectChange">
							<Option v-for="item in classifications" :value="item.value" :key="item.value">{{ item.label }}</Option>
						</Select>
					</p>
							<Table border :columns="tableOrganization" :data="allOrganizations" v-if="this.SelectType == 0"></Table>
							<Table border :columns="tableOrganization" :data="manageOrganizations" v-if="this.SelectType == 1"></Table>
							<Table border :columns="tableOrganization" :data="createOrganizations" v-if="this.SelectType == 2"></Table>
							<Table border :columns="tableOrganization" :data="joinOrganizations" v-if="this.SelectType == 3"></Table>					
				</Card>			
            </Content>
            <Footer class="layout-footer-center">2019-2019 &copy; SYSU</Footer>
        </Layout>
		<Drawer
			title="充值"
			v-model="topup"
			width="400"
			:mask-closable="true"
			:styles="styles"
		>
			<Form :model="topupData">
					<FormItem label="充值金额 : " label-position="top">
					<InputNumber
								:max="10000"
								:min="1"
								 v-model="topupData.value"
								></InputNumber>
					</FormItem>
					<FormItem label="支付方式" label-position="top">
						<Select v-model="topupData.mode">
							<Option value="支付宝">支付宝</Option>
							<Option value="微信支付">微信支付</Option>
							<Option value="信用卡">信用卡</Option>
						</Select>
					</FormItem>
				</Row>
			</Form>
			<div class="demo-drawer-footer">
				<Button style="margin-right: 8px" @click="topup = false">取消</Button>
				<Button type="primary" v-on:click="recharge">充值</Button>
			</div>
		</Drawer>    
    </div>
</template>
<script>
  export default {
        data () {
            return {
				userID: '',
                tableOrganization: [
                    {
                        title: '组织名称',
                        key: 'organization_name'
                    },
                    {
                        title: '权限',
                        key: 'status'
                    },
                    {
                        title: '更多',
                        key: 'action',
                        width: 150,
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: {
                                        type: 'primary',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
											this.goOrganInfo(params.index);
                                        }
                                    }
                                }, '详情')
                            ]);
                        }
                    }
                ],
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
				profilePhotoPath:'',
				organclass:'全部组织',
				classifications: [
                    {
                        value: '全部组织',
                        label: '全部组织'
                    },
                    {
                        value: '我管理的',
                        label: '我管理的'
                    },
                    {
                        value: '我创建的',
                        label: '我创建的'
                    },
                    {
                        value: '我加入的',
                        label: '我加入的'
                    }
                ],				
				allOrganizations:[

				],
				manageOrganizations:[

				],
				joinOrganizations:[

				],
				createOrganizations:[

				],
				SelectType: 0,
            }
        },
		mounted(){
		  this.$nextTick(()=>{
		  })
		},
		created: function () { 
			this.getEventData();
		},
        methods: {
			getEventData:function() {
				//要用完全的路径	
				let uID = window.localStorage.getItem('userID')
			
				if(uID == null || uID == ""){
					//跳转到主页
					this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				}
		
				var url = "/users/" + uID + "/organizations";
				this.$data.userID = uID;
				var jwt = "JWT " + window.localStorage.getItem('token');
		
				var _this = this;
				this.$axios({
						 method:"get",
						 url:url,
						 headers:{
							'Authorization': jwt,
						 }
				}).then(function (response){
					//console.log(response);					
					_this.allOrganizations = response.data.organizations;
					for(var i=0; i<_this.allOrganizations.length;i++){
						if(_this.allOrganizations[i].status == "member"){
							_this.joinOrganizations.push(_this.allOrganizations[i]);
						}else if(_this.allOrganizations[i].status == "owner"){
							_this.createOrganizations.push(_this.allOrganizations[i]);
						}else if(_this.allOrganizations[i].status == "manager"){
							_this.manageOrganizations.push(_this.allOrganizations[i]);
						}
					} 
										
				}).catch(function (error) {
					_this.$Message.error('请先登录!');
					//跳转到主页
					_this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				});

			   this.profilePhotoPath = window.localStorage.getItem('MyProfilePhotoPath');
			},
            handleReturnHomepage () {
                // 返回主页
				this.$router.push({
					path: '/', 
					name: 'mainpage',
				});		
            },
			goOrganInfo(index){
                // 去组织的详情页面
				
				if(this.SelectType == 0){
					window.localStorage.setItem('organID', this.allOrganizations[index].organization_id);
					this.$router.push({
						path: '/', 
						name: 'organizationInfo',
						params: { 
								organID: this.allOrganizations[index].organization_id
						},
					});		
				}else if(this.SelectType == 1){
					window.localStorage.setItem('organID', this.manageOrganizations[index].organization_id);
					this.$router.push({
						path: '/', 
						name: 'organizationInfo',
						params: { 
								organID: this.manageOrganizations[index].organization_id
						},
					});						
				}else if(this.SelectType == 2){
					window.localStorage.setItem('organID', this.createOrganizations[index].organization_id);
					this.$router.push({
						path: '/', 
						name: 'organizationInfo',
						params: { 
								organID: this.createOrganizations[index].organization_id
						},
					});						
				}else if(this.SelectType == 3){
					window.localStorage.setItem('organID', this.joinOrganizations[index].organization_id);
					this.$router.push({
						path: '/', 
						name: 'organizationInfo',
						params: { 
								organID: this.joinOrganizations[index].organization_id
						},
					});						
				};			
			},
			GotoTopup (){
				this.topup = true;
			},
			recharge(){
				this.$Message.success('充值成功!');
				this.money = this.topupData.value + this.money;
				this.topup = false;
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
					_this.$router.push({
						path: '/', 
						name: 'mainpage'
					});	
				}).catch(function (error) {
					console.log(error);
				});
			},
			selectChange(value){
				//console.log(value);
				if(value == '全部组织'){
					this.SelectType = 0;
				}else if(value == '我管理的'){
					this.SelectType = 1;
				}else if(value == '我创建的'){
					this.SelectType = 2;
				}else if(value == '我加入的'){
					this.SelectType = 3;
				}
			},
			createNewTask() {
				this.$router.push({
					path: '/', 
					name: 'missioncreate'
				});		
			}
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
    margin-right: 112px;
}
.layout-footer-center{
    text-align: center;
}
.ivu-layout-header{
    padding-right: 25px;
}
</style>
