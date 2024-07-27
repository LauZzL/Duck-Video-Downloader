import webview
import api
import urllib3
import sys
from run_args import RunArgs

urllib3.disable_warnings()

ra = RunArgs(sys.argv)

# 渲染地址
RENDERER_URL = ra.renderer_url()
# 开发者工具
DEV_TOOLS = ra.dev_tools()
APP_VERSION = "v1.1.1"

def expose():
    webview.windows[0].evaluate_js('window.duck = window.pywebview.api;window.duck.APP_VERSION="{}";console.info("started")'.format(APP_VERSION))


def create_window():
    webview.create_window(
        title="Duck Video Downloader {}".format(APP_VERSION),
        url=RENDERER_URL,
        width=800,
        height=600,
        min_size=(800, 600),
        js_api=api.Api(),
        confirm_close=True,
    )
    webview.start(expose, debug=DEV_TOOLS)



if __name__ == '__main__':
    create_window()
