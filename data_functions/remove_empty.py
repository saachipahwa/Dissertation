#Remove user files that are empty

import os
import pandas as pd

directory = "nursetweets"

followers_df_name = "data/filteredRCONfollowers.csv"

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
    else:
        count_removed+=1
        followers_df.drop(index=index, inplace=True)

followers_df.to_csv(followers_df_name)
print(count_removed, "removed")

