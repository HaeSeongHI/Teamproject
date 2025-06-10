import matplotlib.pyplot as plt
from pathlib import Path
import json

data_file = Path('satisfaction_data.json')

with data_file.open('rt') as df:
    loaded = json.load(df)

dict1 = loaded[0] 
dict2 = loaded[1]
dict3 = loaded[2]

dict1v = [x for x in loaded[0].values()]
print(dict1v)
dict2v = [x for x in loaded[1].values()]
dict3v = [x for x in loaded[2].values()]

x_data = ['Worst', 'Bad', "Usual", "Good", "Best"]
fig,ax = plt.subplots(1,3)

ax[0].bar(x_data, dict1v, alpha = 0.5, color = 'red')
ax[1].bar(x_data, dict2v, alpha = 0.5, color = 'blue')
ax[2].bar(x_data, dict3v, alpha = 0.5, color = 'yellow')

ax[0].set_title('rec result')
ax[1].set_title('interface')
ax[2].set_title('speed')


plt.show()