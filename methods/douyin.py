import json

import requests
import utils
import re
from entity.Result import Result
from entity.Media import Media
from entity.MediaInfo import MediaInfo
from entity.Author import Author


__api = 'https://www.iesdouyin.com/share/video/{}'
__enable_proxy = utils.read_yaml_key('douyin.proxy.enable')
__proxy_http = utils.read_yaml_key('proxy.http')
__proxy_https = utils.read_yaml_key('proxy.https')


def get_video(url):
    proxy = __enable_proxy and None or {
        'http': __proxy_http,
        'https': __proxy_https
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }
    video_id = __extract_video_id(url, proxy)
    if utils.is_empty(video_id):
        return Result().Error('视频ID获取失败')
    response = requests.get(__api.format(video_id), headers=headers, proxies=proxy)
    return __extract_data(url, video_id, response.text)



def __extract_data(url, video_id, data):
    if video_id not in data:
        return Result().Error('视频信息获取失败')
    searcher = re.compile("_ROUTER_DATA = (.*?)};")
    search_data = searcher.findall(data)
    if utils.is_empty(search_data) or len(search_data) == 0:
        return Result().Error('视频信息获取失败')
    mediaInfo = MediaInfo()
    json_data = json.loads(search_data[0] + '}')
    item_list = utils.extract_key_value(json_data, 'item_list')
    """
    提取作者信息
    """
    author = Author(
        name=item_list[0]['author']['nickname'],
        url='https://www.douyin.com/user/{}'.format(item_list[0]['author']['sec_uid']),
        avatar=item_list[0]['author']['avatar_medium']['url_list'][0],
        user_id=item_list[0]['author']['sec_uid']
    )
    mediaInfo.setAuthor(author)
    """
    提取媒体
    """
    media_list = []
    for item in item_list:
        content = item['desc']
        media_id = item['aweme_id']
        href = 'https://www.douyin.com/video/{}'.format(item['aweme_id'])
        if 'video' in item:
            media = Media()
            video = item['video']
            url = video['play_addr']['url_list'][0]
            cover = video['cover']['url_list'][0]
            aspect_ratio = '{}:{}'.format(video['height'], video['width'])
            media.setUrl(url.replace('playwm', 'play'))
            media.setHref(href)
            media.setContent(content)
            media.setCover(cover)
            media.setAspectRatio(aspect_ratio)
            media.setMediaId(media_id)
            media.setIndex(len(media_list))
            media_list.append(media)
        if 'images' in item:
            images = item['images']
            if images is None or len(images) == 0:
                continue
            for image in images:
                media = Media()
                url = image['url_list'][len(image['url_list']) - 1]
                cover = url
                aspect_ratio = '{}.{}'.format(image['height'], image['width'])
                media.setUrl(url)
                media.setHref(href)
                media.setContent(content)
                media.setCover(cover)
                media.setAspectRatio(aspect_ratio)
                media.setMediaId(media_id)
                media.setIndex(len(media_list))
                media_list.append(media)
    mediaInfo.setMediaList(media_list)
    return Result().Success(mediaInfo, '视频信息获取成功')



def __get_redirect_url(url, proxy):
    response = requests.get(url, allow_redirects=False, proxies=proxy)
    return response.headers['Location']

def __extract_video_id(url, proxy, retry=0):
    if retry > 3:
        return None
    url = utils.extract_url(url)
    if url and len(url) > 0:
        url = url[0]
    else:
        return None
    video_id = None
    if 'video' in url:
        video_id = url.split('video/')[1].split('/')[0]
        if utils.is_number(video_id):
            return video_id
    elif 'modal_id=' in url:
        video_id = url.split('modal_id=')[1].split('&')[0]
        if utils.is_number(video_id):
            return video_id
    else:
        return __extract_video_id(__get_redirect_url(url, proxy), proxy, retry=retry + 1)


