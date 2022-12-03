import os

import pandas as pd

directory = "nursetweets"

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        df = pd.read_csv(f)
        lastrow = df.iloc[-1]
        date = lastrow["created_at"]
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]
        print("year: " + year)
        print("month: " + month)
        print("day: " + day)
        # if int(year) < 2022:
        #     os.remove(f)
        # if int(year) == 2022 and int(month)<8:
        #     os.remove(f)
