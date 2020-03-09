import pandas as pd
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False  # 以上两句是为了让图表中的中文正常显示
pan = pd.read_excel('panel.xlsx')
# 下面先搞个简单的
'''
data_0201 = pan[pan['日期'] == '20200201']  # 提取某一天的数据
data_0201.sort_values(by='现存', ascending=False, inplace=True)
# 以现存为依据进行筛选并降序排序，替换原有数据，这里可能会有警告提示，可以忽略
data_0201.iloc[1:11].plot(x='省市', y='现存', kind='bar', figsize=(15, 5),
                          color='r', alpha=0.8, grid=True, rot=45,
                          title='湖北省外2020.2.1现存病例top10')
# 以上参数以后可以直接套用，figsize是图表大小、alpha是不透明度、grid是网格线、rot是坐标文字倾斜度
# iloc是索引范围，由于是非湖北，所以从1开始而不是0，然后由于这区间取值是左闭右开，因此右边取11
'''
# 再来个稍微复杂点的柱状图
'''
data_0201 = pan[pan['日期'] == '20200201']
data_0201.iloc[1:11].plot(x='省市', y=['现存', '确诊'], kind='bar', figsize=(15, 5),
                          grid=True, rot=45, title='湖北省外2020.2.1现存与确诊top10')
'''
# 再来个条形图
'''
data_0201 = pan[pan['日期'] == '20200201']
data_0201.iloc[1:11].plot(x='省市', y=['现存', '确诊'], kind='barh', figsize=(15, 5),
                          grid=False, title='湖北省外2020.2.1现存与确诊top10')
'''
# 建立绘图函数
'''
def fig1(time,tp,topn):
    datai = pan[pan['日期'] == time]  # 筛选数据
    datai.sort_values(by=tp, ascending=False, inplace=True)  # 排序
    datai.iloc[1:topn+1].plot(x='省市', y=tp, kind='bar', figsize=(15, 5),
                              color='r', alpha=0.8, grid=True, rot=45,
                              title='湖北省外%s%s病例最多的%i省市' % (time, tp, topn))
fig1('20200202', '现存', 15)
'''

