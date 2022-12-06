from bertopic import BERTopic
from sklearn.datasets import fetch_20newsgroups
from sentence_transformers import SentenceTransformer
import umap
import hdbscan

data = fetch_20newsgroups(subset='all')['data']
# sentence_model = SentenceTransformer("roberta-base-nli-stsb-mean-tokens")
# embeddings = sentence_model.encode(data, show_progress_bar=False)
# print("1")
# umap_model = umap.UMAP(n_neighbors=15,
#                        n_components=10,
#                        min_dist=0.0,
#                        metric='cosine',
#                        low_memory=False)
# print("2")
# hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=10,
#                                 min_samples=1,
#                                 metric='euclidean',
#                                 cluster_selection_method='eom',
#                                 prediction_data=True)
print("3")
topic_model = BERTopic(top_n_words=20,
                       n_gram_range=(1, 2),
                       calculate_probabilities=True,
                       # umap_model= umap_model,
                       # hdbscan_model=hdbscan_model,
                       verbose=True,
                       language = "english")
print("4")
# Train model, extract topics and probabilities
# topics, probabilities = topic_model.fit_transform(data, embeddings)
topics, probabilities = topic_model.fit_transform(data)

print("5")
freq = topic_model.get_topic_info()
print(type(freq))
print(freq)

details_list = []
for i in freq['Topic']:
    if i > -1:
        details_list.append(topic_model.get_topic(i))
    else:
        details_list.append([])
freq['details'] = details_list
print("6")

freq.to_csv('test_topics.csv')