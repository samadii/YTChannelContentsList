import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from py_youtube import Data
from telethon import TelegramClient, events
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)
print("Starting...")

# system path to chromedriver.exe
CHROMEDRIVER_PATH = r" "

USE_HEROKU = os.environ.get("USE_HEROKU")
api_id = int(os.environ.get("API_ID", 12345))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
try:
    Bot = TelegramClient("Bot", api_id, api_hash).start(bot_token=bot_token)
except Exception as e:
    print(e)


@Bot.on(events.NewMessage(incoming=True, pattern="^/start"))
async def start_(event):
    await event.reply("**Hi !**\n\nI am a bot to listing youtube channel videos urls, just send me a youtube channel link.")


@Bot.on(events.NewMessage(incoming=True))
async def send(event):
    if event.text and not event.text.startswith("/") and not event.document:
        if "/c/" in event.text:
            url = event.text + '/videos'
        elif "/channel/" in event.text:
            url = event.text + '/videos?view=0&sort=dd&shelfid=0'
        else:
            return await event.reply("`Not a YouTube channel URL!`")
        msg = await event.reply("`Processing...`")
        try:
            if USE_HEROKU == "TRUE":
                chrome_options = Options()
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.headless = True
                chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome"
                driver = webdriver.Chrome(executable_path="/app/.chromedriver/bin/chromedriver", options=chrome_options)
                driver.get(url)
                links = driver.find_elements_by_xpath('//*[@id="video-title"]')
            else:
                chrome_options = webdriver.ChromeOptions()
                ser = Service(CHROMEDRIVER_PATH)
                driver = webdriver.Chrome(service=ser, options=chrome_options)
                driver.get(url)
                links = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
            MESSAGE = ''
            COUNT = 0
            for link in links:
                result = link.get_attribute('href')
                yt = Data(result)
                title = yt.title()
                COUNT+=1
                MESSAGE += f"{COUNT}. [{title}]({result})\n\n"
                await msg.edit(MESSAGE)
        except Exception as e:
            await msg.edit(f"**ERROR**:\n`{e}`")
    
    
print("Bot has started.")
Bot.run_until_disconnected()
