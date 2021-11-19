## YT Channel Contents Lister
A Telegram bot to listing youtube channel videos urls.

## Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/samadii/YTChannelContentsList)


## Local Deploying

1. Clone the repo
   ```
   git clone https://github.com/samadii/YTChannelContentsList
   ```

2. Install [Google Chrome](https://support.google.com/chrome/answer/95346?hl=en&co=GENIE.Platform%3DDesktop) and [ChromeDriver](https://chromedriver.chromium.org/downloads).

3. Add ChromeDriver folder path to your System PATH environment variable.

4. Go to [this line](https://github.com/samadii/YTChannelContentsList/blob/master/main.py#L14) and add path where chromedriver is there.

5. Enter the directory
   ```
   cd YTChannelContentsList
   ```
  
6. Install all requirements using pip.
   ```
   pip3 install -r requirements.txt
   ```

7. Run the file
   ```
   python3 main.py
   ```
