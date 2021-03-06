# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 16:00:09 2021

@author: harsh
"""

# ----------------------------------------------------
# Parse yahoo finance webpage 
# ----------------------------------------------------

import pandas as pd
from lxml import html
import requests


ROOT_WEBPAGE = 'https://finance.yahoo.com'

def get_tree(PAGE):
    page = requests.get(PAGE)
    tree = html.fromstring(page.content)
    return tree

tree = get_tree(ROOT_WEBPAGE)

# ---------------------------------------------------
# do what ever with the tree 


#crypto subsection



def get_attrib_list(tree_obj, XPATH, keep_tags):
    
    # XPATH = '//*[@id="data-util-col"]/section[3]/header/a'
    # keep_tags = ['href', 'title']
    
    buyers = tree_obj.xpath(XPATH)
    
    dir(buyers[0])
    attrib_dict = buyers[0].attrib
    
    attrib_df = pd.DataFrame(attrib_dict)
    attrib_df.columns = ['tag']
    attrib_df = attrib_df[attrib_df['tag'].isin(keep_tags)]
    attrib_df['desc'] = attrib_df['tag'].apply(lambda x : attrib_dict[x]) 
    attrib_df.set_index('tag', inplace=True)
    attrib_df = attrib_df.T
    
    return attrib_df

def get_subsection_link(item):
    section_link = f'//*[@id="data-util-col"]/section[{item}]/header/a'
    return section_link


coll_attribs = []
for i in range(1,12):
    try:
        coll_attribs.append(get_attrib_list(get_subsection_link(i), ['href', 'title']))
    except:
        pass
    
attrib_master = pd.concat(coll_attribs)
# ---------------------------------------------------



title_sel = 'Cryptocurrencies'


attrib_sel = attrib_master[attrib_master['title'] == title_sel]
attrib_link = attrib_sel['href'].values[0]


further_parse = f'{ROOT_WEBPAGE}{attrib_link}'
print(further_parse)



# ============================================================================
sub_tree = get_tree(further_parse)

get_attrib_list(tree_obj, XPATH, keep_tags)


ck = sub_tree.xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr[1]/td[1]')
ck = sub_tree.xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr[1]/td[1]/a')


dir(ck[0])

ck[0].text_content()

ck[0].attrib

f'{ROOT_WEBPAGE}{ck[0].attrib["href"]}'
