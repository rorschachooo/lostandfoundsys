<script setup>
import '@wangeditor/editor/dist/css/style.css' // Import CSS
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import {onBeforeUnmount, onMounted, ref, shallowRef} from "vue";
import config from "../../config";


// Content HTML
const valueHtml = ref('<p>hello</p>')

// Simulate ajax asynchronous acquisition of content
onMounted(() => {
  setTimeout(() => {
    valueHtml.value = 'Setting content'
  }, 1000)
})
// Editor instance, must use shallowRef
const editorRef = shallowRef()
const toolbarConfig = {}
const editorConfig = {
  placeholder: 'Please enter content...',
}
editorConfig.MENU_CONF['uploadImage'] = {
  server: `http://${config.serverUrl}/file/uploadImg`
}
const handleCreated = (editor) => {
  editorRef.value = editor // Record the editor instance, important!
}
// When the component is destroyed, the editor is also destroyed in time
onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
})
</script>

<template>
  <div>
    <div style="border: 1px solid #ccc">
      <Toolbar
          style="border-bottom: 1px solid #ccc"
          :editor="editorRef"
          :defaultConfig="toolbarConfig"
          :mode="'simple'"
      />
      <Editor
          style="height: 500px; overflow-y: hidden;"
          v-model="valueHtml"
          :defaultConfig="editorConfig"
          :mode="'simple'"
          @onCreated="handleCreated"
      />
    </div>
  </div>
</template>