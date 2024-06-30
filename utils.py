import json
import os
import re

import yaml

# 配置文件路径
CONFIG_YAML_FILE = os.path.join(os.path.dirname(__file__), 'duck.yaml')

def read_yaml_key(key):
    """
    读取yaml配置
    :param key:
    :return:
    """
    with open(CONFIG_YAML_FILE, 'r', encoding='utf-8') as file:
        config_data = yaml.safe_load(file)
    keys = key.split('.')
    value = config_data
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return None
    return value

def save_yaml_key(key, value):
    """
    保存yaml配置
    :param key:
    :param value:
    :return:
    """
    try:
        with open(CONFIG_YAML_FILE, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)
    except yaml.YAMLError:
        config_data = {}

    if config_data is None:
        config_data = {}

    keys = key.split('.')
    nested_dict = config_data
    for k in keys[:-1]:
        if k not in nested_dict:
            nested_dict[k] = {}
        nested_dict = nested_dict[k]
    nested_dict[keys[-1]] = value

    with open(CONFIG_YAML_FILE, 'w', encoding='utf-8') as file:
        yaml.safe_dump(config_data, file, default_flow_style=False)


def extract_key_value(json_data, key_to_find):
    """
    从json数据中提取指定键的值
    :param json_data:
    :param key_to_find:
    :return:
    """
    # 递归函数来查找给定键的值
    def find_key(d, key):
        if isinstance(d, dict):
            for k, v in d.items():
                if k == key:
                    return v
                elif isinstance(v, (dict, list)):
                    result = find_key(v, key)
                    if result is not None:
                        return result
        elif isinstance(d, list):
            for item in d:
                result = find_key(item, key)
                if result is not None:
                    return result
        return None

    # 调用递归函数来查找给定键的值
    return find_key(json_data, key_to_find)


def extract_status_id(url):
    # 定义正则表达式模式，使用捕获组来提取数字部分
    regex = r"/status/(\d+)"
    # 使用 re.search 在字符串中查找模式
    match = re.search(regex, url)
    # 如果找到匹配项，返回第一个捕获组中的内容，否则返回 None
    return match.group(1) if match else None

def extract_ppx_id(url):
    # 定义正则表达式模式，使用捕获组来提取数字部分
    regex = r"/item/(\d+)"
    # 使用 re.search 在字符串中查找模式
    match = re.search(regex, url)
    # 如果找到匹配项，返回第一个捕获组中的内容，否则返回 None
    return match.group(1) if match else None


def is_empty(s):
    return s is None or s == ''

def is_url(url):
    return url.startswith('https://') or url.startswith('http://')


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def md5(s):
    import hashlib
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()

def fileType2Ext(fileType):
    if 'mp4' in fileType:
        return '.mp4'
    elif 'image' in fileType:
        return '.jpg'
    elif 'audio' in fileType:
        return '.mp3'
    elif 'gif' in fileType:
        return '.gif'
    elif 'document' in fileType:
        return '.doc'
    elif 'video' in fileType:
        return '.mp4'
    elif 'animated_gif' in fileType:
        return '.gif'
    else:
        return '.mp4'



# print(extract_status_id('https://x.com/tinger777/status/1805994426768224556'))
# print(extract_ppx_id('https://h5.pipix.com/item/7356873518186764585?app_id=1319&app=super&timestamp=1719566336&user_id=101282140452&carrier_region=&region=&language=&utm_source=weixin'))
