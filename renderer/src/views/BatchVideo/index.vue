<template>
  <div class="batch-container">
    <t-space>
      <t-button :loading="start_loading" theme="success" @click="exec">开始</t-button>
      <t-button :disabled="!start_loading" theme="danger" @click="stop_flag = true">停止</t-button>
      <t-button @click="importData">导入数据</t-button>
      <t-button @click="formatText(true)">格式化数据</t-button>
      <t-button @click="outputErrorData">导出失败数据</t-button>
    </t-space>
    <div class="input-data">
      <t-textarea v-model="input_data" placeholder="请输入链接，每行一个" />
    </div>
    <div class="batch-data">
      <t-card>
        <div class="batch-info">
          <t-space>
            <div>
              总链接数：<t-tag>{{ input_data_count }}</t-tag>
            </div>
            <div>
              当前执行：<t-tag>{{ executed }}</t-tag>
            </div>
            <div>
              剩余执行：<t-tag>{{ unexecuted }}</t-tag>
            </div>
            <div>
              成功数：<t-tag theme="success">{{ success_count }}</t-tag>
            </div>
            <div>
              失败数：<t-tag theme="danger">{{ error_count }}</t-tag>
            </div>
          </t-space>
        </div>
      </t-card>
    </div>
    <medias-component v-if="media_info" :media-info="media_info" />
  </div>
</template>
<script setup>
import { ref } from "vue";
import { extract_urls } from "../../utils/util";
import MediasComponent from "@/components/mediasComponent.vue";
import { MessagePlugin } from "tdesign-vue-next";
import { get_func } from "@/utils/util";

const input_data = ref(
  "开源地址，点个star：https://github.com/LauZzL/Duck-Video-Downloader\n批量解析仅支持帖子不支持主页。这是预置的测试数据，可以在同一行，也可以在多行，点下格式化数据试试。https://h5.pipix.com/s/iMFMMdvC/。{'url':'https://h5.pipix.com/s/iMSrmKA6/'}\n真的假的https://h5.pipix.com/s/iML6VSuw/好好看哦"
);
const input_data_count = ref(0);
const success_count = ref(0);
const error_count = ref(0);
const executed = ref(0);
const unexecuted = ref(0);
const urls_data = ref([]);
const error_data = ref([]);
const media_info = ref(null);
const media_list = ref([]);
const start_loading = ref(false);
const stop_flag = ref(false);

const formatText = (review) => {
  const urls = extract_urls(input_data.value);
  urls_data.value = urls;
  input_data_count.value = urls.length;
  success_count.value = 0;
  error_count.value = 0;
  executed.value = 0;
  unexecuted.value = urls.length;
  if (review) {
    input_data.value = urls.join("\n");
  }
};

const exec = async (obj) => {
  error_data.value = [];
  error_count.value = 0;
  media_info.value = null;
  formatText(false);
  start_loading.value = true;
  for (let i in urls_data.value) {
    if (stop_flag.value) {
      MessagePlugin.error("解析已停止");
      start_loading.value = false;
      return;
    }
    let url = urls_data.value[i];
    const func = get_func(url, "details");
    if (!func) {
      error_count.value += 1;
      unexecuted.value -= 1;
      executed.value += 1;
      error_data.value.push({
        url: url,
        error: "不支持该视频",
      });
      continue;
    }
    let result = await func({
      url: url,
      cursor: "",
    });
    if (result.success) {
      success_count.value += 1;
      unexecuted.value -= 1;
      executed.value += 1;
      media_list.value = media_list.value.concat(result.data.media_list);
      if (media_list && media_list.value.length > 0) {
        result.data.media_list = media_list.value;
      }
      // 不需要展示作者信息
      result.data.author = null;
      media_info.value = result.data;
    } else {
      error_count.value += 1;
      unexecuted.value -= 1;
      executed.value += 1;
      error_data.value.push({
        url: url,
        error: result.message,
      });
    }
  }
  start_loading.value = false;
};

const outputErrorData = async () => {
  let data = JSON.stringify(error_data.value);
  const result = await duck.write_file({
    filename: "error_data.json",
    data: data,
  })
  if (result.success) {
    MessagePlugin.success("导出成功");
  } else {
    MessagePlugin.error(result.message);
  }
}

const importData = async () => {
  const result = await duck.read_file()
  if (result.success){
    input_data.value = result.data
    MessagePlugin.success('导入成功')
  }else{
    MessagePlugin.error(result.message)
  }
}

</script>
<style scoped>
.batch-container {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  margin: 15px;
}
.input-data {
  margin-top: 15px;
}
.batch-info {
  display: flex;
}
.batch-data {
  margin-top: 15px;
}
</style>