#encoding=utf-8
__author__ = 'Administrator'

from bs4 import BeautifulSoup
import requests
import lxml
import pymongo
import  time


client = pymongo.MongoClient('localhost',27017)
ceshi = client['ceshi']
url_lists = ceshi['url_lists']
item_info = ceshi['item_info1']


headers = {
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
}

#spider 1
def get_links_from(channel,pages,who_sells=0):
    #http://bj.58.com/diannao/pn2
    list_view = '{}{}/pn{}/'.format(channel,str(who_sells),str(pages))
    wb_data =requests.get(list_view,headers=headers)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text,'lxml')
    if who_sells == 0:
        for link in soup.select('td.t a.t'):
            item_link = link.get('href').split('?')[0]
            url_lists.insert_one({'url':item_link})
            print(item_link)
    else:
        for link in soup.select('a.business_img'):
            item_link = link.get('href').split('?')[0]
            url_lists.insert_one({'url':item_link})
            print(item_link)

#get_links_from('http://bj.58.com/danche/',2,1)

def get_item_info(url,who_sells=0):
    if url.endswith('html'):
        wb_data = requests.get(url,headers=headers)
        print(url)
        soup = BeautifulSoup(wb_data.text,'lxml')
        if who_sells == 1:
            title = soup.title.text.strip()
            price = soup.select('span.price.c_f50')[0].text.strip()   if soup.find_all('span','price') else None
            date = soup.select('.time')[0].text.strip().split(' ')[0] if soup.find_all('li','time') else None
            area = list(map(lambda x:x[0].text,soup.select('.c_25d a'))) if soup.find_next('span','c_25d') else None
            item_info.insert_one({'title':title,'price':price,'date':date,'area':area,'url':url})
            print({'title':title,'price':price,'date':date,'area':area,'url':url})
        else:
            title = soup.title.text.strip()
            price = soup.select('span.price_now > i')[0].text if soup.select('span.price_now > i') else None
            date = soup.select('li.time')[0].text.strip().split(' ')[0] if soup.find_all('li', 'time') else None
            area = soup.select('div.palce_li > span > i')[0].text if soup.select('div.palce_li > span > i') else None
            item_info.insert_one({'title':title,'price':price,'date':date,'area':area,'url':url})
            print({'title':title,'price':price,'date':date,'area':area,'url':url})
    else:
        pass

#get_item_info('http://bj.58.com/jiadian/31992475328831x.shtml')