# %%
import requests
import time
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd
# %%
tags = pd.read_csv('tags.csv')
data = pd.read_csv('data.csv')
tags
# %%
def get_page_data(soup, data, tag):
    internships = soup.find_all('div', 'internship_meta')
    if 'Sorry, We couldn\'t find internships matching your requirements.' in internships[0].get_text():
        return (False, False)
    for post in internships:
        txt = lambda elem: elem.get_text().strip()
        txt0 = lambda elem: txt(elem).split()[0]
        meta = dict(zip(['Profile', 'Company', 'Location'],
                        map(txt, post.find_all('a'))))
        meta.update(dict(zip(map(txt0, post.find_all('th')), map(txt, post.find_all('td')))))
        meta['Tag'] = tag
        meta['Link'] = post.find('a')['href']
        # pprint(meta)
        data = data.append(pd.DataFrame(meta, index=[0]), ignore_index=True)
    return True, data
#%%
t0 = time.time()
page_link = lambda tag_link, j: tag_link + '/page-' + str(j)
for i in range(tags.shape[0]):
    data = pd.read_csv('data.csv')
    link = tag_link = tags.iloc[i]['link']
    tag = tags.iloc[i]['tag']
    print('\n' + tag)
    j = 1
    while True:
        soup = BeautifulSoup(requests.get(link).content, 'lxml')
        response = get_page_data(soup, data, tag)
        if response[0]:
            link = page_link(tag_link, j)
            data = response[1]
            print('new data appenend', j)
            j +=1
        else: 
            print('reached end of pages', j)
            break
        if j > 10:
            time.sleep(1)
    time.sleep(1)
    data.to_csv(f'data/{tag}.csv')
    print('Elapsed time', (time.time() - t0)/60, 'mins')
elapsed_time = time.time() - t0
print(elapsed_time)
# %%
# %%
