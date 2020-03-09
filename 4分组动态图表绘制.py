import pandas as pd
import pyecharts as pe
import warnings
warnings.filterwarnings('ignore')

pan = pd.read_excel('panel.xlsx')
data_china = pan.groupby('日期')[['确诊', '死亡', '治愈', '现存']].sum()
# 教程里计算了下面的这些数据，虽然没怎么用到
data_china['确诊新增'] = data_china['确诊'] - data_china['确诊'].shift()
data_china['死亡新增'] = data_china['死亡'] - data_china['死亡'].shift()
data_china['治愈新增'] = data_china['治愈'] - data_china['治愈'].shift()
data_china['现存新增'] = data_china['现存'] - data_china['现存'].shift()
# 下面这个是我自己自创的,用治愈数除以前一天的现存数
data_china['治愈率'] = data_china['治愈'] / data_china['现存'].shift()
data_china['治愈率'] = data_china['治愈率'].round(2)
# 先绘制分组柱状图
'''
bar = pe.Bar('每日治愈与现存病例柱状图')
x = data_china.iloc[1::].index.astype('str')
y1 = data_china['治愈'].iloc[1::]
y2 = data_china['现存'].iloc[1::]

bar.add('治愈病例', x, y1, is_datazoom_show=True, datazoom_range=[0, 100])
bar.add('现存病例', x, y2)  # 以此类推，还可以继续增加分组数据
# 然后绘制折线图
line = pe.Line('治愈率 折线图')
x = data_china.iloc[1::].index.astype('str')
y = data_china['治愈率'].iloc[1::]
line.add('治愈率', x, y,
         is_datazoom_show=True, datazoom_range=[0, 100],
         tooltip_trigger='axis', tooltip_axispointer_type='cross')
line.render('治愈率.html')
'''
# 同样的，再来个合并的
x = data_china.iloc[1::].index.astype('str')
y1 = data_china['治愈'].iloc[1::]
y2 = data_china['现存'].iloc[1::]
y3 = data_china['治愈率'].iloc[1::]

bar = pe.Bar('每日治愈率变化情况')
bar.add('治愈病例', x, y1, is_datazoom_show=True, datazoom_range=[0, 100],
        tooltip_trigger='axis', tooltip_axispointer_type='cross')
bar.add('现存病例', x, y2)

line = pe.Line('治愈率 折线图')
line.add('治愈率', x, y3, line_width=2, line_color='yellow',)

overlap = pe.Overlap()
overlap.add(bar)
overlap.add(line, yaxis_index=1, is_add_yaxis=True)  # 新增y轴
overlap.render('分组动态图综合.html')