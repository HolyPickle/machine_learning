import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.externals import joblib
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt


# Eşit elemanlı kategori datası
data = pd.read_csv('news_backup.csv', sep= ';', index_col=False)

data['merged'] = data['title'].astype(str)+' '+data['content'].astype(str)

# Start with one review:
text = " ".join(review for review in data.merged)

# Create and generate a word cloud image:
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
# Display the generated image:
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

X = data.merged
Y = data.category_name


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.05, random_state=40)

print(X_test.shape)
print(Y_test.shape)
print(X_train.shape)
print(Y_train.shape)


#myClassifier = Pipeline([('tfid', TfidfVectorizer(encoding='utf-8', lowercase=False, binary=False, analyzer='word', decode_error='strict',max_features=None)),
                        # ('cnb', ComplementNB(norm=False, alpha=1, fit_prior=True, class_prior=None)),
                         #])
SVC = Pipeline([('tfid', TfidfVectorizer(encoding='utf-8', lowercase=False, binary=False, analyzer='word', decode_error='strict', smooth_idf=True, ngram_range=(1,4), max_features=100000,max_df=1000,min_df=1)),
                #('tsvd', TruncatedSVD(n_components=600, algorithm='arpack')),
                ('svc', LinearSVC(tol=0.5, C=1.0, verbose=0, fit_intercept=False, intercept_scaling=0.0, dual=False, random_state=42)),
                ])

###############################################


SVC.fit(X_train, Y_train)
print("------------------------")
# param_grid = {"tsvd__n_components" : range(180,200),
#               "tsvd__algorithm": ('randomized', 'arpack'),
#               "svc__verbose" : range(0,4),
#               "svc__tol": (0.1, 0.2, 0.3, 0.5, 1.0),
#               "svc__C": (0.1, 0.2, 0.3, 0.5, 0.7, 1.0),
#               "svc__intercept_scaling": (0.0, 0.1, 0.2, 0.3, 0.4),
#               "svc__dual": (True, False),
#               }
#
# grid_search = GridSearchCV(SVC, param_grid=param_grid, cv=10, n_jobs=-1, verbose=1)
# grid_search.fit(X,Y)
#
# print(grid_search.best_score_)
# print(grid_search.best_params_)
# print(grid_search.best_estimator_)

prediction = SVC.predict(X_test)

fscore = f1_score(Y_test, prediction, average='weighted',pos_label=1)
print("F1 Score: ", fscore)


score = accuracy_score(Y_test, prediction)
print("------------------------")
print("Score: \t", score)
print("------------------------")

denemeDF = pd.read_csv('temp.csv', sep=';', index_col=False)

denemeX = ["elo musk"]
deneme_pred = SVC.predict(denemeX)
print(deneme_pred)

print("------------------------")
print("Model Dumping.....")
joblib.dump(SVC, "model.pkl")
print("Model Dumped.")