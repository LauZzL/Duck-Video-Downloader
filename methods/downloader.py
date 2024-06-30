import os
import time

import requests
import threading
import utils


class Downloader:
    def __init__(self):
        """
        初始化
        :return:
        """
        self.thread_list = []
        self.task_id_list = []
        # 任务状态，0 未开始，1 下载中，2 下载完成，3 下载失败
        self.status_message = {
            0: '未开始',
            1: '下载中',
            2: '下载完成',
            3: '下载失败',
            -1: '任务取消'
        }
        self.task_status = {}
        self.proxy = {
            "http": utils.read_yaml_key('proxy.http'),
            "https": utils.read_yaml_key('proxy.https')
        }
        self.download_path = utils.read_yaml_key('download.path')
        self.lock = threading.BoundedSemaphore(
            utils.is_empty(utils.read_yaml_key('download.thread')) and 10 or utils.read_yaml_key('download.thread')
        )
        pass

    def add_task(self, url, headers, options):
        """
        添加下载任务
        :param url:
        :param headers:
        :param options:
        :return:
        """
        self.lock.acquire()
        task_id = utils.md5(url)
        if task_id in self.task_id_list:
            return {
                'success': False,
                'message': '任务已存在'
            }
        self.task_id_list.append(task_id)
        thread = threading.Thread(target=self.__download, args=(task_id,))
        self.task_status[task_id] = {
            'url': url,
            'status': 0,
            'message': self.status_message[0],
            'total_size': 0,
            'downloaded_size': 0,
            'speed': 0,
            'headers': headers,
            'options': options,
            'thread': thread
        }
        self.thread_list.append(thread)
        thread.start()
        self.lock.release()
        return {
            'success': True,
            'task_id': task_id,
            'message': '任务已添加'
        }

    def get_task_status(self, task_id):
        """
        获取任务状态
        :param task_id:
        :return:
        """
        task_status = self.task_status[task_id]
        task_status['thread'] = str(task_status['thread'])
        return {
            'success': True,
            'data': task_status,
        }

    def get_all_task(self):
        """
        获取所有任务状态
        :return:
        """
        task_status_list = []
        for task_id in self.task_id_list:
            task_status = self.task_status[task_id]
            task_status['thread'] = str(task_status['thread'])
            task_status['task_id'] = task_id
            task_status_list.append(task_status)
        return {
            'success': True,
            'data': task_status_list,
        }

    def __download(self, task_id):
        self.lock.acquire()
        task = self.task_status[task_id]
        thread = task['thread']
        if task['status'] == -1:
            self.thread_list.remove(thread)
            self.lock.release()
            return
        if task['status'] > 0:
            return
        url = task['url']
        options = task['options']
        headers = task['headers']
        proxy = options['enable_proxy'] and self.proxy or None
        start_time = time.time()
        self.task_status[task_id]['status'] = 1
        self.task_status[task_id]['message'] = self.status_message[1]
        try:
            stream = requests.get(url, headers=headers, proxies=proxy, stream=True)
            print('task {} start download!'.format(task_id))
            if stream.status_code == 200:
                # 获取文件类型
                file_type = stream.headers.get('Content-Type')
                # 文件类型转换为文件后缀
                suffix = utils.fileType2Ext(file_type)
                filename = task_id
                save_path = os.path.join(self.download_path, filename + suffix)
                print(save_path)
                # 创建文件夹
                if not os.path.exists(os.path.dirname(save_path)):
                    os.makedirs(os.path.dirname(save_path))
                total_size = int(stream.headers.get("Content-Length", 0))
                downloaded_size = 0
                with open(save_path, "wb") as f:
                    for chunk in stream.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            self.task_status[task_id]['downloaded_size'] = downloaded_size
                            self.task_status[task_id]['total_size'] = total_size
                            self.task_status[task_id]['speed'] = str(round(downloaded_size / (time.time() - start_time) / 1024, 2)) + 'KB/s'

                print(f"Downloaded video {filename} to {self.download_path}")
                self.task_status[task_id]['status'] = 2
                self.task_status[task_id]['message'] = self.status_message[2]
            else:
                print(f"Failed to download from {url}")
                self.task_status[task_id]['status'] = 3
                self.task_status[task_id]['message'] = self.status_message[3]
        except Exception as e:
            print(f"Error occurred while downloading from {url}: {e}")
            self.task_status[task_id]['status'] = 3
            self.task_status[task_id]['message'] = str(e)
        self.lock.release()








