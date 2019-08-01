from sklearn.externals import joblib
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords
from snowballstemmer import TurkishStemmer
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('deneme.html')

print("Loading Model...")
model = joblib.load("model.pkl")
print("Model Loaded.")

@app.route('/', methods=['POST'])
def my_form_post():
    get_article = request.form['text']
    snow = TurkishStemmer()
    get_article= get_article.lower()
    cleanr = re.compile('<.*?>')
    get_article = re.sub(cleanr, ' ', get_article)
    get_article = re.sub(r'[?|!|:|´|\'|"|#]', r'', get_article)
    get_article = re.sub(r'[.|,|)|´|:|(|\|/]', r' ', get_article)

    words = [snow.stemWord(word) for word in get_article.split() if
             word not in set(stopwords.words('turkish'))]  # Stemming and removing stopwords
    get_article = ' '.join(words)
    predict = (model.predict([get_article]))
    predicted = predict[0]
    predicted = predicted.upper()
    predicted = predicted.replace("_", " ")


    return '''
        <html>
            <head>
            <link rel="stylesheet" type="text/css" href="/static/mainstyle3.css">
                <title>Tahmin Zamanı</title>
            </head>
            <body>
            <div class="container">
                <h1>Haber başlığın şununla ilgili olabilir</h1>
                <h2 class="rainbow">{}</h2>
            </div>
            </body>
        </html>'''.format(predicted)

    #return "DÜŞÜNÜYORUM ÖYLEYSE VARIM:" + "" + str(model.predict([get_article]))


#
# def web_form():
#     get_article = input("Enter Article:")
#     snow = TurkishStemmer()
#     get_article = get_article.lower()
#     cleanr = re.compile('<.*?>')
#     get_article = re.sub(cleanr, ' ', get_article)
#     get_article = re.sub(r'[?|!|:|´|\'|"|#]', r'', get_article)
#     get_article = re.sub(r'[.|,|)|´|:|(|\|/]', r' ', get_article)
#
#     words = [snow.stemWord(word) for word in get_article.split() if
#              word not in set(stopwords.words('turkish'))]  # Stemming and removing stopwords
#     get_article = ' '.join(words)

    #text = get_article
    # # Create and generate a word cloud image:
    # wordcloud = WordCloud(max_font_size=50, max_words=50, background_color="white").generate(text)
    # # Display the generated image:
    # plt.figure()
    # plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()
    # get_article = model.predict([get_article])
    # return get_article

if __name__ == "__main__":
    app.run()