import json


class Media:
    def __init__(self, url=None, href=None, title=None, content=None, media_id=None, content_type=None, bitrate=None, cover=None, duration=None, aspect_ratio=None, index=0):
        # 视频地址
        self.url = url
        # href
        self.href = href
        # 视频标题
        self.title = title
        # 视频正文
        self.content = content
        # media_id
        self.media_id = media_id
        # 视频类型
        self.content_type = content_type
        # 视频码率
        self.bitrate = bitrate
        # 封面
        self.cover = cover
        # 持续时长
        self.duration = duration
        # 分辨率
        self.aspect_ratio = aspect_ratio
        # index
        self.index = index

    def getUrl(self):
        return self.url if self.url else ''

    def getHref(self):
        return self.href if self.href else ''

    def getTitle(self):
        return self.title if self.title else ''

    def getContent(self):
        return self.content if self.content else ''

    def getMediaId(self):
        return self.media_id if self.media_id else ''

    def getContentType(self):
        return self.content_type if self.content_type else ''

    def getBitrate(self):
        return self.bitrate if self.bitrate else ''

    def getCover(self):
        return self.cover if self.cover else ''

    def getDuration(self):
        return self.duration if self.duration else ''

    def getAspectRatio(self):
        return self.aspect_ratio if self.aspect_ratio else ''

    def getIndex(self):
        return self.index if self.index else 0

    def setUrl(self, url):
        self.url = url

    def setHref(self, href):
        self.href = href

    def setMediaId(self, media_id):
        self.media_id = media_id

    def setTitle(self, title):
        self.title = title

    def setContent(self, content):
        self.content = content

    def setContentType(self, content_type):
        self.content_type = content_type

    def setBitrate(self, bitrate):
        self.bitrate = bitrate

    def setCover(self, cover):
        self.cover = cover

    def setDuration(self, duration):
        self.duration = duration

    def setAspectRatio(self, aspect_ratio):
        self.aspect_ratio = aspect_ratio

    def setIndex(self, index):
        self.index = index

    def toString(self):
        return 'Video{url=' + self.getUrl() + ', href=' + self.getHref() + ', title=' + self.getTitle() + ', content=' + self.getContent() + ', media_id=' + self.getMediaId() + ', content_type=' + self.getContentType() + ', bitrate=' + self.getBitrate() + ', cover=' + self.getCover() + ', duration=' + self.getDuration() + ', aspect_ratio=' + self.getAspectRatio() + ', index=' + self.getIndex() + '}'

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)



