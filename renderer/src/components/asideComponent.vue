<template>
  <t-header>
    <t-head-menu
      theme="light"
      default-value="index"
      height="120px"
      expand-type="popup"
      @change="changeHandler"
    >
      <template v-for="item in dynamicMenuRoutes" :key="item.name">
        <t-menu-item
          :value="item.name"
          v-if="!item.children || item.children.length === 0"
        >
          {{ item.meta.title }}
        </t-menu-item>
        <t-submenu
          :value="item.name"
          :title="item.meta.title"
          v-if="item.children && item.children.length > 0"
        >
          <t-menu-item
            :value="item.name"
            v-for="(item, index) in item.children"
            :key="index"
          >
            {{ item.meta.title }}
          </t-menu-item>
        </t-submenu>
      </template>

      <template #operations>
        <a href="javascript:void(0);" @click="toGithub"
          ><t-icon class="t-menu__operations-icon" name="logo-github"
        /></a>
      </template>
    </t-head-menu>
  </t-header>
</template>

<script setup>
import { ref } from "vue";
import router from "@/router";
// 获取路由信息
const dynamicMenuRoutes = router
  .getRoutes()
  .filter((route) => route.meta && route.meta.menu);
const changeHandler = (active) => {
  router.push({ name: active });
};
const toGithub = () => {
  window.open('https://github.com/LauZzL/duck-video-downloader')
};
</script>