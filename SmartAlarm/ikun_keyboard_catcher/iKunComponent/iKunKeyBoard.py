#-*- coding:utf-8 -*-
"""
    iKunMain中的组件类
"""
from pynput.keyboard import Listener, GlobalHotKeys, Key


## 键盘监听
class KeyBoardListener():

    def __init__(self, on_press_func, on_release_func, hot_keys_func_map=None):
        self.on_press = on_press_func
        self.on_release = on_release_func
        self.hot_key = hot_keys_func_map
        # 常规键盘按键
        self.listener = Listener(on_press=self.on_press,
                                 on_release=self.on_release)
        # 热键
        if hot_keys_func_map is not None:
            self.h = GlobalHotKeys(self.hot_key)
        else:
            self.h = None

    # 开启键盘监听
    def start_monitor(self):
        self.listener.start()
        # 开启热键监控
        if self.hot_key is not None:
            self.h.start()

    # 停止键盘监听
    def hotkey_stop_monitor(self):
        self.listener.stop()
        if self.h is not None:
            self.h.stop()


def on_activate_h():
    print('<ctrl>+<alt>+h pressed')


def on_activate_i():
    print('<ctrl>+<alt>+i pressed')


def on_activate_esc():
    print('<ctrl>+<alt>+j pressed')
    raise Exception


# with keyboard.GlobalHotKeys({
#         '<ctrl>+<alt>+h': on_activate_h,
#         '<ctrl>+<alt>+i': on_activate_i}) as h:
#     h.join()


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))


def on_release(key):
    if key == Key.esc:
        # Stop listener
        print('{0} released'.format(key))
        return False


if __name__ == "__main__":
    print("fuc")
    if True:
        kl = KeyBoardListener(on_press_func=on_press,
                              on_release_func=on_release,
                              hot_keys_func_map={
                                  '<ctrl>+<alt>+h': on_activate_h,
                                  '<ctrl>+<alt>+i': on_activate_i,
                                  '<ctrl>+<alt>+j': on_activate_esc
                              })
    else:
        kl = KeyBoardListener(on_press_func=on_press,
                              on_release_func=on_release,
                              hot_keys_func_map=None)
    kl.start_monitor()
