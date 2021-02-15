import pandas as pd
import glob

logs = glob.glob('log_sub_*.out')
for log in logs:
    df = pd.read_csv(log,header=None, comment = '#',names=["topic", "type", "ID", "mesg No.", "pub time","recv time","prog time", "loop time"])
    print(log)
    print(df.head())