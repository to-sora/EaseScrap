import requests
from bs4 import BeautifulSoup
import os
import re
import sys
import pickle
import csv
import _thread
import re
import random
import os
import time
import hashlib
from urllib.parse import urljoin
import csv
import threading
import queue
import tqdm
from BaseClass import setup, PageInterface ,Controller ,WebsitePage

class Demo(WebsitePage):
    """
    A class that represents a demo page of a website.

    Attributes:
    -----------
    htm : str
        The HTML content of the page.
    url : str
        The URL of the page.
    tiitle : str
        The title of the page.
    dir : str
        The directory where the page will be saved.
    loggingfile : str
        The path of the log file.

    Methods:
    --------
    extract_text(dir)
        Extracts the text from the page and saves it to a file.
    extract_links(dir='')
        Extracts all links from the page and saves them to a file.
    worker_func(**kwargs)
        A worker function for multithreading.
    """
class Demo(WebsitePage):
    def __init__(self, htm, url, tiitle='' , dir='',loggingfile=''):
        super().__init__(htm, url, tiitle, dir,loggingfile=loggingfile)
        self.links = []
        
    def extract_text(self, dir):
        '''
        extract text from novel page
        '''
        ## extract all paragraphs from soup
        try:
            ### get all class you want and extract all detail

            pass
            # content = self.soup.find('div', class_='contentbox')
            # content = str(' '.join([i.get_text() for i in content]))
            # if len(content) == 0:
            #     self.log_control(f'No content in page{self.title}')
            #     return False
            # self.log_control(content[:25].strip() + '...'+content[-25:].strip()+'| '+str(len(content)))
            # self.extracted_pth = os.path.join(dir, str(self.title+'__'+self.uniqued_id) + '.txt').strip().replace(' ', '')
            # with open( self.extracted_pth, 'w') as f:
            #     f.write(content)
            self.extracted = True
        except Exception as e:
            self.log_control(e)
            self.log_control('fail to extract text')
            ## using base class extract text
            super().extract_text(dir)

    def extract_links(self, dir=''):
        '''
        extract all links from  page
        reconstruct all links to absolute path
        save if dir is not empty
        return list of links(str)
        '''
        try:
            links = []
            for link in self.soup.find_all('a'):
                #self.log_control(link)
                href = link.get('href')
                #self.log_control(href)
                if href and not href.startswith('http'):
                    href = urljoin(self.url, href)
                #self.log_control(href)
                links.append(href)
            # remove None
            links = [i for i in links if i]
            # unique
            links = list(set(links))
            # remove all links not start with http 
            links = [i for i in links if i.startswith('http')]
            # remocelen > 86
            if dir:
                self.link_pth = os.path.join(dir, str(self.title+'__'+self.uniqued_id) + '.link').strip()
                with open(self.link_pth, 'w') as f:
                    for i in links:
                        f.write(i+'\n')
        except Exception as e:
            self.log_control(e)
            self.log_control('fail to extract links in NovelPage')
            links = []
        return links
    def worker_func(self,**kwargs):
        '''
        worker function for multithreading
        '''
        self.extract_text(self.dir)
        # extrac save html in **kwargs
        if 'save_html' in kwargs:
            if kwargs['save_html']:
                self.save_html(self.dir)
        link = self.extract_links()
        state = self.get_state()
        return link, state
    


def main():
    # recorder driver init time

    args = sys.argv
    usearg=False
    if len(args) == 3:
        v1 = args[1]
        v2 = args[2]
        usearg=True
    
    
    init_time = time.time()
    driver = setup()

    print('driver init time: ', time.time() - init_time)
    init_url = 'https://zh.wikipedia.org/zh-hk/Wiki'
    controller = Controller(init_url, 'scrapped/'
                            ,thread_limit=3,driver=driver,page_class=NovelPage
                            ,loggingfile='scrapped/log.txt')
    time.sleep(1)
    #assert False
    init_time = time.time()

    if usearg:
        print('v1: ', v1)
        print('v2: ', v2)
        controller.loop(int(v1),int(v2),data={'save_html':False},wait_time=2,randomize=True)
    else:
        controller.loop(4,10,data={'save_html':True},wait_time=1,randomize=False)
    print('loop time: ', time.time() - init_time)
    toatl_size, total_len = controller.analy_dir()
    print('total size: ', toatl_size)
    print('total len: ', total_len)


    driver.close()
    driver.quit()
print('start')           
main()
    
