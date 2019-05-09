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
							<MenuItem name="1-1">我的任务</MenuItem>
							<MenuItem name="1-2">新建任务</MenuItem>
							<MenuItem name="1-3">所有任务</MenuItem>
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
					
					<Col span="8" v-for="item in selectOrganizations" :key="item.id" style="padding-left: 30px; padding-top: 50px;">
						<Card>
							<p slot="title">{{item.name}}</p>
							<div slot="extra" @click="goOrganInfo(item.id)">
								    <Tooltip content="点击进入组织信息页面" placement="top">
										<Avatar :src="item.organPhotoPath" style="background-color: #87d068">{{item.name}}</Avatar>
									</Tooltip>
							</div>	
							<p>{{item.bio}}</p>
							 
						</Card>
					</Col>
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
				jwt:{},
				profilePhotoName:'',
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
					{
						name:'红太阳',
						bio:'我们是共产主义接班人，hhhhhhhhhhhhhhh',
						organPhotoPath:'',
						status:'创建者',
						id:1,
					},
					{
						name:'绿太阳',
						bio:'我们是共产主义接班人，hhhhhhhhhhhhhhh',
						organPhotoPath:'',
						status:'管理者',
						id:2
					},
					{
						name:'黄太阳',
						bio:'我们是共产主义接班人，hhhhhhhhhhhhhhh',
						organPhotoPath:'',
						status:'成员',
						id:3
					},
					{
						name:'蓝太阳',
						bio:'我们是共产主义接班人，hhhhhhhhhhhhhhh',
						organPhotoPath:'',
						status:'成员',
						id:4
					},
				],
				manageOrganizations:[
					{
						name:'绿太阳',
						bio:'我们是共产主义接班人，hhhhhhhhhhhhhhh',
						organPhotoPath:'',
						status:'管理者',
						id:2
					}
				],
				joinOrganizations:[
					{
						name:'黄太阳',
						bio:'我们是共产主义接班人，hhhhhhhhhhhhhhh',
						organPhotoPath:'',
						status:'成员',
						id:3
					},
					{
						name:'蓝太阳',
						bio:'我们是共产主义接班人，hhhhhhhhhhhhhhh',
						organPhotoPath:'',
						status:'成员',
						id:4
					},
				],
				createOrganizations:[
					{
						name:'红太阳',
						bio:'我们是共产主义接班人，hhhhhhhhhhhhhhh',
						organPhotoPath:'',
						status:'创建者',
						id:1
					}
				],
				selectOrganizations:[],
            }
        },
		mounted(){
		  this.$nextTick(()=>{
			  // 设置导航的当前菜单项
			//this.activeName = this.$route.path.slice(1);
			//console.log(this.activeName);
			//this.$refs.menu.updateOpened();
			//this.$refs.menu.updateActiveName();
		  })
		},
		created: function () { 
			this.getEventData();
		},
        methods: {
			getEventData:function() {
				this.selectOrganizations = this.allOrganizations;
				this.$data.profilePhotoName = '头像';
				//要用完全的路径
				this.$data.profilePhotoUrl = "/users/:"  + "profile_photo_path";		
				let uID = window.localStorage.getItem('userID')
				if(uID == null || uID == ""){
					//跳转到主页
					this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				}
				var url = "/users/" + uID.toString() + "organizations";
				this.$data.userID = uID;
				this.$data.profilePhotoUrl = "/users/" + uID.toString() + "profile_photo_path";
				var jwt = "JWT " + window.localStorage.getItem('token');
				this.$set(this.jwt,'Authorization',jwt);
				
				/*
				var _this = this;
				this.$axios({
						 method:"get",
						 url:url,
						 headers:{
							'Authorization': jwt,
						 }
				}).then(function (response){
					console.log(response);
					this.$data.allOrganizations =  response.data.organizations;
					// 根据状态筛选出哪些是管理哪些是创建
					// TODO
					
				}).catch(function (error) {
					_this.$Message.error('请先登录!');
					//跳转到主页
					_this.$router.push({
						path: '/', 
						name: 'mainpage'
					});
				});
				*/
			},
            handleReturnHomepage () {
                // 返回主页
				this.$router.push({
					path: '/', 
					name: 'mainpage',
				});		
            },
			goOrganInfo(id){
                // 去组织的详情页面
				this.$router.push({
					path: '/', 
					name: 'organizationInfo',
					params: { 
							organID: id
					},
				});					
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
				console.log(value);
				if(value == '全部组织'){
					this.selectOrganizations = this.allOrganizations;
				}else if(value == '我管理的'){
					this.selectOrganizations = this.manageOrganizations;
				}else if(value == '我创建的'){
					this.selectOrganizations = this.createOrganizations;
				}else if(value == '我加入的'){
					this.selectOrganizations = this.joinOrganizations;
				}
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
