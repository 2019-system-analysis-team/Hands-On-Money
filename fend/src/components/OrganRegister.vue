<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark" active-name="1">
					<div class="layout-head">
						组织创建
					</div>
				</Menu>
            </Header>
            <Content :style="{padding: '50px 50px'}">
                <Card :bordered="false">
					<p slot="title">请填写下列信息</p>
					<Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80" id="form">
						<FormItem label="组织头像" prop="photo">
							<div class="demo-upload-list" v-for="item in uploadList">
								<template v-if="item.status === 'finished'">
									<img :src="item.url">
									<div class="demo-upload-list-cover">
										<Icon type="ios-eye-outline" @click.native="handleView(item.name)"></Icon>
									</div>
								</template>
								<template v-else>
									<Progress v-if="item.showProgress" :percent="item.percentage" hide-info></Progress>
								</template>
							</div>
							<Upload
								ref="upload"
								:show-upload-list="false"
								:default-file-list="defaultList"
								:on-success="handleSuccess"
								:format="['jpg','jpeg','png']"
								:max-size="2048"
								:on-format-error="handleFormatError"
								:on-exceeded-size="handleMaxSize"
								:before-upload="handleBeforeUpload"
								multiple
								type="drag"
								action="//jsonplaceholder.typicode.com/posts/"
								style="display: inline-block;width:78px;">
								<div style="width: 78px;height:78px;line-height: 78px;">
									<Icon type="ios-camera" size="40"></Icon>
								</div>
							</Upload>
							<Modal title="浏览头像" v-model="visible">
								<img :src="'https://o5wwk8baw.qnssl.com/' + imgName + '/avatar'" v-if="visible" style="width: 100%">
							</Modal>
						</FormItem>
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
			ageoptionsList:[],
			 formValidate: {
				 name: '',
				 desc: ''
			 },
			 defaultList: [
				 {
					 'name': 'a42bdcc1178e62b4694c830f028db5c0',
					 'url': 'https://o5wwk8baw.qnssl.com/a42bdcc1178e62b4694c830f028db5c0/avatar'
				 }
			 ],
			 imgName: '',
			 visible: false,
			 uploadList: [],
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
		methods: {
            handleSubmit (name) {
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        this.$Message.success('组织注册成功!');
                    } else {
                        this.$Message.error('信息填写有误!');
                    }
                })
            },
            handleReset (name) {
                this.$refs[name].resetFields();
            },
			handleView (name) {
                this.imgName = name;
                this.visible = true;
            },
            handleSuccess (res, file) {
                file.url = 'https://o5wwk8baw.qnssl.com/a42bdcc1178e62b4694c830f028db5c0/avatar';
                file.name = 'a42bdcc1178e62b4694c830f028db5c0';
            },
            handleFormatError (file) {
                this.$Notice.warning({
                    title: '文件格式不正确',
                    desc: '文件 ' + file.name + ' 的格式不正确, 请选择 jpg 或者 png.'
                });
            },
            handleMaxSize (file) {
                this.$Notice.warning({
                    title: '超出文件大小限制',
                    desc: '文件  ' + file.name + ' 太大, 不能超过 2M.'
                });
            },
            handleBeforeUpload () {
                const check = this.uploadList.length == 1;
                if (check) {
					this.$refs.upload.fileList.splice(0, 1);
                }
				else
				{
					return !check;
				}
                return check;
            }
        },
        mounted () {
            this.uploadList = this.$refs.upload.fileList;
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
	margin:0 auto;
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