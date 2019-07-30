from sklearn.externals import joblib
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

print("Loading Model...")
model = joblib.load("model.pkl")
print("Model Loaded.")
import re
# from nltk import download
from nltk.corpus import stopwords
from snowballstemmer import TurkishStemmer
stopwords = list(stopwords.words('turkish'))
newStop = ['bir', 'ol', 'ola', 'belki', 'olur', 'bugün', 'yarın', 'şimdi', 'mu', 'onlar','seksen','ama','trilyon','buna'
,'bizim','şeyden','yirmi','altı','iki','seni','doksan','dört','bunun','ki','nereye','altmış','hem','milyon','kez','otuz','beş'
,'elli','bizi','da','sekiz','ve','çok','bu','veya','ya','kırk','onların','ona','bana','yetmiş','milyar','þunu'
,'senden','birşeyi','dokuz','yani','kimi','þeyler','kim','neden','senin','yedi','niye','üç','şey','mı','tüm','onlari'
,'bunda','ise','þundan','hep','þuna','bin','ben','ondan','kimden','bazı','belki','ne','bundan','gibi','de','onlardan','sizi','sizin'
,'daha','niçin','þunda','bunu','beni','ile','şu','şeyi','sizden','defa','biz','için','dahi','siz','nerde','kime','birþey'
,'birkez','her','biri','on','mü','diye','acaba','sen','en','hepsi','bir','bizden','sanki','benim','nerede','onu','benden'
,'yüz','birkaç','çünkü','nasýl','hiç','katrilyon']
stopwords.extend(newStop)
while True:
    print("Enter article:")
    X = input()
    if (X == '0'):
        break
    snow = TurkishStemmer()
    X = X.lower()
    cleanr = re.compile('<.*?>')
    X = re.sub(cleanr, ' ', X)
    X = re.sub(r'[?|!|:|´|\'|"|#]', r'', X)
    X = re.sub(r'[.|,|)|´|:|(|\|/]', r' ', X)
    words = [snow.stemWord(word) for word in X.split() if
             word not in stopwords]  # Stemming and removing stopwords
    X = ' '.join(words)

    text = X
    # Create and generate a word cloud image:
    wordcloud = WordCloud(max_font_size=50, max_words=50, background_color="white").generate(text)
    # Display the generated image:
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    print(X)

    print("Preidction: ")
    print(model.predict([X]))
    print("END")