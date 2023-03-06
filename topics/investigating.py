import pandas as pd

docs_topics = pd.read_csv("topics/docs_topics.csv")
life_docs = docs_topics[(docs_topics['Topic'] != -1) & (docs_topics['Topic'] != 2)]# & (docs_topics['Representative_document']==True)]
life_docs.to_csv("topics/life_docs.csv")

nurse_words = life_docs[life_docs['Document'].str.match("nurse")]
nurse_words.to_csv("topics/life_docs_w_nurse.csv")

nursing_words = life_docs[life_docs['Document'].str.match("nursing")]
nurse_words.to_csv("topics/life_docs_w_nursing.csv")

work = life_docs[life_docs['Document'].str.match("work")]
nurse_words.to_csv("topics/life_docs_w_work.csv")
