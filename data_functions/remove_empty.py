#Remove tweet files that contained only RT's

import os
import pandas as pd

directory = "teachertweets"

followers_df_name = "data/filteredNEUfollowers.csv"

followers_df = pd.read_csv(followers_df_name)
count_removed = 0
for index, row in followers_df.iterrows():
    f = "{}/{}.csv".format(directory, str(int(row["id"])))
    if os.path.isfile(f):
        df = pd.read_csv(f)
        print(len(df))
        if len(df) == 0:
            count_removed+=1
            os.remove(f)
            followers_df.drop(index=index, inplace=True)

followers_df.to_csv(followers_df_name)
print(count_removed, "removed")
# for filename in os.listdir(directory):
#     f = os.path.join(directory, filename)
#
#     # checking if it is a file
#     if os.path.isfile(f):
#         df = pd.read_csv(f)
#         if len(df)==0:
#             os.remove(f)
