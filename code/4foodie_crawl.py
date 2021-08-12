#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import re


# In[3]:


#不顯示圖片
# chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)

#windows
# driver = webdriver.Chrome('./../chromedriver_win32 (7)/chromedriver.exe',chrome_options=chrome_options)
driver = webdriver.Chrome('./../chromedriver_win32 (7)/chromedriver.exe')
#mac
# driver = webdriver.Chrome('./../chromedriver 4',chrome_options=chrome_options)


# In[4]:


driver.get('https://google.com')
time.sleep(2)
with open('cookie.json', 'r', encoding='utf-8') as f: #ig帳號cookie
    cookie_dict = json.load(f)
    for c in cookie_dict:
        del c['httpOnly']
        del c['secure']
    for c in cookie_dict:
        driver.add_cookie(c)
driver.get('https://instagram.com')
# update cookies
with open('cookie.json', 'w', encoding='utf-8') as f:
    json.dump(driver.get_cookies(), f)


# In[10]:


#每則貼文
def crawl_post_info(scroll_times):
    time.sleep(2)
    post_len = [0,0]

    ele_arr = dict()
    ele_arr['lc_ele'] = []
    ele_arr['url_ele'] = []

    result = dict()
    result['l_c'] = []
    result['url'] = []

    #get post like & comments
    post_ele = driver.find_elements_by_class_name("eLAPa")
    #get post url
    url_ele = driver.find_elements_by_css_selector(".v1Nh3.kIKUG._bz0w a")

    ele_arr['lc_ele'].extend(post_ele)
    ele_arr['url_ele'].extend(url_ele)

    for lc,u in zip(ele_arr['lc_ele'],ele_arr['url_ele']):
        #likes and comments
        hover = ActionChains(driver).move_to_element(lc)
        hover.perform()
        result['l_c'].append(lrv_counter())
        #url
        result['url'].append(u.get_attribute('href'))

    for i in range(scroll_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        #likes and comments
        post_ele = driver.find_elements_by_class_name("eLAPa")
        new_post_ele = [x for x in post_ele if x not in ele_arr['lc_ele']]
        ele_arr['lc_ele'].extend(new_post_ele)
        #url
        url_ele = driver.find_elements_by_css_selector(".v1Nh3.kIKUG._bz0w a")
        new_url_ele = [x for x in url_ele if x not in ele_arr['url_ele']]
        ele_arr['url_ele'].extend(new_url_ele)

        post_len.append(len(ele_arr['lc_ele']))
        print(post_len[-1],end=',')

        for lc,u in zip(new_post_ele,new_url_ele):
            #likes and comments
            hover = ActionChains(driver).move_to_element(lc)
            hover.perform()
            result['l_c'].append(lrv_counter())
            #url
            result['url'].append(u.get_attribute('href'))

        if post_len[i+2] == post_len[i]:
            break
    print('done')
    return result


# In[13]:


#每則貼文
def get_post_link(scroll_times):
    post_len = [0,0]

    ele_arr = []
    result = []

    #get post like & comments
    post_ele = driver.find_elements_by_class_name("eLAPa")
    #get post url
    url_ele = driver.find_elements_by_css_selector(".v1Nh3.kIKUG._bz0w a")

#     ele_arr['lc_ele'].extend(post_ele)
    ele_arr.extend(url_ele)

    for u in ele_arr:
        #likes and comments
#         hover = ActionChains(driver).move_to_element(lc)
#         hover.perform()
#         result['l_c'].append(lrv_counter())
        #url
        result.append(u.get_attribute('href'))

    for i in range(scroll_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        #likes and comments
#         post_ele = driver.find_elements_by_class_name("eLAPa")
#         new_post_ele = [x for x in post_ele if x not in ele_arr['lc_ele']]
#         ele_arr['lc_ele'].extend(new_post_ele)
        #url
        url_ele = driver.find_elements_by_css_selector(".v1Nh3.kIKUG._bz0w a")
        new_url_ele = [x for x in url_ele if x not in ele_arr]
        ele_arr.extend(new_url_ele)

        post_len.append(len(ele_arr))
        print(post_len[-1],end=',')

        for u in new_url_ele:
            #likes and comments
#             hover = ActionChains(driver).move_to_element(lc)
#             hover.perform()
#             result['l_c'].append(lrv_counter())
            #url
            result.append(u.get_attribute('href'))

        if post_len[i+2] == post_len[i]:
            break
    print('done')
    return result


# In[25]:


def getPostcontent(link_list):
    post_content = []
    for l in link_list:
        driver.get(l)
        post_content.append(driver.find_elements_by_css_selector('.C4VMK span')[1].text)
    return(post_content)


# In[154]:


driver.get('https://www.instagram.com/4foodie/')


# In[155]:


result = get_post_link(50)


# In[156]:


link_list = result


# In[158]:


list1 = link_list[:150]
list2 = link_list[150:300]
list3 = link_list[300:450]
list4 = link_list[450:]


# In[162]:


result1 = getPostcontent(list1)
result2 = getPostcontent(list2)
result3 = getPostcontent(list3)
result4 = getPostcontent(list4)


# In[172]:


post_result = result1+result2+result3+result4


# In[173]:


len(post_result)


# In[23]:


mrt_list = ['動物園','木柵','萬芳社區','萬芳醫院','辛亥','麟光','六張犁','科技大樓','大安','忠孝復興','南京復興','中山國中','松山機場','大直','劍南路','西湖','港墘','文德','內湖','大湖公園','葫洲','東湖','南港軟體園區','南港展覽館','象山','台北101/世貿','信義安和','大安','大安森林公園','東門','中正紀念堂','台大醫院','台北車站','中山','雙連','民權西路','圓山','劍潭','士林','芝山','明德','石牌','唭哩岸','奇岩','北投','新北投','復興崗','忠義','關渡','竹圍','紅樹林','淡水','新店','新店區公所','七張','小碧潭','大坪林','景美','萬隆','公館','台電大樓','古亭','中正紀念堂','小南門','西門','北門','中山','松江南京','南京復興','台北小巨蛋','南京三民','松山','南勢角','景安','永安市場','頂溪','古亭','東門','忠孝新生','松江南京','行天宮','中山國小','民權西路','大橋頭','台北橋','菜寮','三重','先嗇宮','頭前庄','新莊','輔大','丹鳳','迴龍','三重國小','三和國中','徐匯中學','三民高中','蘆洲','頂埔','永寧','土城','海山','亞東醫院','府中','板橋','新埔','江子翠','龍山寺','西門','台北車站','善導寺','忠孝新生','忠孝復興','忠孝敦化','國父紀念館','市政府','永春','後山埤','昆陽','南港','南港展覽館,']


# In[175]:


content_list = post_result


# In[176]:


final = []
for c in content_list:
    res = []
    for m in mrt_list: 
        se = re.search(m,c)
        if se:
            res.append(se.group())
#     print(res)
    final.append(set(res))


# In[182]:


foodie_df = pd.DataFrame()
foodie_df['post_link'] = link_list
foodie_df['content'] = content_list
foodie_df['mrt_tags'] = final
foodie_df


# In[183]:


for i in range(len(foodie_df['mrt_tags'])):
    string = ''
#     print(foodie_df['mrt_tags'][i])
    c = 0
    for t in foodie_df['mrt_tags'][i]:  
        if c == 0:
            string += t
        else : string += ',' + t 
        c+=1
    foodie_df['mrt_tags'][i] = string


# In[185]:


foodie_df.to_csv('./data/4foodie.csv',encoding = 'utf-8-sig')


# In[ ]:


#driver.close()

