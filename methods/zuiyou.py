import json

import requests
import utils
import re
from entity.Result import Result
from entity.Media import Media
from entity.MediaInfo import MediaInfo
from entity.Author import Author


__api = 'https://share.xiaochuankeji.cn/planck/share/post/detail'
__enable_proxy = utils.read_yaml_key('zuiyou.proxy.enable')
__proxy_http = utils.read_yaml_key('proxy.http')
__proxy_https = utils.read_yaml_key('proxy.https')


def __extract_data(href, pid ,response):
    data = response.json()
    if data['ret'] != 1:
        return Result().Error(data['msg'])
    if 'imgs' not in data['data']['post']:
        return Result().Error('data.post.imgs is empty')
    mediaInfo = MediaInfo()
    content = data['data']['post']['content']
    """
    提取作者信息
    """
    # data.post.member
    member = data['data']['post']['member']
    author = Author(
        name=member['name'],
        url='https://share.xiaochuankeji.cn/hybrid/share/profile?mid={}&from=profile'.format(member['id']),
        avatar=member['avatar_urls']['origin']['urls'][len(member['avatar_urls']['origin']['urls']) - 1],
        user_id=member['id']
    )
    mediaInfo.setAuthor(author)
    """
    提取媒体信息
    """
    media_list = []
    imgs = data['data']['post']['imgs']
    for _img in imgs:
        media = Media()
        media_id = _img['id']
        if 'origin_webp' in _img:
            urls = _img['urls']['origin_webp']['urls']
        else:
            urls = _img['urls']['540_webp']['urls']

        img_url = urls[len(urls) - 1]
        url = img_url
        aspect_ratio = '{}:{}'.format(_img['w'], _img['h'])
        has_video = False
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
        media.setCover(img_url)
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
    if utils.is_empty(pid):
        return Result().Error('pid is empty')
    payload = json.dumps({
        "pid": int(pid),
        "h_av": "5.2.13.011"
    })
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(__api, data=payload, proxies=proxy, headers=headers)
    return __extract_data(url, pid, response)

