<script setup>
import { RouterView } from 'vue-router'
import router from "@/router";
import {useUserStore} from "@/stores/user";
import request from "@/utils/request";
import {ElMessage} from "element-plus";
import {nextTick, ref} from "vue";
import config from "../../config";

const userStore = useUserStore()
let user = userStore.getUser
const activePath = router.currentRoute.value.path
const name = ref('')  
name.value = router.currentRoute.value.query.name || ''
const childRef = ref()
const menus = ref([])


const logout = () => {
  request.get('/logout/' + user.uid).then(res => {
    if (res.code === '200') {
      userStore.logout()
	  window.location.href="/front"
    } else {
      ElMessage.error(res.msg)
    }
  })
}


const getAvatarHandler = (avatar) => {
  user.avatar = avatar
}

const search = () => {
  router.push('/front/recruit?name=' + name.value)
}

</script>

<template>
  <div>
    <div style="display: flex; height: 100px; line-height: 100px; border-bottom: 1px solid #eee;">
      <div style="flex: 2; font-size: 26px; color: #FF9900; font-weight: bold;margin-left: 180px;">{{config.projectName}}</div>
      <div style="flex: 2;">
        <!-- Search bar -->
        <el-input style="width: 250px" placeholder="Search lost and found information" v-model="name" clearable size="large"></el-input>
        <el-button style="margin-left: 5px;background-color: #FF9900;color: #FFFFFF;" @click="search" size="large">search</el-button>
      </div>
      <div style="flex: 3; font-size: 16px; color: #FF9900;" v-if="user.id">
        <el-avatar :size="30" :src="user.avatar" style="margin-top: 10px;" />
        Hello，{{ user.name }}
        <a href="javascript:void(0)" @click="router.push('/person')" class="loginCls">Modification information</a>
        <a href="javascript:void(0)" @click="router.push('/password')" class="loginCls">Change password</a>
        <a href="javascript:void(0)" @click="logout" class="loginCls">Log out</a>
      </div>
      <div style="flex: 3; font-size: 16px; color: #FF9900; margin-left: 180px;" v-else>
        <a href="javascript:void(0)" @click="router.push('/login')" class="loginCls">Log in</a>
        <a href="javascript:void(0)" @click="router.push('/register-member')" class="loginCls">User Registration</a>
      </div>
    </div>

    <div style="display: flex; height: 60px; line-height: 60px; border-bottom: 1px solid #eee;background-color: #FF9900;">
      <div style="width: 200px; display: flex; padding-left: 30px">
      </div>
      <div style="flex: 1; display: flex">
        <el-menu :default-active="activePath" mode="horizontal" router style="border: none; height: 100%; width: 100%;background-color: #FF9900;">
          <el-menu-item index="/front/home">Front page</el-menu-item>
          <el-menu-item index="/front/notice">System Announcement</el-menu-item>
          <el-menu-item index="/front/recruit">Lost and Found Information</el-menu-item>
          <el-menu-item index="/front/lost">Lost property information</el-menu-item>
          <el-menu-item index="/front/orders">Lost and found records</el-menu-item>
          <el-menu-item index="/recruit" v-if="user.id!=null && user.role=='MEMBER'">Post a lost and found</el-menu-item>
          <el-menu-item index="/lost" v-if="user.id!=null && user.role=='MEMBER'">Report a lost item</el-menu-item>
          <el-menu-item index="/home" v-if="user.id!=null && user.role=='ADMIN'">Enter the backend management</el-menu-item>
        </el-menu>
      </div>
    </div>

    <div style="width: 100%; margin: 0 auto;min-height: 600px;">
      <router-view v-slot="{ Component }">
        <component @getAvatar="getAvatarHandler" @getUnread="getUnRead" ref="childRef" :is="Component" />
      </router-view>
    </div>


    <div style="height: 100px; line-height: 100px; border-top: 1px solid rgba(208,208,208,0.08);text-align: center;background-color: #FF9900;color: #FFFFFF;">
      <span>{{config.projectName}}</span>
    </div>
  </div>
</template>

<style scoped>
  .badge {
    margin-top: 10px;
    margin-right: 40px;
  }
  :deep(.el-badge__content.is-fixed) {
    top: 10px !important;
  }

  .content {
    text-align: center;
  }

  .el-menu-item{
    background-color: #FF9900;
    color: #FFFFFF;
  }

  .el-menu--horizontal>.el-menu-item.is-active{
    color: #ffffff !important;
    border-bottom: 2px solid #ffffff !important;
  }

  .loginCls{
    margin-left: 25px;
    text-decoration: none;
    color: #FF9900;
  }
  .loginCls a {
    text-decoration: none;
    color: #333;
    transition: color 0.3s;
  }

  .loginCls:hover {
    color: #f00;
  }

  .loginCls:visited {
    color: #999;
  }

  .loginCls::after {
    content: '';
    width: 0;
    height: 1px;
    background-color: #f00;
    transition: width 0.3s;
  }

  .loginCls:hover::after {
    width: 100%;
  }
</style>
