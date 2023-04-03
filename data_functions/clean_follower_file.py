import os
import pandas as pd

directory = "teachertweets"
followers_df_name = "data/filteredNEUfollowers.csv"
followers_df = pd.read_csv(followers_df_name, error_bad_lines=False)
count_removed = 0

for index, row in followers_df.iterrows():
    f = "{}/{}.csv".format(directory, str(int(row["id"])))

    if not os.path.isfile(f):
        followers_df.drop(index=index, inplace=True)
        count_removed+=1

followers_df.to_csv(followers_df_name)
print(count_removed, "removed")

