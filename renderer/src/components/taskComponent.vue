<template>
  <div class="result-card">
    <div>
        <div>
          <t-table
            row-key="index"
            :data="tasks"
            :columns="columns"
            :stripe="stripe"
            :bordered="bordered"
            :hover="hover"
            :table-layout="tableLayout ? 'auto' : 'fixed'"
            :size="size"
            :show-header="showHeader"
            cell-empty-content="-"
            resizable
            lazy-load
          >
          <template #progress="{ row }">
            {{ row.total_size }} / {{ row.downloaded_size }}
          </template>
          <template #operate="{ row }">
            <t-space>
              <t-button theme="primary" size="small" @click="removeTask(row)"
                >移除</t-button
              >
            </t-space>
          </template>
          </t-table>
        </div>
      </div>
  </div>
</template>
  
  <script setup>
import { MessagePlugin } from "tdesign-vue-next";
import { onMounted, ref, defineProps } from "vue";
import router from "@/router";
const stripe = ref(true);
const bordered = ref(true);
const hover = ref(false);
const tableLayout = ref(false);
const size = ref("medium");
const showHeader = ref(true);
const title = ref("视频信息");
const visible = ref(true);
const columns = ref([
  { colKey: "task_id", ellipsis: true, title: "任务ID" },
  { colKey: "url", ellipsis: true, title: "链接" },
  { colKey: "progress", ellipsis: true, title: "下载进度" },
  { colKey: "speed", ellipsis: true, title: "下载速度" },
  { colKey: "message", ellipsis: true, title: "状态" },
  { colKey: "operate", ellipsis: true, title: "操作" },
]);
const props = defineProps({ tasks: Object });
const removeTask = async (row) => {
  const result = await duck.http_download_remove_task({
    task_id: row.task_id,
  })
  if (result.success) {
    MessagePlugin.success("移除成功");
  } else {
    MessagePlugin.error(result.message);
  }
};
</script>
  
<style scoped>
.result-card {
  margin: 15px;
}
</style>