from selenium import webdriver
import time
from bs4 import BeautifulSoup

# options = webdriver.ChromeOptions()
# prefs = {'profile.default_content_setting_values': { 'images': 2,'plugins': 2, 'popups': 2, 'geolocation': 2,
#                             'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
#                             'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
#                             'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
#                             'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
#                             'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
#                             'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
#                             'durable_storage': 2}}
# options.add_experimental_option('prefs', prefs)


# options.add_argument('--disk-cache-size')
# options.add_argument('--media-cache-size')
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument('--no-sandbox')

import pandas as pd
from parse import prs_twtr
cols=["tweet","data","reply","commenti","retweet","like" ]
base=pd.DataFrame([],columns=cols)
PATH= "/Users/danilofiumi/Downloads/chromedriver 2"

# ls_account=["ForbesCrypto","VitalikButerin","BTCTN","bitcoincom","BitcoinMagazine","TheBitcoinConf","SatoshiLite","blockchain"]
ls_account=["CoinMarketCap"]
dt_since = "2020-01-01"
dt_until = "2021-01-01"

for account in ls_account:

    # Access to Twitter

    url = "https://twitter.com/search?q=From%3A" + account + "%20since%3A"+dt_since+"%20until%3A"+dt_until+ "&src=typed_query&f=live"


    driver=webdriver.Chrome(executable_path=PATH)
    # driver.delete_all_cookies()
    driver.get(url)
    time.sleep(5)

    while True:
        with open("/Users/danilofiumi/PycharmProjects/Twitter_parse/page_source.html", "w") as f:
            f.write(driver.page_source)

        # driver.execute_script("window.localStorage.clear()")
        # driver.execute_script("window.sessionStorage.clear()")
        # driver.delete_all_cookies()

        df=prs_twtr('page_source.html')
        final=base.append(df)
        base=final

        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, {})".format(last_height + 500))
        time.sleep(4)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
            time.sleep(5)
            last_height = driver.execute_script("return document.body.scrollHeight")
            if last_height==new_height:
                with open("/Users/danilofiumi/PycharmProjects/Twitter_parse/page_source.html", "w") as f:
                    f.write(driver.page_source)
                df = prs_twtr('page_source.html')
                final = base.append(df)
                final = final.drop_duplicates(subset='tweet', keep="first")
                final.to_excel("/Users/danilofiumi/Documents/tweet_parsati/"+ str(account)+'.xlsx')
                # driver.quit()
                break

