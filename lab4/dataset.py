import pandas as pd
from catboost.datasets import titanic

df = pd.read_csv("titanic_test.csv")
mean_age = df["Age"].mean()
df["Age"] = df["Age"].fillna(mean_age)
df.to_csv("titanic2.csv", index=False)
