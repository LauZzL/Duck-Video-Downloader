<template>
  <div class="media-container">
    <t-collapse
      v-if="yaml"
      :expand-icon-placement="direction"
      :expand-on-row-click="!onlyIcon"
    >
      <t-collapse-panel value="twitter">
        <template #expandIcon><LogoGithubIcon /></template>
        <template #header>Twitter</template>
        <div class="setting-item">
          <div class="item-c">
            <span>代理：</span><t-switch
              v-model="yaml.twitter.proxy.enable"
              size="large"
            >
              <template #label="slotProps">{{
                slotProps.value ? "开" : "关"
              }}</template>
            </t-switch>
          </div>
          <div class="item-c">
            <t-input label="媒体单次最大获取数:" v-model="yaml.twitter.media.count" />
          </div>
          <div class="item-c">
            <t-input label="Cookie:" v-model="yaml.twitter.cookie" />
          </div>
          <div class="item-c">
            <t-input label="Authorization:" v-model="yaml.twitter.authorization" />
          </div>
          <div class="item-c">
            <t-input label="X-Csrf-Token:" v-model="yaml.twitter['x-csrf-token']" />
          </div>
        </div>
      </t-collapse-panel>
      <t-collapse-panel value="pipixia">
        <template #expandIcon><ShrimpIcon /></template>
        <template #header>皮皮虾</template>
        <div class="setting-item">
          <div class="item-c">
            <span>代理：</span><t-switch
              v-model="yaml.pipixia.proxy.enable"
              size="large"
            >
              <template #label="slotProps">{{
                slotProps.value ? "开" : "关"
              }}</template>
            </t-switch>
          </div>
        </div>
      </t-collapse-panel>
      <t-collapse-panel value="download">
        <template #expandIcon><Download1Icon /></template>
        <template #header>下载</template>
        <div class="setting-item">
          <div class="item-c">
            <t-input label="路径:" v-model="yaml.download.path" />
          </div>
          <div class="item-c">
            <t-input label="线程数:" v-model="yaml.download.thread" />
          </div>
        </div>
      </t-collapse-panel>
      <t-collapse-panel value="proxy">
        <template #expandIcon><InternetIcon /></template>
        <template #header>代理</template>
        <div class="setting-item">
          <div class="item-c">
            <t-input label="HTTP:" v-model="yaml.proxy.http" />
          </div>
          <div class="item-c">
            <t-input label="HTTPS:" v-model="yaml.proxy.https" />
          </div>
        </div>
      </t-collapse-panel>
    </t-collapse>
    <div class="btn-operate">
      <t-space>
        <t-button @click="save">保存</t-button>
      </t-space>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { LogoGithubIcon, ShrimpIcon, Download1Icon, InternetIcon } from "tdesign-icons-vue-next";
import { MessagePlugin } from "tdesign-vue-next";
const direction = ref("left");
const onlyIcon = ref(false);
const yaml = ref(null);
onMounted(() => {
  const interval = setInterval(async () => {
    if (window.pywebview && window.pywebview.api && window.duck) {
      const result = await duck.get_yaml();
      yaml.value = result.data;
      clearInterval(interval);
    }
  }, 1000);
});
const save = async () => {
  if (!yaml || !yaml.value) {
    MessagePlugin.error('保存失败，未读取到有效配置')
    return
  }
  const result = await duck.save_yaml(yaml.value)
  if (result.success){
    MessagePlugin.success(result.message)
  }else{
    MessagePlugin.error(result.message)
  }
}
</script>

<style scoped>
.media-container {
  margin: 15px;
}
.setting-item {
  display: flex;
  flex-direction: column;
}
.setting-item .item-c {
  display: flex;
  align-items: center; 
  margin-top: 5px;
}
.btn-operate {
  margin-top: 10px;
}
</style>