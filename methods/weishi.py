import json
import re

import requests
import utils
from entity.Result import Result
from entity.Media import Media
from entity.MediaInfo import MediaInfo
from entity.Author import Author

__api = 'https://h5.weishi.qq.com/webapp/json/weishi/WSH5GetPlayPage'

__enable_proxy = utils.read_yaml_key('weishi.proxy.enable')
__proxy_http = utils.read_yaml_key('proxy.http')
__proxy_https = utils.read_yaml_key('proxy.https')

def __get_redirect_url(url, proxy):
    response = requests.get(url, allow_redirects=False, proxies=proxy)
    return response.headers['Location']

def __extract_data(href, feed_id ,response):
    data = response.json()
    if data['ret'] != 0:
        return Result().Error(data['msg'])
    mediaInfo = MediaInfo()
    feeds = data['data']['feeds']
    media_list = []
    for feed in feeds:
        content = feed['feed_desc']
        """
        提取作者信息
        """
        # data.feeds[0].poster
        poster = feed['poster']
        author = Author(
            name=poster['nick'],
            url='https://isee.weishi.qq.com/ws/app-pages/wspersonal/index.html?_wv=1&id={}'.format(poster['id']),
            avatar=poster['avatar'],
            user_id=poster['id']
        )
        mediaInfo.setAuthor(author)
        """
        提取媒体信息
        """
        media = Media()
        url = feed['video_url']
        cover = feed['images'][0]['url']
        media_id = feed['id']
        duration = feed['video']['duration']
        aspect_ratio = '{}:{}'.format(feed['video']['width'], feed['video']['height'])
        media.setUrl(url)
        media.setCover(cover)
        media.setMediaId(media_id)
        media.setDuration(duration)
        media.setAspectRatio(aspect_ratio)
        media.setContent(content)
        media.setHref(href)
        media.setIndex(len(media_list))
        media_list.append(media)
    mediaInfo.setMediaList(media_list)
    return Result().Success(mediaInfo, '获取成功')

def get_video(url):
    proxy = __enable_proxy and None or {
        'http': __proxy_http,
        'https': __proxy_https
    }
    url = utils.extract_url(url)[0]
    if 'id=' not in url:
        url = __get_redirect_url(url, proxy)
    feed_id = url.split('id=')[1].split('&')[0]
    if utils.is_empty(feed_id):
        return Result().Error('cannot extract feed_id')
    payload = json.dumps({
        "feedid": feed_id
    })
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Content-Type': 'application/json'
    }
    response = requests.post(__api, headers=headers, data=payload, proxies=proxy)
    return __extract_data(url, feed_id, response)

