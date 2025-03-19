<script setup>
import { nextTick, reactive, ref } from "vue";
import request from "@/utils/request";
import {ElMessage} from "element-plus";
import config from "../../config";
import {useUserStore} from "@/stores/user";


const name = ref('')
const pageNum = ref(1)
const pageSize = ref(5)
const total = ref(0)

const userStore = useUserStore()
const token = userStore.getBearerToken
const auths =  userStore.getAuths
const user = userStore.getUser

const state = reactive({
  tableData: [],
  form: {}
})

const valueHtml = ref('')  // Rich text content

state.userOptions = []
request.get('/user').then(res => state.userOptions = res.data)
state.bizUserOptions = []
request.get('/bizUser').then(res => state.bizUserOptions = res.data)


const multipleSelection = ref([])

// Batch Deletion
const handleSelectionChange = (val) => {
  multipleSelection.value = val
}

const confirmDelBatch = () => {
  if (!multipleSelection.value || !multipleSelection.value.length) {
    ElMessage.warning("Please select data")
    return
  }
  const idArr = multipleSelection.value.map(v => v.id)
  request.post('/cart/del/batch', idArr).then(res => {
    if (res.code === '200') {
      ElMessage.success('Operation successful')
      load()  // Refresh table data
    } else {
      ElMessage.error(res.msg)
    }
  })
}

const load = () => {
  request.get('/cart/page', {
    params: {
      name: name.value,
      pageNum: pageNum.value,
      pageSize: pageSize.value
    }
  }).then(res => {
    state.tableData = res.data.records
    total.value = res.data.total
  })
}
load()  // Call the load method to get the background data

const reset = () => {
  name.value = ''
  load()
}

const dialogFormVisible = ref(false)

const rules = reactive({
  name: [
    { required: true, message: 'Please enter a name', trigger: 'blur' },
  ]
})
const ruleFormRef = ref()

// add
const handleAdd = () => {
  dialogFormVisible.value = true
  nextTick(() => {
    ruleFormRef.value.resetFields()
    state.form = {}
    valueHtml.value = ''  // Rich Text
  })
}

// save
const save = () => {
  ruleFormRef.value.validate(valid => {   // valid is the result of the verification
    if (valid) {
      state.form.content = valueHtml.value  // Rich text storage content
      request.request({
        url: '/cart',
        method: state.form.id ? 'put' : 'post',
        data: state.form
      }).then(res => {
        if (res.code === '200') {
          ElMessage.success('Saved successfully')
          dialogFormVisible.value = false
          load()  // Refresh table data
        } else {
          ElMessage.error(res.msg)
        }
      })
    }
  })
}

// edit
const handleEdit = (raw) => {
  dialogFormVisible.value = true
  nextTick(() => {
    ruleFormRef.value.resetFields()
    state.form = JSON.parse(JSON.stringify(raw))
    valueHtml.value = raw.content  // Rich Text
  })
}

// delete
const del = (id) => {
  request.delete('/cart/' + id).then(res => {
    if (res.code === '200') {
      ElMessage.success('Operation successful')
      load()  // Refresh table data
    } else {
      ElMessage.error(res.msg)
    }
  })
}

// Export interface
const exportData = () => {
  window.open(`http://${config.serverUrl}/cart/export`)
}


const handleImportSuccess = () => {
  // Refresh table
  load()
  ElMessage.success("Import Success")
}

const handleFileUploadSuccess = (res) => {
  state.form.file = res.data
  ElMessage.success('Upload Successfully')
}
const handleImgUploadSuccess = (res) => {
  state.form.img = res.data
  ElMessage.success('Upload Successfully')
}
</script>

<template>
  <div>
    <div>
      <el-input v-model="name" placeholder="Please enter a name" class="w300" />
      <el-button type="primary" class="ml5" @click="load">
        <el-icon style="vertical-align: middle">
          <Search />
        </el-icon>  <span style="vertical-align: middle"> Query </span>
      </el-button>
      <el-button type="warning" class="ml5" @click="reset">
        <el-icon style="vertical-align: middle">
          <RefreshLeft />
        </el-icon>  <span style="vertical-align: middle"> Clear </span>
      </el-button>

    </div>

    <div style="margin: 10px 0">
      <el-button type="success" @click="handleAdd" v-if="auths.includes('cart.add')">
        <el-icon style="vertical-align: middle">
          <Plus />
        </el-icon>  <span style="vertical-align: middle"> Add </span>
      </el-button>
      <el-upload
          v-if="auths.includes('cart.import')"
          class="ml5"
          :show-file-list="false"
          style="display: inline-block; position: relative; top: 3px"
          :action='`http://${config.serverUrl}/cart/import`'
          :on-success="handleImportSuccess"
          :headers="{ Authorization: token}"
      >
        <el-button type="primary">
          <el-icon style="vertical-align: middle">
            <Bottom />
          </el-icon>  <span style="vertical-align: middle"> Import </span>
        </el-button>
      </el-upload>
      <el-button type="primary" @click="exportData" class="ml5" v-if="auths.includes('cart.export')">
        <el-icon style="vertical-align: middle">
          <Top />
        </el-icon>  <span style="vertical-align: middle"> Export </span>
      </el-button>
      <el-popconfirm title="Are you sure you want to delete?" @confirm="confirmDelBatch" v-if="auths.includes('cart.deleteBatch')">
        <template #reference>
          <el-button type="danger" style="margin-left: 5px">
            <el-icon style="vertical-align: middle">
              <Remove />
            </el-icon>  <span style="vertical-align: middle"> Batch Deletion </span>
          </el-button>
        </template>
      </el-popconfirm>
    </div>

    <div style="margin: 10px 0">
      <el-table :data="state.tableData" stripe border  @selection-change="handleSelectionChange" :header-cell-class-name="'headerBg'">
        <el-table-column type="selection" width="55" />
      <el-table-column prop="id" label="Claim Number"></el-table-column>
      <el-table-column label="Claim User"><template #default="scope"><span v-if="scope.row.user_id">{{ state.userOptions.find(v => v.id === scope.row.user_id) ? state.userOptions.find(v => v.id === scope.row.user_id).name : '' }}</span></template></el-table-column>
      <el-table-column prop="name" label="Claiming items"></el-table-column>
      <el-table-column label="Item Image"><template #default="scope"><el-image preview-teleported style="width: 80px; height: 80px" :src="scope.row.img" :preview-src-list="[scope.row.img]"></el-image></template></el-table-column>
      <el-table-column label="Pickup Person"><template #default="scope"><span v-if="scope.row.biz_user_id">{{ state.biz_userOptions.find(v => v.id === scope.row.biz_user_id) ? state.biz_userOptions.find(v => v.id === scope.row.biz_user_id).name : '' }}</span></template></el-table-column>
      <el-table-column prop="goodid" label="Item Number"></el-table-column>

        <el-table-column label="operate" width="220">
          <template #default="scope">
            <el-button type="primary" @click="handleEdit(scope.row)" v-if="auths.includes('cart.edit')">Revise<el-icon style="vertical-align: middle"><Edit /></el-icon></el-button>
            <el-popconfirm title="Are you sure you want to delete?" @confirm="del(scope.row.id)" v-if="auths.includes('cart.delete')">
              <template #reference>
                <el-button type="danger">delete<el-icon style="vertical-align: middle"><Remove /></el-icon></el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="page">
      <el-pagination
          prev-text="Previous"
          next-text="Next"
          @current-change="load"
          @size-change="load"
          v-model:current-page="pageNum"
          v-model:page-size="pageSize"
          background
          :page-sizes="[4, 8, 12, 16]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
      />
    </div>

    <el-dialog v-model="dialogFormVisible" title="Information to be claimed" width="40%">
      <el-form ref="ruleFormRef" :rules="rules" :model="state.form" label-width="80px" style="padding: 0 20px" status-icon>
        <el-form-item prop="name" label="Claiming items">
          <el-input v-model="state.form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item prop="img" label="Item Image">
          <el-upload :show-file-list="false" :action="`http://${config.serverUrl}/file/upload`" ref="file" :headers="{ Authorization: token}" :on-success="handleImgUploadSuccess">
            <el-button size="small" type="primary">Click Upload</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item prop="goodid" label="Item Number">
          <el-input v-model="state.form.goodid" autocomplete="off"></el-input>
        </el-form-item>

      </el-form>
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="save">
          save
        </el-button>
      </span>
      </template>
    </el-dialog>


  </div>
</template>
<style>
.page {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 13px;
  color: #656565;
  margin-top: 20px;
  padding-bottom: 20px;
}

.page > div.homePage, .page > div.lastPage {
  height: 34px;
  line-height: 34px;
  width: 60px;
  text-align: center;
  border: 1px solid #EAEAEA;
  box-sizing: border-box;
  cursor: pointer;
}

.page > div.homePage {
  border-radius: 2px 0 0 2px;
}

.page > div.lastPage {
  border-radius: 0 2px 2px 0;
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

.map_search_result {
  position: absolute;
  top: calc(100% - 40vh);
  right: 20px;
  z-index: 9999;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
}

.map_search_result ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.map_search_result li {
  padding: 10px;
  cursor: pointer;
}

.map_search_result li:hover {
  background-color: #f5f5f5;
}
</style>