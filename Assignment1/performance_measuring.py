import pandas as pd
import glob
import matplotlib.pyplot as plt
import datetime

logs = glob.glob('log_sub_*.out')
for log in logs:
    df = pd.read_csv(log,header=None, comment = '#',names=["topic", "type", "ID", "mesg No.", "pub time","recv time","prog time", "loop time"])
    # df['pub time'] = df['pub time'].apply(lambda x: datetime.datetime.strptime(x, '%H:%M:%S.%f'))
    # df['recv time'] = df['recv time'].apply(lambda x: datetime.datetime.strptime(x, '%H:%M:%S.%f'))
    df['pub time s'] = df['pub time'].apply(lambda x: float(x.split(':')[2]))
    df['recv time s'] = df['recv time'].apply(lambda x: float(x.split(':')[2]))
    df['loop time s'] = df['loop time'].apply(lambda x: float(x.split(':')[2]))
    df['end-to-end'] = (df['pub time s'] -df['recv time s']).astype('timedelta64[ms]')
    print(log)
    print(df.head())
    try:
        # plt.figure()
        # df['loop time'].plot()
        # plt.savefig(log + '_loop_time.png')
        plt.figure()
        df['end-to-end'].plot()
        plt.savefig(log + '_end-to-end.png')
    except Exception as e:
        print(e)
        print(df['loop time'])