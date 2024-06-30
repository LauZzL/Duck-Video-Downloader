<template>
  <div>
    <vue3VideoPlay
      width="800px"
      height="600px"
      :src="src"
      :type="video_type"
      webFullScreen="true"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import router from "@/router";
const src = ref("");
const video_type = ref("video/mp4mp4");

onMounted(() => {
  const url = router.currentRoute.value.query.url;
  if (!url) {
    alert("请传入视频地址");
    return;
  }
  video_type.value = url.match("m3u8") ? "m3u8" : "video/mp4";
  src.value = url;
});
</script>

<style scoped>
</style>