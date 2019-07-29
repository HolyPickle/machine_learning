import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('news.csv', sep=';', index_col=False)

tempDf = pd.read_csv('temp.csv', sep=';', index_col=False)

df = df.append(tempDf, ignore_index=True, sort=True)

df.drop_duplicates(subset='title', inplace=True)

df['content'] = df['content'].str.replace('bir', '')
df['title'] = df['title'].str.replace('bir', '')
df['content'] = df['content'].str.replace('başka', '')
df['title'] = df['title'].str.replace('başka', '')
df['content'] = df['content'].str.replace('ol', '')
df['title'] = df['title'].str.replace('ol', '')
df['content'] = df['content'].str.replace('ola', '')
df['title'] = df['title'].str.replace('ola', '')
df['content'] = df['content'].str.replace('olduk', '')
df['title'] = df['title'].str.replace('olduk', '')
df['content'] = df['content'].str.replace('ilk', '')
df['title'] = df['title'].str.replace('ilk', '')
df['content'] = df['content'].str.replace('belirtti', '')
df['title'] = df['title'].str.replace('belirtti', '')


# temp_data_to_clean = pd.DataFrame()
#
# temp_data_to_clean['merged'] = df['title'].astype(str)+' '+df['content'].astype(str)
#
# freq_d = pd.Series(' '.join(temp_data_to_clean['merged']).split()).value_counts()
# freq_d.plot(kind='line', ax=None, figsize=None, use_index=True,
#             title=None, grid=None, legend=False, style=None,
#             logx=False, logy=False, loglog=False, xticks=None,
#             yticks=None, xlim=None, ylim=None, rot=None,
#             fontsize=None, colormap=None, table=False, yerr=None,
#             xerr=None, label=None, secondary_y=False)
# plt.show()
#
# #
# #Remove the least frequent words
# rare_d = pd.Series(' '.join(temp_data_to_clean['merged']).split()).value_counts()[9000:]
# rare_d = list(rare_d.index)
# temp_data_to_clean['merged'] = temp_data_to_clean['merged'].apply(lambda x: " ".join(x for x in x.split() if x not in rare_d))
# #Remove the most frequent words
# freq_d = pd.Series(' '.join(temp_data_to_clean['merged']).split()).value_counts()[:30]
# freq_d = list(freq_d.index)
# temp_data_to_clean['merged'] = temp_data_to_clean['merged'].apply(lambda x: " ".join(x for x in x.split() if x not in freq_d))
#
# df = temp_data_to_clean
df.sort_values(by='category_name', inplace=True)
df.to_csv('cleaned_news.csv',encoding='utf-8',sep=';', index=False)