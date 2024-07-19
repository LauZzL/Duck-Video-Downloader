import json

import requests
import utils
import re
from entity.Result import Result
from entity.Media import Media
from entity.MediaInfo import MediaInfo
from entity.Author import Author


__enable_proxy = utils.read_yaml_key('kuaishou.proxy.enable')
__proxy_http = utils.read_yaml_key('proxy.http')
__proxy_https = utils.read_yaml_key('proxy.https')

def __get_redirect_url(url, proxy):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36"
    }
    response = requests.get(url, allow_redirects=False, proxies=proxy, headers=headers)
    return response.headers['Location']

def __extract_data(href, photo_id, authorId, response):
    if 'VisionVideoDetailAuthor' not in response.text:
        return Result().Error('获取失败')
    searcher = re.compile('__APOLLO_STATE__=(.*?);')
    data = searcher.findall(response.text)[0]
    if utils.is_empty(data):
        return Result().Error('获取失败')
    data = json.loads(data)
    data = data['defaultClient']
    mediaInfo = MediaInfo()
    media_list = []
    """
    获取author信息
    """
    author_path = 'VisionVideoDetailAuthor:{}'.format(authorId)
    author = Author(
        name=data[f'{author_path}']['name'],
        url='https://www.kuaishou.com/profile/{}'.format(data[f'{author_path}']['id']),
        avatar=data[f'{author_path}']['headerUrl'],
        user_id=data[f'{author_path}']['id']
    )
    mediaInfo.setAuthor(author)
    """
    获取媒体信息
    """
    photo_path = 'VisionVideoDetailPhoto:{}'.format(photo_id)
    content = data[f'{photo_path}']['caption']
    cover = data[f'{photo_path}']['coverUrl']
    url = data[f'{photo_path}']['photoH265Url']
    videoResource = data[f'{photo_path}']['videoResource']
    media_id = videoResource['json']['h264']['videoId']
    representation = videoResource['json']['h264']['adaptationSet'][0]['representation'][0]
    duration = videoResource['json']['h264']['adaptationSet'][0]['duration']
    aspect_ratio = '{}:{}'.format(representation['width'], representation['height'])
    media = Media(
        url=url,
        href=href,
        content=content,
        media_id=media_id,
        cover=cover,
        duration=duration,
        aspect_ratio=aspect_ratio,
        index=len(media_list)
    )
    media_list.append(media)
    mediaInfo.setMediaList(media_list)
    return Result().Success(mediaInfo, '获取成功')


def get_video(url):
    proxy = __enable_proxy and None or {
        'http': __proxy_http,
        'https': __proxy_https
    }
    url = utils.extract_url(url)[0]
    if 'short-video' not in url:
        url = __get_redirect_url(url, proxy)
        if 'short-video' not in url:
            return Result().Error('url is not a kuaishou video url')
    photo_id = url.split('short-video/')[1].split('?')[0]
    authorId = url.split('authorId=')[1].split('&')[0]
    if utils.is_empty(photo_id) or utils.is_empty(authorId):
        return Result().Error('获取photo_id或author_id失败')
    """
    Host: www.kuaishou.com
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36
    """
    headers = {
        "Host": "www.kuaishou.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Upgrade-Insecure-Requests": "1"
    }
    response = requests.get(url, proxies=proxy, headers=headers)
    return __extract_data(url, photo_id, authorId, response)

