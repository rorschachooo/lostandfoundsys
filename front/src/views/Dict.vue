<script setup>
import {nextTick, reactive, ref} from "vue";
import request from "@/utils/request";
import {ElMessage} from "element-plus";
import config from "../../config";
import {useUserStore} from "@/stores/user";

const name = ref('')
const pageNum = ref(1)
const pageSize = ref(10)
const total = ref(0)

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
  request.post('/dict/del/batch', idArr).then(res => {
    if (res.code === '200') {
      ElMessage.success('Operation successful')
      load()  // Refresh table data
    } else {
      ElMessage.error(res.msg)
    }
  })
}

const load = () => {
  // Use pagination API instead of getting all data
  request.get('/dict/page', {
    params: {
      pageNum: pageNum.value,
      pageSize: pageSize.value,
      name: name.value
    }
  }).then(res => {
    // Use paginated data returned
    state.tableData = res.data.records;
    // Set total data count
    total.value = res.data.total;
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
  load()
}

const dialogFormVisible = ref(false)

const rules = reactive({
  name: [
    { required: true, message: 'Please enter a name', trigger: 'blur' },
  ]
})
const ruleFormRef = ref()

// Added
const handleAdd = () => {
  dialogFormVisible.value = true
  nextTick(() => {
    ruleFormRef.value.resetFields()
    state.form = {}
  })
}

// save
const save = () => {
  ruleFormRef.value.validate(valid => {   // valid is the result of the verification
    if (valid) {
      request.request({
        url: '/dict',
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
  request.delete('/dict/' + id).then(res => {
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
  window.open(`http://${config.serverUrl}/dict/export`)
}

const userStore = useUserStore()
const token = userStore.getBearerToken
const auths =  userStore.getAuths

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
      <el-button type="success" @click="handleAdd" v-if="auths.includes('dict.add')">
        <el-icon style="vertical-align: middle">
          <Plus />
        </el-icon>  <span style="vertical-align: middle"> Add </span>
      </el-button>
      <el-upload
          v-if="auths.includes('dict.import')"
          class="ml5"
          :show-file-list="false"
          style="display: inline-block; position: relative; top: 3px"
          :action='`http://${config.serverUrl}/dict/import`'
          :on-success="handleImportSuccess"
          :headers="{ Authorization: token}"
      >
        <el-button type="primary">
          <el-icon style="vertical-align: middle">
            <Bottom />
          </el-icon>  <span style="vertical-align: middle"> Import </span>
        </el-button>
      </el-upload>
      <el-button type="primary" @click="exportData" class="ml5" v-if="auths.includes('dict.export')">
        <el-icon style="vertical-align: middle">
          <Top />
        </el-icon>  <span style="vertical-align: middle"> Export </span>
      </el-button>
      <el-popconfirm title="are you sure you want to delete?" @confirm="confirmDelBatch" v-if="auths.includes('dict.deleteBatch')">
        <template #reference>
          <el-button type="danger" style="margin-left: 5px">
            <el-icon style="vertical-align: middle">
              <Remove />
            </el-icon>  <span style="vertical-align: middle"> Batch Deletion </span>
          </el-button>
        </template>
      </el-popconfirm>
    </div>

    <div>
      <el-table 
        :data="state.tableData" 
        stripe 
        border 
        @selection-change="handleSelectionChange" 
        :header-cell-class-name="'headerBg'"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="number" width="80"></el-table-column>
        <el-table-column prop="code" label="coding" min-width="120"></el-table-column>
        <el-table-column prop="value" label="content" min-width="120">
          <template #default="scope">
            <el-icon>
              <component :is="scope.row.value" />
            </el-icon>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="type" min-width="120"></el-table-column>

        <el-table-column label="operate" width="180">
          <template #default="scope">
            <el-button type="primary" @click="handleEdit(scope.row)" v-if="auths.includes('dict.edit')">edit</el-button>
            <el-popconfirm title="are you sure you want to delete?" @confirm="del(scope.row.id)" v-if="auths.includes('dict.delete')">
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
          :page-sizes="[2, 5, 10, 20]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
      />
    </div>

    <el-dialog v-model="dialogFormVisible" title="information" width="40%">
      <el-form ref="ruleFormRef" :rules="rules" :model="state.form" label-width="80px" style="padding: 0 20px" status-icon>
        <el-form-item prop="code" label="coding" >
          <el-input v-model="state.form.code" autocomplete="off" />
        </el-form-item>
        <el-form-item prop="value" label="content" >
          <el-input v-model="state.form.value" autocomplete="off" />
        </el-form-item>
        <el-form-item prop="type" label="type" >
          <el-select v-model="state.form.type" style="width: 100%">
            <el-option v-for="item in ['icon']" :key="item" :label="item" :value="item"></el-option>
          </el-select>
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
