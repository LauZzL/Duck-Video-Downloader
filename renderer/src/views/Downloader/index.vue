<template>
    <t-space style="margin: 15px;">
        <t-button @click="getAllTask">获取所有任务</t-button>
    </t-space>
    <taskComponent :tasks="tasks" />
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'
import taskComponent from '@/components/taskComponent.vue'
const tasks = ref([])
const getAllTask = async () => {
    const result = await duck.http_download_get_all_task()
    tasks.value = result.data
}
onMounted(() => {
    getAllTask()
})
</script>