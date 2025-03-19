<script setup>
  import router from "@/router";
  import request from "@/utils/request";
  import {ElMessage} from "element-plus";
  import {onMounted, reactive, ref} from "vue";
  import {useUserStore} from "@/stores/user";
  import '@wangeditor/editor/dist/css/style.css' // Import CSS
  import { Editor, Toolbar } from '@wangeditor/editor-for-vue'

  const userStore = useUserStore()
  const user = userStore.getUser

  
  const id = router.currentRoute.value.query.id // Parameter id
  const state = reactive({
    data: {},
  })

  const load = () => {
    request.get('/front/lost/' + id).then(res => {
      state.data = res.data
    })

  }
  onMounted(() => {
    load()
  })

  //Slideshow
  request.get('/front/banner/list').then(res => {
    state.rotationList = res.data
    state.rotationList = state.rotationList.filter((item) => item.indexRadio === 'NO');
  })


  state.activeTab = 'content'


  state.userOptions = []
  request.get('/front/user/list').then(res => state.userOptions = res.data)
  state.categoryOptions = []
  request.get('/front/category/list').then(res => state.categoryOptions = res.data)


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


    <div class="mc detail-container">
        <div style="padding-bottom: 15px ;text-align: left;">
          <span style="font-size: 14px;margin-right: 20px;">Current location: Home> {{ state.data.name }}</span>
        </div>

        <div class="detail-content">
          <div class="detail-left">
            <img :src="state.data.img" style="height: 420px;width: 100%;"/>
          </div>
          <div class="detail-right">
            <div class="big-name"> {{ state.data.name }}</div>
            <div class="detail-info-list">
              <div>
                <span>Contact Details：</span><span style="color: red;font-size: 20px;">{{ state.data.phone }}</span>
              </div>
              <div>
                <span>Publisher：</span>{{ state.userOptions.find(v => v.id === state.data.userId) ? state.userOptions.find(v => v.id === state.data.userId).name : '' }}
              </div>
              <div>
                <span>Lost time：</span>{{ state.data.time }}
              </div>
              <div>
                <span>Lost location：</span>{{ state.data.address }}
              </div>
              <div>
                <span>Item Classification：</span>{{ state.categoryOptions.find(v => v.id === state.data.categoryId) ? state.categoryOptions.find(v => v.id === state.data.categoryId).name : '' }}
              </div>
            </div>
          </div>
        </div>


        <el-tabs v-model="state.activeTab" style="margin-top: 20px;min-height: 500px;">
          <el-tab-pane label="Reporting Lost Items" name="content">
            <span class="markdown-body" v-html="state.data.content"></span>
          </el-tab-pane>
        </el-tabs>

    </div>

  </div>
</template>

<style scoped>
  .detail-container {
    padding: 20px 0;
    width:85%;margin: 0 auto;margin-bottom: 50px;
  }

  .big-name {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
    font-size: 28px;
    font-weight: 700;
    line-height: 40px;
    color: #101d37;
  }


  .detail-content {
    display: flex;
  }

  .detail-left {
    width: 48%;
    margin-right: 2%;

  }

  .detail-right {
    width: 50%;
    border: 1px solid #e4e6f0;
    padding: 17px 30px 0;
    background-color: #eeeeee;
    box-sizing: border-box;
    height: 420px;
  }

  .detail-tag div {
    background-color: rgba(132, 154, 174, .1);
    border-radius: 2px;
    display: inline-block;
    padding: 2px 10px;
    height: 23px;
    line-height: 23px;
    text-align: center;
    font-size: 12px;
    color: #849aae;
    margin-right: 5px;
    margin-bottom: 5px;
  }

  .detail-info-list {
    padding: 10px 0;
    border-bottom: 1px solid #e4e6f0;
  }

  .detail-info-list div {
    margin-bottom: 5px;
    font-size: 14px;
  }

  .detail-info-list div span {
    color: #9399a5;

  }

  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
  }

  .detail-btn {
    display: flex;

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


  /* el-tabs */
  ::v-deep .el-tabs__nav {
    margin: 0 20px;
    /* Using rpx has no effect */
  }
  ::v-deep .el-tabs--top .el-tabs__item.is-top:nth-child(2) {
    padding-left: 20px;
  }
  ::v-deep .el-tabs--top .el-tabs__item.is-top:last-child {
    padding-right: 20px;
  }
  /*Floating Style*/
  ::v-deep .el-tabs__item:hover {
    color: #e1251b;
  }
  /*Selected Style*/
  ::v-deep .el-tabs__item.is-active {
    color: #fff;
    font-weight: bold;
    background-color: #FF9900;
  }
  /*Hide the horizontal line under the tab*/
  ::v-deep .el-tabs__active-bar {
    display: none;
  }

</style>