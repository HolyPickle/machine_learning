import pandas as pd

df = pd.read_csv('news.csv', encoding='utf-8',sep=';')
new_data = pd.DataFrame()

new_data = new_data.append(df.iloc[0][:])
df.drop(index=0, axis=0)

for row in df.rows:
    temp_cat = row.category_name
    if temp_cat ==


