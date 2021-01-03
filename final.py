import requests
from bs4 import BeautifulSoup
import re
import threading
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

dict1000=dict()
dict200=dict()
city1000=dict()
city200=dict()

# !wget -O /usr/share/fonts/truetype/liberation/simhei.ttf "https://www.wfonts.com/download/data/2014/06/01/simhei/chinese.simhei.ttf"

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False


# 自定義字體變數
myfont = mpl.font_manager.FontProperties(fname=r'/usr/local/lib/python3.6/dist-packages/matplotlib/mpl-data/fonts/ttf/taipei_sans_tc_beta.ttf')

# !!!!後續在相關函式中增加fontproperties=myfont屬性即可!!!!
# myfont = FontProperties(fname=os.environ['WINDIR']+'\\Fonts\\kaiu.ttf', size=16)

def search(url):
    html=requests.get(url).content.decode('utf-8')
    sp=BeautifulSoup(html,'html.parser')

    table1000 = sp.find('table',{'id':'fbonly'})
    tr1000 = table1000.find_all('tr')

    table200 = sp.find('table',{'id':'fbonly_200'})
    tr200 = table200.find_all('tr')

    for idx,link in enumerate(tr1000[1:]):

        tdTable=link.find_all('td')
        for i,j in enumerate(tdTable):
            tdTable[i]=j.text
        items=tdTable[4]
        # print(items)
        addr=tdTable[3]
        # print(addr)
        addr=addr[:3]
        if addr in city1000:
            city1000[addr] += 1
        else:
            city1000[addr] = 1        
        # tmp_city=re.findall('([]*?)(縣|市)')
        # print(addr,tmp_city)
        items=re.split('及|、|和',items)
        for i in items:
            tmp = i.split('*')
            tmp = re.split('，|共|等|計|一|二|三|四|五|六|七|八|九|0|1|2|3|4|5|6|7|8|9|,| ',tmp[0])[0]
            if(len(tmp)<1):
                continue
            # print(tmp)
            if tmp in dict1000:
                dict1000[tmp] += 1
            else:
                dict1000[tmp] = 1
    #--------------------------------------
    for idx,link in enumerate(tr200[1:]):

        tdTable=link.find_all('td')
        for i,j in enumerate(tdTable):
            tdTable[i]=j.text
        items=tdTable[4]
        # print(items)

        addr=tdTable[3]
        # print(addr)
        addr=addr[:3]
        if addr in city200:
            city200[addr] += 1
        else:
            city200[addr] = 1  

        items=re.split('及|、|和',items)
        for i in items:
            tmp = i.split('*')
            tmp = re.split('，|共|等|計|一|二|三|四|五|六|七|八|九|0|1|2|3|4|5|6|7|8|9|,| ',tmp[0])[0]
            if(len(tmp)<1):
                continue
            # print(tmp)
            if tmp in dict200:
                dict200[tmp] += 1
            else:
                dict200[tmp] = 1

def cal(start,end):
    year=int(start[0])
    month=int(start[1])
    threads = []
    while year<int(end[0]) or (year==int(end[0]) and month<=int(end[1])):
        if(month<10):
            threads.append(threading.Thread(target=search,args=('https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_'+str(year)+'0'+str(month),)))
            threads[len(threads)-1].start()
        else:
            threads.append(threading.Thread(target=search,args=('https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_'+str(year)+str(month),)))
            threads[len(threads)-1].start()
        month+=2
        if(month>12):
            month=1
            year+=1
    for i in threads:
        i.join()
    # print(dict1000)
    # print(city1000)
def show():
    plt.figure(figsize=(20,5))
    value=[]
    x_labels=[]
    for i,j in city1000.items():
        x_labels.append(i)
        value.append(j)
    plt.bar(x_labels,value)
    plt.show()
    #-------------------------
    plt.figure(figsize=(20*len(dict1000)/20,5))
    value=[]
    x_labels=[]
    for i,j in dict1000.items():
        x_labels.append(i)
        value.append(j)
    plt.bar(x_labels,value)
    plt.xticks(rotation=90)
    plt.show()
    #----------------------------
    plt.figure(figsize=(20,5))
    value=[]
    x_labels=[]
    for i,j in city200.items():
        x_labels.append(i)
        value.append(j)
    plt.bar(x_labels,value)
    plt.show()
    #-----------------------------
    plt.figure(figsize=(20*len(dict200)/20,5))
    value=[]
    x_labels=[]
    for i,j in dict200.items():
        x_labels.append(i)
        value.append(j)
    plt.bar(x_labels,value)
    plt.xticks(rotation=90)
    plt.show()

startDate=[102,1]
endDate=[109,10]
cal(startDate,endDate)
show()