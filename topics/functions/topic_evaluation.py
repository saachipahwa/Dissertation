from bertopic import BERTopic
from octis.evaluation_metrics.topic_significance_metrics import KL_uniform, KL_vacuous, KL_background
from octis.evaluation_metrics.diversity_metrics import TopicDiversity
import pandas as pd

# print function
def print_topic_words(model):
    for i in list(model.get_topics().values):
        print('topic {}:'.format(i), model.get_topic(i))

#set up evaluation spreadsheet
evaluation_df = pd.DataFrame(columns=['nr_topics', 'topic_diversity', 'KL_uniform', 'KL_vacuous', 'KL_background'])
evaluation_df.set_index('nr_topics')
evaluation_df.to_csv("Dissertation/topics/topic_evaluation.csv")
print("set up evaluation csv")

#load models
model_5 = BERTopic.load("nursetweets_5_model")
model_10 = BERTopic.load("nursetweets_10_model")
model_15 = BERTopic.load("nursetweets_15_model")
model_20 =  BERTopic.load("nursetweets_20_model")

#turn models into dictionaries
def get_words_from_topic(topic):
    #get words without probabilities
    words = []
    for x,y in topic:
        words.append(x)
    return words

def get_words_from_model(model):
    topics_list = model.get_topics().values()
    list_of_word_lists = []
    for topic in topics_list:
        list_of_word_lists.append(get_words_from_topic(topic))
    return list_of_word_lists

model_5_dict = {"topics":get_words_from_model(model_5)}
model_10_dict = {"topics":get_words_from_model(model_10)}
model_15_dict= {"topics":get_words_from_model(model_15)}
model_20_dict = {"topics":get_words_from_model(model_20)}

#topic diversity evaluation
TD_metric = TopicDiversity(topk=10)

TD_score_5 = TD_metric.score(model_5_dict)
print("model 5 score", TD_score_5)

TD_score_10 = TD_metric.score(model_10_dict)
print("model 10 score", TD_score_10)

TD_score_15 = TD_metric.score(model_15_dict)
print("model 15 score", TD_score_15)

TD_score_20 = TD_metric.score(model_20_dict)
print("model 20 score", TD_score_20)

#turn models into matrices
print(model_5.topic_sizes_)

#KL metrics
KLu_metric = KL_uniform()
KLv_metric = KL_vacuous()
KLb_metric = KL_background()

# KL_scores_5 = [KLu_metric.score(model_5_dict), KLv_metric.score(model_5_dict), KLb_metric.score(model_5_dict)]
# print("KL metrics for 5 topics", KL_scores_5)
# KL_scores_10 = [KLu_metric.score(model_10_dict), KLv_metric.score(model_10_dict), KLb_metric.score(model_10_dict)]
# print("KL metrics for 10 topics", KL_scores_10)
# KL_scores_15 = [KLu_metric.score(model_15_dict), KLv_metric.score(model_15_dict), KLb_metric.score(model_15_dict)]
# print("KL metrics for 15 topics", KL_scores_15)
# KL_scores_20 = [KLu_metric.score(model_20_dict), KLv_metric.score(model_20_dict), KLb_metric.score(model_20_dict)]
# print("KL metrics for 20 topics", KL_scores_20)
#
# evaluation_df.loc[len(evaluation_df)] = [5, TD_score_5, KL_scores_5[0], KL_scores_5[1], KL_scores_5[2]]
# evaluation_df.loc[len(evaluation_df)] = [10, TD_score_10, KL_scores_10[0], KL_scores_10[1], KL_scores_10[2]]
# evaluation_df.loc[len(evaluation_df)] = [15, TD_score_15, KL_scores_15[0], KL_scores_15[1], KL_scores_15[2]]
# evaluation_df.loc[len(evaluation_df)] = [20, TD_score_20, KL_scores_20[0], KL_scores_20[1], KL_scores_20[2]]
#
# evaluation_df.to_csv("Dissertation/topics/topic_evaluation.csv")