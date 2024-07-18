import json
import re

import requests
import utils
from entity.Result import Result
from entity.Media import Media
from entity.MediaInfo import MediaInfo
from entity.Author import Author


__enable_proxy = utils.read_yaml_key('tiktok.proxy.enable')
__proxy_http = utils.read_yaml_key('proxy.http')
__proxy_https = utils.read_yaml_key('proxy.https')


__headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

def __get_redirect_url(url, proxy):
    response = requests.get(url, allow_redirects=False, proxies=proxy)
    return response.headers['Location']


def __extract_detail(response, href):
    cookie = response.cookies.get_dict()
    # 下载视频需要此cookie，否则会403
    options = {
        'cookie': cookie
    }
    searcher = re.compile('webapp.video-detail":(.*?),"webapp.a-b":')
    search_data = searcher.findall(response.text)
    if utils.is_empty(search_data) or len(search_data) == 0:
        return Result().Error('视频信息获取失败')
    mediaInfo = MediaInfo()
    json_data = json.loads(search_data[0])
    # itemInfo.itemStruct.desc
    content = json_data['itemInfo']['itemStruct']['desc']
    # itemInfo.itemStruct.id
    media_id = json_data['itemInfo']['itemStruct']['id']
    """
    提取作者信息
    """
    # itemInfo.itemStruct.author
    authorInfo = json_data['itemInfo']['itemStruct']['author']
    author = Author(
        name=authorInfo['uniqueId'],
        url='https://www.tiktok.com/@{}'.format(authorInfo['uniqueId']),
        avatar=authorInfo['avatarLarger'],
        user_id=authorInfo['id']
    )
    mediaInfo.setAuthor(author)
    """
    提取媒体
    """
    # itemInfo.itemStruct.video
    videoInfo = json_data['itemInfo']['itemStruct']['video']
    aspect_ratio = '{}:{}'.format(videoInfo['height'], videoInfo['width'])
    duration = videoInfo['duration']
    cover = videoInfo['cover']
    media_list = []
    medias = videoInfo['bitrateInfo']
    for item in medias:
        media = Media()
        bitrate = item['Bitrate']
        url = item['PlayAddr']['UrlList'][0]
        media.setUrl(url)
        media.setHref(href)
        media.setBitrate(bitrate)
        media.setAspectRatio(aspect_ratio)
        media.setDuration(duration)
        media.setMediaId(media_id)
        media.setContent(content)
        media.setCover(cover)
        media.setOptions(options)
        media.setIndex(len(media_list))
        media_list.append(media)
    mediaInfo.setMediaList(media_list)
    return Result().Success(mediaInfo, '视频信息获取成功')



def get_video(url):
    proxy = __enable_proxy and None or {
        'http': __proxy_http,
        'https': __proxy_https
    }
    if 'video/' in url:
        pass
    else:
        url = __get_redirect_url(url, proxy)
    response = requests.get(url, headers=__headers, proxies=proxy, verify=False)
    if response.status_code == 200 and 'webapp.video-detail' in response.text:
        return __extract_detail(response, url)
    return Result().Error('视频解析失败')




