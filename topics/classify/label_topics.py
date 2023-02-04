import pandas as pd

df = pd.load_csv("Dissertation/topics/docs_topics.csv")

df = df[df["Representative document"]==True]

df.to_csv("representative_docs.csv")