import os
from bertopic import BERTopic
import pandas as pd
from sentence_transformers import SentenceTransformer
from octis.evaluation_metrics.diversity_metrics import TopicDiversity

# os.environ["TOKENIZERS_PARALLELISM"] = "false"
#
# def get_all_tweets(directory = None):
#     df = pd.DataFrame()
#     for filename in os.listdir("Dissertation/"+directory):
#         f = os.path.join("Dissertation/"+directory, filename)
#         print(f)
#         user_df = pd.read_csv(f, index_col=0)
#         df = pd.concat([df, user_df], ignore_index=True)
#     return df
#
# def get_topics_from(directory_name = "nursetweets", nr_topics=None, embeddings=None):
#     #set up model parameters
#     topic_model = BERTopic(language="english",
#                            calculate_probabilities=False,
#                            verbose=True,
#                            low_memory=True,
#                            n_gram_range=(1, 3),
#                            nr_topics=nr_topics
#                            )
#     print("set up topic model. about to fit model")
#
#     #fit transform
#     topics, probabilities = topic_model.fit_transform(tweet_text, embeddings)
#     print("model has been fit")
#
#     # open("topics/models/{}_{}_model".format(directory_name, nr_topics), 'w+')
#     # topic_model.save("topics/models/{}_{}_model".format(directory_name, nr_topics))
#     # print("model has been saved", nr_topics)
#
#     freq = topic_model.get_topic_info()
#     print(type(freq))
#     print(freq)
#
#     details_list = []
#     for i in freq['Topic']:
#         if i > -1:
#             details_list.append(topic_model.get_topic(i))
#         else:
#             details_list.append([])
#     freq['details'] = details_list
#
#     freq.to_csv('Dissertation/topics/{}_topics_{}.csv'.format(directory_name, nr_topics))
#     print("info saved to csv")
#
#     return topic_model
#
# #get tweets
# directories =  ["nursetweets", "doctortweets", "teachertweets", "railtweets", "journalisttweets", "musiciantweets"]
# df = get_all_tweets(directories[0])
# print("tweet count", len(df))
#
# #get tweet text
# tweet_text = df['nouns'].astype(str).tolist()
# print("got df")
#
# #pre-compute embeddings
# print("computing embeddings")
# sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
# embeddings = sentence_model.encode(tweet_text, show_progress_bar=False)
#
# #get topics
# print("getting topics ", "5")
# model_5 = get_topics_from(directory_name="nursetweets", nr_topics=5, embeddings=embeddings)
# print("getting topics ", "10")
# model_10 = get_topics_from(directory_name="nursetweets", nr_topics=10, embeddings=embeddings)
# print("getting topics ", "15")
# model_15 = get_topics_from(directory_name="nursetweets", nr_topics=15, embeddings=embeddings)
# print("getting topics for", "20")
# model_20 = get_topics_from(directory_name="nursetweets", nr_topics=20, embeddings=embeddings)
model_5 = BERTopic.load("nursetweets_5_model")
with open('Dissertation/topics/nursetweets_5_docs.txt', 'w+') as f:
    f.write(str(model_5.get_representative_docs()))
# print(model_10.get_representative_docs())
# print(model_15.get_representative_docs())
# print(model_20.get_representative_docs())