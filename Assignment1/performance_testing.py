import pandas as pd

df = pd.read_csv('log_sub_6_topic2.out',header=None, comment = '#',names=["topic", "type", "ID", "pub time","recv time","prog time", "loop time"])
print(df.head())