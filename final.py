import requests
from bs4 import BeautifulSoup
import re
import threading
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import csv
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import collections

lock = threading.Lock()
dict1000 = collections.Counter()
dict200 = collections.Counter()
city1000 = collections.Counter()
city200 = collections.Counter()
BigRewardNumber = []

# !wget -O /usr/share/fonts/truetype/liberation/simhei.ttf "https://www.wfonts.com/download/data/2014/06/01/simhei/chinese.simhei.ttf"

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

myfont = mpl.font_manager.FontProperties(fname=r'/usr/local/lib/python3.6/dist-packages/matplotlib/mpl-data/fonts/ttf/taipei_sans_tc_beta.ttf')

class myGUI:
    def getRewardNumber(self,url):
        html = requests.get(url).content.decode('utf-8')
        sp = BeautifulSoup(html, 'html.parser')

        trList = sp.find('div', {'id': 'tablet01'}).find_all('tr')

        RewardNumber = [trList[1].find('td').text, trList[3].find('td').text]
        tmp = []
        for i in trList[5].find_all('p'):
            if len(i.text) != 0:
                tmp.append(i.text)
        RewardNumber.append(tmp)
        RewardNumber.append(trList[12].find('td').text.split('、'))

        return RewardNumber

    def getReward(self,rewardNumber, targetNum, winTicket):
        if targetNum[-8:] == rewardNumber[0]:
            winTicket.append(
                targetNum+'/'+rewardNumber[4]+'/'+rewardNumber[5]+':10000000')
            return 10000000
        if targetNum[-8:] == rewardNumber[1]:
            winTicket.append(
                targetNum+'/'+rewardNumber[4]+'/'+rewardNumber[5]+':2000000')
            return 2000000
        for i in rewardNumber[2]:
            if i == targetNum[-8:]:
                winTicket.append(
                    targetNum+'/'+rewardNumber[4]+'/'+rewardNumber[5]+':200000')
                return 200000

        for i in rewardNumber[2]:
            if i[-7:] == targetNum[-7:]:
                winTicket.append(
                    targetNum+'/'+rewardNumber[4]+'/'+rewardNumber[5]+':40000')
                return 40000

        for i in rewardNumber[2]:
            if i[-6:] == targetNum[-6:]:
                winTicket.append(
                    targetNum+'/'+rewardNumber[4]+'/'+rewardNumber[5]+':10000')
                return 10000

        for i in rewardNumber[2]:
            if i[-5:] == targetNum[-5:]:
                winTicket.append(
                    targetNum+'/'+rewardNumber[4]+'/'+rewardNumber[5]+':4000')
                return 4000

        for i in rewardNumber[2]:
            if i[-4:] == targetNum[-4:]:
                winTicket.append(
                    targetNum+'/'+rewardNumber[4]+'/'+rewardNumber[5]+':1000')
                return 1000

        for i in rewardNumber[2]:
            if i[-3:] == targetNum[-3:]:
                winTicket.append(
                    targetNum+'/'+rewardNumber[4]+'/'+rewardNumber[5]+':200')
                return 200

        for i in rewardNumber[3]:
            if i[-3:] == targetNum[-3:]:
                winTicket.append(
                    targetNum+'/'+rewardNumber[4]+'/'+rewardNumber[5]+':200')
                return 200
        return 0

    def cal(self,start, end):
        if not int(start[1])&1:
            start[1]=int(start[1])-1

        year = int(start[0])
        month = int(start[1])
        threads = []
        while year < int(end[0]) or (year == int(end[0]) and month <= int(end[1])):
            if(month < 10):
                threads.append(threading.Thread(target=self.search, args=('https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_'+str(year)+'0'+str(month),)))
                threads[len(threads)-1].start()
            else:
                threads.append(threading.Thread(target=self.search, args=('https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_'+str(year)+str(month),)))
                threads[len(threads)-1].start()
            month += 2
            if(month > 12):
                month = 1
                year += 1
        for i in threads:
            i.join()

    def search(self,url):

        html = requests.get(url).content.decode('utf-8')
        sp = BeautifulSoup(html, 'html.parser')

        table1000 = sp.find('table', {'id': 'fbonly'})
        tr1000 = table1000.find_all('tr')

        table200 = sp.find('table', {'id': 'fbonly_200'})
        tr200 = table200.find_all('tr')


        lock.acquire()  
        for link in tr1000[1:]:

            tdTable = link.find_all('td')
            for i, j in enumerate(tdTable):
                tdTable[i] = j.text
            items = tdTable[4]
            addr = tdTable[3]
            addr = addr[:3]

            if addr=='台北市':
                addr='臺北市'
            if addr=='桃園縣':
                addr='桃園市'
            
            if addr in city1000:
                city1000[addr] += 1
            else:
                city1000[addr] = 1

            items = re.split('及|、|和', items)
            for i in items:
                tmp = i.split('*')
                tmp = re.split(
                    '，|共|等|計|一|二|三|四|五|六|七|八|九|0|1|2|3|4|5|6|7|8|9|,| ', tmp[0])[0]
                if not len(tmp):
                    continue
                if tmp in dict1000:
                    dict1000[tmp] += 1
                else:
                    dict1000[tmp] = 1
        # --------------------------------------
        for link in tr200[1:]:

            tdTable = link.find_all('td')
            for i, j in enumerate(tdTable):
                tdTable[i] = j.text
            items = tdTable[4]
            addr = tdTable[3]
            addr = addr[:3]

            if addr=='台北市':
                addr='臺北市'
            if addr=='桃園縣':
                addr='桃園市'

            if addr in city200:
                city200[addr] += 1
            else:
                city200[addr] = 1

            items = re.split('及|、|和', items)
            for i in items:
                tmp = i.split('*')
                tmp = re.split(
                    '，|共|等|計|一|二|三|四|五|六|七|八|九|0|1|2|3|4|5|6|7|8|9|,| ', tmp[0])[0]
                if(len(tmp) < 1):
                    continue
                if tmp in dict200:
                    dict200[tmp] += 1
                else:
                    dict200[tmp] = 1

        lock.release() 


    def makeform(self, root, fields):
        entries = []
        for field in fields:
            row = tk.Frame(root)
            lab = tk.Label(row, width=15, text=field, anchor='w')
            ent = tk.Entry(row)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries.append((field, ent))
        return entries

    def fetch(self, entries):
        self.analyzeDate = []
        self.dictArr = []
        for entry in entries:
            text = entry[1].get()
            self.analyzeDate.append(int(text))

        self.cal([self.analyzeDate[0], self.analyzeDate[1]],[self.analyzeDate[2], self.analyzeDate[3]])
        self.drawChart()

    def __init__(self):
        self.analyzeDate = dict()
        self.chartIndex = 0
        self.scrollbar = None
        self.master = tk.Tk()
        self.listbox = None
        w, h = self.master.maxsize()
        self.master.geometry("{}x{}".format(w, h))
        self.master.title('自動對獎與發票分析程式')
        self.fields = ['StartYear', 'StartMonth', 'EndYear', 'EndMonth']
        self.ents = self.makeform(self.master, self.fields)
        self.label = tk.Label(self.master, text='輸入發票號碼到同資料夾下的\'發票號碼.csv\'')
        self.label.pack()
        self.autoCheckButton = tk.Button(self.master, text='自動對獎', command=self.autoChecking)
        self.autoCheckButton.pack(pady=5)
        self.analyzeButton = tk.Button(self.master, text='中獎分析', command=lambda e=self.ents: self.fetch(e))
        self.analyzeButton.pack(pady=5)

        self.exitButton = tk.Button(self.master, text='Exit', command=self.master.quit)
        self.exitButton.pack(pady=5)

        self.canvasPic = None

        self.itemText_var = tk.StringVar()
        self.itemText_var.set("")
        self.itemText = tk.Label(self.master, textvariable=self.itemText_var)
        self.itemText.pack(pady=5)

        self.chartText_var = tk.StringVar()
        self.chartText_var.set("")
        self.chartText = tk.Label(self.master, textvariable=self.chartText_var)
        self.chartText.pack(pady=5)

        self.ticketText_var = tk.StringVar()
        self.ticketText_var.set("")
        self.ticketText = tk.Label(
            self.master, textvariable=self.ticketText_var)
        self.ticketText.pack(pady=5)

        self.master.mainloop()

    def claerBottom(self):
        if self.canvasPic != None:
            self.canvasPic.destroy()
        self.chartText_var.set("")
        self.itemText_var.set("")
        self.ticketText_var.set("")
        if self.scrollbar != None:
            self.scrollbar.destroy()
        if self.listbox != None:
            self.listbox.destroy()

    def autoChecking(self):
        csvRows = []
        ans = 0
        winTicket = []
        rewardSet = []
        urls = []

        self.claerBottom()

        with open("./發票號碼.csv", 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                csvRows.append(row)

        titleDate = csvRows[0]
        csvRows = csvRows[1:]
        for i in range(len(titleDate)):
            titleDate[i] = titleDate[i].split('/')

        for i in titleDate:
            if int(i[1]) < 10:
                urls.append('https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_'+str(i[0])+'0'+str(i[1]))
            else:
                urls.append('https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_'+str(i[0])+str(i[1]))

        for i in range(len(urls)):
            rewardSet.append(self.getRewardNumber(urls[i]))
            rewardSet[len(rewardSet)-1].extend(titleDate[i])

        for row in csvRows:
            for index in range(len(row)):
                ans += self.getReward(rewardSet[index], row[index], winTicket)

        self.ticketText_var.set('中獎金額:{}\n中獎名單:'.format(ans))

        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self.master, width=50, height=40)
        self.listbox.pack(pady=5)

        for i in winTicket:
            self.listbox.insert(tk.END, i)

        return ans

        # 1-base 特別獎1000萬:1 二獎200萬:4 頭獎20萬:6 七碼相同4萬:8 末六碼相同1萬:9 末五碼相同4千:10 末四碼相同1千 末三碼相同200  增開六獎200元:13

    def drawChart(self):
        self.chartText_var.set("")
        self.chartIndex = 0
        self.dictArr = [dict1000, city1000, dict200, city200]
        self.instanciateChart()

    def instanciateChart(self, event=None):
        drawitems = self.dictArr[self.chartIndex]
        labelArr = ['1000萬中獎物品統計(點一下圖片可看其他統計)', '1000萬中獎城市統計(點一下圖片可看其他統計)',
                    '200萬中獎物品統計(點一下圖片可看其他統計)', '200萬中獎城市統計(點一下圖片可看其他統計)']

        self.claerBottom()
        self.chartText_var.set(labelArr[self.chartIndex])
        if not self.chartIndex&1:
            self.itemText_var.set('物品總數:'+str(len(drawitems)))
        self.chartIndex += 1
        self.chartIndex %= 4

        if len(drawitems) > 15 and self.chartIndex&1:
            drawitems = dict(drawitems.most_common(15))
        if not self.chartIndex&1:
            drawitems = dict(drawitems.most_common(len(drawitems)))
            
        fig = plt.figure(figsize=(20*len(drawitems)/20, 5))
        value = []
        x_labels = []
        for i, j in drawitems.items():
            x_labels.append(i)
            value.append(j)
        plt.bar(x_labels, value)
        plt.xticks(rotation=90)

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        self.canvasPic = canvas.get_tk_widget()
        self.canvasPic.bind("<Button-1>", self.instanciateChart)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1, pady=5)

my_gui = myGUI()
