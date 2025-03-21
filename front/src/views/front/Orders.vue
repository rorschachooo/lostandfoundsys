﻿<script setup>
  import router from "@/router";
  import request from "@/utils/request";
  import {ElMessage} from "element-plus";
  import {onMounted, reactive, ref, nextTick} from "vue";
  import {useUserStore} from "@/stores/user";
  import '@wangeditor/editor/dist/css/style.css' // Import CSS
  import { Editor, Toolbar } from '@wangeditor/editor-for-vue'

  const userStore = useUserStore()
  const user = userStore.getUser
  const pageNum = ref(1)
  const pageSize = ref(5)
  const total = ref(0)

    //Determine whether the user is logged in
  if(user.id==null){
      router.push('/login')
  }

  const content = ref('')
  const viewShow = ref(false)
  const view = (value) => {
    viewShow.value = true
    content.value = value
  }

  const state = reactive({
    tableData:[],
    form:{},
  })

  const load = () => {
    request.get('/front/orders/list').then(res => {
      state.tableData = res.data
      state.tableData = state.tableData.filter((item) => item.userId === user.id);
    })
  }
  load()  // Call the load method to get the background data

  //Slideshow
  request.get('/front/banner/list').then(res => {
      state.rotationList = res.data
      state.rotationList = state.rotationList.filter((item) => item.indexRadio === 'NO');
  })

  //delete order
  const deleteOrders =(id) =>{
      request.delete('/front/orders/' + id).then(res => {
          if (res.code === '200') {
              ElMessage.success('Operation successful')
              load()  // Refresh table data
          } else {
              ElMessage.error(res.msg)
          }
      })
  }

  //Cancel order
  const cancelOrders =(id) =>{
      request.put('/front/orders/cancel/' + id).then(res => {
          if (res.code === '200') {
              ElMessage.success('Operation successful')
              load()  // Refresh table data
          } else {
              ElMessage.error(res.msg)
          }
      })
  }

  state.userOptions = []
  request.get('/front/user/list').then(res => state.userOptions = res.data)

</script>

<template>
  <div>

          <!-- Slideshow -->
          <div>
                  <div style="width: 100%">
                      <el-carousel :interval="5000" arrow="always" height="200px">
                          <el-carousel-item v-for="item in state.rotationList" :key="item">
                              <a :href="item.url" target="_blank"><img :src="item.img" alt="" style="width: 100%; height: 100%"></a>
                          </el-carousel-item>
                      </el-carousel>
                  </div>
          </div>


      <div style="width:85%;margin: 0 auto;margin-bottom: 50px;">
        <div style="padding-bottom: 15px ;margin-top: 20px;text-align: left;">
            <span style="font-size: 14px;margin-right: 20px;">Current location: Home> My lost and found record</span>
        </div>

          <div style="padding-bottom: 15px ;border-bottom: 3px solid #FF9900; text-align: left;display: flex;">
              <span style="font-weight: bold; font-size: 24px;float: left;flex: 3;color: #FF9900;">My lost and found record</span>
          </div>

          <el-table :data="state.tableData" style="width: 100%;margin-top: 20px;" stripe border :header-cell-class-name="'headerBg'">
                <el-table-column prop="id" label="Serial number">
                  <template #default="scope">
                    {{ scope.$index + 1 }}
                  </template>
                </el-table-column>
                <el-table-column prop="name" label="Claim Number"></el-table-column>
                <el-table-column label="Pickers" width="250px;">
                    <template #default="scope">
                        <span v-if="scope.row.bizUserId">{{ state.userOptions.find(v => v.id === scope.row.bizUserId) ? state.userOptions.find(v => v.id === scope.row.bizUserId).name : '' }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="Claim details"><template #default="scope"><el-button @click="view(scope.row.content)">Check</el-button></template></el-table-column>
                <el-table-column prop="createTime" label="Application period"></el-table-column>
                <el-table-column prop="stateRadio" label="Claim status"></el-table-column>
              <el-table-column label="operate" width="150px;">
                  <template #default="scope">
                      <a href="javascript:void(0)" @click="deleteOrders(scope.row.id)" class="delete-link" style="margin-right: 15px;" v-if="scope.row.stateRadio=='Applying'">delete</a>
                      <a href="javascript:void(0)" @click="cancelOrders(scope.row.id)" class="delete-link" v-if="scope.row.stateRadio=='Applying'">Cancel</a>
                  </template>
              </el-table-column>
        </el-table>

    </div>

      <el-dialog v-model="viewShow" title="Preview" width="40%">
          <div  id="editor-content-view" class="editor-content-view" v-html="content" style="padding: 0 20px"></div>
          <template #footer>
      <span class="dialog-footer">
        <el-button @click="viewShow = false">closure</el-button>
      </span>
          </template>
      </el-dialog>

  </div>
</template>

<style>

.total-container {
  margin-top: 20px;
  text-align: right;
}

.total-label {
  font-weight: bold;
}

.total-price {
  color: red;
  font-weight: bold;
}

a.delete-link {
    color: #ff0000;
    text-decoration: none;
}

a.delete-link:hover {
    text-decoration: underline;
}

.el-dialog {
    background-color: #fff; /* Set the background color of the dialog box */
    border: 1px solid #ccc; /* Set the border color of the dialog box */
    border-radius: 4px; /* Set the border radius of the dialog box */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15); /* Set the shadow effect of the dialog box */
    padding: 20px; /* Set the dialog box padding */
    box-sizing: border-box; /* Prevent padding and borders from extending beyond the container */
}

.el-dialog__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background-color: #FF9900;
    border-bottom: 1px solid #ccc;
}

.el-dialog__header > * {
    margin-right: 10px;
    color: #ffffff;
}

.el-dialog__title {
    font-size: 18px;
    font-weight: bold;
}

.el-dialog__body {
    padding: 20px;
}

.el-dialog__footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    border-top: 1px solid #ccc;
}

.el-dialog__footer > * {
    margin-left: 10px;
}

.headerBg {
    background: #FF9900!important;
    color: #ffffff!important;
}
</style>