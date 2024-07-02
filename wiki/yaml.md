# Yaml 配置说明

## download 下载配置

| 参数名    | 类型      | 默认值                                                                                         | 说明                                 | 必填 |
|--------|---------|---------------------------------------------------------------------------------------------|------------------------------------|----|
| path  | string  | `download/${$.author.name}/${$.media.media_id}/${$.media.title}_${$.media.index}.${suffix}` | 下载路径 | 是  |
| thread | integer | 10                                                                                          | 下载线程数                              | 是  |

### path 说明

path 支持模板语法，使用`${key}`格式来提取变量。

点击下载时，会向task方法中发送options.media_info参数，你可以使用`jsonpath`语法来提取变量并将变量替换到path中。

- 常量
  - `suffix`: 文件后缀，会根据文件类型自动设置


- media_info 参数
```json
{
    "media": {
        "aspect_ratio": "分辨率",
        "bitrate": "比特率",
        "content": "正文内容",
        "content_type": "video/mp4",
        "cover": "视频封面",
        "duration": "视频时间",
        "href": "视频地址",
        "index": "序号，从0开始",
        "media_id": "视频ID",
        "title": "视频标题",
        "url": "下载地址"
    },
    "author": {
        "avatar": "头像",
        "name": "昵称",
        "url": "主页地址",
        "user_id": "用户ID"
    }
}
```






## proxy 代理

| 参数名    | 类型     | 默认值 | 说明                                | 必填 |
|--------|--------|------|-----------------------------------|---|
| http  | string | 无 | http代理地址，例如 http://127.0.0.1:7890 | -  |
| https | string | 无 | http代理地址，例如 http://127.0.0.1:7890 | -  |

## twitter 推特配置

| 参数名          | 类型      | 默认值   | 说明                                         | 必填 |
|--------------|---------|-------|--------------------------------------------|----|
| media.count  | integer | 20    | 每次获取主页media的数量，最大不确定，可以自己尝试                | 否  |
| proxy.enable | boolean | false | 请求时是否使用代理                                  | 否  |
| cookie | string  | -     | 账号Cookie  获取方法查看[twitter.md](/wiki/twitter.md)     | 是  |
| authorization | string  | -     | authorization 获取方法查看[twitter.md](/wiki/twitter.md) | 是  |
| cookie | string  | -     | 账号Cookie 获取方法查看[twitter.md](/wiki/twitter.md) | 是  |

## pipixia 皮皮虾配置

| 参数名          | 类型      | 默认值   | 说明                                         | 必填 |
|--------------|---------|-------|--------------------------------------------|----|
| proxy.enable | boolean | false | 请求时是否使用代理                                  | 否  |

