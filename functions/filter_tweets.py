import os

import pandas as pd

directory = "nursetweets"

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(f)
        df = pd.read_csv(f)
        print("Length of df: " + str(len(df)))
        df['text'] = df['text'].loc[~df['text'].str.startswith('RT ', na=False)] #remove RT's
        df.to_csv(f)
        print("Length of df: " + str(len(df)))

