<script setup>
import { reactive, ref} from "vue"
import { User, Lock, Message } from '@element-plus/icons-vue'
import request from "@/utils/request";
import {ElMessage} from "element-plus";
import router from "@/router";
import config from "../../config";

  const loginData = reactive({})
  const rules = reactive({
    username: [
      { required: true, message: 'Please enter your login account', trigger: 'blur' },
    ],
    email: [
      { required: true, message: 'Please enter your email address', trigger: 'blur' },
    ],
    password: [
      { required: true, message: 'Please enter your password', trigger: 'blur' },
      { min: 3, max: 20, message: 'The password length is between 3 and 20 characters.', trigger: 'blur' },
    ],
    confirmPassword: [
      { required: true, message: 'Please confirm your password', trigger: 'blur' },
      { min: 3, max: 20, message: 'The password length is between 3 and 20 characters.', trigger: 'blur' },
    ],
  })
  const ruleFormRef = ref()
  const register = () => {
    ruleFormRef.value.validate(valid => {
      if (valid) {
        if (loginData.password !== loginData.confirmPassword) {
          ElMessage.warning('The two passwords do not match')
        }
		loginData.role = 'MEMBER'
        // Send form data to the backend
        request.post('/register', loginData).then(res => {
          if (res.code === '200') {
            ElMessage.success('Successful registration')
            router.push('/login')
          } else {
            ElMessage.error(res.msg)
          }
        })
      }
    })
  }

</script>

<template>
  <div class="wrapper">
    <div style="margin: 150px auto; background-color: #FF9900; width: 400px; height: 460px; padding: 20px; border-radius: 10px">
      <div style="margin: 20px 0; text-align: center; font-size: 24px;color: #ffffff;"><b>{{config.projectName}}</b></div>
      <el-form
              ref="ruleFormRef"
              :model="loginData"
              :rules="rules"
              size="large"
              status-icon
      >
        <el-form-item prop="username">
          <el-input v-model="loginData.username" placeholder="Please enter your login account"  />
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="loginData.email" placeholder="Please enter your email address"  />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginData.password" show-password placeholder="Please enter your password" />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="loginData.confirmPassword" show-password placeholder="Please confirm your password"/>
        </el-form-item>
        <el-form-item style="margin: 10px 0; text-align: right">
          <el-button type="primary" autocomplete="off" @click="register">Register</el-button>
          <el-button type="info" autocomplete="off" @click="router.push('/login')">Log in</el-button>
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
