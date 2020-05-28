from bokeh.io import curdoc
import math
import requests 
from bs4 import BeautifulSoup 
from tabulate import tabulate 
import os 
import pandas as pd
import numpy as np 
from bokeh.io import output_notebook
from bokeh.plotting import figure, show
from bokeh.models import  LabelSet,ColumnDataSource,Text
from bokeh.plotting import figure,output_file,show,ColumnDataSource
from bokeh.models import  LabelSet,ColumnDataSource,Text
from bokeh.layouts import widgetbox, column,row
from bokeh.models import RangeSlider
from bokeh.models.tools import HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Turbo256,linear_palette,Magma256
from bokeh.models import Div
extract_contents = lambda row: [x.text.replace('\n', '') for x in row]  
URL = 'https://www.mohfw.gov.in/'    
SHORT_HEADERS = ['SNo', 'State','Indian-Confirmed(Including Foreign Confirmed)','Cured','Death']      
response = requests.get(URL).content  
soup = BeautifulSoup(response, 'html.parser')  
updatedon=soup.find('div', class_="status-update").find('h2').text
header = extract_contents(soup.tr.find_all('th'))    
stats = []  
all_rows = soup.find_all('tr')    
for row in all_rows:  
    stat = extract_contents(row.find_all('td'))       
    if stat:  
        if len(stat) == 4:  
            # last row  
            stat = ['', *stat]  
            stats.append(stat)  
        elif len(stat) == 5:  
            stats.append(stat)    
stats[-1][0] = len(stats)  
stats[-1][1] = "Total Cases"  
objects = []  
for row in stats :  
    objects.append(row[1])       
y_pos = np.arange(len(objects))    
performance = []  
for row in stats[:len(stats)-1] :  
    performance.append(int(row[2]))    
performance.append(int(stats[-1][2][:len(stats[-1][2])-1]))   
table = tabulate(stats, headers=SHORT_HEADERS)  
df = pd.DataFrame(list(zip(objects,performance)),columns =['states','cases'])
l=len(df)
df = df.drop(l-1)
df = df.drop(l-2)
performance2 = []  
for row in stats[:len(stats)-2] :  
    performance2.append(int(row[3]))
df = pd.DataFrame(list(zip(objects,performance,performance2)),columns =['states','cases','cured'])
performance3 = []  
for roww in stats[:len(stats)-2] :  
    performance3.append((roww[4]))
j=0
for j in range(len(performance3)):
    if("#" in performance3[j]):
        performance3[j]='0'
lll=[]
for i in range(len(performance3)):
    lll.append(int(performance3[i]))
df = pd.DataFrame(list(zip(objects,performance,performance2,lll)),columns =['states','cases','cured','death'])  
a=df['states'].tolist()
b = df['cases'].tolist()
c=df['cured'].tolist()
e=df['death'].tolist()
d=len(df['states'])

nn=[updatedon]
source6 = ColumnDataSource(dict(
    t=[2],
    b=[1],
    l=[1],
    r=[2],
    color=['blue'],
    label=nn,
    lx=[1.05],
    ly=[1.75],
    lx2=[1.4],
    ly2=[1.2],
))
p6 = figure(x_range=(1, 2), y_range=(1,2), plot_height=50, plot_width=1300,tools="",toolbar_location=None)
p6.quad(top='t', bottom='b', left='l',right='r',color='color',source=source6)
labels = LabelSet(x='lx', y='ly', text='label',x_offset=70,y_offset=-20,
               source=source6, render_mode='canvas',text_font_size="20px",text_color="white")
p6.axis.visible = None
p6.xgrid.visible = False
p6.ygrid.visible = False
p6.add_layout(labels)

sum1=df['cases'].sum()
sum2=df['cured'].sum()
sum3=df['death'].sum()
s1=str(sum1)
s2=str(sum2)
s3=str(sum3)
nn=['Total Confirmed Cases','Cured Cases','No of Deaths']
mm=[s1,s2,s3]
source3 = ColumnDataSource(dict(
    t=[2, 2, 2],
    b=[1, 1, 1],
    l=[1, 2, 3],
    r=[2, 3, 4],
    color=['orange','green','red'],
    label=['Total Confirmed Cases','Cured Cases','No of Deaths'],
    lx=[1.05,2.05,3.05],
    ly=[1.75,1.75,1.75],
    lx2=[1.4,2.4,3.4],
    ly2=[1.2,1.2,1.2],
    label2=mm,
))
p4 = figure(x_range=(1, 4), y_range=(1,2), plot_height=100, plot_width=1300,tools="",toolbar_location=None)
p4.quad(top='t', bottom='b', left='l',right='r',color='color',source=source3)
labels = LabelSet(x='lx', y='ly', text='label',x_offset=0,y_offset=0,
               source=source3, render_mode='canvas',text_font_size="20px",text_color="white")
labels2 = LabelSet(x='lx2', y='ly2', text='label2',x_offset=0,y_offset=0,
               source=source3, render_mode='canvas',text_font_size="40px",text_color="white")
p4.axis.visible = None
p4.xgrid.visible = False
p4.ygrid.visible = False
p4.add_layout(labels)
p4.add_layout(labels2)

def changeArea(attr, old, new):
    scale1 = slider.value[0]
    scale2 = slider.value[1]
    dd=df.loc[df['cases'].between(scale1,scale2), 'states']
    d=len(dd)
    new_data = {
        'states' : df.loc[df['cases'].between(scale1,scale2), 'states'],
        'cases'    : df.loc[df['cases'].between(scale1,scale2), 'cases'],
	'colors'  : linear_palette(Magma256,d)
    }
    source.data = new_data
p=figure(y_range=a,plot_width=1300,plot_height=600,title="Confirmed Corona Cases in India Statewise ",x_axis_label="No of cases ",y_axis_label="States",tools="pan,wheel_zoom,box_zoom,reset")
source = ColumnDataSource(data={'states': a, 'cases': b , 'colors':linear_palette(Magma256,d)})
slider = RangeSlider(title='Cases Range', start=0, end=100000, step=1, value=(0,100000),bar_color="green")
slider.on_change('value', changeArea)
p.hbar(y='states',right='cases',left=0,height=0.6,fill_color='colors',fill_alpha=0.9,source=source)
p1=figure(x_range=a,plot_width=1300,plot_height=600,title=" Cured Corona Cases in India Statewise ",x_axis_label="States ",y_axis_label="No of cases",tools="pan,wheel_zoom,box_zoom,reset")
source1 = ColumnDataSource(data={'states': a, 'cured': c , 'colors':linear_palette(Turbo256,d)})
p1.vbar(x='states',top='cured',bottom=0,width=0.5,fill_color='colors',fill_alpha=0.9,source=source1)
p.x_range.start=0
p1.y_range.start=0
hover=HoverTool()
hover.tooltips="""
<div>
<div><strong>State : </strong>@states</div>
<div><strong>Cases : </strong>@cases</div>
</div>
"""
p.add_tools(hover)
p.xgrid.visible = False
p.ygrid.visible = False
p.title.align='left'
hover1=HoverTool()
hover1.tooltips="""
<div>
<div><strong>State : </strong>@states</div>
<div><strong>Cured : </strong>@cured</div>
</div>
"""
p1.add_tools(hover1)
p1.xgrid.visible = False
p1.ygrid.visible = False
p1.title.align='left'
p.title.text_font_size = '13pt'
p1.title.text_font_size = '13pt'
p.title.text_color = "red"
p1.title.text_color = "red"
p1.xaxis.major_label_orientation = math.pi/2

factors = df['states'].tolist()
source4=ColumnDataSource(df)
p5 = figure(x_range=factors, plot_height=600, plot_width=1300,x_axis_label="States ",y_axis_label="No of death",title="No of Deaths in India due to Corona Statewise")
p5.circle(x='states',y='death', size=15, fill_color="red", line_color="black", line_width=3,source=source4)
p5.xaxis.major_label_orientation = math.pi/2
p5.title.text_font_size = '13pt'
p5.title.text_color = "red"
p5.xgrid.visible = False
p5.ygrid.visible = False
hover3=HoverTool()
hover3.tooltips="""
<div>
<div><strong>State : </strong>@states</div>
<div><strong>Deaths : </strong>@death</div>
</div>
"""
p5.add_tools(hover3)

pre = Div(text="""<div><h2><strong><center>Corona India Live Dashboard</center></strong></h2></div>""",align='center',style={'color': 'black','font-size':'20px'})
layout = column(pre,p6,p4,widgetbox(slider), p,p1,p5)
curdoc().add_root(layout)