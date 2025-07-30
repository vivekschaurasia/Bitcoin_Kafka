import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn


df = pd.read_csv("bitcoin.csv")


df = df.drop(['Adj Close'], axis=1) #Removing it because "Adj Close" and "close have the same value"


features = ['Open', 'High', 'Low', 'Close']

plt.subplots(figsize=(20,10))
for i, col in enumerate(features):
  plt.subplot(2,2,i+1)
  seaborn.distplot(df[col])
plt.show()


"""
print(df.head(2))
         Date        Open        High         Low       Close   Adj Close    Volume
0  2014-09-17  465.864014  468.174011  452.421997  457.334015  457.334015  21056800
1  2014-09-18  456.859985  456.859985  413.104004  424.440002  424.440002  34483200


print(df.describe())

               Open          High           Low         Close     Adj Close        Volume
count   2713.000000   2713.000000   2713.000000   2713.000000   2713.000000  2.713000e+03
mean   11311.041069  11614.292482  10975.555057  11323.914637  11323.914637  1.470462e+10
std    16106.428891  16537.390649  15608.572560  16110.365010  16110.365010  2.001627e+10
min      176.897003    211.731003    171.509995    178.102997    178.102997  5.914570e+06
25%      606.396973    609.260986    604.109985    606.718994    606.718994  7.991080e+07
50%     6301.569824   6434.617676   6214.220215   6317.609863   6317.609863  5.098183e+09
75%    10452.399414  10762.644531  10202.387695  10462.259766  10462.259766  2.456992e+10
max    67549.734375  68789.625000  66382.062500  67566.828125  67566.828125  3.509679e+11

"""

