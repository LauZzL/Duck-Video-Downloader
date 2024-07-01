import json


class Author:
    def __init__(self, name=None, url=None, avatar=None, user_id=None):
        # 作者名称
        self.name = name
        # 作者主页
        self.url = url
        # 作者头像
        self.avatar = avatar
        # 作者id
        self.user_id = user_id

    def getName(self):
        return self.name if self.name else ''

    def getUrl(self):
        return self.url if self.url else ''

    def getAvatar(self):
        return self.avatar if self.avatar else ''

    def getUserId(self):
        return self.user_id if self.user_id else ''

    def setName(self, name):
        self.name = name

    def setUrl(self, url):
        self.url = url

    def setAvatar(self, avatar):
        self.avatar = avatar

    def setUserId(self, user_id):
        self.user_id = user_id

    def toString(self):
        return 'Author{name=' + self.getName() + ', url=' + self.getUrl() + ', avatar=' + self.getAvatar() + ', user_id=' + self.getUserId() + '}'

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)

