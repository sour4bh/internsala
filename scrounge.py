# %%
import requests
import time
from pprint import pprint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# %%
driver_path = 'driver/chromedriver.exe'
options = Options()
# options.add_argument('start-maximized')
# options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-extensions')
options.headless = True
driver = webdriver.Chrome(driver_path, options=options)
# %%

tags = pd.read_csv('tags.csv')
data = pd.read_csv('data.csv')
# %%
def get_page_data(data, cateogry):
    container_list = driver.find_element_by_id('internship_list_container')
    internships = container_list.find_elements_by_css_selector('div.internship_meta')
    if 'Sorry, We couldn\'t find internships matching your requirements.' in internships[0].text:
        return (False, False)
    for post in internships:
        def txt(elem): return elem.text
        def txt0(elem): return txt(elem).split()[0]
        meta = dict(zip(['Profile', 'Company', 'Location'],
                        map(txt, post.find_elements_by_tag_name('a'))))
        meta.update(dict(zip(map(txt0, post.find_elements_by_tag_name(
            'th')), map(txt, post.find_elements_by_tag_name('td')))))
        # pprint(meta)
        # meta['Data'] = post.text
        meta['Category'] = cateogry
        meta['Link'] = post.find_element_by_tag_name('a').get_attribute('href')
        data = data.append(pd.DataFrame(meta, index=[0]), ignore_index=True)
    return True, data
#%%
page_link = lambda tag_link, j: tag_link + '/page-' + str(j)
for i in range(tags.shape[0]):
    data = pd.read_csv('data.csv')
    j = 1
    link = tag_link = tags.iloc[i]['link']
    tag = tags.iloc[i]['tag']
    print('\n' + tag)
    while j < 20:
        driver.get(link)
        response = get_page_data(data, tag)
        if response[0]:
            link = page_link(tag_link, j)
            data = response[1]
            print('new data appenend', j)
            j +=1
        else: 
            print('reached end of pages', j)
            break
        time.sleep(2)
    data.to_csv(f'data/{tag}.csv')

    # %%
