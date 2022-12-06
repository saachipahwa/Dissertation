#Remove tweet files that contained only RT's

import os
import pandas as pd

directory = "doctortweets"

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)

    # checking if it is a file
    if os.path.isfile(f):
        df = pd.read_csv(f)
        if len(df)==0:
            os.remove(f)
