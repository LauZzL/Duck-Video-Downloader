<template>
  <div v-if="info" class="result-card">
    <t-checkbox v-model="enable_proxy">下载使用代理</t-checkbox>
    <t-card :title="title" :bordered="false" hover-shadow>
      <div>
        <div v-if="info.aspect_ratio">分辨率：{{ info.aspect_ratio }}</div>
        <div v-if="info.duration_millis">
          持续时间：{{ info.duration_millis }}
        </div>
        <div v-if="info.variants">
          <h4>视频</h4>
          <t-table
            row-key="index"
            :data="info.variants"
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
            <template #operate="{ row }">
              <t-space>
                <t-button theme="primary" size="small" @click="copy(row)"
                  >复制</t-button
                >
                <t-button theme="primary" size="small" @click="play(row)"
                  >播放</t-button
                >
                <t-button theme="primary" size="small" @click="download(row)"
                  >下载</t-button
                >
              </t-space>
            </template>
          </t-table>
        </div>
      </div>
    </t-card>
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
  { colKey: "url", ellipsis: true, title: "视频地址" },
  { colKey: "content_type", ellipsis: true, title: "视频类型" },
  { colKey: "bitrate", ellipsis: true, title: "码率" },
  { colKey: "operate", ellipsis: true, title: "操作" },
]);
const props = defineProps({ info: Object });
const copy = (row) => {
  navigator.clipboard.writeText(row.url);
  MessagePlugin.success("复制成功");
};
const enable_proxy = ref(false);
const play = (row) => {
  const routeUrl = router.resolve({ path: "/player", query: { url: row.url } });
  const href = location.href;
  const url = href.substring(0, href.lastIndexOf("/")) + routeUrl.href.replace("#", "");
  duck.create_player({
    url: url
  });
};
const download = async (row) => {
  const result = await duck.http_download_add_task({
        url: row.url,
        headers: {
          referer: row.url
        },
        options: {
            enable_proxy: enable_proxy.value
        }
    });
  if (result.success){
    MessagePlugin.success("添加下载任务成功,请前往下载页面查看");
  }else{
    MessagePlugin.error(result.message);
  }
};
</script>

<style scoped>
.result-card {
  margin-top: 30px;
}
</style>