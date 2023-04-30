#Remove tweet files that contained only RT's

import os
import pandas as pd

directory = "nursetweets_og"

followers_df_name = "data/filteredRMTfollowers.csv"

# followers_df = pd.read_csv(followers_df_name)
# count_removed = 0
# for index, row in followers_df.iterrows():
#     f = "{}/{}.csv".format(directory, str(int(row["id"])))
#     if os.path.isfile(f):
#         df = pd.read_csv(f)
#         print(len(df))
#         if len(df) == 0:
#             count_removed+=1
#             os.remove(f)
#             followers_df.drop(index=index, inplace=True)
#     else:
#         count_removed+=1
#         followers_df.drop(index=index, inplace=True)
#
# followers_df.to_csv(followers_df_name)
# print(count_removed, "removed")

count_removed=0
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        df = pd.read_csv(f)
        print(f)
        print(len(df))
        if len(df) == 0 or len(df)==1:
            os.remove(f)
        else:
            lastrow = df.iloc[-1]
            date = lastrow["created_at"]
            year = date[0:4]
            month = date[5:7]
            day = date[8:10]
            print("year: " + year)
            print("month: " + month)
            print("day: " + day)
            if int(year) < 2022:
                os.remove(f)
                count_removed+=1
            elif int(year) == 2022 and int(month)<4:
                os.remove(f)
                count_removed+=1
print(count_removed)