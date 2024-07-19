<template>
  <div class="media-container">
    <t-card :bordered="false">
      <div v-if="mediaInfo.author" class="info">
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
            用户昵称：<t-tag
              @click="copy_data(mediaInfo.author.name, '复制用户昵称成功')"
              >{{ mediaInfo.author.name }}</t-tag
            >
          </div>
          <div>
            用户名：<t-tag
              max-width="150"
              @click="copy_data(mediaInfo.author.user_id, '复制用户ID成功')"
              >{{ mediaInfo.author.user_id }}</t-tag
            >
          </div>
          <div>
            帖子数量：<t-tag theme="default">{{ post_ids.length }}</t-tag>
          </div>
          <div>
            媒体数量：<t-tag theme="default">{{ media_all.length }}</t-tag>
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
          <t-button
            theme="success"
            size="small"
            v-if="mediaInfo.author && mediaInfo.author.url"
            @click="copy_data(mediaInfo.author.url, '复制用户主页地址成功')"
            >复制主页地址</t-button
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
          :scroll="{ type: 'virtual', rowHeight: 48, bufferSize: 10 }"
          :height="height"
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
            <t-image
              :src="row.cover"
              :overlay-content="renderMask"
              overlay-trigger="hover"
              @click="preview_image(row.cover)"
            />
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
    <t-image-viewer
      v-model:visible="visibleImageViewer"
      :images="[view_image]"
    >
    </t-image-viewer>
  </div>
</template>

<script setup lang="jsx">
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
const height = ref(300);
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
const visibleImageViewer = ref(false);
const view_image = ref(null);
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
    let options = {
      enable_proxy: enable_proxy.value,
      media_info: {
        media: element,
        author: props.mediaInfo.author,
      },
    };
    options = { ...element.options, ...options };
    const result = await duck.http_download_add_task({
      url: element.url,
      headers: {},
      options: options,
    });
    if (result.success) {
      element.status = "已添加下载任务";
    } else {
      element.status = result.message;
    }
  });
};
const download = async (row) => {
  let options = {
    enable_proxy: enable_proxy.value,
    media_info: {
      media: row,
      author: props.mediaInfo.author,
    },
  };
  options = { ...row.options, ...options };
  const result = await duck.http_download_add_task({
    url: row.url,
    headers: {},
    options: options,
  });
  if (result.success) {
    MessagePlugin.success(result.message);
  } else {
    MessagePlugin.error(result.message);
  }
  row.status = result.message;
};
const play = (row) => {
  router.push({
    path: "/player",
    query: { 
      url: row.url,
      cover: row.cover
    },
  });
};
const copy = (row) => {
  navigator.clipboard.writeText(row.url);
  MessagePlugin.success("复制成功");
};
const copy_data = (data, message) => {
  navigator.clipboard.writeText(data);
  MessagePlugin.success(message);
};
const saveExcel = async () => {
  const result = await duck.save_media_excel({
    data: media_all.value,
    filename:
      props.mediaInfo.author.name +
      " - " +
      props.mediaInfo.author.user_id +
      ".csv",
    keys: columns.value.map((item) => item.colKey),
  });
  if (result.success) {
    MessagePlugin.success(result.message);
  } else {
    MessagePlugin.error(result.message);
  }
};

const renderMask = () => (
  <div
    style={{
      background: 'rgba(0,0,0,.4)',
      color: '#fff',
      height: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    }}
  >
    预览
  </div>
);
const preview_image = (imgurl) => {
  view_image.value = imgurl;
  visibleImageViewer.value = true;
}

onresize = () => {
  height.value = getWindowHeight();
};

const getWindowHeight = () => {
  return window.innerHeight - 100;
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