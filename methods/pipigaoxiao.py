import json

import requests
import utils
from entity.Result import Result
from entity.Media import Media
from entity.MediaInfo import MediaInfo


__api = 'https://h5.ippzone.com/ppapi/share/fetch_content'
__enable_proxy = utils.read_yaml_key('pipigaoxiao.proxy.enable')
__proxy_http = utils.read_yaml_key('proxy.http')
__proxy_https = utils.read_yaml_key('proxy.https')


def __extract_data(href, pid ,response):
    data = response.json()
    if data['ret'] != 1:
        return Result().Error(data['msg'])
    if 'imgs' not in data['data']['post']:
        return Result().Error('data.posts.imgs is empty')
    mediaInfo = MediaInfo()
    content = data['data']['post']['content']

    """
    提取媒体信息
    """
    media_list = []
    imgs = data['data']['post']['imgs']
    for _img in imgs:
        media = Media()
        media_id = _img['id']
        aspect_ratio = '{}:{}'.format(_img['w'], _img['h'])
        has_video = False
        url = None
        if 'video' in _img:
            has_video = _img['video'] == 1
        if has_video:
            videos = data['data']['post']['videos'][f'{media_id}']
            url = videos['url']
        media.setUrl(url)
        media.setMediaId(media_id)
        media.setAspectRatio(aspect_ratio)
        media.setContent(content)
        media.setHref(href)
        media.setIndex(len(media_list))
        media.setCover('https://file.ippzone.com/img/frame/id/{}'.format(media_id))
        media_list.append(media)
    mediaInfo.setMediaList(media_list)
    return Result().Success(mediaInfo, '获取成功')


def get_video(url):
    proxy = __enable_proxy and None or {
        'http': __proxy_http,
        'https': __proxy_https
    }
    url = utils.extract_url(url)
    if url and len(url) > 0:
        url = url[0]
    else:
        return Result().Error('url is empty')
    pid = url.split('pid=')[1].split('&')[0]
    mid = url.split('mid=')[1].split('&')[0]
    if utils.is_empty(pid):
        return Result().Error('pid is empty')
    payload = json.dumps({
        "pid": int(pid),
        "mid": int(mid),
        "type": "post"
    })
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(__api, data=payload, proxies=proxy, headers=headers)
    return __extract_data(url, pid, response)

