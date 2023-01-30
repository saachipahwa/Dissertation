import os

from bertopic import BERTopic
from octis.evaluation_metrics.topic_significance_metrics import KL_uniform, KL_vacuous, KL_background
from octis.evaluation_metrics.diversity_metrics import TopicDiversity
import pandas as pd

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
    evaluation_df.to_csv("Dissertation/topics/topic_evaluation.csv")
    print("set up evaluation csv")
    return evaluation_df

def get_all_tweets(directory = None):
    df = pd.DataFrame()
    for filename in os.listdir("Dissertation/"+directory):
        f = os.path.join("Dissertation/"+directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0)
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


evaluation_df = make_csv()
tweet_text = get_tweets()

# load models
model_5 = BERTopic.load("nursetweets_5_model")
model_10 = BERTopic.load("nursetweets_10_model")
model_15 = BERTopic.load("nursetweets_15_model")
model_20 = BERTopic.load("nursetweets_20_model")

model_5_dict = {"topics": get_words_from_model(model_5)}
model_10_dict = {"topics": get_words_from_model(model_10)}
model_15_dict = {"topics": get_words_from_model(model_15)}
model_20_dict = {"topics": get_words_from_model(model_20)}

# topic diversity evaluation
TD_metric = TopicDiversity(topk=10)
TD_score_5 = TD_metric.score(model_5_dict)
print("model 5 score", TD_score_5)
TD_score_10 = TD_metric.score(model_10_dict)
print("model 10 score", TD_score_10)
TD_score_15 = TD_metric.score(model_15_dict)
print("model 15 score", TD_score_15)
TD_score_20 = TD_metric.score(model_20_dict)
print("model 20 score", TD_score_20)

# turn models into matrices
model_5_matrix = {"topic-word-matrix": model_5.c_tf_idf_.toarray(), 'topic-document-matrix': model_5.tranform(tweet_text)}
model_10_matrix = {"topic-word-matrix": model_10.c_tf_idf_.toarray(), 'topic-document-matrix': model_10.tranform(tweet_text)}
model_15_matrix = {"topic-word-matrix": model_15.c_tf_idf_.toarray(), 'topic-document-matrix': model_15.tranform(tweet_text)}
model_20_matrix = {"topic-word-matrix": model_20.c_tf_idf_.toarray(), 'topic-document-matrix': model_20.tranform(tweet_text)}

# KL significance evaluation
KLu_metric = KL_uniform()
KLv_metric = KL_vacuous()
KLb_metric = KL_background()

KL_scores_5 = [KLu_metric.score(model_5_matrix), KLv_metric.score(model_5_matrix), KLb_metric.score(model_5_matrix)]
print("KL metrics for 5 topics", KL_scores_5)
KL_scores_10 = [KLu_metric.score(model_10_matrix),  KLv_metric.score(model_10_matrix), KLb_metric.score(model_10_matrix)]
print("KL metrics for 10 topics", KL_scores_10)
KL_scores_15 = [KLu_metric.score(model_15_matrix),  KLv_metric.score(model_15_matrix), KLb_metric.score(model_15_matrix)]
print("KL metrics for 15 topics", KL_scores_15)
KL_scores_20 = [KLu_metric.score(model_20_matrix),  KLv_metric.score(model_20_matrix), KLb_metric.score(model_20_matrix)]
print("KL metrics for 20 topics", KL_scores_20)

evaluation_df.loc[len(evaluation_df)] = [5, TD_score_5, KL_scores_5[0], KL_scores_5[1], KL_scores_5[2]]
evaluation_df.loc[len(evaluation_df)] = [10, TD_score_10, KL_scores_10[0], KL_scores_10[1], KL_scores_10[2]]
evaluation_df.loc[len(evaluation_df)] = [15, TD_score_15, KL_scores_15[0], KL_scores_15[1], KL_scores_15[2]]
evaluation_df.loc[len(evaluation_df)] = [20, TD_score_20, KL_scores_20[0], KL_scores_20[1], KL_scores_20[2]]

evaluation_df.to_csv("Dissertation/topics/topic_evaluation.csv")

make_csv()