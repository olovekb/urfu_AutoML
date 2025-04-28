import pandas as pd
from catboost.datasets import titanic

df = pd.read_csv("titanic2.csv")
df_onehot = pd.get_dummies(df, columns=["Sex"])
df_onehot.to_csv("titanic_onehot.csv", index=False)
