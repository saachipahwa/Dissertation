from bertopic import BERTopic
from octis.evaluation_metrics.diversity_metrics import TopicDiversity
import pandas as pd

#set up evaluation spreadsheet
data= {'nr_topics': [5, 10, 15, 20], 'topic_diversity': [None, None, None, None]}
evaluation_df = pd.DataFrame(data)
evaluation_df.set_index('nr_topics')
evaluation_df.to_csv("topics/topic_evaluation.csv")
print("set up evaluation csv")

def get_words_from_topic(topic):
    #get words without probabilities
    words = []
    for x,y in topic:
        words.append(x)
    return words

def get_words_from_model(model):
    topics_list = model_5.get_topics().values()
    list_of_word_lists = []
    for topic in topics_list:
        list_of_word_lists.append(get_words_from_topic(topic))
    return list_of_word_lists

#evaluation
metric = TopicDiversity(topk=10)

model_5 = BERTopic.load("topics/models/nursetweets_5_model")
score_5 = metric.score({"topics":get_words_from_model(model_5)})
print("model 5 score", score_5)
evaluation_df.at[5,'topic_diversity'] = score_5

model_10 = BERTopic.load("topics/models/nursetweets_10_model")
print("doing evaluation for", "10")
score_10 = metric.score({"topics":get_words_from_model(model_10)})
print("model 10 score", score_10)
evaluation_df.at[10,'topic_diversity'] = score_10

model_15 = BERTopic.load("topics/models/nursetweets_15_model")
print("doing evaluation for", "15")
score_15 = metric.score({"topics":get_words_from_model(model_15)})
print("model 15 score", score_15)
evaluation_df.at[15,'topic_diversity'] = score_15

model_20 =  BERTopic.load("topics/models/nursetweets_20_model")
print("doing evaluation for", "20")
score_20 = metric.score({"topics":get_words_from_model(model_20)})
print("model 20 score", score_20)
evaluation_df.at[20,'topic_diversity'] = score_20

evaluation_df.to_csv("topics/topic_evaluation.csv")
