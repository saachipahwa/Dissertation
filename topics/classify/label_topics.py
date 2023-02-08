import pandas as pd

df = pd.read_csv("topics/docs_topics.csv")

df = df[df["Representative_document"]==True]

df.to_csv("topics/representative_docs.csv")