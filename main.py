#encoding=utf-8
__author__ = 'Administrator'
from multiprocessing import Pool
from channel_extract import channel_list
from page_parsing import get_links_from,get_item_info,url_lists,item_info
import pymongo


def get_all_links_from(channel):
    for num in range(1,101):
        get_links_from(channel,num,1)



total_urls = [i['url'] for i in url_lists.find()]
used_urls = [i['url'] for i in item_info.find()]
x = set(total_urls)
y = set(used_urls)
left_urls = x - y

if __name__ == '__main__':
    pool = Pool(processes=6)
    pool.map(get_item_info,list(left_urls))
