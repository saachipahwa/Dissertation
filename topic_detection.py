import pandas as pd
from bertopic import BERTopic


# for tweet in json_data:
#     print(tweet)
# topic_model = BERTopic(language="english", calculate_probabilities=True, verbose=True)
#
# topics, probs = topic_model.fit_transform()

df = pd.read_csv('data/healthcareworkertweets.csv', index_col=0)

tweet_text = df['text'].tolist()

topic_model = BERTopic(language="english", calculate_probabilities=True, verbose=True)

topics, probs = topic_model.fit_transform(tweet_text)

freq = topic_model.get_topic_info()
print(type(freq))
print(freq)

details_list = []
for i in freq['Topic']:
    if i>-1:
        details_list.append(topic_model.get_topic(i))
    else:
        details_list.append([])
freq['details'] = details_list

freq.to_csv('healthcare_topics.csv')

# similar_topics, similarity = topic_model.find_topics("wellbeing", top_n=5); similar_topics