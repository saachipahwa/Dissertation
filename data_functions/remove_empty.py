#Remove tweet files that contained only RT's

import os
import pandas as pd

directory = "railtweets"

followers_df_name = "data/filteredRMTfollowers.csv"

followers_df = pd.read_csv(followers_df_name)

def remove_empty():
    count_removed=0
    for index, row in followers_df.iterrows():
        f = "{}/{}.csv".format(directory, str(int(row["id"])))
        if os.path.isfile(f):
            df = pd.read_csv(f)
            if len(df) == 0:
                count_removed+=1
                os.remove(f)
                print("removed file", f)
        else:
            followers_df.drop(labels=[index],axis=0, inplace=True)
            print("dropped", index, str(int(row["id"])))

    followers_df.to_csv(followers_df_name)
    print(count_removed, "removed")

remove_empty()

def print_empty():
    for index, row in followers_df.iterrows():
        f = "{}/{}.csv".format(directory, str(int(row["id"])))
        if os.path.isfile(f):
            df = pd.read_csv(f)
            if len(df) == 0:
                print(f)


# print_empty()


# for filename in os.listdir(directory):
#     f = os.path.join(directory, filename)
#
#     # checking if it is a file
#     if os.path.isfile(f):
#         df = pd.read_csv(f)
#         if len(df)==0:
#             os.remove(f)
