<template>
  <div class="media-container">
    <t-card :bordered="false">
      <div class="info">
        <t-space style="margin-top: 10px">
          <div style="display: flex; height: 32px; align-items: center">
            用户头像：<t-image
              style="border-radius: 50%; width: 32px; height: 32px"
              :src="mediaInfo.author.avatar"
            />
          </div>
        </t-space>
        <t-space style="margin-top: 10px">
          <div>
            用户昵称：<t-tag>{{ mediaInfo.author.name }}</t-tag>
          </div>
          <div>
            用户名：<t-tag>{{ mediaInfo.author.user_id }}</t-tag>
          </div>
          <div>
            帖子数量：<t-tag theme="success">{{ post_ids.length }}</t-tag>
          </div>
          <div>
            媒体数量：<t-tag theme="primary">{{ media_all.length }}</t-tag>
          </div>
        </t-space>
      </div>
    </t-card>
    <t-card :bordered="false">
      <div class="info">
        <t-space>
          <t-button theme="success" size="small" @click="downloadAll"
            >全部下载</t-button
          >
          <t-button theme="success" size="small" @click="saveExcel"
            >保存至Excel</t-button
          >
          <t-checkbox v-model="enable_proxy">下载使用代理</t-checkbox>
        </t-space>
      </div>
    </t-card>
    <t-card :bordered="false">
      <div class="info">
        <t-table
          row-key="index"
          :data="media_all"
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
          <template #cover="{ row }">
            <t-image :src="row.cover" width="100px" height="100px" />
          </template>

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
    </t-card>
  </div>
</template>

<script setup>
import { ref, defineProps, onMounted, watch, watchEffect } from "vue";
import router from "@/router";
import { MessagePlugin } from "tdesign-vue-next";
const stripe = ref(true);
const bordered = ref(true);
const hover = ref(false);
const tableLayout = ref(false);
const size = ref("medium");
const showHeader = ref(true);
const visible = ref(true);
const media_all = ref([]);
const post_ids = ref([]);
const enable_proxy = ref(false);
const columns = ref([
  { colKey: "index", ellipsis: true, title: "Index" },
  { colKey: "cover", ellipsis: true, title: "封面" },
  { colKey: "media_id", ellipsis: true, title: "帖子ID" },
  { colKey: "href", ellipsis: true, title: "帖子地址" },
  { colKey: "url", ellipsis: true, title: "地址" },
  { colKey: "title", ellipsis: true, title: "标题" },
  { colKey: "content", ellipsis: true, title: "正文" },
  { colKey: "bitrate", ellipsis: true, title: "码率" },
  { colKey: "aspect_ratio", ellipsis: true, title: "分辨率" },
  { colKey: "duration", ellipsis: true, title: "持续时间" },
  { colKey: "content_type", ellipsis: true, title: "类型" },
  { colKey: "status", title: "状态" },
  { colKey: "operate", title: "操作", fixed: "right", width: 200 },
]);
const props = defineProps({
  mediaInfo: Object,
});
const get_media_count = () => {
  media_all.value = [];
  props.mediaInfo.media_list.forEach((element) => {
    media_all.value = media_all.value.concat(element);
  });
  media_all.value.some((item) => {
    if (post_ids.value.includes(item.media_id)) return;
    post_ids.value.push(item.media_id);
  });
};
const downloadAll = () => {
  media_all.value.forEach(async (element) => {
    const result = await duck.http_download_add_task({
      url: element.url,
      headers: {},
      options: {
        enable_proxy: enable_proxy.value,
        media_info: {
          media: element,
          author: props.mediaInfo.author,
        },
      },
    });
    if (result.success) {
      element.status = "已添加下载任务";
    } else {
      element.status = result.message;
    }
  });
};
const download = async (row) => {
  const result = await duck.http_download_add_task({
    url: row.url,
    headers: {},
    options: {
      enable_proxy: enable_proxy.value,
      media_info: {
        media: row,
        author: props.mediaInfo.author,
      },
    },
  });
  if (result.success) {
    MessagePlugin.success(result.message);
  } else {
    MessagePlugin.error(result.message);
  }
  row.status = result.message;
};
const play = (row) => {
  const routeUrl = router.resolve({ path: "/player", query: { url: row.url } });
  const href = location.href;
  const url =
    href.substring(0, href.lastIndexOf("/")) + routeUrl.href.replace("#", "");
  duck.create_player({
    url: url,
  });
};
const saveExcel = async () => {
  const result =  await duck.save_media_excel({
    data: media_all.value,
    filename: props.mediaInfo.author.name + " - " + props.mediaInfo.author.user_id + '.csv',
    keys: columns.value.map((item) => item.colKey),
  });
  if (result.success) {
    MessagePlugin.success(result.message);
  } else {
    MessagePlugin.error(result.message);
  }
};
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
  flex-direction: column;
}
</style>