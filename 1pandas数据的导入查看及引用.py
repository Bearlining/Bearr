import pandas as pd
hb = pd.read_excel('hubei.xlsx')
pan = pd.read_excel('panel.xlsx')
# hb.head(10)  查看前若干行数据
# hb.info()  查看数据基本情况
# hb.colums  查看所有字段，即列标签
# hb.index 查看行数
# hb['日期'].dtype  列索引并查看数据类型,由于要进行时间序列分析，需要把日期转换为日期的数据类型
# hb.['日期'] = pd.to_dateime(hb['日期'])  转换为时间序列数据
# data_0201 = hb[hb['日期'] == '2020-02-01']  行索引且附带条件，其实就是按条件筛选数据啦
# data_0201.head(1)  查看一下，因为我们的数据只有湖北一个省，所以只会有一行值，只显示一行就可以了
# data_china = pan.groupby('日期')[['确诊','死亡','治愈','现存']].sum()
# 按照日期分类，并汇总求和，就得到了全国的时间序列数据
# data_nohb = pan[pan['省市'] != '湖北'] 筛选出非湖北地区数据
# data_nohb = data_nohb.groupby('日期')[['确诊','死亡','治愈','现存']].sum() 再根据日期分类加总
# 如此一来就得到了全国及非湖北地区的时间序列数据，湖北的可以按省市索引一下
