import webview
import api
import urllib3

urllib3.disable_warnings()

# 渲染地址
RENDERER_URL = "http://127.0.0.1:5173/"
def expose():
    webview.windows[0].evaluate_js('window.duck = window.pywebview.api;console.info("started")')


def create_window():
    webview.create_window(
        title="Duck Video Downloader - https://github.com/LauZzL/duck-video-downloader",
        url=RENDERER_URL,
        width=800,
        height=600,
        min_size=(800, 600),
        js_api=api.Api(),
        confirm_close=True,
    )
    webview.start(expose, debug=True)



if __name__ == '__main__':
    create_window()
