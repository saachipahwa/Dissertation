import os
import pandas as pd

# #get number of followers
# df = pd.read_csv("data/NUJfollowers.csv")
# print(len(df))

#get mean number of tweets
directories = ["nursetweets", "doctortweets", "teachertweets",
               "railtweets", "journalisttweets", "musiciantweets"]
directory_index = 2

def get_mean(directory=directories[directory_index]):
    df = pd.DataFrame()
    user_count=0
    for filename in os.listdir(directory):
        user_count+=1
        f = os.path.join(directory, filename)
        user_df = pd.read_csv(f, index_col=0)
        df = pd.concat([df, user_df], ignore_index=True)
    total_count = len(df)
    print("total", total_count)
    mean = total_count/user_count
    print("user", user_count)
    print("mean", mean)
    print("mean per day", mean/1308)
    return mean

get_mean()

def variance(data):
    # Number of observations
    n = len(data)
    # Mean of the data
    mean = sum(data) / n
    # Square deviations
    deviations = [(x - mean) ** 2 for x in data]
    # Variance
    variance = sum(deviations) / n
    return variance

def get_variance(directory=directories[directory_index]):
    df = pd.DataFrame()
    user_count = 0
    lengths = []
    # total_squares = 0
    for filename in os.listdir(directory):
        user_count += 1
        f = os.path.join(directory, filename)
        user_df = pd.read_csv(f, index_col=0)
        lengths.append(len(user_df))
        df = pd.concat([df, user_df], ignore_index=True)
    var = variance(lengths)
    print("var", var)
    print("var per day", var/1308)


get_variance()
