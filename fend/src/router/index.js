import Vue from 'vue'
import Router from 'vue-router'
import mainpage from '@/components/MainPage'
import userlogin from '@/components/UserLogin'
import userregister from '@/components/UserRegister'
import userinfomodify from '@/components/UserInfoModify'
import organregister from '@/components/OrganRegister'
import iView from 'iview';
import axios from 'axios'
import 'iview/dist/styles/iview.css';

Vue.use(Router);
Vue.use(iView);
Vue.prototype.$axios = axios    //全局注册，使用方法为:this.$axios
axios.defaults.headers.post['Content-Type'] = 'application/json';//配置请求头信息
axios.defaults.baseURL = 'http://localhost:5000';

export default new Router({
	mode: 'history',
    routes: [
		{
		  path: '/',
		  name: 'mainpage',
		  component: mainpage
		},
		{
			path: '/userlogin',
			name: 'userlogin',
			component: userlogin
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
		}
  ]
})

