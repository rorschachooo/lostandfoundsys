<script setup>
import {nextTick, reactive, ref} from "vue";
import request from "@/utils/request";
import {ElMessage} from "element-plus";
import config from "../../config";
import {useUserStore} from "@/stores/user";

const name = ref('')
const address = ref('')
const pageNum = ref(1)
const pageSize = ref(10)
const total = ref(0)
const roles = ref([])

const state = reactive({
  tableData: [],
  form: {}
})
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
  request.post('/user/del/batch', idArr).then(res => {
    if (res.code === '200') {
      ElMessage.success('Operation successful')
      load()  // Refresh table data
    } else {
      ElMessage.error(res.msg)
    }
  })
}

const load = () => {
  request.get('/user/page', {
    params: {
      name: name.value,
      address: address.value,
      pageNum: pageNum.value,
      pageSize: pageSize.value
    }
  }).then(res => {
    state.tableData = res.data.records
    total.value = res.data.total
  })

  request.get('/role?all=true').then(res => {
    roles.value = res.data
  })
}

// Handle page number change
const handleCurrentChange = (val) => {
  pageNum.value = val
  load()
}

// Handle page size change
const handleSizeChange = (val) => {
  pageSize.value = val
  pageNum.value = 1 // Reset to first page
  load()
}

load()  // Call the load method to get the background data

const reset = () => {
  name.value = ''
  address.value = ''
  load()
}

const dialogFormVisible = ref(false)

const rules = reactive({
  username: [
    { required: true, message: 'Please enter your username', trigger: 'blur' },
    { min: 3, max: 20, message: 'Length between 3-20', trigger: 'blur' },
  ],
  name: [
    { required: true, message: 'Please enter a Name', trigger: 'blur' },
  ],
  email: [
    { required: true, message: 'Please enter your email address', trigger: 'blur' },
  ],
  address: [
    { required: true, message: 'Please enter your address', trigger: 'blur' },
  ],
  role: [
    { required: true, message: 'Please select a role', trigger: 'blur' },
  ]
})
const ruleFormRef = ref()

// Added
const handleAdd = () => {
  dialogFormVisible.value = true
  ruleFormRef.value.resetFields()
  state.form = {}
}

// save
const save = () => {
  ruleFormRef.value.validate(valid => {   // valid is the result of the verification
    if (valid) {
      request.request({
        url: '/user',
        method: state.form.id ? 'put' : 'post',
        data: state.form
      }).then(res => {
        if (res.code === '200') {
          ElMessage.success('save successfully')
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
  })
}

// delete
const del = (id) => {
  request.delete('/user/' + id).then(res => {
    if (res.code === '200') {
      ElMessage.success('Operation successful')
      load()  // Refresh table data
    } else {
      ElMessage.error(res.msg)
    }
  })
}

// Export Interface
const exportData = () => {
  window.open(`http://${config.serverUrl}/user/export`)
}

const userStore = useUserStore()
const token = userStore.getBearerToken
const auths = userStore.getAuths

const handleImportSuccess = () => {
  // Refresh table
  load()
  ElMessage.success("Import Success")
}



</script>

<template>
  <div>
    <div>
      <el-input v-model="name" placeholder="Please enter a name" class="w300" />
      <el-input v-model="address" placeholder="Please enter your address" class="w300 ml5" />
      <el-button type="primary" class="ml5" @click="load">
        <el-icon style="vertical-align: middle">
          <Search />
        </el-icon>  <span style="vertical-align: middle"> search </span>
      </el-button>
      <el-button type="warning" class="ml5" @click="reset">
        <el-icon style="vertical-align: middle">
          <RefreshLeft />
        </el-icon>  <span style="vertical-align: middle"> Reset </span>
      </el-button>

    </div>

    <div style="margin: 10px 0">
      <el-button type="success" @click="handleAdd" v-if="auths.includes('user.add')">
        <el-icon style="vertical-align: middle">
          <Plus />
        </el-icon>  <span style="vertical-align: middle"> Add </span>
      </el-button>
      <el-upload
          v-if="auths.includes('user.import')"
          class="ml5"
          :show-file-list="false"
          style="display: inline-block; position: relative; top: 3px"
          :action='`http://${config.serverUrl}/user/import`'
          :on-success="handleImportSuccess"
          :headers="{ Authorization: token}"
      >
        <el-button type="primary">
          <el-icon style="vertical-align: middle">
            <Bottom />
          </el-icon>  <span style="vertical-align: middle"> Import </span>
        </el-button>
      </el-upload>
      <el-button type="primary" @click="exportData" class="ml5"  v-if="auths.includes('user.export')">
        <el-icon style="vertical-align: middle">
          <Top />
        </el-icon>  <span style="vertical-align: middle"> Export </span>
      </el-button>
      <el-popconfirm title="are you sure you want to delete?" @confirm="confirmDelBatch" v-if="auths.includes('user.deleteBatch')">
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
      <el-table :data="state.tableData" stripe border  @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" v-if="auths.includes('user.deleteBatch')" />
        <el-table-column prop="username" label="username"></el-table-column>
        <el-table-column prop="name" label="name"></el-table-column>
        <el-table-column prop="address" label="address"></el-table-column>
        <el-table-column prop="email" label="Mail"></el-table-column>
        <el-table-column prop="role" label="Role">
          <template #default="scope">
            <span v-if="roles.length">{{ roles.find(r => r.flag === scope.row.role) ? roles.find(r => r.flag === scope.row.role).name : '' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="operate" width="180">
          <template #default="scope">
            <el-button type="primary" @click="handleEdit(scope.row)"  v-if="auths.includes('user.edit')">edit</el-button>
            <el-popconfirm title="are you sure you want to delete?" @confirm="del(scope.row.id)"  v-if="auths.includes('user.delete')">
              <template #reference>
                <el-button type="danger">delete</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div style="margin: 10px 0">
      <el-pagination
          @current-change="handleCurrentChange"
          @size-change="handleSizeChange"
          v-model:current-page="pageNum"
          v-model:page-size="pageSize"
          background
          :page-sizes="[5, 10, 15, 20]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
      />
    </div>

    <el-dialog v-model="dialogFormVisible" title="User information" width="40%">
      <el-form ref="ruleFormRef" :rules="rules" :model="state.form" label-width="90px" style="padding: 0 20px" status-icon>
        <el-form-item prop="username" label="username" >
          <el-input v-model="state.form.username" autocomplete="off" />
        </el-form-item>
        <el-form-item prop="name" label="Name">
          <el-input v-model="state.form.name" autocomplete="off" />
        </el-form-item>
        <el-form-item prop="role" label="Role" >
          <el-select v-model="state.form.role" style="width: 100%">
            <el-option v-for="item in roles" :label="item.name" :value="item.flag" :key="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="email" label="Mail">
          <el-input v-model="state.form.email" autocomplete="off" />
        </el-form-item>
        <el-form-item prop="address" label="address">
          <el-input type="textarea" v-model="state.form.address" autocomplete="off" />
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
