# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # 1. Library Setting

import pandas as pd
import json
import requests

pd.set_option('display.max_columns', None) # 데이터프레임 출력 시 컬럼수 최대
pd.set_option('display.max_rows', None) # 데이터프레임 출력 시 행수 최대

# ## 1-1. read_json

pd.read_json('[{"A" : 1, "B" : 2}, {"A" : 3, "B" : 4}]')

# # 2. Get JSON

# ## 2-1. Load JSON

# * 둘 중 뭘로 불러도 크게 속도 차이 없음

file = open("C:/Users/HOME/Dropbox/dataset/used/perf-history/raw_nyc_phil.json",'r')
json_file = json.load(file)

with open("C:/Users/HOME/Dropbox/dataset/used/perf-history/raw_nyc_phil.json",'r') as json_file :
    json_sample = json.load(json_file)

# ## 2-2. KEY1

json_sample.keys()

json_sample.values()

# ## 2-3. KEY2

json_sample['programs'].keys()

type(json_sample['programs'])

len(json_sample['programs'])

type(json_sample['programs'][0])

json_sample['programs'][0].keys()

type(json_sample['programs'][0]['works'])

json_sample['programs'][0]['works'][0]

json_sample['programs'][0].values()

# # 3. JSON DECODE1. JSON_NORMALIZE

# ## 3-1. simple_load

json_data = pd.json_normalize(json_sample['programs'])

json_data.info()

json_data.shape

json_data.head(1)

len(json_data.head(1)['works'][0])

len(json_data.head(1)['concerts'][0])

# ## 3-2. Get_Works

works_data = pd.json_normalize(data=json_sample['programs'],
                            record_path = 'works',
                           meta=['season', 'orchestra', 'programID', 'id'])

works_data.head(3)

works_data.rename(columns = { 'ID': 'workTitle_ID', 'id' : 'work_ID'}, inplace=True)

works_data.head(1)

works_data.drop.drop_duplicates().shape

# ## 3-3. Get_concerts

concerts_data = pd.json_normalize(data=json_sample['programs'],
                            record_path = 'concerts',
                           meta=['programID', 'id'])

concerts_data.head()

concerts_data.rename(columns = {'id' : 'work_ID'}, inplace=True)

concerts_data.shape

len(concerts_data.work_ID.unique())

concerts_group1 = concerts_data.groupby('work_ID')['programID'].size().reset_index()
concerts_group2 = concerts_data.groupby('programID')['work_ID'].size().reset_index()

print(len(concerts_group1.loc[(concerts_group1.programID > 1)]))
print(len(concerts_group2.loc[(concerts_group2.work_ID > 1)]))

# ## 3-4. Get_soloists

soloists_data = pd.json_normalize(data=json_sample['programs'],
                                  record_path=['works', 'soloists'],
                                  meta=['ID', 'programID'])

# * 뭔가 마음 같지가 않다.
#     * record_path : 말 그대로 path일 뿐이다. 그래서, ID값이 키에 없는 것

# # 4. Make soloists data

# ## 4-1. Check_Unique Key

works_data['workTitle_ID'].value_counts()

len(works_data.loc[(works_data.workTitle_ID == '0*'), 'work_ID'].unique())

# * 유니크 키로 구분하기 위해서는 worktitle_ID와 work_ID 모두가 필요

# ## 4-2. preprocessing

# ### 4-2-1. dict in list To dict

works_to_json = works_data.loc[(works_data.soloists.str.len() != 0)].reset_index(drop=True)

# * 빈 리스트 값은 필요가 없으므로 제거

a = [{'1':2}]

dict(a[0])


def listTodict(df, col1) :
    for i in df.index:
        df.at[i, col1] = df.at[i, col1][0]


def listTodict2(s):
    return s[0]


works_to_json.columns

test_df = works_to_json.copy()
test_df2 = works_to_json.copy()

listTodict(test_df, 'soloists')

test_df2['soloists'] = test_df2['soloists'].apply(listTodict2)

# * apply의 속도가 더 빠르다.

print(test_df['soloists'].head(2))
print(test_df2['soloists'].head(2))

# ### 4-2-2. dict to dataframe

pd.DataFrame(test_df2.soloists.tolist()).head()

test_df2.soloists.apply(pd.Series).head()

# * tolist의 속도가 더 빠르다.

# ### 4-2-3. add other columns

worksWithSolo = pd.concat([test_df2[['workTitle_ID','programID','work_ID']]
                           , pd.DataFrame(test_df2.soloists.tolist())], axis=1)

worksWithSolo.rename(columns = {'id' : 'Work_ID'}, inplace=True)

worksWithSolo.shape

pd.DataFrame(test_df2.soloists.tolist()).shape

worksWithSolo.drop_duplicates(inplace=True)

worksWithSolo.shape

worksWithSolo.head(1)

# # 5. Final_DataFrame

# ## 5-1. Get DataFrame

semi_final = works_data.drop('soloists', axis=1).merge(worksWithSolo, 
                             left_on=['workTitle_ID', 'programID', 'work_ID'],
                            right_on=['workTitle_ID', 'programID', 'work_ID'],
                            how='left')

semi_final.head(1)

# +
# len(works_data.loc[(works_data.programID.notnull())])
# -

semi_final.shape

print(len(semi_final.work_ID.unique()))
print(len(works_data.work_ID.unique()))

semi_final = semi_final.drop_duplicates()

semi_final.shape

final = semi_final.merge(concerts_data,
                    left_on = ['programID', 'work_ID'],
                   right_on = ['programID', 'work_ID'],
                   how = 'left')

final.shape

mask = final.duplicated()

final[mask].shape

final.drop_duplicates(inplace=True)

final.shape

final.head(2)

# ## 5-2. Get unique key

# * 심심해서 그냥 해봄... 별로 의미 없는 듯

final2 = final.copy()

final2.columns

col_list = ['workTitle_ID', 'work_ID', 'Date']

final2['test1'] = final2[col_list].values.tolist()

final2['test1'].head()


def join_list(s):
    return ''.join(s)


final2['test1'] = final2['test1'].apply(join_list)

len(final2['test1'].unique())

# ## 5-3. assign unique id

import uuid
print(uuid.uuid4())

uuid_list = [uuid.uuid4() for i in range(final.shape[0])]

final['key'] = uuid_list

len(final['key'].unique()) == final.shape[0]

len(final['key'].unique())

final.head(1)
