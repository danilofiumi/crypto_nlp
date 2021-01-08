from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
from parse import prs_twtr
import time
time.sleep(2)


options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'images': 2, 'media_stream': 2,
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                            'ppapi_broker': 2, 'automatic_downloads': 2,}}

options.add_experimental_option('prefs', prefs)


t=1
for i in range(11):
    start_time = time.time()
    p = 0

    cols = ["tweet", "data", "reply", "commenti", "retweet", "like"]
    final = pd.DataFrame([], columns=cols)
    chrome_path = "/Users/danilofiumi/Downloads/chromedriver 2"
    base_path = "/Users/danilofiumi/Documents/tweet_parsati/"
    source_path = base_path + "page_source" + str(p) + ".html"

    ls_account = ["elonmusk"]
    dt_since = "2020-01-01"
    dt_until = "2021-01-01"



    for account in ls_account:
        url = "https://twitter.com/search?q=From%3A" + account + "%20since%3A" + dt_since + "%20until%3A" + dt_until + "&src=typed_query&f=live"


        driver = webdriver.Chrome(options=options, executable_path=chrome_path)
        driver.get(url)
        time.sleep(5)

        dummy=0
        iter=0
        previous_height=1

        x=33/100
        while True:
            # parte 1
            with open(source_path, "w") as f:
                f.write(driver.page_source)

            df = prs_twtr(source_path)
            final = final.append(df)
            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, {})".format(((last_height-previous_height)*x)+previous_height))
            time.sleep(t)

            # parte 2
            with open(source_path, "w") as f:
                f.write(driver.page_source)

            df = prs_twtr(source_path)
            final = final.append(df)
            driver.execute_script("window.scrollTo(0, {})".format(((last_height-previous_height)*2*x)+previous_height))
            time.sleep(t)

            # parte 3
            with open(source_path, "w") as f:
                f.write(driver.page_source)


            df = prs_twtr(source_path)
            final = final.append(df)
            previous_height = last_height
            driver.execute_script("window.scrollTo(0, {})".format(last_height))
            time.sleep(t)

            new_height = driver.execute_script("return document.body.scrollHeight")

            if (final.shape[0] - dummy) >= 1000:
                driver.close()
                dt_until = str(final.index[-10].date())
                url = "https://twitter.com/search?q=From%3A" + account + "%20since%3A" + dt_since + "%20until%3A" + dt_until + "&src=typed_query&f=live"
                driver = webdriver.Chrome(options=options, executable_path=chrome_path)
                driver.get(url)
                time.sleep(t)
                dummy = final.shape[0]

            if last_height == new_height:
                time.sleep(5)
                last_height = driver.execute_script("return document.body.scrollHeight")

                if last_height == new_height:
                    with open(source_path, "w") as f:
                        f.write(driver.page_source)

                    df = prs_twtr(source_path)
                    final = final.append(df)
                    final = final.drop_duplicates(subset='tweet', keep="first")
                    final.to_excel("/Users/danilofiumi/PycharmProjects/Twitter_parse/tweet/"+ str(account)+'.xlsx')
                    driver.close()
                    print(str(final.shape[0]) + " rows with time sleep = " + str(t) + " for "+ account + " account")
                    print("--- %s minutes ---" % round((time.time() - start_time)/60))
                    break