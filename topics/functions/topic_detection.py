import os
from bertopic import BERTopic
import pandas as pd
from sentence_transformers import SentenceTransformer
from octis.evaluation_metrics.diversity_metrics import TopicDiversity

def get_all_tweets(directory = None):
    df = pd.DataFrame()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0)
        df = pd.concat([df, user_df], ignore_index=True)
    return df

def get_topics_from(directory_name = "nursetweets", nr_topics=None, embeddings=None):
    #set up model parameters
    topic_model = BERTopic(language="english",
                           calculate_probabilities=False,
                           verbose=True,
                           low_memory=True,
                           n_gram_range=(1, 3),
                           nr_topics=nr_topics
                           )
    print("set up topic model. about to fit model")

    #fit transform
    topics, probabilities = topic_model.fit_transform(tweet_text, embeddings)
    topic_model.save("topics/models/{}_{}_model".format(directory_name, nr_topics))

    print("fit model")
    freq = topic_model.get_topic_info()
    print(type(freq))
    print(freq)

    details_list = []
    for i in freq['Topic']:
        if i > -1:
            details_list.append(topic_model.get_topic(i))
        else:
            details_list.append([])
    freq['details'] = details_list

    freq.to_csv('topics/{}_topics_{}.csv'.format(directory_name, nr_topics))
    print("saved to csv")

    return topic_model

#get tweets
directories =  ["nursetweets", "doctortweets", "teachertweets", "railtweets", "journalisttweets", "musiciantweets"]
df = get_all_tweets(directories[0])
print("tweet count", len(df))

#get tweet text
tweet_text = df['nouns'].astype(str).tolist()
print("got df")

#set up evaluation spreadsheet
data= {'nr_topics': [5, 10, 15, 20], 'topic_diversity': [None, None, None, None]}
evaluation_df = pd.DataFrame(data)
evaluation_df.set_index('nr_topics')
evaluation_df.to_csv("topics/topic_evaluation.csv")

#pre-compute embeddings
sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = sentence_model.encode(tweet_text, show_progress_bar=False)
model_5 = get_topics_from(directory_name="nursetweets", nr_topics=5, embeddings=embeddings)
model_10 = get_topics_from( directory_name="nursetweets", nr_topics=10, embeddings=embeddings)
model_15 = get_topics_from(directory_name="nursetweets", nr_topics=15, embeddings=embeddings)
model_20 = get_topics_from(directory_name="nursetweets", nr_topics=20, embeddings=embeddings)

#evaluation
metric = TopicDiversity(topk=10)
evaluation_df.at[5,'topic_diversity'] = metric.score(model_5)
evaluation_df.at[10,'topic_diversity'] = metric.score(model_10)
evaluation_df.at[15,'topic_diversity'] = metric.score(model_15)
evaluation_df.at[20,'topic_diversity'] = metric.score(model_20)

evaluation_df.to_csv("topics/topic_evaluation.csv")
