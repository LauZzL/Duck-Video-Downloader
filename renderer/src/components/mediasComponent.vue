<template>
  <div class="media-container">
    <t-card :bordered="false">
      <div class="info">
        <t-space>
          <div>
            用户昵称：<t-tag>{{ profile.name }}</t-tag>
          </div>
          <div>
            用户名：<t-tag>{{ profile.screen_name }}</t-tag>
          </div>
          <div>
            帖子数量：<t-tag theme="success">{{ medias.length }}</t-tag>
          </div>
          <div>
            媒体数量：<t-tag theme="primary">{{ media_count }}</t-tag>
          </div>
        </t-space>
      </div>
    </t-card>
    <t-card :bordered="false">
      <div class="info">
        <t-space>
          <t-button theme="success" size="small" @click="downloadAll">下载</t-button>

          <t-checkbox v-model="enable_proxy">下载使用代理</t-checkbox>
        </t-space>
      </div>
    </t-card>
    <t-card :bordered="false">
      <div class="info">
        <t-table
          row-key="index"
          :data="video_all"
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
        ></t-table>
      </div>
    </t-card>
  </div>
</template>

<script setup>
import { ref, defineProps, onMounted, watch, watchEffect } from "vue";
const stripe = ref(true);
const bordered = ref(true);
const hover = ref(false);
const tableLayout = ref(false);
const size = ref("medium");
const showHeader = ref(true);
const visible = ref(true);
const media_count = ref(0);
const video_all = ref([]);
const enable_proxy = ref(false);
const columns = ref([
  { colKey: "href", ellipsis: true, title: "帖子地址" },
  { colKey: "url", ellipsis: true, title: "地址" },
  { colKey: "type", ellipsis: true, title: "类型" },
  { colKey: "status", title: "状态" },
]);
const props = defineProps({
  medias: Object,
  profile: Object,
});
const get_media_count = () => {
  media_count.value = 0;
  video_all.value = [];
  for (let i = 0; i < props.medias.length; i++) {
    media_count.value += props.medias[i].medias.length;
    let item = props.medias[i].medias;
    item.forEach((element) => {
        element.href = props.medias[i].href;
        element.status = "未下载";
    });
    video_all.value = video_all.value.concat(item);
  }
};
const downloadAll = () => {
  video_all.value.forEach( async (element) => {
    const result = await duck.http_download_add_task({
        url: element.url,
        headers: {},
        options: {
            enable_proxy: enable_proxy.value
        }
    })
  if (result.success) {
    element.status = "已添加下载任务";
  } else {
    element.status = result.message;
  }
  });
};
onMounted(() => {
  get_media_count();
});
watchEffect(() => {
  get_media_count();
});
</script>

<style scoped>
.media-container {
  margin: 15px;
}
.info {
  display: flex;
}
</style>