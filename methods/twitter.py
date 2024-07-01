import json
import re

import requests
import utils
from entity.Result import Result
from entity.Media import Media
from entity.MediaInfo import MediaInfo
from entity.Author import Author


TWITTER_BASE_URL = 'https://twitter.com/{}'

__api_status_url = 'https://x.com/i/api/graphql/VwKJcAd7zqlBOitPLUrB8A/TweetDetail?variables=%7B%22focalTweetId%22%3A%22{' \
        '}%22%2C%22with_rux_injections%22%3Afalse%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue' \
        '%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withBirdwatchNotes%22%3Atrue%2C%22withVoice%22' \
        '%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22rweb_tipjar_consumption_enabled%22%3Atrue%2C' \
        '%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse' \
        '%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C' \
        '%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C' \
        '%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C' \
        '%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C' \
        '%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C' \
        '%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue' \
        '%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C' \
        '%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C' \
        '%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled' \
        '%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C' \
        '%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C' \
        '%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C' \
        '%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C' \
        '%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse' \
        '%7D&fieldToggles=%7B%22withArticleRichContentState%22%3Atrue%2C%22withArticlePlainText%22%3Afalse%2C' \
        '%22withGrokAnalyze%22%3Afalse%7D '

__api_user_profile_url = ('https://x.com/i/api/graphql/xmU6X_CKVnQ5lSrCbAmJsg/UserByScreenName?variables=%7B'
                          '%22screen_name%22%3A%22{'
                          '}%22%2C%22withSafetyModeUserFields%22%3Atrue%7D&features=%7B'
                          '%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22'
                          '%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C'
                          '%22verified_phone_label_enabled%22%3Afalse%2C'
                          '%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C'
                          '%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C'
                          '%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C'
                          '%22responsive_web_twitter_article_notes_tab_enabled%22%3Atrue%2C'
                          '%22subscriptions_feature_can_gift_premium%22%3Afalse%2C'
                          '%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C'
                          '%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C'
                          '%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D&fieldToggles=%7B'
                          '%22withAuxiliaryUserLabels%22%3Afalse%7D')


__api_user_media_url = 'https://x.com/i/api/graphql/MOLbHrtk8Ovu7DUNOLcXiA/UserMedia?variables=%7B%22userId%22%3A%22{' \
                       '}%22%2C%22count%22%3A{}%2C%22cursor%22%3A%22{' \
                       '}%22%2C%22includePromotedContent%22%3Afalse%2C%22withClientEventToken%22%3Afalse%2C' \
                       '%22withBirdwatchNotes%22%3Afalse%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D' \
                       '&features=%7B%22rweb_tipjar_consumption_enabled%22%3Atrue%2C' \
                       '%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C' \
                       '%22verified_phone_label_enabled%22%3Afalse%2C' \
                       '%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C' \
                       '%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C' \
                       '%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C' \
                       '%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C' \
                       '%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22articles_preview_enabled%22' \
                       '%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C' \
                       '%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C' \
                       '%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C' \
                       '%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled' \
                       '%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C' \
                       '%22tweet_awards_web_tipping_enabled%22%3Afalse%2C' \
                       '%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C' \
                       '%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22' \
                       '%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22' \
                       '%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C' \
                       '%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C' \
                       '%22longform_notetweets_inline_media_enabled%22%3Atrue%2C' \
                       '%22responsive_web_enhance_cards_enabled%22%3Afalse%7D&fieldToggles=%7B%22withArticlePlainText' \
                       '%22%3Afalse%7D '

__cookie = utils.read_yaml_key('twitter.cookie')
__media_count = utils.is_empty(utils.read_yaml_key('twitter.media.count')) and 20 or int(utils.read_yaml_key('twitter.media.count'))
__authorization = utils.read_yaml_key('twitter.authorization')
__x_csrf_token = utils.read_yaml_key('twitter.x-csrf-token')
__proxy_http = utils.read_yaml_key('proxy.http')
__proxy_https = utils.read_yaml_key('proxy.https')
__enable_proxy = utils.read_yaml_key('twitter.proxy.enable')


def __checkParam():
    if utils.is_empty(__cookie) or utils.is_empty(__authorization) or utils.is_empty(__x_csrf_token):
        return Result().Error('请到设置填写推特对应的Cookie、Authorization、X-Csrf-Token')
    if __enable_proxy:
        if utils.is_empty(__proxy_http) or utils.is_empty(__proxy_https):
            return Result().Error('请到设置填写代理')
    return Result().Success(None, None)



def __generate_requests(api, method='GET', **kwargs):
    headers = {
        'Cookie': __cookie,
        'Authorization': __authorization,
        'X-Csrf-Token': __x_csrf_token
    }
    proxy = __enable_proxy and None or {
        'http': __proxy_http,
        'https': __proxy_https
    }
    for key, value in kwargs.items():
        api = api.format(**{key: value})
    return requests.request(method, api, headers=headers, data={}, proxies=proxy, verify=False)

def __check_response(response):
    if utils.is_empty(response.text):
        return Result().Error('获取视频信息失败，请检查是否正确填写了推特对应的Cookie、Authorization、X-Csrf-Token')
    if 'data' not in response.json():
        return Result().Error('获取视频信息失败，错误原因：{}'.format(utils.extract_key_value(response.json(), 'message')))
    return Result().Success(None, None)


def __extract_details(url, status_id, data):
    instructions = data['data']['threaded_conversation_with_injections_v2']
    content = None
    for instruction in instructions['instructions']:
        entries = instruction['entries']
        if utils.is_empty(entries):
            continue
        for entry in entries:
            entry_id = entry['entryId']
            if not utils.is_empty(entry_id) and status_id in entry_id:
                content = entry['content']
                break
        if not utils.is_empty(content):
            break
    if utils.is_empty(content):
        return Result().Error('获取视频信息失败，错误原因：{}'.format(utils.extract_key_value(data, 'message')))
    contentResult = content['itemContent']['tweet_results']['result']
    # 提取到了对应的内容
    mediaInfo = MediaInfo()
    # 获取author信息
    author_legacy = contentResult['core']['user_results']['result']['legacy']
    author_name = author_legacy['name']
    author_id = author_legacy['screen_name']
    author_avatar = author_legacy['profile_image_url_https']
    author_url = TWITTER_BASE_URL.format(author_id)
    author = Author(name=author_name, url=author_url, avatar=author_avatar, user_id=author_id)
    mediaInfo.setAuthor(author)
    # 获取video信息
    video_legacy = contentResult['legacy']
    video_content = video_legacy['full_text']
    # 获取media
    medias = video_legacy['extended_entities']['media']
    media_list = []
    for media in medias:
        vi = media['video_info']
        media_videos = vi['variants']
        duration = vi['duration_millis']
        aspect_ratio = '{}:{}'.format(vi['aspect_ratio'][0], vi['aspect_ratio'][1])
        media_cover = media['media_url_https']
        for media_video in media_videos:
            mediaEntry = Media()
            media_video_url = media_video['url']
            if 'bitrate' in media_video:
                media_video_bitrate = media_video['bitrate']
                mediaEntry.setBitrate(media_video_bitrate)
            media_video_content_type = media_video['content_type']
            mediaEntry.setUrl(media_video_url)
            mediaEntry.setHref(url)
            mediaEntry.setContent(video_content)
            mediaEntry.setMediaId(status_id)
            mediaEntry.setContentType(media_video_content_type)
            mediaEntry.setCover(media_cover)
            mediaEntry.setDuration(duration)
            mediaEntry.setAspectRatio(aspect_ratio)
            mediaEntry.setIndex(len(media_list))
            media_list.append(mediaEntry)
    mediaInfo.setMediaList(media_list)
    return Result().Success(message='获取成功', data=mediaInfo)


def get_status_details(url):
    """
    获取帖子视频信息（仅限正文包含媒体信息的帖子）
    :param url:
    :return:
    """
    flag = __checkParam()
    if not flag['success']:
        return flag
    status_id = utils.extract_status_id(url)
    if utils.is_empty(status_id):
        return Result().Error('请输入正确的推特链接')
    req_url = __api_status_url.format(status_id)
    response = __generate_requests(req_url, 'GET')
    flag = __check_response(response)
    if not flag['success']:
        return flag
    data = response.json()
    return __extract_details(url, status_id, data)


def __get_user_profile(url):
    """
    获取用户信息
    :param url: 该值为用户主页链接 格式为 https://x.com/xxxxxxx
    :return:
    """
    flag = __checkParam()
    if not flag['success']:
        return flag
    username = url.split('/')[-1]
    url = __api_user_profile_url.format(username)
    response = __generate_requests(url, 'GET')
    data = response.json()
    flag = __check_response(response)
    if not flag['success']:
        return flag
    return {
        'success': True,
        'message': '获取用户信息成功',
        'data': {
            'user_id': utils.extract_key_value(response.json(), 'rest_id'),
            'legacy': utils.extract_key_value(response.json(), 'legacy')
        }
    }


def __extract_user_media(url, legacy, data):
    instructions = utils.extract_key_value(data, 'instructions')
    if utils.is_empty(instructions):
        return Result().Error('获取失败：{}'.format(utils.extract_key_value(data, 'message')))
    timelineAddEntries = None
    # 获取media列表和cursor
    for instruction in instructions:
        if 'type' in instruction and 'TimelineAddEntries' == instruction['type']:
            timelineAddEntries = instruction
            break
    # 获取cursor
    entries = timelineAddEntries['entries']
    cursor = entries[len(entries) - 1]['content']['value']
    moduleItems = utils.extract_key_value(data, 'moduleItems') is None and utils.extract_key_value(data, 'items') or utils.extract_key_value(data, 'moduleItems')
    if utils.is_empty(moduleItems) and utils.is_empty(timelineAddEntries):
        return Result().Error('获取失败：{}'.format(utils.extract_key_value(data, 'message')))
    elif not utils.is_empty(timelineAddEntries) is None:
        return Result().Error('主页以获取到全部内容')
    mediaInfo = MediaInfo()
    # 设置游标
    mediaInfo.setCursor(cursor)
    # 获取作者信息
    author_name = legacy['name']
    author_id = legacy['screen_name']
    author_cover = legacy['profile_image_url_https']
    author = Author()
    author.setName(author_name)
    author.setUrl(TWITTER_BASE_URL.format(author_id))
    author.setUserId(author_id)
    author.setAvatar(author_cover)
    mediaInfo.setAuthor(author)
    media_list = []
    # 遍历所有帖子
    for module in moduleItems:
        # 获取帖子信息
        tweet = utils.extract_key_value(module, 'tweet')
        if tweet is None:
            tweet = module['item']['itemContent']['tweet_results']['result']
        # 帖子legacy信息
        media_legacy = tweet['legacy']
        # 帖子ID
        media_id = tweet['rest_id']
        # 帖子正文
        content = media_legacy['full_text']
        href = TWITTER_BASE_URL.format('status/{}'.format(media_id))
        # 帖子的所有媒体信息
        medias = media_legacy['entities']['media']
        for media in medias:
            mediaEntry = Media()
            content_type = media['type']
            media_url = media['media_url_https']
            mediaEntry.setCover(media_url)
            # 当存在该值时，代表media不是一个图片媒体
            if 'original_info' in media:
                aspect_ratio = '{}:{}'.format(media['original_info']['width'], media['original_info']['height'])
                mediaEntry.setAspectRatio(aspect_ratio)
            if 'video_info' in media:
                # 最高品质
                media_variants = media['video_info']['variants']
                media_url = media_variants[len(media_variants) - 1]['url']
                media_bitrate = media_variants[len(media_variants) - 1]['bitrate']
                if 'duration_millis' in media['video_info']:
                    media_duration = media['video_info']['duration_millis']
                    mediaEntry.setDuration(media_duration)
                mediaEntry.setBitrate(media_bitrate)
            mediaEntry.setUrl(media_url)
            mediaEntry.setMediaId(media_id)
            mediaEntry.setContentType(content_type)
            mediaEntry.setContent(content)
            mediaEntry.setHref(href)
            mediaEntry.setIndex(len(media_list))
            media_list.append(mediaEntry)
    mediaInfo.setMediaList(media_list)
    return Result().Success(message='获取成功', data=mediaInfo)

def get_user_media(url, cursor=''):
    """
    获取用户主页media
    :param url: 该值为用户主页链接 格式为 https://x.com/xxxxxxx
    :param cursor: 游标，每个用户首次获取不需要，若本次获取完且并未获取所有则会返回游标信息用于从本次结束的地方继续获取
    :return:
    """
    flag = __checkParam()
    if not flag['success']:
        return flag
    flag = __get_user_profile(url)
    if not flag['success']:
        return flag
    user_id = flag['data']['user_id']
    legacy = flag['data']['legacy']
    url = (__api_user_media_url.format(user_id, __media_count, cursor))
    url = re.sub(r'{}|None', '', url)
    response = __generate_requests(url, 'GET')
    flag = __check_response(response)
    if not flag['success']:
        return flag
    data = response.json()
    return __extract_user_media(url, legacy, data)
