from bertopic import BERTopic
from octis.evaluation_metrics.diversity_metrics import TopicDiversity
import pandas as pd

#set up evaluation spreadsheet
# data= {'nr_topics': [5, 10, 15, 20], 'topic_diversity': [None, None, None, None]}
# evaluation_df = pd.DataFrame(data)
# evaluation_df.set_index('nr_topics')
# evaluation_df.to_csv("topics/topic_evaluation.csv")
# print("set up evaluation csv")

#evaluation
model_5 = BERTopic.load("topics/models/nursetweets_5_model")
metric = TopicDiversity(topk=5)
score = metric.score({"topics":list(model_5.get_topics().values())})
print("model 5 score", score)

model_10 = BERTopic.load("topics/models/nursetweets_10_model")
print("doing evaluation for", "10")
print("model 10 score", metric.score({"topics":list(model_10.get_topics().values())}))

model_15 = BERTopic.load("topics/models/nursetweets_15_model")
print("doing evaluation for", "15")
print("model 15 score",  metric.score({"topics":list(model_15.get_topics().values())}))

model_20 =  BERTopic.load("topics/models/nursetweets_20_model")
print("doing evaluation for", "20")
print("model 20 score", metric.score({"topics":list(model_20.get_topics().values())}))
# evaluation_df.at[20,'topic_diversity'] = metric.score(model_20)