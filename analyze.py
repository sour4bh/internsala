#%%
import pandas as pd
import bokeh
import os
#%%
files = os.listdir('data/')
data = pd.read_csv('data.csv')
for f in files:
    data = data.append(pd.read_csv(os.path.join('data', f)), ignore_index=True)
data
# %%