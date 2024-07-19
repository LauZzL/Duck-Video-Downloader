import utils
from methods import twitter, pipxia, douyin, tiktok, zuiyou, pipigaoxiao, weishi, kuaishou
import downloader
import webview

class Api():

    def __init__(self):
        self.downloader = downloader.Downloader()


    def get_latest_release(self):
        """
        检查更新
        :return:
        """
        return utils.get_latest_release()

    def twitter_get_status_details(self, obj):
        """
        获取推特视频详情
        :param obj:
        :return:
        """
        try:
            return twitter.get_status_details(obj['url'])
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

    def twitter_get_user_media(self, obj):
        """
        获取推特用户媒体
        :param obj:
        :return:
        """
        try:
            return twitter.get_user_media(
                obj['url'],
                obj['cursor']
            )
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

    def pipixia_get_video(self, obj):
        """
        获取皮皮虾视频
        :param obj:
        :return:
        """
        try:
            return pipxia.get_video(
                obj['url']
            )
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

    def pipixia_get_user_media(self, obj):
        """
        获取皮皮虾主页视频、图集
        :param obj:
        :return:
        """
        try:
            return pipxia.get_user_media(
                obj['url'],
                obj['cursor']
            )
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }



    def douyin_get_video(self, obj):
        """
        获取抖音视频
        :param obj:
        :return:
        """
        try:
            return douyin.get_video(
                obj['url']
            )
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }


    def tiktok_get_video(self, obj):
        """
        获取tiktok视频
        :param obj:
        :return:
        """
        try:
            return tiktok.get_video(
                obj['url']
            )
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }


    def zuiyou_get_video(self, obj):
        """
        获取最右视频
        :param obj:
        :return:
        """
        try:
            return zuiyou.get_video(
                obj['url']
            )
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }


    def pipigaoxiao_get_video(self, obj):
        """
        获取皮皮搞笑视频
        :param obj:
        :return:
        """
        try:
            return pipigaoxiao.get_video(
                obj['url']
            )
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

    def weishi_get_video(self, obj):
        """
        获取微视视频
        :param obj:
        :return:
        """
        try:
            return weishi.get_video(
                obj['url']
            )
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

    def kuaishou_get_video(self, obj):
        """
        获取快手视频
        :param obj:
        :return:
        """
        try:
            return kuaishou.get_video(
                obj['url']
            )
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }


    def get_yaml(self):
        return {
            'success': True,
            'data': utils.get_yaml()
        }

    def save_yaml(self, obj):
        try:
            utils.save_yaml(obj)
            return {
                'success': True,
                'message': '保存成功'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

    def save_media_excel(self, obj):
        """
        保存媒体信息到excel
        :return:
        """
        try:
            path = webview.windows[0].create_file_dialog(
                webview.SAVE_DIALOG,
                directory='',
                save_filename=obj['filename']
            )
            utils.save_csv(obj, path)
            return {
                'success': True,
                'message': '保存成功'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }


    def http_download_add_task(self, obj):
        """
        添加下载任务
        :param obj
        :return:
        """
        try:
            return self.downloader.add_task(
                url=obj['url'],
                headers=obj['headers'],
                options=obj['options']
            )
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

    def http_download_get_all_task(self):
        """
        获取所有下载任务
        :return:
        """
        return self.downloader.get_all_task()


    def http_download_remove_task(self, obj):
        """
        移除下载任务
        :param obj:
        :return:
        """
        return self.downloader.remove_task(obj['task_id'])


    def get_readme(self):
        """
        获取README
        :return:
        """
        return {
            'success': True,
            'data': open('README.md', 'r', encoding='utf-8').read()
        }

    def create_player(self, obj):
        """
        创建播放器
        :param obj:
        :return:
        """
        webview.create_window("Player", obj['url'], width=800, height=600, confirm_close=False)


