from bertopic import BERTopic

for nr_topics in [5,10,15,20]:
    for ul_ngram in range(1,4): #upper limit of ngram range
        #load model
        topic_model = BERTopic.load("nursetweets_{}_{}_model".format(nr_topics, ul_ngram))
        freq = topic_model.get_topic_info()
        details_list = []
        for i in freq['Topic']:
            details_list.append([x for x,y in topic_model.get_topic(i)])

        freq['details'] = details_list
        freq.to_csv('Dissertation/topics/nursetweets_topics_{}_{}.csv'.format(nr_topics, ul_ngram))
        print("info saved to csv")