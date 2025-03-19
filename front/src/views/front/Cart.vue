<script setup>
  import router from "@/router";
  import request from "@/utils/request";
  import {ElMessage} from "element-plus";
  import {onMounted, reactive, ref} from "vue";
  import {useUserStore} from "@/stores/user";
  import '@wangeditor/editor/dist/css/style.css' // Import CSS
  import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
  import config from "../../../config";

  const userStore = useUserStore()
  const token = userStore.getBearerToken
  const auths =  userStore.getAuths
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

  const id = router.currentRoute.value.query.id
  let name = router.currentRoute.value.query.name
  const state = reactive({
    tableData:[],
  })

  const load = () => {
    request.get('/front/cart/list').then(res => {
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

  //Calculate the total shopping cart price
  const getTotalPrice =() =>{
      const totalPrice = state.tableData.reduce((sum, item) => {
          return sum + item.price*1;
      }, 0);
      return totalPrice.toFixed(2);
  }

  //Revise Shopping Cart
  const changeNum = (row) =>{
      request.request({
          url: '/front/cart/update',
          method: 'post',
          data: {
              id:row.id,
              name:row.name,
              userId:user.id,
              num:row.num,
          }
      }).then(res => {
          if (res.code === '200') {
              ElMessage.success('Revise successful')
          } else {
              ElMessage.error(res.msg)
          }
      })
  }

  //delete shopping cart
  const deleteCart =(id) =>{
      request.delete('/front/cart/' + id).then(res => {
          if (res.code === '200') {
              ElMessage.success('Operation successful')
              load()  // Refresh table data
          } else {
              ElMessage.error(res.msg)
          }
      })
  }

  //Batch Deletion Shopping Cart
  const deleteBatchCart =(ids) =>{
      ids.forEach((e)=>{
          request.delete('/front/cart/' + e).then(res => {})
      })
  }



  const validateForm = () =>{
      if(state.tableData.length==0){
          ElMessage.error('The shopping cart is empty! Please add first')
          return false;
      }
      if(state.form.name==null ||state.form.name==''){
          ElMessage.error('The name of the claimant is empty! Please fill it in first')
          return false;
      }
      if(state.form.phone==null ||state.form.phone==''){
          ElMessage.error('The claimant\' mobile phone number is empty! Please fill it in first')
          return false;
      }
      if(state.form.remark==null ||state.form.remark==''){
          ElMessage.error('The description of the lost item is empty! Please fill it in first')
          return false;
      }
      return true
  }

  state.form = {
      name:'',
      phone:'',
      remark:'',
  }
  state.orders = {}
  state.pList = ``
  //save order
  const saveOrder = () =>{
      const flag = validateForm()
      if(!flag)return;

      const groups = state.tableData.reduce((acc, cur) => {
          const bizUser = cur.bizUserId;
          if (!acc[bizUser]) {
              acc[bizUser] = [];
          }
          acc[bizUser].push(cur);
          return acc;
      }, {});
      const result = Object.values(groups);

      result.forEach((array)=>{
          state.pList = ``

          state.orders.name = generateOrderNumber()
          state.pList += `User lost property claim information:<br/>`;
          state.pList += `<ul>`
          state.pList += '<li>Claimant Name:'+state.form.name+'</li>'
          state.pList += '<li>Mobile phone number of claimant:'+state.form.phone+'</li>'
          state.pList += '<li>Description of lost items:'+state.form.remark+'</li>'
          state.pList += `</ul>`
          state.pList += `Lost items details:<br/>`;
          state.pList += `<ul>`
          const goodids = [];
          array.forEach((e,i)=>{
              goodids.push(e.goodid)
              state.pList += `<li>Item Name：${e.name}</li>`
          })
          state.orders.goodids = goodids.join(',');
          state.pList += `</ul>`
          state.orders.content = state.pList
          state.orders.stateRadio = 'Applying'
          state.orders.userId = user.id
          state.orders.amount = array.reduce((acc, item) => {
              return acc + (item.price * 1);
          }, 0).toFixed(2);

          state.orders.bizUserId = array[0].bizUserId

          request.request({
              url: '/front/orders/update',
              method: 'post',
              data: state.orders
          }).then(res => {
              if (res.code === '200') {

                  //Clear shopping cart data
                  const ids = state.tableData.map(obj => obj.id);
                  deleteBatchCart(ids)

                  router.push('/front/orders')
              } else {
                  ElMessage.error(res.msg)
              }
          })
      });

  }

  //Generate order number
  function generateOrderNumber() {
      const date = new Date();
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const seconds = String(date.getSeconds()).padStart(2, '0');
      const orderNumber = `${year}${month}${day}${hours}${minutes}${seconds}`;
      return orderNumber;
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
            <span style="font-size: 14px;margin-right: 20px;">Current location: Home > Claim lost property</span>
        </div>

        <div style="padding-bottom: 15px ;border-bottom: 3px solid #FF9900; text-align: left;display: flex;">
            <span style="font-weight: bold; font-size: 24px;float: left;flex: 3;color: #FF9900;">Claim lost property</span>
        </div>

          <el-table :data="state.tableData" style="width: 100%;margin-top: 20px;" stripe border :header-cell-class-name="'headerBg'">
            <el-table-column prop="id" label="Serial number" width="80px;">
                <template #default="scope">
                    {{ scope.$index + 1 }}
                </template>
                </el-table-column>
                <el-table-column label="Lost property pictures" width="120px;">
                    <template #default="scope" >
                        <img :src="scope.row.img" alt="Lost property pictures" style="width: 100px; height: 80px;">
                    </template>
                </el-table-column>
                <el-table-column prop="name" label="Lost property name" width="320px;"></el-table-column>
                <el-table-column label="Pickers" width="160px;">
                    <template #default="scope">
                        <span v-if="scope.row.bizUserId">{{ state.userOptions.find(v => v.id === scope.row.bizUserId) ? state.userOptions.find(v => v.id === scope.row.bizUserId).name : '' }}</span>
                    </template>
                </el-table-column>


                <el-table-column label="operate">
                    <template #default="scope">
                        <a href="javascript:void(0)" @click="deleteCart(scope.row.id)" class="delete-link">delete</a>
                    </template>
                </el-table-column>
        </el-table>


              <!-- Fill in the order information -->
              <div class="order-list" style="margin-top: 30px;">
                  <div style="padding-bottom: 15px ;border-bottom: 3px solid #FF9900; text-align: left;display: flex;">
                      <span style="font-weight: bold; font-size: 20px;float: left;flex: 3;color: #FF9900;">Fill in the application information</span>
                  </div>

                  <div style="margin-top: 20px;margin-left: 50px;">
                      <span>Claimant Name:</span>
                      <span><el-input v-model="state.form.name" placeholder="Please fill in the name of the claimant" style="width: 400px;"></el-input></span>
                  </div>
                  <div style="margin-top: 20px;margin-left: 50px;">
                      <span>Mobile phone number of claimant:</span>
                      <span><el-input v-model="state.form.phone" placeholder="Please fill in the claimant's mobile phone number" style="width: 400px;"></el-input></span>
                  </div>
                  <div style="margin-top: 20px;margin-left: 50px;">
                      <span>Description of lost items:</span>
                      <span><el-input v-model="state.form.remark" placeholder="Please fill in the description of the lost item" style="width: 400px;"></el-input></span>
                  </div>
              </div>




          <div class="detail-btn" style="display: flex; justify-content: center; align-items: center; height: 100%;margin-top: 30px;">
              <div @click="saveOrder"><i class="el-icon-date"></i>Confirm your claim</div>
          </div>
    </div>

      <!-- Payment Box -->
    <el-dialog v-model="dialogFormVisible" title="Order Payment" width="40%">
        <div style="text-align: center;">
            lump sum:<span style="font-size: 25px;color: red;">{{ getTotalPrice() }}</span><span style="margin-left: 20px;">Please scan the QR code below to pay</span>
        </div>
        <div style="margin-top: 10px;text-align: center;">
            <img :src="state.qrcode" alt="Payment QR Code" style="width: 200px;height: 220px;">
        </div>
        <div style="margin-top: 10px;text-align: center;">
            <el-button type="primary" @click="saveOrder">Confirm purchase</el-button>
        </div>
    </el-dialog>

  </div>
</template>

<style>

    .total-container {
        margin-top: 20px;
        text-align: right;
        margin-right: 20px;
    }

    .total-label {
        font-weight: bold;
    }

    .total-price {
        color: red;
        font-size: 25px;
        font-weight: bold;

    }

    a.delete-link {
        color: #ff0000;
        text-decoration: none;
    }

    a.delete-link:hover {
        text-decoration: underline;
    }


    .pay-list {
        width: 100%;
        margin: 0 auto;
        display: flow;
    }

    .detail-btn{
        width: 100%;
        margin: 0 auto;
        display: flow;
    }

    .detail-btn div {
        width: 160px;
        height: 50px;
        line-height: 14px;
        padding: 18px 0;
        font-size: 16px;
        box-sizing: border-box;
        background: #FF9900;
        color: #fff;
        text-align: center;
        margin-right: 15px;
        cursor: pointer;
        border-radius: 20px;
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