import Vue from 'vue'
import Router from 'vue-router'
import mainpage from '@/components/MainPage'
import userregister from '@/components/UserRegister'
import userinfomodify from '@/components/UserInfoModify'
import organregister from '@/components/OrganRegister'
import organization from '@/components/MyOrganization'
import organizationInfo from '@/components/OrganizationInfo'
import mytasks from '@/components/MyTasks'
import taskinfoforcreate from '@/components/TaskInfoForCreate'
import missioncreate from '@/components/MissionCreate'
import taskinfoforreceiver from '@/components/TaskInfoForReceiver'

import iView from 'iview'
import axios from 'axios'
import 'iview/dist/styles/iview.css'


Vue.use(Router);
Vue.use(iView);
Vue.prototype.$axios = axios    //全局注册，使用方法为:this.$axios
axios.defaults.headers.post['Content-Type'] = 'application/json';//配置请求头信息
axios.defaults.baseURL = process.env.BASE_API;
Vue.prototype.$profilePath = "http://localhost:5000/static/profile_pics/"; // 读取头像的路径
export default new Router({
	mode: 'history',
    routes: [
		{
		  path: '/',
		  name: 'mainpage',
		  component: mainpage
		},
		{
			path: '/userregister',
			name: 'userregister',
			component: userregister			
		},
		{
			path: '/userinfomodify',
			name: 'userinfomodify',
			component: userinfomodify
		},
		{
			path: '/organregister',
			name: 'organregister',
			component: organregister
		},
		{
			path: '/organization',
			name: 'organization',
			component: organization
		},
		{
			path: '/organizationInfo',
			name: 'organizationInfo',
			component: organizationInfo
		},
		{
			path: '/mytasks',
			name: 'mytasks',
			component: mytasks
		},
		{
			path: '/taskinfoforcreate',
			name: 'taskinfoforcreate',
			component: taskinfoforcreate
		},
		{
			path: '/missioncreate',
			name: 'missioncreate',
			component: missioncreate
		},
		{
			path: '/taskinfoforreceiver',
			name: 'taskinfoforreceiver',
			component: taskinfoforreceiver
		}
  ]
})

