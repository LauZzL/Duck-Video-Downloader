import re

import requests
import utils

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

__api_user_profile_url = 'https://x.com/i/api/graphql/-0XdHI-mrHWBQd8-oLo1aA/ProfileSpotlightsQuery?variables=%7B%22screen_name%22%3A%22{}%22%7D'


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
        return {
            'success': False,
            'message': '请到设置填写推特对应的Cookie、Authorization、X-Csrf-Token'
        }
    if __enable_proxy:
        if utils.is_empty(__proxy_http) or utils.is_empty(__proxy_https):
            return {
                'success': False,
                'message': '请到设置填写代理'
            }
    return {
        'success': True
    }


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
        return {
            'success': False,
            'message': '获取视频信息失败，请检查是否正确填写了推特对应的Cookie、Authorization、X-Csrf-Token'
        }
    if 'data' not in response.json():
        return {
            'success': False,
            'message': '获取视频信息失败，请检查是否正确填写了推特对应的Cookie、Authorization、X-Csrf-Token'
        }
    return {
        'success': True
    }


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
        return {
            'success': False,
            'message': '请输入正确的推特链接'
        }
    url = __api_status_url.format(status_id)
    response = __generate_requests(url, 'GET')
    video_info = utils.extract_key_value(response.json(), 'video_info')
    flag = __check_response(response)
    if not flag['success']:
        return flag
    return {
        'success': True,
        'message': '获取视频信息成功',
        'data': video_info
    }


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
    instructions = utils.extract_key_value(response.json(), 'instructions')
    if utils.is_empty(instructions):
        return {
            'success': False,
            'message': '获取失败：{}'.format(utils.extract_key_value(response.json(), 'message'))
        }
    if len(instructions) < 2:
        return {
            'success': False,
            'message': '获取结束，该用户主页媒体已全部获取完毕'
        }
    entries = instructions[len(instructions) - 1]['entries']
    cursor = entries[len(entries) - 1]['content']['value']
    flag = __check_response(response)
    if not flag['success']:
        return flag
    __extract_item = utils.extract_key_value(response.json(), 'items')
    __module_item = utils.extract_key_value(response.json(), 'moduleItems')
    media_items = __extract_item is None and __module_item or __extract_item
    if utils.is_empty(media_items):
        return {
            'success': False,
            'message': '获取失败：{}'.format(utils.extract_key_value(response.json(), 'message'))
        }
    data = []
    for media_item in media_items:
        item = utils.extract_key_value(media_item, 'tweet')
        if item is None:
            item = media_item['item']['itemContent']['tweet_results']['result']
        # 帖子ID
        rest_id = item['rest_id']
        medias = []
        # 帖子的所有媒体信息
        media = item['legacy']['entities']['media']
        for i in media:
            m_type = i['type']
            m_url = i['media_url_https']
            # 判断类型
            if m_type == 'video':
                # 获取最高码率
                m_url = i['video_info']['variants'][3]['url']
            if m_type == 'animated_gif':
                m_url = i['video_info']['variants'][0]['url']
            medias.append({
                'url': m_url,
                'type': m_type
            })
        data.append({
            'href': 'https://x.com/{}/status/{}'.format(legacy['screen_name'], rest_id),
            'medias': medias,
        })

    return {
        'success': True,
        'message': '获取用户media成功',
        'data': data,
        'legacy': legacy,
        'cursor': cursor
    }
