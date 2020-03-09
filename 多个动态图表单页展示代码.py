import pyecharts as pe
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

pan = pd.read_excel('panel.xlsx')
# 全国数据
data_china = pan.groupby('日期')[['确诊', '死亡', '治愈', '现存']].sum()  # 汇总全国数据
data_china['确诊新增'] = data_china['确诊'] - data_china['确诊'].shift()
data_china['死亡新增'] = data_china['死亡'] - data_china['死亡'].shift()
data_china['治愈新增'] = data_china['治愈'] - data_china['治愈'].shift()
data_china['现存新增'] = data_china['现存'] - data_china['现存'].shift()
data_china['确诊增长率'] = data_china['确诊新增'] / data_china['确诊'].shift()
data_china['确诊增长率'] = data_china['确诊增长率'].round(2)
data_china['治愈率'] = data_china['治愈'] / data_china['现存'].shift()
data_china['治愈率'] = data_china['治愈率'].round(2)
# 湖北省数据
data_hb = pan[pan['省市'] == '湖北']
data_hb['确诊新增'] = data_hb['确诊'] - data_hb['确诊'].shift()
data_hb['死亡新增'] = data_hb['死亡'] - data_hb['死亡'].shift()
data_hb['治愈新增'] = data_hb['治愈'] - data_hb['治愈'].shift()
data_hb['现存新增'] = data_hb['现存'] - data_hb['现存'].shift()
# 非湖北省数据
data_nothb_all = pan[pan['省市'] != '湖北']

data_nothb = data_nothb_all.groupby('日期')[['确诊', '死亡', '治愈', '现存']].sum()
data_nothb['确诊新增'] = data_nothb['确诊'] - data_nothb['确诊'].shift()
data_nothb['死亡新增'] = data_nothb['死亡'] - data_nothb['死亡'].shift()
data_nothb['治愈新增'] = data_nothb['治愈'] - data_nothb['治愈'].shift()
data_nothb['现存新增'] = data_nothb['现存'] - data_nothb['现存'].shift()
# 下面开始由简入难展示图表
# 1.简单柱状图
bar1 = pe.Bar('累计确诊病例 柱状图')
b1x = data_china.iloc[1::].index.astype('str')
b1y = data_china['确诊'].iloc[1::]
bar1.add('确诊病例', b1x, b1y, is_datazoom_show=True, datazoom_range=[0, 100], tooltip_trigger='axis')

# 2.简单折线图
line1 = pe.Line('累计确认病例增长率 折线图')
l1x = data_china.iloc[1::].index.astype('str')
l1y = data_china['确诊增长率'].iloc[1::]
line1.add('增长率', l1x, l1y, is_smooth=False, tooltip_trigger='axis', tooltip_axispointer_type='line')

# 3.简单柱状图、折线图合体
c1x = data_china.iloc[1::].index.astype('str')
c1y1 = data_china['确诊'].iloc[1::]
c1y2 = data_china['确诊增长率'].iloc[1::]
# 绘制柱状图
bar2 = pe.Bar('累计确诊病例走势')
bar2.add('确诊病例', c1x, c1y1, is_datazoom_show=True, datazoom_range=[0, 100], tooltip_trigger='axis',
         tooltip_axispointer_type='cross')
# 绘制折线图
line2 = pe.Line('累计确诊病例增长率 折线图')
line2.add('增长率', c1x, c1y2, is_smooth=True)
# 合并图表
overlap1 = pe.Overlap()
overlap1.add(bar2)
overlap1.add(line2, yaxis_index=1, is_add_yaxis=True)

# 4.分组柱状图
bar3 = pe.Bar('每日治愈与现存病例柱状图')
bx2 = data_china.iloc[1::].index.astype('str')
by3 = data_china['治愈'].iloc[1::]
by4 = data_china['现存'].iloc[1::]
bar3.add('治愈病例', bx2, by3, is_datazoom_show=True, datazoom_range=[0, 100])
bar3.add('现存病例', bx2, by4)

# 5.分组柱状图与折线图合并
c2x = data_china.iloc[1::].index.astype('str')
c2y1 = data_china['治愈'].iloc[1::]
c2y2 = data_china['现存'].iloc[1::]
c2y3 = data_china['治愈率'].iloc[1::]

bar4 = pe.Bar('每日治愈率变化情况')
bar4.add('治愈病例', c2x, c2y1, is_datazoom_show=True, datazoom_range=[0, 100], tooltip_trigger='axis',
         tooltip_axispointer_type='cross')
bar4.add('现存病例', c2x, c2y2)

line3 = pe.Line('治愈率 折线图')
line3.add('治愈率', c2x, c2y3, line_width=2, line_color='yellow', )

overlap2 = pe.Overlap()
overlap2.add(bar4)
overlap2.add(line3, yaxis_index=1, is_add_yaxis=True)

# 6.多系列折线图
line4 = pe.Line('不同地区疫情病例增长曲线')
l4x = data_china.index.astype('str')
l4y1 = data_hb['确诊新增']
l4y2 = data_nothb['确诊新增']
l4y3 = data_china['确诊新增']

line4.add('湖北新增', l4x, l4y1)
line4.add('非湖北新增', l4x, l4y2)
line4.add('全国新增', l4x, l4y3, tooltip_trigger='axis', tooltip_axispointer_type='cross',
          is_datazoom_show=True, datazoom_range=[0, 100])


# 7.用函数生成地区病例情况的图
# 构建函数获取地区病例数据


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
    fx = data1['日期'].astype('str')
    fy1 = data1['确诊新增']
    fy2 = data2['确诊新增']
    fy3 = data3['确诊新增']

    line5 = pe.Line('不同地区新增确诊病例情况')
    line5.add(r1, fx, fy1)
    line5.add(r2, fx, fy2)
    line5.add(r3, fx, fy3, tooltip_trigger='axis', tooltip_axispointer_type='cross', is_datazoom_show=True,
              datazoom_range=[0, 100])
    return line5  # .render('不同地区确诊增长曲线auto.html')


line6 = fig2('北京', '上海', '湖南')


def merge_charts():
    page = pe.Page()
    page.add(bar1)
    page.add(line1)
    page.add(overlap1)
    page.add(bar3)
    page.add(overlap2)
    page.add(line4)
    page.add(line6)
    return page


merge_charts().render('图表集合.html')
