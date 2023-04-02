import os

import hdbscan
from bertopic import BERTopic
from octis.evaluation_metrics.topic_significance_metrics import KL_uniform, KL_vacuous, KL_background
from octis.evaluation_metrics.diversity_metrics import TopicDiversity
import pandas as pd
from sentence_transformers import SentenceTransformer

directories = ["nursetweets", "doctortweets", "teachertweets",
               "railtweets", "journalisttweets", "musiciantweets"]
directory_index = 4
directory = directories[directory_index]
profession = "journalist"
# print function


def print_topic_words(model):
    for i in list(model.get_topics().values):
        print('topic {}:'.format(i), model.get_topic(i))


def make_csv(path):
    # set up evaluation spreadsheet
    evaluation_df = pd.DataFrame(columns=[
                                 'nr_topics',  'topic_diversity', 'KL_uniform'])
    evaluation_df.set_index('nr_topics')
    evaluation_df.to_csv(path)
    print("set up evaluation csv")
    return evaluation_df


def get_all_tweets(directory=None):
    df = pd.DataFrame()
    for filename in os.listdir("Dissertation/"+directory):
        f = os.path.join("Dissertation/"+directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0, error_bad_lines=False)
        df = pd.concat([df, user_df], ignore_index=True)
    return df


def get_tweets():
    df = get_all_tweets(directories[directory_index])
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


evaluation_df = make_csv(path="Dissertation/topics/{}_docs/topic_evaluation.csv".format(profession))
tweet_text = get_tweets()


def get_embeddings():
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    return sentence_model.encode(tweet_text, show_progress_bar=False)

embeddings = get_embeddings()

# initialise metrics
TD_metric = TopicDiversity(topk=10)
KLu_metric = KL_uniform()
KLv_metric = KL_vacuous()
KLb_metric = KL_background()

nr_topics = 10
ul_ngram = 1

for nr_topics in [5,10,15,20]:
    model = BERTopic.load("{}_{}_{}_model".format(directory, nr_topics, ul_ngram))
    model_dict = {"topics": get_words_from_model(model)}
    TD_score = TD_metric.score(model_dict)

    predictions, model_doc_matrix = model.transform(tweet_text, embeddings)
    model_matrix = {"topic-word-matrix": model.c_tf_idf_.toarray(),
                    'topic-document-matrix': model_doc_matrix}
    KL_score = KLu_metric.score(model_matrix)
    evaluation_df.loc[len(evaluation_df)] = [
        nr_topics , TD_score, KL_score]

evaluation_df.to_csv("Dissertation/topics/{}_docs/topic_evaluation.csv".format(profession))


# load models
# model_5_1 = BERTopic.load("nursetweets_5_1_model")
# model_5_2 = BERTopic.load("nursetweets_5_2_model")
# model_5_3 = BERTopic.load("nursetweets_5_3_model")
# model_10_1 = BERTopic.load("nursetweets_10_1_model")
# model_15_1 = BERTopic.load("nursetweets_15_1_model")
# model_20_1 = BERTopic.load("nursetweets_20_1_model")
#
# model_5_1_dict = {"topics": get_words_from_model(model_5_1)}
# model_10_1_dict = {"topics": get_words_from_model(model_10_1)}
# model_15_1_dict = {"topics": get_words_from_model(model_15_1)}
# model_20_1_dict = {"topics": get_words_from_model(model_20_1)}
#
#
# TD_metric = TopicDiversity(topk=10)

#
# TD_score_5_1 = TD_metric.score(model_5_1_dict)
# print("model 5 score", TD_score_5_1)
# TD_score_10_1 = TD_metric.score(model_10_1_dict)
# print("model 10 score", TD_score_10_1)
# TD_score_15_1 = TD_metric.score(model_15_1_dict)
# print("model 15 score", TD_score_15_1)
# TD_score_20_1 = TD_metric.score(model_20_1_dict)
# print("model 20 score", TD_score_20_1)

# turn models into matrices
# predictions5, model_5_doc_matrix = model_5_1.transform(tweet_text, embeddings)
# predictions10, model_10_doc_matrix = model_10_1.transform(tweet_text, embeddings)
# predictions15, model_15_doc_matrix = model_15_1.transform(tweet_text, embeddings)
# predictions20, model_20_doc_matrix = model_20_1.transform(tweet_text, embeddings)

# model_5_1_matrix = {"topic-word-matrix": model_5_1.c_tf_idf_.toarray(), 'topic-document-matrix': model_5_doc_matrix}
# model_10_1_matrix = {"topic-word-matrix": model_10_1.c_tf_idf_.toarray(), 'topic-document-matrix': model_10_doc_matrix}
# model_15_1_matrix = {"topic-word-matrix": model_15_1.c_tf_idf_.toarray(), 'topic-document-matrix': model_15_doc_matrix}
# model_20_1_matrix = {"topic-word-matrix": model_20_1.c_tf_idf_.toarray(), 'topic-document-matrix': model_20_doc_matrix}

# KL significance evaluation
# KLu_metric = KL_uniform()
# KLv_metric = KL_vacuous()
# KLb_metric = KL_background()

# print("word matrix", model_5_1_matrix["topic-word-matrix"])
# print("document matrix", model_5_1_matrix["topic-document-matrix"])
# print("predictions", predictions5)


# KL_scores_5 = [KLu_metric.score(model_5_1_matrix), 0, 0]
# print("KL metrics for 5 topics", KL_scores_5)
# KL_scores_10 = [KLu_metric.score(model_10_1_matrix), 0, 0]
# print("KL metrics for 10 topics", KL_scores_10)
# KL_scores_15 = [KLu_metric.score(model_15_1_matrix),  0, 0]
# print("KL metrics for 15 topics", KL_scores_15)
# KL_scores_20 = [KLu_metric.score(model_20_1_matrix),  0, 0]
# print("KL metrics for 20 topics", KL_scores_20)

# evaluation_df.loc[len(evaluation_df)] = [5, TD_score_5, KL_scores_5[0], KL_scores_5[1], KL_scores_5[2]]
# evaluation_df.loc[len(evaluation_df)] = [10, TD_score_10, KL_scores_10[0], KL_scores_10[1], KL_scores_10[2]]
# evaluation_df.loc[len(evaluation_df)] = [15, TD_score_15, KL_scores_15[0], KL_scores_15[1], KL_scores_15[2]]
# evaluation_df.loc[len(evaluation_df)] = [20, TD_score_20, KL_scores_20[0], KL_scores_20[1], KL_scores_20[2]]
#
# evaluation_df.to_csv("Dissertation/topics/topic_evaluation.csv")
#
