<template>
  <div class="player-container">
    <vue3VideoPlay 
      :src="src" 
      height="100%"
      width="100%"
      :type="video_type"
      :poster="cover"
      class="video-player" 
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import router from "@/router";
const src = ref("");
const video_type = ref("video/mp4");

onMounted(() => {
  const url = router.currentRoute.value.query.url;
  const cover = router.currentRoute.value.query.cover;
  if (url) {
    video_type.value = url.match("m3u8") ? "m3u8" : "video/mp4";
    src.value = url;
  }
});
</script>

<style scoped>
.player-container {
  width: 100%;
  height: 100%;
}
</style>