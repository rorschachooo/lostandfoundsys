<script setup>
import {nextTick, reactive, ref} from "vue";
import request from "@/utils/request";
import {ElMessage} from "element-plus";
import config from "../../config";
import {useUserStore} from "@/stores/user";

const pageNum = ref(1)
const pageSize = ref(10)
const total = ref(0)
const allData = ref([]) // 存储所有数据

const state = reactive({
  tableData: [], // 当前页显示的数据
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
  request.post('/permission/del/batch', idArr).then(res => {
    if (res.code === '200') {
      ElMessage.success('Operation successful')
      load()  // Refresh table data
    } else {
      ElMessage.error(res.msg)
    }
  })
}

const load = () => {
  request.get('/permission').then(res => {
    // Store all data
    allData.value = res.data;
    // Set total data count
    total.value = res.data.length;
    // Apply pagination in frontend
    updatePageData();
  })
}

// Apply pagination in frontend
const updatePageData = () => {
  const start = (pageNum.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  state.tableData = allData.value.slice(start, end);
}

// Handle page number change
const handleCurrentChange = (val) => {
  pageNum.value = val;
  updatePageData();
}

// Handle page size change
const handleSizeChange = (val) => {
  pageSize.value = val;
  pageNum.value = 1; // Reset to first page
  updatePageData();
}

load()  // Call the load method to get the background data

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
    state.form = { type: 1, orders: 1 }
  })
}

// save
const save = () => {
  ruleFormRef.value.validate(valid => {   // valid is the result of the verification
    if (valid) {
      request.request({
        url: '/permission',
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

const changeHide = (row) => {
  request.request({
    url: '/permission',
    method: 'put',
    data: row
  }).then(res => {
    if (res.code === '200') {
      ElMessage.success('Operation successful')
      load()  // Refresh table data
    } else {
      ElMessage.error(res.msg)
    }
  })
}

// Icon dictionary collection
const icons = ref([])
// Requested icon data set
request.get('/dict?all=true').then(res => {
  icons.value = res.data
})
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
  request.delete('/permission/' + id).then(res => {
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
  window.open(`http://${config.serverUrl}/permission/export`)
}

const userStore = useUserStore()
const token = userStore.getBearerToken
const auths =  userStore.getAuths

const handleImportSuccess = () => {
  // Refresh table
  load()
  ElMessage.success("Import Success")
}

const handleNodeClick = (data) => {
  if (data.id === state.form.id) {  // If the id of the current edit row is the same as the id of the selected parent node, it will not be selected.
    console.log(data)
    ElMessage.warning('A parent node cannot select itself')

    nextTick(() => {  // Wait until the DOM of the tree node is rendered before going to Revisepid
      // Reset pid
      state.form.p_id = null
      console.log(state.form)
    })
  }
}
</script>

<template>
  <div>
    <div style="margin: 10px 0">
      <el-button type="success" @click="handleAdd"  v-if="auths.includes('permission.add')">
        <el-icon style="vertical-align: middle">
          <Plus />
        </el-icon>  <span style="vertical-align: middle"> Add </span>
      </el-button>
<!--      <el-popconfirm title="are you sure you want to delete?" @confirm="confirmDelBatch" v-if="auths.includes('permission.deleteBatch')">-->
<!--        <template #reference>-->
<!--          <el-button type="danger" style="margin-left: 5px">-->
<!--            <el-icon style="vertical-align: middle">-->
<!--              <Remove />-->
<!--            </el-icon>  <span style="vertical-align: middle"> Batch Deletion </span>-->
<!--          </el-button>-->
<!--        </template>-->
<!--      </el-popconfirm>-->
    </div>

    <div>
      <el-table 
        :data="state.tableData" 
        stripe 
        border 
        row-key="id" 
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="number" width="80"></el-table-column>
        <el-table-column prop="name" label="name" min-width="120"></el-table-column>
        <el-table-column prop="path" label="Access path" min-width="120"></el-table-column>
        <el-table-column prop="page" label="Page Path" min-width="120"></el-table-column>
        <el-table-column prop="orders" label="order" width="80"></el-table-column>
        <el-table-column prop="icon" label="icon" width="80">
          <template #default="scope">
            <el-icon v-if="scope.row.icon">
              <component :is="scope.row.icon" />
            </el-icon>
          </template>
        </el-table-column>
        <el-table-column prop="auth" label="Permissions" min-width="120"></el-table-column>
        <el-table-column prop="p_id" label="Parent" width="80"></el-table-column>
        <el-table-column prop="type" label="type" min-width="120">
          <template #default="scope">
            <el-tag type="warning" v-if="scope.row.type === 1">Menu Contents</el-tag>
            <el-tag v-if="scope.row.type === 2">Menu Page</el-tag>
            <el-tag type="success" v-if="scope.row.type === 3">Page Button</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="hide" label="Is it hidden" width="100">
          <template #default="scope">
            <el-switch v-model="scope.row.hide" @change="changeHide(scope.row)"></el-switch>
          </template>
        </el-table-column>

        <el-table-column label="operate" width="180">
          <template #default="scope">
            <el-button type="primary" @click="handleEdit(scope.row)" v-if="auths.includes('permission.edit')">edit</el-button>
            <el-popconfirm title="are you sure you want to delete?" @confirm="del(scope.row.id)" v-if="auths.includes('permission.delete')">
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
          :page-sizes="[5, 10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
      />
    </div>

    <el-dialog v-model="dialogFormVisible" title="information" width="40%">
      <el-form ref="ruleFormRef" :rules="rules" :model="state.form" label-width="80px" style="padding: 0 20px" status-icon>
        <el-form-item prop="type" label="type" >
          <el-radio-group v-model="state.form.type">
            <el-radio :label="1">Menu Contents</el-radio>
            <el-radio :label="2">Menu Page</el-radio>
            <el-radio :label="3">Page Button</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item prop="name" label="name" >
          <el-input v-model="state.form.name" autocomplete="off" />
        </el-form-item>
        <el-form-item prop="path" label="Access path" v-if="state.form.type === 2">
          <el-input v-model="state.form.path" autocomplete="off"  />
        </el-form-item>
        <el-form-item prop="page" label="Page Path" v-if="state.form.type === 2" >
          <el-input v-model="state.form.page" autocomplete="off"  />
        </el-form-item>
        <el-form-item prop="orders" label="order"  v-if="state.form.type === 1 || state.form.type === 2" >
          <el-input-number v-model="state.form.orders" :min="1" />
        </el-form-item>
        <el-form-item prop="icon" label="icon"  v-if="state.form.type === 1 || state.form.type === 2">
          <el-select v-model="state.form.icon"  placeholder="Please select" style="width: 100%">
            <el-option
                v-for="item in icons"
                :key="item.id"
                :label="item.code"
                :value="item.value"
            >
              <el-icon>
                <component :is="item.value"></component>
              </el-icon>
              <span style="font-size: 14px; margin-left: 5px; top: -3px">{{ item.code }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="auth" label="Permissions"  v-if="state.form.type === 2 || state.form.type === 3" >
          <el-input v-model="state.form.auth" autocomplete="off"  />
        </el-form-item>
        <el-form-item prop="p_id" label="Parent" >
          <el-tree-select style="width: 100%" v-model="state.form.p_id" :data="state.tableData"
                          @node-click="handleNodeClick"
                          :props="{ label: 'name', value: 'id' }" :render-after-expand="false" check-strictly />
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
.w300 {
  width: 300px;
}

.ml5 {
  margin-left: 5px;
}
</style>
