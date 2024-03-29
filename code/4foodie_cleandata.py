#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[124]:


df = pd.read_csv('./data/foodie.csv',index_col=0)
df.fillna('',inplace=True)
df['mrt'] = df['mrt_tags'].apply(lambda x : x.split(','))


# In[139]:


df = df.loc[:271] #篩選時間區間


# In[158]:


map_dict = {
    '台北車站':[167,225],
    '中山':[167,254],
    '西門':[140,225],
    '龍山寺':[119,216],
    '三重':[100,257],
    '大直':[304,325],
    '劍南路':[325,332],
    '忠孝復興':[254,225],
    '忠孝敦化':[282,225],
    '大安':[254,183],
    '東門':[202,183],
    '士林':[167,352],
    '劍潭':[167,334],
    '圓山':[167,315],
    '松江南京':[217,254],
    '信義安和':[293,183],
    '中山國中':[279,277],
    '中山國小':[202,297],
    '古亭':[192,167],
    '中正紀念堂':[175,183],
    '忠孝新生':[215,225],
    '國父紀念館':[307,225],
    '新店':[236,21],
    '市政府':[332,225],
    '三民高中':[71,364],
    '蘆洲':[54,382],
    '台北101/世貿':[332,183],
    '松山':[365,254],
    '善導寺':[190,222],
    '行天宮':[217,276],
    '南京復興':[265,255],
    '新莊':[55,218],
    '公館':[222,137],
    '內湖':[425,334],
    '板橋':[72,163],
    '江子翠':[100,200],
    '雙連':[178,275],
    '南勢角':[169,57],
    '南京三民':[332,254],
    '六張犁':[280,141],
    '民權西路':[168,297],
    '北門':[142,249]
}


# In[159]:


res = pd.DataFrame()
for i in range(len(df)):
    for j in range(len(df['mrt'][i])):
        if df['mrt'][i][j] != "":
            data = df.loc[i]
            data['new_mrt'] = df['mrt'][i][j]
            data['X'] = map_dict[df['mrt'][i][j]][0]
            data['Y'] = map_dict[df['mrt'][i][j]][1]
            res = res.append(data)
res.reset_index(drop=True,inplace=True)


# In[161]:


res


# In[163]:


res.to_excel('4foodie_viz.xlsx',encoding='utf-8-sig',header=True)

