import pandas as pd
import glob, sys, os
import matplotlib.pyplot as plt
import datetime
import numpy as np

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)
print('hello now')


print('starting analysis')
logs = glob.glob('log_sub_h*.out')
TAG = "# starting loop"
for log in logs:
    clog = 'cleaned_' + log
    tag_found = False
    with open(log) as in_file:
        with open(clog, 'w') as out_file:
            for line in in_file:
                if not tag_found:
                    if line.strip() == TAG:
                        tag_found = True
                else:
                    out_file.write(line)
    df = pd.read_csv(clog,header=None, comment = '#',names=["topic", "type", "ID", "mesg No.", "pub time","recv time","prog time", "loop time"])
    # df['pub time'] = df['pub time'].apply(lambda x: datetime.datetime.strptime(x, '%H:%M:%S.%f'))
    # df['recv time'] = df['recv time'].apply(lambda x: datetime.datetime.strptime(x, '%H:%M:%S.%f'))
    df['pub time s'] = df['pub time'].apply(lambda x: float(x.split(':')[2]))
    df['recv time s'] = df['recv time'].apply(lambda x: float(x.split(':')[2]))
    df['loop time s'] = df['loop time'].apply(lambda x: float(x.split(':')[2]))
    df['end-to-end'] = (df['recv time s']-df['pub time s'] ).astype('float')  #timedelta64[ms]
    print(log)
    print(df.head())
    p90 = str(round(np.percentile(df['end-to-end'].to_numpy(), 90),5))
    p95 = str(round(np.percentile(df['end-to-end'].to_numpy(), 95),5))
    p99 = str(round(np.percentile(df['end-to-end'].to_numpy(), 99),5))
    line = log + ',' + p90 + ',' + p95 + ',' + p99  + '\n'
    with open('metrics.csv','a+') as fout:
        fout.write(line)
    try:
        plt.figure()
        df['end-to-end'].plot()
        unsorted = df['end-to-end'].to_numpy()
        sorted_d = np.sort(unsorted)
        t = range(len(sorted_d))
        fig, ax = plt.subplots()
        ax.plot(t, unsorted, 'r',label='Unsorted') # plotting t, a separately 
        ax.plot(t, sorted_d, label='Sorted Asc') # plotting t, b separately 
        # df['end-to-end'].sort_values(by=['end-to-end'], axis=0, ascending=True).plot()
        legend = ax.legend(loc='upper center', shadow=True, fontsize='x-large')
        # Put a nicer background color on the legend.
        # legend.get_frame().set_facecolor('C0')
        plt.title('Message Transit Time (s)')
        plt.ylabel('Time (s)')
        plt.xlabel('Message Number')
        plt.savefig(log + '_end-to-end.png')
    except Exception as e:
        print(e)
        print(df['loop time'])
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)