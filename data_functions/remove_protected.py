#Remove tweet files of private accounts (/remove empty tweet files)
import os

import pandas as pd

#To remove tweet files of bots or private users
#This is done in filter_following for rail workers, musicians and journalists

directory = "teachertweets"
df = pd.read_csv("data/bots/privateNEUfollowers.csv")
private_IDs = list(df['id'].astype(int).astype(str))
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        id = filename[:-4]
        if id in private_IDs:
            try:
                os.remove(f)
            except OSError as e: # name the Exception `e`
                print("Failed with:", e.strerror) # look what it says
                print("Error code:", e.code)
