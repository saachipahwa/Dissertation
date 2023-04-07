import os
from bertopic import BERTopic
import pandas as pd
from sentence_transformers import SentenceTransformer
from octis.evaluation_metrics.diversity_metrics import TopicDiversity

os.environ["TOKENIZERS_PARALLELISM"] = "false"

directories = ["nursetweets", "doctortweets", "teachertweets",
               "railtweets", "journalisttweets", "musiciantweets"]
directory_index = 3
directory_name = directories[directory_index]
profession_name = "rail"

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


def get_embeddings(tweet_text):
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    return sentence_model.encode(tweet_text, show_progress_bar=False)


def get_topics_from(directory_name=directory_name, embeddings=None, nr_topics=None, ngram_max=1):
    # set up model parameters
    topic_model = BERTopic(language="english",
                           calculate_probabilities=False,
                           verbose=True,
                           low_memory=True,
                           n_gram_range=(1, ngram_max),
                           nr_topics=nr_topics
                           )
    print("set up topic model. about to fit model")

    # fit transform
    topics, probabilities = topic_model.fit_transform(tweet_text, embeddings)
    print("model has been fit")

    # save model
    open("{}_{}_{}_model".format(directory_name, nr_topics, ngram_max), 'w+')
    topic_model.save("{}_{}_{}_model".format(
        directory_name, nr_topics, ngram_max))
    print("model has been saved", nr_topics, ngram_max)

    # get details of topics
    freq = topic_model.get_topic_info()
    print(freq)

    # save details to csv
    details_list = []
    for i in freq['Topic']:
        details_list.append([x for x, y in topic_model.get_topic(i)])

    freq['details'] = details_list
    freq.to_csv(
        'Dissertation/topics/{}_docs/{}_topics_{}_{}.csv'.format(profession_name, directory_name, nr_topics, ngram_max))
    print("info saved to csv")

    return topic_model


def pad_out_dict(dict):
    maxlength = 0
    for k in dict.keys():
        if len(dict[k]) > maxlength:
            maxlength = len(dict[k])

    for k in dict.keys():
        if len(dict[k]) < maxlength:
            dict[k] = dict[k] + list([0] * (maxlength - len(dict[k])))

    return dict


# get tweet text
tweet_text = get_tweets()
print("got df")

# pre-compute embeddings
embeddings = get_embeddings(tweet_text)
print("computing embeddings")

# get topics
print("getting topics ", "5")
model_5 = get_topics_from(
    directory_name=directory_name, embeddings=embeddings, nr_topics=5, ngram_max=1)

print("getting topics ", "10")
model_10 = get_topics_from(directory_name=directory_name,  embeddings=embeddings, nr_topics=10, ngram_max=1)

print("getting topics ", "15")
model_15 = get_topics_from(
    directory_name=directory_name, embeddings=embeddings, nr_topics=15, ngram_max=1)

print("getting topics ", "20")
model_20 = get_topics_from(
    directory_name=directory_name,  embeddings=embeddings, nr_topics=20, ngram_max=1)

model5_docs = pd.DataFrame.from_dict(pad_out_dict(model_5.get_representative_docs())).sort_index(axis=1)
model5_docs.to_csv(f'Dissertation/topics/{profession_name}_docs/5.csv')

model10_docs = pd.DataFrame.from_dict(pad_out_dict(model_10.get_representative_docs())).sort_index(axis=1)
model10_docs.to_csv(f'Dissertation/topics/{profession_name}_docs/10.csv')

model15_docs = pd.DataFrame.from_dict(pad_out_dict(model_15.get_representative_docs())).sort_index(axis=1)
model15_docs.to_csv(f'Dissertation/topics/{profession_name}_docs/15.csv')

model20_docs = pd.DataFrame.from_dict(pad_out_dict(model_20.get_representative_docs())).sort_index(axis=1)
model20_docs.to_csv(f'Dissertation/topics/{profession_name}_docs/20.csv')
