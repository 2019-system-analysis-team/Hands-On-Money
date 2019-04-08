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
					<div class="layout-button">
						<Button type="default" ghost v-on:click="login">登录</Button>
						<Button type="primary" ghost v-on:click="login">注册</Button>
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
                    <div style="min-height: 200px;">
                        Content
                    </div>
                </Card>
            </Content>
            <Footer class="layout-footer-center">2019-2019 &copy; SYSU</Footer>
        </Layout>
    </div>
</template>
<script>
    export default {
		data() {
			return { 
			};
		}, 
		methods: {
			login: function () {
				this.$router.push({
						path: '/userlogin'
				});			
			},
			register: function () {
				this.$router.push({
						path: '/userregister'
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
</style>
