import pandas as pd

df = pd.read_csv("topics/doctor_docs/docs_topics.csv")

df = df[df["Representative_document"]==True]

df.to_csv("topics/doctor_docs/representative_docs.csv")