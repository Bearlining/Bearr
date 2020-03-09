import pyecharts as pe
import pandas as pd
import warnings
# import matplotlib as mpl

# mpl.rcParams['font.sans-serif'] = ['SimHei']
# mpl.rcParams['axes.unicode_minus'] = False  # 以上两句是为了让图表中的中文正常显示
warnings.filterwarnings('ignore')
pan = pd.read_excel('panel.xlsx')
data_china = pan.groupby('日期')[['确诊', '死亡', '治愈', '现存']].sum()  # 汇总全国数据

data_china['确诊新增'] = data_china['确诊'] - data_china['确诊'].shift()
data_china['死亡新增'] = data_china['死亡'] - data_china['死亡'].shift()
data_china['治愈新增'] = data_china['治愈'] - data_china['治愈'].shift()
data_china['现存新增'] = data_china['现存'] - data_china['现存'].shift()
# shift()是将数据向前移动一位，即实现了后一天减前一天的效果,括号里默认一位
data_china['确诊增长率'] = data_china['确诊新增'] / data_china['确诊'].shift()
data_china['确诊增长率'] = data_china['确诊增长率'].round(2)
# 接下来要用pe画图啦
'''
bar = pe.Bar('累计确诊病例 柱状图')
x = data_china.iloc[1::].index.astype('str')
# 设置x轴，由于数据是按照日期筛选得到的，因此索引index即表示x为日期，且将其字符串化
# 并且由于日期数据是从第二行开始的，所以是[1::]
y = data_china['确诊'].iloc[1::]
bar.add('确诊病例', x, y,
        is_datazoom_show=True, datazoom_range=[0, 100], # 这两个是用来设置图片下面的拖动条的
        tooltip_trigger='axis')
bar.render('柱状图axis.html')

bar = pe.Bar('累计确诊病例 柱状图')
x = data_china.iloc[1::].index.astype('str')
y = data_china['确诊'].iloc[1::]
bar.add('确诊病例', x, y,
        is_datazoom_show=True, datazoom_range=[0, 100],
        tooltip_trigger='item')  # 只是换一种动态标签的样式而已，没啥大区别
bar.render('柱状图item.html')
'''
# 接下来我们再试试增长率折线图
'''
line = pe.Line('累计确认病例增长率 折线图')
x = data_china.iloc[1::].index.astype('str')
y = data_china['确诊增长率'].iloc[1::]

line.add('增长率', x, y, is_smooth=False,  # 可选参数，设置折线是否平滑
         tooltip_trigger='axis', tooltip_axispointer_type='line')  # 指示器类型设置，可以有cross、shadow、line三种
line.render('折线图2.html')
'''
# 最后来把上面的柱状图和折线图进行合并
# 设置坐标轴数据
x = data_china.iloc[1::].index.astype('str')
y1 = data_china['确诊'].iloc[1::]
y2 = data_china['确诊增长率'].iloc[1::]
# 绘制柱状图
bar = pe.Bar('累计确诊病例走势')
bar.add('确诊病例', x, y1,
        is_datazoom_show=True, datazoom_range=[0, 100],
        tooltip_trigger='axis', tooltip_axispointer_type='cross')
# 绘制折线图
line = pe.Line('累计确诊病例增长率 折线图')
line.add('增长率', x, y2, is_smooth=True)
# 合并图表
overlap = pe.Overlap()
overlap.add(bar)
overlap.add(line,
            yaxis_index=1, is_add_yaxis=True)
overlap.render('合并柱状图与折线图.html')
