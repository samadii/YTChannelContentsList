import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.options import Options
from pyyoutube import Data
from telethon import TelegramClient, events
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

print("Starting...")

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
            id = Data(f"{event.text}")
            input = f'https://youtube.com/channel/{id.id}/videos?view=0&sort=dd&shelfid=0'
        else:
            input = event.text + '/videos?view=0&sort=dd&shelfid=0'
        url = f"{input}"
        try:
            msg = await event.reply("`Processing...`")
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
                await msg.edit(MESSAGE)
        except Exception as e:
            await msg.edit(f"**ERROR**:\n`{e}`")
    
    
print("Bot has started.")
Bot.run_until_disconnected()
