import pandas as pd

df = pd.read_csv("Dissertation/topics/docs_topics.csv")

df = df[df["Representative_document"]==True]

df.to_csv("representative_docs.csv")