<template>
  <t-layout style="width: 100%; height: 100%;">
    <aside-component></aside-component>
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
import asideComponent from '@/components/asideComponent.vue'
import { onMounted } from 'vue'
onMounted(() => {
    const interval = setInterval(() => {
      if (window.pywebview && window.pywebview.api) window.duck = window.pywebview.api;console.info('duck is loaded!');clearInterval(interval);
    }, 1000)
})
</script>

<style scoped>
.content {
  margin: 3px;
  overflow: auto;
  background-color: #f3f3f3;
}
</style>