import os
import time
import re

import requests
import threading
import utils
import jsonpath



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
        self.download_path = None
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
        media_id = options['media_info']['media']['media_id']
        media_index = str(options['media_info']['media']['index'])
        task_id = utils.md5('{}_{}'.format(media_id, media_index))
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

    def remove_task(self, task_id):
        """
        移除任务
        :param task_id:
        :return:
        """
        self.lock.acquire()
        if task_id not in self.task_id_list:
            return {
                'success': False,
                'message': '任务不存在'
            }
        self.task_status[task_id]['status'] = -1
        self.task_status[task_id]['message'] = '任务取消'
        self.task_id_list.remove(task_id)
        self.lock.release()
        return  {
            'success': True,
            'message': '任务已取消'
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

    def __extract_keys(self, string):
        pattern = r"\$\{(.*?)\}"
        keys = re.findall(pattern, string)
        return keys

    def __format_path(self, suffix, options):
        """
        格式化下载地址
        :param suffix:
        :param options:
        :return:
        """
        # 时间戳
        timestamp = int(time.time())
        # download_path 支持 ${} 占位符，从 author 和 media_info 中获取，若获取到的值为空，则使用时间戳代替
        ex_path = utils.read_yaml_key('download.path')
        ex_path = ex_path.replace('${suffix}', suffix)
        # 获取download_path中所有占位符的key
        keys = self.__extract_keys(ex_path)
        # 替换
        for key in keys:
            value = jsonpath.jsonpath(options['media_info'], key)
            if value:
                ex_path = ex_path.replace('${' + key + '}', str(value[0]))
            else:
                ex_path = ex_path.replace('${' + key + '}', str(timestamp))
        # 取出ex_path中的文件名
        file_name = os.path.basename(ex_path)
        # 替换文件名中的特殊字符
        file_name = re.sub(r'[\\/:*?"<>|]', '_', file_name)
        ex_path = ex_path.replace(os.path.basename(ex_path), file_name)
        os.path.join(ex_path)
        return ex_path



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
                save_path = self.__format_path(suffix, options)
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

                print(f"Downloaded video {task_id} to {save_path}")
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








