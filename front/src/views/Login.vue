<script setup>
import {onMounted, reactive, ref, watch} from "vue"
import {User, Lock} from '@element-plus/icons-vue'
import request from "@/utils/request";
import {ElMessage} from "element-plus";
import {useUserStore} from "@/stores/user";
import router, {setRoutes} from "@/router";
import SIdentify from '../components/Sidentify.vue';
import config from "../../config";

// Graphic verification code
let identifyCodes = "1234567890"
let identifyCode = ref('')
const failCount = ref(0)
const randomNum = (min, max) => {
  return Math.floor(Math.random() * (max - min) + min)
}
const makeCode = (o, l) => {
  for (let i = 0; i < l; i++) {
    identifyCode.value += o[randomNum(0, o.length)];
  }
}
const refreshCode = () => {
  identifyCode.value = "";
  makeCode(identifyCodes, 4);
}
// Generate verification code
onMounted(() => {
  identifyCode.value = "";
  makeCode(identifyCodes, 4);
})

const loginData = reactive({})
const rules = reactive({
  username: [
    {required: true, message: 'Please enter your account number', trigger: 'blur'},
  ],
  password: [
    {required: true, message: 'Please enter your password', trigger: 'blur'},
    {min: 3, max: 20, message: 'The password length is between 3 and 20 characters.', trigger: 'blur'},
  ],
})
const ruleFormRef = ref()
const login = () => {
  ruleFormRef.value.validate(valid => {
    if (valid) {
      //Fail 3 times to trigger the verification code
      if (failCount.value >= 3 && loginData.code !== identifyCode.value) {
        ElMessage.warning('Verification code error')
        return
      }
      // Send form data to the backend
      request.post('/login', loginData).then(res => {
        if (res.code === '200') {
          if (res.data.user.role === 'ADMIN') {
            router.push('/') // Home page of the backend
          }
          		  else if(res.data.user.role === 'MEMBER'){
            router.push('/front') 
          }
          ElMessage.success('Login successful')
          const userStore = useUserStore()
          userStore.setManagerInfo(res.data)
        } else {
          ElMessage.error(res.msg)
          failCount.value ++  // The number of failures increases by 1
        }
      })
    }
  })
}

</script>

<template>
  <div class="wrapper">
    <div style="margin: 150px auto; background-color: #FF9900; width: 400px; height: 380px; padding: 20px; border-radius: 10px">
      <div style="margin: 20px 0; text-align: center; font-size: 24px;color: #ffffff;"><b>{{config.projectName}}</b></div>
      <el-form
              ref="ruleFormRef"
              :model="loginData"
              :rules="rules"
              size="large"
              status-icon
      >
        <el-form-item prop="username">
          <el-input 
            size="medium" 
            style="margin: 10px 0" 
            :prefix-icon="User" 
            v-model="loginData.username" 
            placeholder="Please enter your username">
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input 
            size="medium" 
            style="margin: 10px 0" 
            :prefix-icon="Lock" 
            show-password 
            v-model="loginData.password" 
            placeholder="Please enter your password">
          </el-input>
        </el-form-item>
        <div style="display: flex; margin: 15px 0" v-if="failCount >= 3">
          <div style="flex: 1">
            <el-input v-model="loginData.code" placeholder="Verification Code"></el-input>
          </div>
          <div>
            <div @click="refreshCode" style="margin-left: 5px">
              <SIdentify :identifyCode="identifyCode" />
            </div>
          </div>
        </div>
        <el-form-item style="margin: 10px 0; text-align: right">
          <el-button type="primary" autocomplete="off" @click="login">Log in</el-button>
          <el-button type="info" autocomplete="off" @click="router.push('/register-member')">User Registration</el-button>
        </el-form-item>
      </el-form>
      <div style="text-align: center; margin-top: 15px;">
        <a style="text-decoration: none; color: #ffffff; font-size: 16px;" href="/front/home">Go to front desk</a>
      </div>
    </div>
  </div>
</template>
<style>
  .wrapper {
    background-image: url("../assets/5c8867aa313c1.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    height: 100vh;
    overflow: hidden;
  }
  
</style>

