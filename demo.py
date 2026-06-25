import requests
from bs4 import BeautifulSoup
import argparse
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
    def __init__(self, htm, url, tiitle='' , dir='',loggingfile='',id=None):
        super().__init__(htm, url, tiitle, dir,loggingfile=loggingfile,id=id)
        self.links = []
        
    def extract_text(self, dir):
        '''
        extract text from novel page
        '''
        ## extract all paragraphs from soup
        try:
            # TODO: change this to your own method to extract text
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


            # TODO: change this to your own method to fiilter out links you don't want
            # e.g. remove links that don't start with 'http' 
            # e.g. remove links that don't contain 'wiki'
            # e.g. remove links that contain 'login'

            
            # unique
            links = list(set(links))
            # remove all links not start with http 
            links = [i for i in links if i.startswith('http')]
            # remocelen > 86
            link = [i for i in links if 'wiki'  in i]
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
    


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description='Run the EaseScrap demo crawler.')
    parser.add_argument('rounds', nargs='?', type=int, default=4,
                        help='number of crawl rounds (default: 4)')
    parser.add_argument('batch', nargs='?', type=int, default=10,
                        help='number of URLs per round (default: 10)')
    parser.add_argument('wait_time', nargs='?', type=float, default=1.0,
                        help='seconds to wait between page loads (default: 1.0)')
    return parser.parse_args(argv)


def main(argv=None):
    # recorder driver init time
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)
    usearg = bool(argv)
    print('start')
    
    init_time = time.time()
    driver = setup()

    print('driver init time: ', time.time() - init_time)

    # TODO: change this to your own url
    init_url = 'https://zh.wikipedia.org/zh-hk/Wiki'


    controller = Controller(init_url, 'scrapped/'                # TODO: <--- change this to your own directory
                            ,thread_limit=3,driver=driver,page_class=Demo
                            ,loggingfile='scrapped/log.txt',     # <--- change this to your own directory
                            use_db=True,db_path='scrapped/scrapped.db')  # <--- change this to your own directory
    time.sleep(1)
    #assert False
    init_time = time.time()

    if usearg:
        print('v1: ', args.rounds)
        print('v2: ', args.batch)
        print('v3: ', args.wait_time)
        controller.loop(args.rounds,args.batch,data={'save_html':False},wait_time=args.wait_time,randomize=False)
    else:
        controller.loop(args.rounds,args.batch,data={'save_html':True},wait_time=args.wait_time,randomize=False)
    # print('loop time: ', time.time() - init_time)
    # toatl_size, total_len = controller.analy_dir()
    # print('total size: ', toatl_size)
    # print('total len: ', total_len)


    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
    
