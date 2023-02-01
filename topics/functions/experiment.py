import os
from bertopic import BERTopic
import pandas as pd
from sentence_transformers import SentenceTransformer
from octis.evaluation_metrics.diversity_metrics import TopicDiversity

os.environ["TOKENIZERS_PARALLELISM"] = "false"

directories =  ["nursetweets", "doctortweets", "teachertweets", "railtweets", "journalisttweets", "musiciantweets"]
directory_index = 0

def get_all_tweets(directory = None):
    df = pd.DataFrame()
    for filename in os.listdir("Dissertation/"+directory):
        f = os.path.join("Dissertation/"+directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0)
        df = pd.concat([df, user_df], ignore_index=True)
    return df

def get_topics_from(directory_name = "nursetweets", embeddings=None, nr_topics = None):
    #set up model parameters
    topic_model = BERTopic(language="english",
                           calculate_probabilities=True,
                           verbose=True,
                           low_memory=False,
                           n_gram_range=(1, 1),
                           nr_topics = nr_topics
                           )
    print("set up topic model. about to fit model")

    #fit transform
    topics, probabilities = topic_model.fit_transform(tweet_text, embeddings)
    print("model has been fit")

    open("{}_test_model".format(directory_name,), 'w+')
    topic_model.save("{}_{}_model_".format(directory_name, nr_topics))
    print("model has been saved")

    freq = topic_model.get_topic_info()
    print(type(freq))
    print(freq)

    details_list = []
    for i in freq['Topic']:
        if i > -1:
            details_list.append([x for x,y in topic_model.get_topic(i)])
        else:
            details_list.append([])
    freq['details'] = details_list

    freq.to_csv('Dissertation/topics/{}_topics_{}.csv'.format(directory_name, nr_topics))
    print("info saved to csv")

    return topic_model

def get_tweets():
    df = get_all_tweets(directories[directory_index])
    print("tweet count", len(df))
    return df['nouns'].astype(str).tolist()

def get_embeddings():
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    return sentence_model.encode(tweet_text, show_progress_bar=False)


def pad_out_dict(dict):
    maxlength = 0
    for k in dict.keys():
        if len(dict[k])>maxlength:
            maxlength=len(dict[k])

    for k in dict.keys():
        if len(dict[k]) < maxlength:
            dict[k] = dict[k] + list([0] * (maxlength - len(dict[k])))

    return dict

def get_docs():
    model5docs = pd.DataFrame.from_dict(pad_out_dict(model_5.get_representative_docs())).sort_index(axis=1)
    model5docs.to_csv('Dissertation/topics/nursetweets_5_docs.csv')
    # model10docs = pd.DataFrame.from_dict(pad_out_dict(model_10.get_representative_docs())).sort_index(axis=1)
    # model10docs.to_csv('Dissertation/topics/nursetweets_10_docs.csv')
    # model15docs = pd.DataFrame.from_dict(pad_out_dict(model_15.get_representative_docs())).sort_index(axis=1)
    # model15docs.to_csv('Dissertation/topics/nursetweets_15_docs.csv')
    # model20docs = pd.DataFrame.from_dict(pad_out_dict(model_20.get_representative_docs())).sort_index(axis=1)
    # model20docs.to_csv('Dissertation/topics/nursetweets_20_docs.csv')

#get tweet text
tweet_text = get_tweets()
print("got df")

#pre-compute embeddings
embeddings = get_embeddings()
print("computing embeddings")

#get topics
print("getting topics ", "5")
model_5 = get_topics_from(directory_name="nursetweets", embeddings=embeddings, nr_topics = 20)
# print("getting topics ", "10")
# model_10 = get_topics_from(directory_name="nursetweets", nr_topics=10, embeddings=embeddings)
# print("getting topics ", "15")
# model_15 = get_topics_from(directory_name="nursetweets", nr_topics=15, embeddings=embeddings)
# print("getting topics for", "20")
# model_20 = get_topics_from(directory_name="nursetweets", nr_topics=20, embeddings=embeddings)

# get_docs()