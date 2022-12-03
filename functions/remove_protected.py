#Remove tweet files of private accounts (/remove empty tweet files)
import os

import pandas as pd

directory = "nursetweets"
df = pd.read_csv("data/privateRCONfollowers.csv")
private_IDs = list(df['id'].astype(int).astype(str))
print(private_IDs)
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
