
from bs4 import BeautifulSoup
import pandas as pd

def clean_parsed(df):
    df['data'] = pd.to_datetime(df['data'].str.replace('T', ' '))
    df.set_index('data', drop=True, inplace=True)
    return (df)

def prs_twtr(path):
    with open(path, 'r') as f:
        contents = f.read()

        page_soup = BeautifulSoup(contents, 'html.parser')

    # finds each product from the store page
    containers = page_soup.findAll("article")

    lista_tweet=[]
    lista_data=[]
    lista_reply=[]
    lista_commenti=[]
    lista_retweet=[]
    lista_like=[]


    for cnt in containers:
        # tweet
        try:
            tweet = cnt.findAll("div", {"class": "css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0"})

            try:
                ls = tweet[0].findAll("span")
            except LookupError:
                ls = "****"

            tmp1 = []

            for i in range(len(ls)):

                try:
                    tmp1.append(ls[i].text)
                except AttributeError:
                    tmp1.append(ls)

            string1 = " ".join(tmp1)

            lista_tweet.append(string1)

        except LookupError:
            lista_tweet.append("****")


        # data del tweet
        try:
            data = cnt.findAll("time")
            dict = data[0].attrs
            ls1 = str(dict.values())
            lista_data.append(ls1[14:-8])

        except LookupError:
            lista_data.append("****")


        # reply
        try:
            reply = cnt.findAll("div",{"class": "css-901oao r-111h2gw r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0"})
            ls2 = reply[0].findAll("a")
            tmp=[]
            for x in range(len(ls2)):
                tmp.append(ls2[x]['href'])
            string = " ".join(tmp)
            lista_reply.append(string)

        except LookupError:
            lista_reply.append(" ")


        # num commenti
        try:
            commenti = cnt.findAll("div", {"class": "css-1dbjc4n r-18u37iz r-1h0z5md"})
            ls3 = commenti[0].span.text

            lista_commenti.append(ls3)
        except LookupError:
            lista_commenti.append('****')


        # num retweet
        try:
            ls4 = commenti[1].span.text

            lista_retweet.append(ls4)
        except LookupError:
            lista_retweet.append('****')


        # num like
        try:
            ls5 = commenti[2].span.text

            lista_like.append(ls5)
        except LookupError:
            lista_like.append('****')



    cols=["tweet","data","reply","commenti","retweet","like" ]
    df = pd.DataFrame(list(zip(lista_tweet, lista_data,lista_reply,lista_commenti,lista_retweet,lista_like)),
                       columns =cols)

    return(clean_parsed(df))

    # null_data = pd.read_excel('elon.xlsx',usecols=cols)
    # df2=df.append(null_data)

# df.to_excel('elon.xlsx')

# df=prs_twtr()
# print(df)