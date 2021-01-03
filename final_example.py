from tkinter import *
from tkinter.ttk import *
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from pandas import DataFrame
import requests
import threading
import re

window = Tk()
window.title('期末專案')
window.geometry('1620x850')

years = (102,103,104,105,106,107,108)
start_months = (1,3,5,7,9,11)
end_months = (2,4,6,8,10,12)

start_year_label = Label(window, text = 'start_year:', justify=RIGHT, width=50)
start_year_label.place(x=10, y=10, width=100, height=20)

start_year = Combobox(width=50, values=years)
start_year.set(108)
start_year.place(x=90, y=10, width=120, height=20)

start_month_label = Label(window, text = 'start_months:', justify=RIGHT, width=50)
start_month_label.place(x=250, y=10, width=100, height=20)

start_month = Combobox(width=50, values=start_months)
start_month.set(9)
start_month.place(x=340, y=10, width=120, height=20)

end_year_label = Label(window, text = 'end_year:', justify=RIGHT, width=50)
end_year_label.place(x=10, y=40, width=100, height=20)

end_year = Combobox(width=50, values=years)
end_year.set(108)
end_year.place(x=90, y=40, width=120, height=20)

end_month_label = Label(window, text = 'end_months:', justify=RIGHT, width=50)
end_month_label.place(x=250, y=40, width=100, height=20)

end_month = Combobox(width=50, values=end_months)
end_month.set(10)
end_month.place(x=340, y=40, width=120, height=20)

warning_label = Label(window, text = '', justify=RIGHT, width=200, foreground ='red')
warning_label.place(x=180, y=110, width=200, height=20)

range_label = Label(window, text = '查詢時間需在 102/01~108/10 之間', justify=RIGHT, width=200 )
range_label.place(x=10, y=75, width=200, height=20)

mp = {}
threads = []

def func(url):
    html=requests.get(url).content.decode('utf-8')
    sp=BeautifulSoup(html,'html.parser')
    for idx,link in enumerate(sp.select('div.container-fluid td')):
        if idx%5 == 4:
            items = link.text.split('，')[0]
            items = re.split('、|及|和',items)
            for i in items:
                tmp = i.split('*')
                tmp = re.split('共|等|計|一|二|三|四|五|六|七|八|九|0|1|2|3|4|5|6|7|8|9|,| ',tmp[0])[0]
                if(len(tmp)<1):
                    continue
                if tmp in mp:
                    mp[tmp] += 1
                else:
                    mp[tmp] = 1
def cal():
    if int(start_year.get()) > int(end_year.get()) or (int(start_year.get())==int(end_year.get()) and int(start_month.get()) > int(end_month.get()) ) or (end_year.get()=="108" and end_month.get()=="12") :
        warning_label['foreground'] = 'red'
        warning_label['text'] = '輸入時間區間錯誤'
        return
    else:
        global mp, threads
        mp = {}
        threads = []
        length = 0
        warning_label['text'] = ''
        year = int(start_year.get())
        month = int(start_month.get())
        while year < int(end_year.get()) or ( year == int(end_year.get()) and month < int(end_month.get()) ):
            if month < 10:
                threads.append(threading.Thread(target = func , args = ('https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_'+str(year)+'0'+str(month),)))
                threads[length].start()
                length += 1
            else:
                threads.append(threading.Thread(target = func , args = ('https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_'+str(year)+str(month),)))
                threads[length].start()
                length += 1
            month += 2
            if month == 13:
                month = 1
                year += 1
    for i in threads:
        i.join()
    warning_label['foreground'] = 'black'
    warning_label['text'] = '共有'+str(len(mp))+'個不同商品交易項目'
    x = []
    y = []
    item = []
    maxn = 0
    Data1 = {'商品交易項目': [],
        '交易項目出現次數': []
       }
    for idx,i in enumerate(mp):
        Data1['交易項目出現次數'].append(mp[i])
        Data1['商品交易項目'].append(i)

    df1 = DataFrame(Data1, columns= ['商品交易項目', '交易項目出現次數'])
    df1 = df1[['商品交易項目', '交易項目出現次數']].groupby('商品交易項目').sum()       

    figure1 = plt.Figure(figsize=(10,5), dpi=100)
    ax1 = figure1.add_subplot(111)
    figure1.set_tight_layout(True)
    bar1 = FigureCanvasTkAgg(figure1, window)
    bar1.get_tk_widget().place(x=10, y=150,width = 1600, height = 700)
    df1.plot(kind='bar', legend=True, ax=ax1)

btn_cal = Button(text="Analyze", command=cal)
btn_cal.place(x=10, y=110, width=60, height=30)

btn_exit = Button(text="Exit", command=quit)
btn_exit.place(x=90, y=110, width=60, height=30)

window.mainloop()

#    _
# ._(.)< (QUACK)
#  \__)