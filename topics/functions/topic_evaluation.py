from bertopic import BERTopic
from octis.evaluation_metrics.diversity_metrics import TopicDiversity

model_5 = BERTopic.load("topics/models/nursetweets_5_model")
print("starting evaluation")
metric = TopicDiversity(topk=10)
print("doing evaluation for", "5")
score = metric.score(model_5)
print(score)
