import requests
from bs4 import BeautifulSoup
import re


dict1000=dict()



def search(url):
    html=requests.get(url).content.decode('utf-8')
    sp=BeautifulSoup(html,'html.parser')

    table1000 = sp.find('table',{'id':'fbonly'})
    tr1000 = table1000.find_all('tr')

    table200 = sp.find('table',{'id':'fbonly_200'})
    for idx,link in enumerate(tr1000[1:]):



        tdTable=link.find_all('td')
        for i,j in enumerate(tdTable):
            tdTable[i]=tdTable[i].text
        items=tdTable[4]
        # print(items)

        items=re.split('及|、',items)
        print(items)

        # items=re.split('[，|共|等|計|,| ]',tdTable[4])[0]
        # print(items)


        # print(items)




# startDate=input().split(" ")
# endDate=input().split(" ")

url='https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_10105/'
url2='https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_10807/'
url3='https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_10607/'
url4='https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_10407/'
search(url)
print()
search(url2)
search(url3)
search(url4)