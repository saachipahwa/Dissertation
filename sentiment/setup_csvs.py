import pandas as pd


directories = ["nursetweets", "doctortweets", "teachertweets",
               "railtweets", "journalisttweets", "musiciantweets"]
directory_index = 4
directory_name = directories[directory_index]
profession_name = "journalist"
nr_topics = 15

#Getting docs for different time periods
def get_before_lockdown():
    df = pd.read_csv(f"Dissertation/sentiment/{profession_name}s_csvs/docs_sentiment.csv")

    #get index range for 46 days before first lockdown
    # df_startdate = df[df['created_at'].str.match("2020-02-09")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-03-25")]
    # print(df_enddate)

    #get index range for 27 days before second lockdown
    # df_startdate = df[df['created_at'].str.match("2020-10-09")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-11-04")]
    # print(df_enddate)

    #get index range for 62 days before third lockdown
    # df_startdate = df[df['created_at'].str.match("2020-11-06")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2021-01-05")]
    # print(df_enddate)

    # make docs csv of first lockdown 8938 to 10838
    before_first_lockdown = df.iloc[1428:1718]
    before_first_lockdown.to_csv(f"Dissertation/sentiment/{profession_name}s_csvs/before_first_lockdown.csv")

    # make docs csv of second lockdown 23578 to 25516
    before_second_lockdown = df.iloc[3123:3389]
    before_second_lockdown.to_csv(f"Dissertation/sentiment/{profession_name}s_csvs/before_second_lockdown.csv")

    # make docs csv of third lockdown 25613 to 30528
    before_third_lockdown = df.iloc[3405:3979]
    before_third_lockdown.to_csv(f"Dissertation/sentiment/{profession_name}s_csvs/before_third_lockdown.csv")

get_before_lockdown()

def get_lockdown_tweets():
    df = pd.read_csv(f"Dissertation/sentiment/{profession_name}s_csvs/docs_sentiment.csv")

    #sorting by date and adding new index
    # df.sort_values(by='created_at', inplace=True)
    # df.reset_index(drop=True, inplace=True)
    # df.to_csv("Dissertation/graphs/topics_with_dates.csv")

    # #find indexes for start and end dates of lockdown periods
    # #confirm first lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2020-03-26")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-05-10")] #46 days
    # print(df_enddate)
    #
    # #confirm second lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2020-11-05")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-12-02")] #28 days
    # print(df_enddate)
    #
    # #confirm third lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2021-01-06")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2021-03-08")] #62 days
    # print(df_enddate)

    # first lockdown 10839 to 13703
    first_lockdown = df.iloc[1718:1968]
    first_lockdown.to_csv(f"Dissertation/sentiment/{profession_name}s_csvs/first_lockdown.csv")
    #
    # #second lockdown 25517 to 27893
    second_lockdown = df.iloc[3389:3657]
    second_lockdown.to_csv(f"Dissertation/sentiment/{profession_name}s_csvs/second_lockdown.csv")
    #
    # #third lockdown 30529 to 37921
    third_lockdown = df.iloc[3979:4683]
    third_lockdown.to_csv(f"Dissertation/sentiment/{profession_name}s_csvs/third_lockdown.csv")
    # print(third_lockdown[third_lockdown['Topic']==2])

get_lockdown_tweets()

def get_after_lockdown():
    df = pd.read_csv(f"Dissertation/sentiment/{profession_name}s_csvs/docs_sentiment.csv")

    #get index range for 46 days after first lockdown
    # df_startdate = df[df['created_at'].str.match("2020-05-11")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-06-18")]
    # print(df_enddate)


    #get index range for 27 days after second lockdown
    # df_startdate = df[df['created_at'].str.match("2020-12-03")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-12-29")]
    # print(df_enddate)


    #get index range for 62 days after third lockdown
    # df_startdate = df[df['created_at'].str.match("2021-03-09")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2021-06-09")]
    # print(df_enddate)

    # make docs csv of first lockdown 13704 to 16139
    before_first_lockdown = df.iloc[1968:2242]
    before_first_lockdown.to_csv(f"Dissertation/sentiment/{profession_name}s_csvs/after_first_lockdown.csv")

    # make docs csv of second lockdown 27894 to 29883
    before_second_lockdown = df.iloc[3657:3894]
    before_second_lockdown.to_csv(f"Dissertation/sentiment/{profession_name}s_csvs/after_second_lockdown.csv")

    # make docs csv of third lockdown 37922 to 47140
    before_third_lockdown = df.iloc[4683:5825]
    before_third_lockdown.to_csv(f"Dissertation/sentiment/{profession_name}s_csvs/after_third_lockdown.csv")

get_after_lockdown()

