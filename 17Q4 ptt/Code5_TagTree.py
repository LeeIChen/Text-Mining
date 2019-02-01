# 目的: 斷好詞(Jieba)之後做decision tree，用來填補剩下的stage & item

import jieba
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from collections import Counter
from pandas.core.frame import DataFrame
import math

df    = pd.read_csv("Data5_pttUTF8.txt")
df_SI = df.loc[:103, ['titl', 'push', 'tag', 'stage', 'item', 'text']]
# print(df_SI)

# 將ppt內文全部斷詞，將原始資料計算項目個數，再做成字串

word_list1 =[]
for item1 in df_SI['text']:
    seglist = jieba.cut(item1, cut_all=False)

    word_list2 = []
    for item2 in seglist:
        if len(item2)>1:
            word_list2.append(item2)
    word_list3 = Counter(word_list2)
    word_list4 = pd.DataFrame.from_dict(word_list3,orient='index')
    word_list5 = pd.DataFrame.transpose(word_list4)
    #print(word_list3)
    #print(word_list4)
    #print(word_list5)
    word_list1.append(word_list5)
df_new  = pd.concat(word_list1, ignore_index=True)
df_Tree = pd.concat([df_SI,df_new], axis=1)
header = list(df_new)
# print(df_Tree)

print(header['鼓勵'])
# ================ Decision tree ================ #
'''
tree = DecisionTreeClassifier(criterion='gini',max_depth=5)
model = tree.fit(df[header], df[['stage']])
print(model)
'''


