import requests
from bs4 import BeautifulSoup
import string
import pandas as pd
from datetime import datetime, timedelta
from multiprocessing import Process, Manager



dt_now = datetime.today()-timedelta(days=28)

class News:
    def __init__(self, category_name, title, content, url):
        self.category_name = category_name
        self.url = url
        self.title = title
        self.content = content

    def to_dict(self):
        return {
            'category_name': self.category_name,
            'title': self.title,
            'content': self.content,
            'url': self.url
        }


class NewsCategory:
    def __init__(self, category_name, news):
        self.category_name = category_name
        self.news = news

all_news = []

news_categories = [NewsCategory('turkiye',[]),NewsCategory('rusya',[]),NewsCategory('avrupa',[]),NewsCategory('dogu_akdeniz',[]),NewsCategory('ortadogu',[]),
                   NewsCategory('abd',[]),NewsCategory('guney_amerika',[]),NewsCategory('asya',[]),NewsCategory('afrika',[]),NewsCategory('bilim',[]),
                   NewsCategory('cevre',[]),NewsCategory('kultur',[]),NewsCategory('spor',[]),NewsCategory('politika',[]),NewsCategory('ekonomi',[]),
                   NewsCategory('savunma',[]),NewsCategory('yasam',[])]
def collector(cat,all_news):
    for i in range(0, 50):
        hour_param = (dt_now - timedelta(hours=i * 8)).strftime('%Y%m%dT%H%M%S')
        page = requests.get(
            'https://tr.sputniknews.com/' + cat.category_name + '/more.html?id=1&date=' + hour_param)
        soup = BeautifulSoup(page.content, 'html.parser')
        weblinks = soup.find_all(class_='b-stories__title')
        for link in weblinks:
            url = 'https://tr.sputniknews.com/' + link.contents[0].find_all('a')[0].get('href')
            print(url)
            page = requests.get(url)
            # parse with BFS
            news_soup = BeautifulSoup(page.text, 'html.parser')
            # get article title
            atitle = news_soup.find(class_="b-article__header-title")
            thetitle = atitle.get_text()
            # get main article page
            articlebody = news_soup.find(class_='b-article__lead')
            # get text
            articletext = articlebody.get_text()
            # print text
            cat.news.append(News(cat.category_name, thetitle, articletext, url))
            all_news.append(News(cat.category_name, thetitle, articletext, url))
    temp_cat_df = pd.DataFrame.from_records([n.to_dict() for n in cat.news])
    temp_cat_df.to_csv(cat.category_name + ".csv", encoding='utf-8', sep=';',)
    print(cat.category_name)
    print(str(all_news.__len__()))

#num_cores = multiprocessing.cpu_count()

with Manager() as manager:
    all_news = manager.list()  # <-- can be shared between processes.
    processes = []

    for i in news_categories:
        p = Process(target=collector, args=(i , all_news))  # Passing the list
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    all_news = list(all_news)
    print("Within WITH")

#Parallel(n_jobs=num_cores)(delayed(collector)(cat,all_news) for cat in news_categories)

print("RowCount: "+str(all_news.__len__()))


import re
from nltk import download
from nltk.corpus import stopwords
from snowballstemmer import TurkishStemmer

download('stopwords')


temp = []
snow = TurkishStemmer()
for eachNew in all_news:
    eachNew.title = eachNew.title.lower()
    eachNew.content = eachNew.content.lower()  # Converting to lowercase
    cleanr = re.compile('<.*?>')
    eachNew.title = re.sub(cleanr, ' ', eachNew.title)
    eachNew.content = re.sub(cleanr, ' ', eachNew.content)  # Removing HTML tags
    eachNew.title = re.sub(r'[?|!|:|´|\'|"|#]', r'', eachNew.title)
    eachNew.content = re.sub(r'[?|!|´|:|\'|"|#]', r'', eachNew.content)
    eachNew.title = re.sub(r'[.|,|)|´|:|(|\|/]', r' ', eachNew.title)
    eachNew.content = re.sub(r'[.|:|´|,|)|(|\|/]', r' ', eachNew.content)  # Removing Punctuations

    words = [snow.stemWord(word) for word in eachNew.title.split() if
             word not in set(stopwords.words('turkish'))]  # Stemming and removing stopwords
    eachNew.title = ' '.join(words)
    words = [snow.stemWord(word) for word in eachNew.content.split() if
             word not in set(stopwords.words('turkish'))]
    eachNew.content = ' '.join(words)


#for eachNew in all_news:
   # eachNew.title = eachNew.title.lower()
   # eachNew.content = eachNew.content.lower()
   # eachNew.title = eachNew.title.translate(str.maketrans('', '', string.punctuation))
   # eachNew.content = eachNew.content.translate(str.maketrans('', '', string.punctuation))


df = pd.DataFrame.from_records([n.to_dict() for n in all_news])
print("Data Frame Constructured !")

print(all_news)

print(df.columns)

print(df.info())

print(df.head())

df.drop_duplicates(subset='title', inplace=True)

df.to_csv('temp.csv',encoding='utf-8',sep=';', index=False)


print(df.head())
print('done!')
