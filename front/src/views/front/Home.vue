<script setup>
import {reactive, ref} from "vue";
import request from "@/utils/request";
import router from "@/router"


const name = ref('')
const state = reactive({
    noticeList:[],
        rotationList:[],
})


state.userOptions = []
request.get('/user').then(res => state.userOptions = res.data)

const pageNum = ref(1)
const pageSize = ref(5)
const total = ref(0)
const load = () => {

  //Request the previous 10 announcements
  request.get('/notice/findTop10').then(res => {
    state.noticeList = res.data
  })
}
load()  // Call the load method to get the background data

//Slideshow
request.get('/front/banner/list').then(res => {
  state.rotationList = res.data
  state.rotationList = state.rotationList.filter((item) => item.indexRadio === 'YES');
})

//Load home page data list
request.get('/front/recruit/page', {
  params: {
    pageNum: 1,
    pageSize: 8,
  }
}).then(res => {
  state.recruitData = res.data.records
})
request.get('/front/lost/page', {
  params: {
    pageNum: 1,
    pageSize: 8,
  }
}).then(res => {
  state.lostData = res.data.records
})
const truncatedContent = (content) => {
  const maxLength = 100;
  if (content.length > maxLength) {
    return content.substring(0, maxLength) + '...';
  }
  return content;
}

</script>

<template>
  <div>
    <!-- Slideshow -->
    <div>
      <div style="width: 100%">
        <el-carousel :interval="5000" arrow="always" height="250px">
          <el-carousel-item v-for="item in state.rotationList" :key="item" v-show="item.indexRadio=='YES'">
            <a :href="item.url" target="_blank"><img :src="item.img" alt="" style="width: 100%; height: 100%"></a>
          </el-carousel-item>
        </el-carousel>
      </div>
    </div>



      <div style="width:85%;margin: 0 auto;margin-bottom: 50px;">
        <div style="padding-bottom: 15px ;border-bottom: 3px solid #FF9900; margin-top: 20px;text-align: left;">
          <span style="font-weight: bold; font-size: 24px;color:#FF9900;">Lost and found information</span>
        </div>
        <div style="margin-top: 20px;">
          <el-row :gutter="10">
            <el-col :span="6" v-for="item in state.recruitData" :key="item.id" style="margin-top: 20px;">
                <div ><img @click="router.push('/front/recruit-detail?id=' + item.id)" :src="item.img" alt="" style="width: 90%; height: 220px;cursor: pointer;"></div>
                <div><span style="font-weight: bold">{{ item.name}}</span></div>
                <div style="width: 90%;margin-top: 20px;">
                  <el-button type="primary" size="small" @click="router.push('/front/recruit-detail?id=' + item.id)" style="float: left;">check the details</el-button>
                  <span style="color:red;font-size: 18px;font-weight: bold;float: right;" v-if="item.price">￥{{item.price}}</span>
                </div>
            </el-col>
          </el-row>
        </div>
    </div>


      <div style="width:85%;margin: 0 auto;margin-bottom: 50px;">
        <div style="padding-bottom: 15px ;border-bottom: 3px solid #FF9900; margin-top: 20px;text-align: left;">
          <span style="font-weight: bold; font-size: 24px;color:#FF9900;">Lost property information</span>
        </div>
        <div style="margin-top: 20px;">
          <el-row :gutter="10">
            <el-col :span="6" v-for="item in state.lostData" :key="item.id" style="margin-top: 20px;">
                <div ><img @click="router.push('/front/lost-detail?id=' + item.id)" :src="item.img" alt="" style="width: 90%; height: 220px;cursor: pointer;"></div>
                <div><span style="font-weight: bold">{{ item.name}}</span></div>
                <div style="width: 90%;margin-top: 20px;">
                  <el-button type="primary" size="small" @click="router.push('/front/lost-detail?id=' + item.id)" style="float: left;">check the details</el-button>
                  <span style="color:red;font-size: 18px;font-weight: bold;float: right;" v-if="item.price">￥{{item.price}}</span>
                </div>
            </el-col>
          </el-row>
        </div>
    </div>


  </div>
</template>

<style scoped>
.refresh:hover {
  cursor: pointer;
}
:deep(.el-card__body) {
  padding: 10px !important;
}


/* Heading Style */
.title {
  font-size: 18px;
  font-weight: bold;
  color: #333;  /* Title default color */
  text-decoration: none;  /* Remove underline */
  /* Hover effects */
  transition: color 0.3s ease;
}

.title:hover {
  color: orangered !important;  /* Mouseover color */
}


.item {
  padding: 20px 0;
  display: flex;
  border-radius: 10px;
}

.item img {
  width: 160px;
  height: 120px;
}

.right-container {
  position: relative;
  margin-left: 20px;
  width: 100%;

}

.right-container div {
  margin-bottom: 7px;
}

.top {
  display: flex;
  color: #101d37;
  font-size: 20px;
  font-weight: bold;
}

.time {
  position: absolute;
  left: 0;
  bottom: 0;
  margin-bottom: 0 !important;
  color: rgba(16, 29, 55, .3);
  font-size: 14px;
}
</style>
