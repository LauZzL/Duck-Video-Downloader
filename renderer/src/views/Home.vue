<template>
  <t-loading :loading="loading" :text="loading_text" attach="#home-layout" fullscreen />
  <t-dialog @confirm="onClickConfirm" v-model:visible="visible_update" confirmBtn="更新">
      <p>
        <MdPreview v-model="update_body"></MdPreview>
      </p>
    </t-dialog>
  <t-layout id="home-layout" style="width: 100%; height: 100%;">
    <aside-component />
    <t-content class="content">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" v-if="$route.meta.keepAlive" :key="$route.fullPath" />
        </keep-alive>
        <component :is="Component" v-if="!$route.meta.keepAlive" :key="$route.fullPath" />
      </router-view>
    </t-content>
  </t-layout>
</template>
  

<script setup>
import { MdPreview } from 'md-editor-v3'
import asideComponent from '@/components/asideComponent.vue'
import { onMounted, ref } from 'vue'
import { get_latest_release } from '../utils/util';
const loading = ref(true);
const loading_text = ref('加载duck中...');
const update_body = ref('')
const visible_update = ref(false)
const update_url = ref('')
const check_update = async () => {
  loading_text.value = '检查更新中...'
  const result = await get_latest_release();
  if (result.success) {
    if (result.data.tag_name !== duck.APP_VERSION) {
      visible_update.value = true
      update_body.value = result.data.body
      update_url.value = result.data.html_url
    }
  }else{
    MessagePlugin.error(result.message)
  }
  loading_text.value = '加载duck中...'
  loading.value = false
}
onMounted(() => {
    const interval = setInterval(() => {
      if (window.pywebview && window.pywebview.api) window.duck = window.pywebview.api;console.info('duck is loaded!');check_update();clearInterval(interval);
    }, 1000)
})
const onClickConfirm = () => {
  visible_update.value = false
  window.open(update_url.value, '_blank')
}
</script>

<style scoped>
.content {
  margin: 3px;
  overflow: auto;
  background-color: #f3f3f3;
}
</style>