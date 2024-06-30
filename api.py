from methods import twitter, pipxia, downloader
import webview

class Api():

    def __init__(self):
        self.downloader = downloader.Downloader()


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
            print(obj)
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
