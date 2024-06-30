<template>
  <div class="index-container">
    <MdPreview v-model="readme"></MdPreview>
  </div>
</template>
<script setup>
import 'md-editor-v3/lib/style.css'
import { MdPreview } from 'md-editor-v3'
import { ref, onMounted } from "vue";
const readme = ref('');
onMounted(() => {
  let reuslt = null;
  const interval = setInterval(async () => {
    if (window.pywebview && window.pywebview.api)
      reuslt = await window.pywebview.api.get_readme();
    readme.value = reuslt.data;
    clearInterval(interval);
  }, 1000);
});
</script>
<style scoped>
.index-container {
  margin: 15px;
}
</style>