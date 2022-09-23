import pandas as pd
from ast import literal_eval

df = pd.read_csv("Art_Views.csv", sep=';')

df2 = df.drop('index', axis=1)
df2.to_csv("Art_Views.csv", index=False)

df['hashtag'] = df['hashtag'].apply(literal_eval)  # convert to list type
df = df.explode('hashtag')
df = df.drop('index', axis=1)
df.to_csv("split_Art_Views.csv", index=False)
