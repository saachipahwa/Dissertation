from bertopic import BERTopic
from octis.evaluation_metrics.diversity_metrics import TopicDiversity
import pandas as pd

#set up evaluation spreadsheet
evaluation_df = pd.DataFrame(columns=['nr_topics', 'topic_diversity'])
evaluation_df.set_index('nr_topics')
evaluation_df.to_csv("Dissertation/topics/topic_evaluation.csv")
print("set up evaluation csv")

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

def print_topic_words(model):
    for i in list(model.get_topics().values):
        print('topic {}:'.format(i), model.get_topic(i))

#topic diversity evaluation
metric = TopicDiversity(topk=10)

model_5 = BERTopic.load("nursetweets_5_model")
score_5 = metric.score({"topics":get_words_from_model(model_5)})
print("model 5 score", score_5)
evaluation_df.loc[len(evaluation_df)] = [5, score_5]

model_10 = BERTopic.load("nursetweets_10_model")
print("doing evaluation for", "10")
score_10 = metric.score({"topics":get_words_from_model(model_10)})
print("model 10 score", score_10)
evaluation_df.loc[len(evaluation_df)] = [10, score_10]

model_15 = BERTopic.load("nursetweets_15_model")
print("doing evaluation for", "15")
score_15 = metric.score({"topics":get_words_from_model(model_15)})
print("model 15 score", score_15)
evaluation_df.loc[len(evaluation_df)] = [15, score_15]

model_20 =  BERTopic.load("nursetweets_20_model")
print("doing evaluation for", "20")
score_20 = metric.score({"topics":get_words_from_model(model_20)})
print("model 20 score", score_20)
evaluation_df.loc[len(evaluation_df)] = [20, score_20]

#KL

evaluation_df.to_csv("Dissertation/topics/topic_evaluation.csv")