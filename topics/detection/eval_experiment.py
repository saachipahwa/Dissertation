import os

import hdbscan
from bertopic import BERTopic
# from octis.evaluation_metrics.topic_significance_metrics import KL_uniform, KL_vacuous, KL_background
# from octis.evaluation_metrics.diversity_metrics import TopicDiversity
import pandas as pd
# from sentence_transformers import SentenceTransformer

directories = ["nursetweets", "doctortweets", "teachertweets", "railtweets", "journalisttweets", "musiciantweets"]
directory_index = 0

# print function
def print_topic_words(model):
    for i in list(model.get_topics().values):
        print('topic {}:'.format(i), model.get_topic(i))

def make_csv():
    # set up evaluation spreadsheet
    evaluation_df = pd.DataFrame(columns=['nr_topics', 'topic_diversity', 'KL_uniform', 'KL_vacuous', 'KL_background'])
    evaluation_df.set_index('nr_topics')
    evaluation_df.to_csv("topics/topic_evaluation.csv")
    print("set up evaluation csv")
    return evaluation_df

def get_all_tweets():
    directory = directories[directory_index]
    df = pd.DataFrame()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0)
        df = pd.concat([df, user_df], ignore_index=True)
        print("tweet count", len(df))
    return df['nouns'].astype(str).tolist()


# turn models into dictionaries
def get_words_from_topic(topic):
    # get words without probabilities
    words = []
    for x, y in topic:
        words.append(x)
    return words

def get_words_from_model(model):
    topics_list = model.get_topics().values()
    list_of_word_lists = []
    for topic in topics_list:
        list_of_word_lists.append(get_words_from_topic(topic))
    return list_of_word_lists

# make_csv()
# evaluation_df = make_csv()

# tweet_text = get_all_tweets()
#
# def get_embeddings():
#     sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
#     return sentence_model.encode(tweet_text, show_progress_bar=False)
#
# embeddings = get_embeddings()
#
# # load models
print('about to load model')
model = BERTopic.load("nursetweets_5_1_model")
print('loaded model')
# model_dict = {"topics": get_words_from_model(model)}
#
# # topic diversity evaluation
# TD_metric = TopicDiversity(topk=10)
# TD_score_5 = TD_metric.score(model_dict)
# print("model score", TD_score_5)
#
# #extracting topics and probabilities
print("about to extract topics")
topics= model._map_predictions(model.hdbscan_model.labels_)
print("extracted topics")
print("topics", topics)

print("about to extract probs")
probs = hdbscan.all_points_membership_vectors(model.hdbscan_model)
print("extracted first part")
probs = model._map_probabilities(probs, original_topics=True)
print("extracted second part")
print("probs", probs)

# turn models into matrices
# predictions5, model_doc_matrix = model.transform(tweet_text, embeddings)

# KL_scores_5=None

#transform method
# try:
#     model_matrix = {"topic-word-matrix": model.c_tf_idf_.toarray(), 'topic-document-matrix': model}
#     KLu_metric = KL_uniform()
#     KLv_metric = KL_vacuous()
#     KLb_metric = KL_background()
#
#     print("word matrix", model_matrix["topic-word-matrix"])
#     print("document matrix", model_matrix["topic-document-matrix"])
#     print("predictions", predictions5)
#
#     KL_scores_5 = [KLu_metric.score(model_matrix), KLv_metric.score(model_matrix), KLb_metric.score(model_matrix)]
#     print("KL metrics", KL_scores_5)
# except Exception as e:
#     print(e)
#
# if KL_scores_5==None:
#     #extracting topics and probabilities
#     topics= model._map_predictions(model.hdbscan_model.labels_)
#
#     probs = hdbscan.all_points_membership_vectors(model.hdbscan_model)
#     probs = model._map_probabilities(probs, original_topics=True)
#     print("topics", topics)
#     print("probs", probs)