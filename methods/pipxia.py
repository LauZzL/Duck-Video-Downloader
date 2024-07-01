import requests
import utils
from entity.Result import Result
from entity.Media import Media
from entity.MediaInfo import MediaInfo
from entity.Author import Author

__api = 'https://ib-hl.snssdk.com/bds/cell/detail/?version_code=4.2.7&app_name=super&device_id=1988391945639406' \
        '&channel=App%20Store&resolution=1170*2532&aid=1319&last_channel=App%20Store&last_update_version_code=42691' \
        '&recommend_disable=0&update_version_code=42780&ac=WIFI&os_version=15.5&device_platform=iphone&iid' \
        '=805274026772804&device_type=iPhone%2012&cell_id={}&cell_type=1&api_version=1 '
__enable_proxy = utils.read_yaml_key('pipixia.proxy.enable')
__proxy_http = utils.read_yaml_key('proxy.http')
__proxy_https = utils.read_yaml_key('proxy.https')

def __get_redirect_url(url, proxy):
    response = requests.get(url, allow_redirects=False, proxies=proxy)
    return response.headers['Location']


def __extract_data(url, cell_id, data):
    if data['status_code'] != 0:
        return Result().Error('获取视频失败,原因:{}'.format(data['message']))
    item = data['data']['data']['item']
    content = item['content']
    _author = item['author']
    _author_id = _author['id']
    _author_name = _author['name']
    _author_avatar = _author['avatar']['url_list'][0]['url']
    cover_url = utils.extract_key_value(data, 'cover')['url_list'][0]['url']
    video_url = utils.extract_key_value(data, 'video_high')['url_list'][0]['url']
    duration = utils.extract_key_value(data, 'duration')
    aspect_ratio = '{}:{}'.format(utils.extract_key_value(data, 'video_width'), utils.extract_key_value(data, 'video_height'))
    if utils.is_empty(cover_url) or utils.is_empty(video_url):
        return Result().Error('获取视频失败,原因:{}'.format(data['message']))
    mediaInfo = MediaInfo()
    media = Media()
    media.setUrl(video_url)
    media.setHref(url)
    media.setTitle(utils.extract_key_value(data, 'title'))
    media.setContent(content)
    media.setMediaId(cell_id)
    media.setContentType('video/mp4')
    media.setCover(cover_url)
    media.setDuration(duration)
    media.setAspectRatio(aspect_ratio)
    media.setIndex(0)
    media_list = [media]
    mediaInfo.setMediaList(media_list)
    author = Author()
    author.setUserId(_author_id)
    author.setName(_author_name)
    author.setAvatar(_author_avatar)
    mediaInfo.setAuthor(author)
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
    response = requests.get(__api.format(cell_id), proxies=proxy)
    data = response.json()
    return __extract_data(url, cell_id, data)


