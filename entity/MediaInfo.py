import json

from entity.Author import Author


class MediaInfo:
    def __init__(self, author=None, media_list=None, cursor=None):
        # 发布者信息
        self.author = author
        # 视频数组
        self.media_list = media_list
        # 游标（该值仅在获取主页时使用）
        self.cursor = cursor

    def getAuthor(self):
        return self.author if self.author else Author()

    def getMediaList(self):
        return self.media_list if self.media_list else []

    def getCursor(self):
        return self.cursor if self.cursor else ''

    def setAuthor(self, author):
        self.author = author

    def setMediaList(self, media_list):
        self.media_list = media_list

    def setCursor(self, cursor):
        self.cursor = cursor

    def toString(self):
        return 'VideoInfo{author=' + self.getAuthor().toString() + ', media_list=' + str(
            self.getMediaList()) + ', cursor=' + self.getCursor() + '}'

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
