#_*_coding: utf-8_*_

import requests
import threading
import telepot
import asyncio
import os, unittest, time, datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.options import Options
from pyyoutube import Data

token = os.environ.get('BOT_TOKEN')
bot = telepot.Bot(token)
             

def START(msg,chat_id):
    if msg == "/start":
        bot.sendMessage(chat_id, "Hi ! \nI am a bot to listing youtube channel videos urls, just send me a youtube channel link.")
    else:
        url = f"{msg}"
        try:
            chrome_options = Options()
            chrome_options.add_argument("--user-data-dir=chrome-data")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
            driver.get(url)
            links = driver.find_elements_by_xpath('//*[@id="video-title"]')
            MESSAGE = ''
            COUNT = 0      
            for link in links:
                result = link.get_attribute('href')
                yt = Data(f"{result}")
                title = yt.title # for more values, see https://github.com/Soebb/PyYouTube#get-videos-data
                COUNT+=1
                MESSAGE += f"{COUNT}. [{title}]({result})\n\n"
            bot.sendMessage(chat_id, MESSAGE, parse_mode='markdown', disable_web_page_preview=True)
        except Exception as e:
            print(e)
            bot.sendMessage(chat_id, f"Error: {e}")
                       
tokenurl = f'https://api.telegram.org/bot{token}'
Update = tokenurl+"/getUpdates"


def UPDATE():
    MESSAGES = requests.get(Update).json()
    return MESSAGES['result']


while 1:
    if threading.activeCount()-1 < 15:
        try:
            for message in UPDATE():
                offset = message['update_id']+1
                offset = Update+f"?offset={offset}"
                offset = requests.post(offset)
                msg = message['message']['text']
                chat_id = message['message']['from']['id']
                thread = threading.Thread(target=START,args=(msg,chat_id))
                thread.start()
        except:
            pass
