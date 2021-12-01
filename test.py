from os import close
import pandas as pd
from datetime import datetime
# ts = int('1284101485')

df = pd.read_csv('example_stats_history.csv')

# print(df.iloc[0][0])
ts = int(df.iloc[0][0])
file1 = open('beginTime.txt', 'w')
begin = (datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:00'))
print(begin)
file1.write(begin)
file1.close()


ts = int(df.iloc[-1][0])
file1 = open('closeTime.txt','w')
close = (datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:00'))
print(close)
file1.write(close)
file1.close()
