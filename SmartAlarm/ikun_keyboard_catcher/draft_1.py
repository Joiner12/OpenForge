from pynput.keyboard import Controller, Listener
import time
import threading


def function():
    keyboard = Controller()

    while True:
        if not paused:
            print("running")
        time.sleep(0.1)


def on_press(key):
    global paused
    global thread

    if "f3" in str(key):
        paused = not paused
        if thread is None:
            # run long-running `function` in separated thread
            thread = threading.Thread(target=function)
            thread.start()


# global variables with default values at star
paused = True
thread = None

with Listener(on_press=on_press) as listener:
    listener.join()