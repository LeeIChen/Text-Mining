import jieba
import pandas as pd
from sklearn import tree
from collections import Counter
from pandas.core.frame import DataFrame
import math

#jieba.set_dictionary('/dict.txt')   #引用預設詞庫
#stop = open('stop_PTT.txt') #引用停用詞

df    = pd.read_csv("Data5_ABC.csv")
#print(df)

# 將ppt內文全部斷詞，將原始資料計算項目個數，再做成字串

word_list1 =[]
for item1 in df[df.A == 1]['text']:
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
df_new = pd.concat(word_list1,ignore_index=True)
header = list(df_new)

# TF-IDF

df_Bank=pd.DataFrame()
list_bank = ['花旗','台新','國泰','富邦','玉山','中信']
for item_bank in list_bank:

    arti_bank = df_new[df_new[item_bank]>0]
    TF = arti_bank.sum(axis=0) / sum(arti_bank.sum(axis=0))
    #print(TF)

    shp = df_new.shape[0]
    cnt = df_new.count()
    sc  = shp/cnt
    print(df_new)
    #print(cnt)
    #print(shp)
    #print(sc)

    IDF = []
    for item_sc in sc:
        item_idf = math.log(item_sc)
        IDF.append(item_idf)
    #print(IDF)

    TFIDF = [i * j for i, j in zip(TF, IDF)]
    #print(TFIDF)
    #print(header)

    Dict_TFIDF={item_bank+'_hd':header, item_bank+'_ti':TFIDF}
    df_TFIDF = DataFrame(Dict_TFIDF)
    df_TFIDF1 = df_TFIDF.sort_values(item_bank+'_ti',ascending=False).reset_index(drop=True)
    df_Bank = pd.concat([df_Bank,df_TFIDF1], axis=1)

print(df_Bank)

df_Bank.to_csv("TFIDF_A.csv")

'''
Cut可以當成切割文字的意思(就是分詞)
結巴中文分詞支持的三種分詞模式包括：
    1.精確模式 ：將句子最精確地切開，叫適合文本分析。
        寫法:words = jieba.cut(content, cut_all=False)
    2.全模式：把句子中所有的可以成詞的詞語都掃描出來, 速度快。
        寫法:words = jieba.cut(content, cut_all=True)
    3.搜索引勤模式：在精確模式的基礎上對長詞再次切分，提高召回率，適合用於搜尋引擎分詞。
        寫法:words = jieba.cut_for_search(Content)
'''