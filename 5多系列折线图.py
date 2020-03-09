import pandas as pd
import pyecharts as pe
import warnings

warnings.filterwarnings('ignore')

pan = pd.read_excel('panel.xlsx')
data_china = pan.groupby('日期')[['确诊', '死亡', '治愈', '现存']].sum()

data_china['确诊新增'] = data_china['确诊'] - data_china['确诊'].shift()
data_china['死亡新增'] = data_china['死亡'] - data_china['死亡'].shift()
data_china['治愈新增'] = data_china['治愈'] - data_china['治愈'].shift()
data_china['现存新增'] = data_china['现存'] - data_china['现存'].shift()
# 提取湖北省数据
data_hb = pan[pan['省市'] == '湖北']
data_hb['确诊新增'] = data_hb['确诊'] - data_hb['确诊'].shift()
data_hb['死亡新增'] = data_hb['死亡'] - data_hb['死亡'].shift()
data_hb['治愈新增'] = data_hb['治愈'] - data_hb['治愈'].shift()
data_hb['现存新增'] = data_hb['现存'] - data_hb['现存'].shift()
# 提取非湖北省的数据并加总
data_nothb_all = pan[pan['省市'] != '湖北']
data_nothb = data_nothb_all.groupby('日期')[['确诊', '死亡', '治愈', '现存']].sum()

data_nothb['确诊新增'] = data_nothb['确诊'] - data_nothb['确诊'].shift()
data_nothb['死亡新增'] = data_nothb['死亡'] - data_nothb['死亡'].shift()
data_nothb['治愈新增'] = data_nothb['治愈'] - data_nothb['治愈'].shift()
data_nothb['现存新增'] = data_nothb['现存'] - data_nothb['现存'].shift()
# 绘制多系列折线图
line1 = pe.Line('不同地区疫情病例增长曲线')
x1 = data_china.index.astype('str')
y1 = data_hb['确诊新增']
y2 = data_nothb['确诊新增']
y3 = data_china['确诊新增']

line1.add('湖北新增', x1, y1)
line1.add('非湖北新增', x1, y2)
line1.add('全国新增', x1, y3, tooltip_trigger='axis', tooltip_axispointer_type='cross',
          is_datazoom_show=True, datazoom_range=[0, 100])
# line1.render('不同地区确诊增长曲线.html')


# 下面用函数实现直接画出省份病例情况曲线
# 首先构建函数提取不同地区数据
def regiondata(where):
    datai = pan[pan['省市'] == where]
    datai['确诊新增'] = datai['确诊'] - datai['确诊'].shift()
    datai['死亡新增'] = datai['死亡'] - datai['死亡'].shift()
    datai['治愈新增'] = datai['治愈'] - datai['治愈'].shift()
    datai['现存新增'] = datai['现存'] - datai['现存'].shift()
    return datai


# 构建函数绘制疫情病例增长曲线
def fig2(r1, r2, r3):
    data1 = regiondata(r1)
    data2 = regiondata(r2)
    data3 = regiondata(r3)
    x = data1['日期'].astype('str')
    y4 = data1['确诊新增']
    y5 = data2['确诊新增']
    y6 = data3['确诊新增']

    line = pe.Line('不同地区新增确诊病例情况')
    line.add(r1, x, y4)
    line.add(r2, x, y5)
    line.add(r3, x, y6, tooltip_trigger='axis', tooltip_axispointer_type='cross',
             is_datazoom_show=True, datazoom_range=[0, 100])
    return line  # .render('不同地区确诊增长曲线auto.html')


line2 = fig2('北京', '上海', '湖南')
# 接下来想要把之前画的图全部在一个网页里显示，不然太麻烦了


def merge_charts():
    page = pe.Page()
    page.add(line1)
    page.add(line2)
    return page


merge_charts().render()
