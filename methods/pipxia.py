import json
import re

import requests
import utils
from entity.Result import Result
from entity.Media import Media
from entity.MediaInfo import MediaInfo
from entity.Author import Author

__api_detail = 'https://ib-hl.snssdk.com/bds/cell/detail/?version_code=4.2.7&app_name=super&device_id=1988391945639406' \
        '&channel=App%20Store&resolution=1170*2532&aid=1319&last_channel=App%20Store&last_update_version_code=42691' \
        '&recommend_disable=0&update_version_code=42780&ac=WIFI&os_version=15.5&device_platform=iphone&iid' \
        '=805274026772804&device_type=iPhone%2012&cell_id={}&cell_type=1&api_version=1 '

__api_publish_list = 'https://api.pipix.com/bds/user/publish_list/?user_id={}&aid=1319&app_name=super&cursor={}'

__enable_proxy = utils.read_yaml_key('pipixia.proxy.enable')
__proxy_http = utils.read_yaml_key('proxy.http')
__proxy_https = utils.read_yaml_key('proxy.https')

def __get_redirect_url(url, proxy):
    response = requests.get(url, allow_redirects=False, proxies=proxy)
    return response.headers['Location']

def __extract_author(item):
    _author = item['author']
    _author_id = _author['id']
    _author_name = _author['name']
    _author_avatar = _author['avatar']['url_list'][0]['url']
    _author_url = _author['profile_schema']
    author = Author()
    author.setUserId(_author_id)
    author.setName(_author_name)
    author.setAvatar(_author_avatar)
    author.setUrl(_author_url)
    return author

def __extract_media(data, item, item_type, index=0):
    content = item['content']
    cover_url = utils.extract_key_value(data, 'cover')['url_list'][0]['url']
    url = None
    aspect_ratio = None
    if item_type == 1:
        url = utils.extract_key_value(data, 'multi_image')[index]['url_list'][0]['url']
        aspect_ratio = '{}:{}'.format(utils.extract_key_value(data, 'multi_image')[index]['width'],
                                      utils.extract_key_value(data, 'multi_image')[index]['height'])
    elif item_type == 2:
        url = utils.extract_key_value(data, 'video_high')['url_list'][index]['url']
        aspect_ratio = '{}:{}'.format(utils.extract_key_value(data, 'video_width'),
                                      utils.extract_key_value(data, 'video_height'))
    duration = utils.extract_key_value(data, 'duration')
    media = Media()
    media.setUrl(url)
    media.setTitle(item['share']['title'])
    media.setContent(content)
    media.setContentType('video/mp4')
    media.setCover(cover_url)
    if item_type == 1:
        media.setCover(url)
    media.setDuration(duration)
    media.setAspectRatio(aspect_ratio)
    return media

def __extract_detail(url, cell_id, data):
    if data['status_code'] != 0:
        return Result().Error('获取视频失败,原因:{}'.format(data['message']))
    item = data['data']['data']['item']
    """
    item_type
    1. 图片
    2. 视频
    """
    item_type = item['item_type']
    mediaInfo = MediaInfo()
    media = None
    media_list = []
    if item_type == 2:
        media = __extract_media(data, item, item_type)
        if utils.is_empty(media.getCover()) or utils.is_empty(media.getUrl()):
            return Result().Error('获取视频失败,原因:{}'.format(data['message']))
        media.setHref(url)
        media.setMediaId(cell_id)
        media.setIndex(len(media_list) - 1)
        media_list = [media]
    if item_type == 1:
        image_list = utils.extract_key_value(data, 'multi_image')
        index = 0
        for _item in image_list:
            media = __extract_media(data, item, item_type, index)
            if utils.is_empty(media.getCover()) or utils.is_empty(media.getUrl()):
                return Result().Error('获取图集失败,原因:{}'.format(data['message']))
            media.setHref(url)
            media.setMediaId(cell_id)
            media.setIndex(len(media_list) - 1)
            media_list.append(media)
            index = index + 1
    mediaInfo.setMediaList(media_list)
    mediaInfo.setAuthor(__extract_author(item))
    return Result().Success(message='获取成功', data=mediaInfo)

def get_video(url):
    proxy = __enable_proxy and None or {
        'http': __proxy_http,
        'https': __proxy_https
    }
    if 'item' not in url:
        url = __get_redirect_url(url, proxy)
    cell_id = utils.extract_ppx_id(url)
    if utils.is_empty(cell_id) and utils.is_number(cell_id):
        return Result().Error('获取cell_id失败')
    response = requests.get(__api_detail.format(cell_id), proxies=proxy)
    data = response.json()
    return __extract_detail(url, cell_id, data)



def __extract_user_media(data):
    if data['status_code'] != 0:
        return Result().Error('获取视频失败,原因:{}'.format(data['message']))
    data = data['data']
    media_data = data['data']
    cursor_data = data['cursor']
    cursor = ''
    if cursor_data['has_more']:
        cursor = cursor_data['loadmore_cursor']
    if media_data and len(media_data) > 0:
        author = __extract_author(media_data[0]['item'])
        mediaInfo = MediaInfo()
        media_list = []
        for _item in media_data:
            item = _item['item']
            item_type = item['item_type']
            if item_type == 2:
                media = __extract_media(_item, item, item_type)
                if utils.is_empty(media.getCover()) or utils.is_empty(media.getUrl()):
                    return Result().Error('获取视频失败,原因:{}'.format(data['message']))
                media.setHref('https://h5.pipix.com/item/{}?app_id=1319&app=super&timestamp=1721213617&user_id=101282140452&carrier_region=cn&region=cn&language=zh&utm_source=weixin'.format(item['item_id']))
                media.setMediaId(item['item_id'])
                media.setMediaId(item['item_id'])
                media.setIndex(len(media_list) - 1)
                media_list.append(media)
            if item_type == 1:
                image_list = utils.extract_key_value(_item, 'multi_image')
                index = 0
                for image_item in image_list:
                    media = __extract_media(_item, item, item_type, index)
                    if utils.is_empty(media.getCover()) or utils.is_empty(media.getUrl()):
                        return Result().Error('获取图集失败,原因:{}'.format(data['message']))
                    media.setHref('https://h5.pipix.com/item/{}?app_id=1319&app=super&timestamp=1721213617&user_id=101282140452&carrier_region=cn&region=cn&language=zh&utm_source=weixin'.format(item['item_id']))
                    media.setMediaId(item['item_id'])
                    media.setIndex(len(media_list) - 1)
                    media_list.append(media)
                    index = index + 1
        mediaInfo.setMediaList(media_list)
        mediaInfo.setAuthor(author)
        mediaInfo.setCursor(cursor)
        return Result().Success(message='获取成功', data=mediaInfo)
    return Result().Error('获取视频失败,原因:{}'.format(data['message']))


def get_user_media(url, cursor=''):
    proxy = __enable_proxy and None or {
        'http': __proxy_http,
        'https': __proxy_https
    }
    headers = {
        'x-vc-bdturing-sdk-version': '3.7.2.cn'
    }
    user_id = None
    if 'bds://user/profile?user_id=' not in url:
        result = get_video(url)
        if result['success']:
            user_id = result['data']['author']['user_id']
    elif 'bds://user/profile?user_id=' in url:
        # bds://user/profile?user_id=101282140452&zlink=https%3A%2F%2Fz.pipix.com
        user_id = url.split('user_id=')[1].split('&')[0]
    if utils.is_empty(user_id):
        return Result().Error('获取user_id失败')
    url = __api_publish_list.format(user_id, cursor)
    url = re.sub(r'{}|None', '', url)
    response = requests.get(url=url, proxies=proxy, headers=headers)
    data = response.json()
    return __extract_user_media(data)


