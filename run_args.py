from utils import get_arg_value


class RunArgs:
    def __init__(self, args):
        self.args = args

    def renderer_url(self):
        if '--dev' in self.args and 'app.py' in self.args:
            return "http://127.0.0.1:5173/"
        return "./dist/index.html"

    def dev_tools(self):
        if '--dev' in self.args:
            return True
        return False


    def shell_mode(self):
        if '--shell' in self.args:
            pass