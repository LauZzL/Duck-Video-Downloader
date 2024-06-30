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
          <t-button @click="parser" theme="primary" :loading="loading"
            >解析</t-button
          >
        </t-form-item>
      </t-form>
    </t-space>
    <video-info-component
      v-if="select_model == 'details' && video_info"
      :info="video_info"
    />
    <medias-component
      v-if="
        select_model == 'posts' && medias && user_profile && medias.length > 0
      "
      :medias="medias"
      :profile="user_profile"
    />
  </div>
</template>
  
<script setup>
import VideoInfoComponent from "@/components/videoInfoComponent.vue";
import MediasComponent from "@/components/mediasComponent.vue";
import { get_func } from "@/utils/util";
import { MessagePlugin } from "tdesign-vue-next";
import { ref } from "vue";
const formData = ref({
  labelAlign: "top",
  url: "",
});
const loading = ref(false);
const select_model = ref(null);
const video_info = ref(null);
const user_profile = ref({
  blocking: false,
  blocked_by: false,
  protected: false,
  following: true,
  followed_by: false,
  name: "汌",
  screen_name: "Songchuanbb",
});
const medias = ref([
  {
    href: "https://x.com/Songchuanbb/status/1807064251145556203",
    medias: [
      {
        url: "https://pbs.twimg.com/media/GRP7WpUWIAA55Lv.jpg",
        type: "photo",
      },
    ],
  },
  {
    href: "https://x.com/Songchuanbb/status/1805844660037796112",
    medias: [
      {
        url: "https://pbs.twimg.com/media/GQ-mJP6XgAEWVzb.jpg",
        type: "photo",
      },
    ],
  },
  {
    href: "https://x.com/Songchuanbb/status/1803287648779346063",
    medias: [
      {
        url: "https://pbs.twimg.com/media/GQaQjPbWgAAU9Ey.jpg",
        type: "photo",
      },
      {
        url: "https://pbs.twimg.com/media/GQaQjPeWkAAIA41.jpg",
        type: "photo",
      },
    ],
  },
  {
    href: "https://x.com/Songchuanbb/status/1801563596385616252",
    medias: [
      {
        url: "https://video.twimg.com/tweet_video/GQBwiMaXIAAjjn-.mp4",
        type: "animated_gif",
      },
    ],
  },
  {
    href: "https://x.com/Songchuanbb/status/1801130128669397471",
    medias: [
      {
        url: "https://pbs.twimg.com/media/GP7mSMoXEAAqz9-.jpg",
        type: "photo",
      },
    ],
  },
  {
    href: "https://x.com/Songchuanbb/status/1798218625943585268",
    medias: [
      {
        url: "https://pbs.twimg.com/media/GPSOTZMXUAACpLQ.jpg",
        type: "photo",
      },
    ],
  },
  {
    href: "https://x.com/Songchuanbb/status/1796045366262894946",
    medias: [
      {
        url: "https://pbs.twimg.com/media/GOzVvHcXQAAAOCy.jpg",
        type: "photo",
      },
      {
        url: "https://pbs.twimg.com/media/GOzVvHdXAAAmXsK.jpg",
        type: "photo",
      },
    ],
  },
  {
    href: "https://x.com/Songchuanbb/status/1794245351404400711",
    medias: [
      {
        url: "https://pbs.twimg.com/media/GOZwojWWQAA62Pp.jpg",
        type: "photo",
      },
    ],
  },
  {
    href: "https://x.com/Songchuanbb/status/1791327772414996906",
    medias: [
      {
        url: "https://pbs.twimg.com/media/GNwTHBFWoAAxR3B.jpg",
        type: "photo",
      },
    ],
  },
  {
    href: "https://x.com/Songchuanbb/status/1787352889305755778",
    medias: [
      {
        url: "https://pbs.twimg.com/media/GM3z-U0XEAAOLqd.jpg",
        type: "photo",
      },
    ],
  },
  {
    href: "https://x.com/Songchuanbb/status/1784101584676245995",
    medias: [
      {
        url: "https://pbs.twimg.com/media/GMJm7hNXkAAJosZ.jpg",
        type: "photo",
      },
    ],
  },
  {
    href: "https://x.com/Songchuanbb/status/1782286761583837332",
    medias: [
      {
        url: "https://pbs.twimg.com/media/GLv0W8AXIAAp7yH.jpg",
        type: "photo",
      },
    ],
  },
  {
    href: "https://x.com/Songchuanbb/status/1772854302924493014",
    medias: [
      {
        url: "https://video.twimg.com/amplify_video/1772853012098076673/vid/avc1/960x720/uTjPwtAGvZXi8Kfv.mp4?tag=14",
        type: "video",
      },
    ],
  },
]);
const exec_func = async (obj) => {
  const url = obj.url;
  const cursor = obj.cursor;
  const func = get_func(url, select_model.value);
  if (!func) {
    MessagePlugin.error("不支持该视频");
    loading.value = false;
    return;
  }
  video_info.value = null;
  const result = await func({
    url: url,
    cursor: obj.cursor,
  });
  if (result.success) {
    user_profile.value = result.legacy;
  }
  if (result.cursor && result.success) {
    // 合并
    medias.value = medias.value.concat(result.data);
    obj.cursor = result.cursor;
    await exec_func(obj);
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
  const result = await exec_func({
    url: url,
    cursor: null,
  });
  if (result.success) {
    MessagePlugin.success("解析成功");
    if (select_model.value == "details") {
      video_info.value = result.data;
    }
  } else {
    MessagePlugin.error(result.message);
    video_info.value = null;
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
  