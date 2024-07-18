<template>
  <div class="form">
    <t-space direction="vertical" size="large">
      <t-form
        :data="formData"
        :label-align="formData.labelAlign"
        :label-width="60"
      >
        <t-form-item label="视频地址" name="url">
          <t-select autoWidth showArrow v-model="select_model">
            <t-option key="details" label="帖子" value="details" />
            <t-option key="posts" label="主页" value="posts" />
          </t-select>
          <t-input v-model="formData.url"></t-input>
        </t-form-item>
        <div>
          <t-space>
            <t-button @click="parser" theme="primary" :loading="loading"
            >开始解析</t-button
          >
          <t-button @click="stop_flag = true; stop_parser_btn = true" :disabled="stop_parser_btn" theme="danger"
            >停止解析</t-button
          >
          </t-space>
        </div>
      </t-form>
    </t-space>
    <medias-component
      v-if="
        media_info
      "
      :media-info="media_info"
    />
  </div>
</template>
  
<script setup>
import MediasComponent from "@/components/mediasComponent.vue";
import { get_func } from "@/utils/util";
import { MessagePlugin } from "tdesign-vue-next";
import { ref } from "vue";
const stop_parser_btn = ref(true);
const stop_flag = ref(false);
const formData = ref({
  labelAlign: "top",
  url: "",
});
const loading = ref(false);
const select_model = ref(null);
const media_info = ref(null);
const media_list = ref([]);
const exec_func = async (obj) => {
  let result = null;
  const url = obj.url;
  const cursor = obj.cursor;
  const func = get_func(url, select_model.value);
  if (!func) {
    MessagePlugin.error("不支持该视频");
    loading.value = false;
    return;
  }
  if (stop_flag.value) {
    MessagePlugin.error("解析已停止");
    return result;
  }
  result = await func({
    url: url,
    cursor: obj.cursor,
  });
  if (result.success && result.data.cursor) {
    // 合并
    media_list.value = media_list.value.concat(result.data.media_list);
    if (media_list && media_list.value.length > 0){
      result.data.media_list = media_list.value;
    }
    media_info.value = result.data;
    obj.cursor = result.data.cursor;
    await exec_func(obj);
  }else if(result.success && !result.data.cursor && media_list.value.length == 0 && result.data.media_list.length > 0){
    media_list.value = result.data.media_list;
    media_info.value = result.data;
    return result;
  }
  return result;
};
const parser = async (e) => {
  e.preventDefault();
  const url = formData.value.url;
  loading.value = true;
  if (!select_model.value) {
    MessagePlugin.error("请选择解析模式");
    loading.value = false;
    return;
  }
  stop_parser_btn.value = false;
  media_info.value = null;
  media_list.value = [];
  const result = await exec_func({
    url: url,
    cursor: null,
  });
  stop_parser_btn.value = true;
  if (!result) {
    MessagePlugin.error("解析失败");
    loading.value = false;
    return;
  }
  if (result.success) {
    MessagePlugin.success(result.message);
    if (select_model.value == "details") {
      media_info.value = result.data;
    }
  } else {
    MessagePlugin.error(result.message);
    media_info.value = null;
  }
  loading.value = false;
};
</script>
  
  <style scoped>
.form {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  margin: 15px;
}
.t-select__wrap {
  width: auto;
}
</style>
  