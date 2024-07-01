import json


class Result:
    def __init__(self, success=False, message=None, data=None):
        self.success = success
        self.message = message
        self.data = data

    def getSuccess(self):
        return self.success

    def getMessage(self):
        return self.message if self.message is not None else ''

    def getData(self):
        return self.data if self.data is not None else {}

    def setSuccess(self, success):
        self.success = success

    def setMessage(self, message):
        self.message = message

    def setData(self, data):
        self.data = data

    def Error(self, message):
        self.success = False
        self.message = message
        return self.toJson()

    def Success(self, data, message):
        self.success = True
        self.data = data
        self.message = message
        return self.toJson()

    def toString(self):
        return 'Result{success=' + str(self.getSuccess()) + ', message=' + self.getMessage() + ', data=' + str(self.getData()) + '}'

    def toJson(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False))


