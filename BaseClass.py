import requests
from bs4 import BeautifulSoup
import os
import re
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
import time
def setup():
    '''
    return selenium fire fox headless
    
    '''
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service

    options = Options()
    options.headless = True

    
    #options.binary_location = 'geckodriver'
    driver = webdriver.Firefox(options=options)
    return driver

import re
def extract_chinese(inputstring):

    '''
    extract chinese word from html and keep emojis and punctuation marks

    '''
    inputstring = str(inputstring)
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+|[^\u4e00-\u9fff\s]+')
    chinese_words = chinese_pattern.findall(inputstring)
    print(chinese_words)
    chinese_words = "".join(chinese_words)
    chinese_words = chinese_words.replace('\n', ' ')
    
    return chinese_words

from abc import ABC, abstractmethod
class PageInterface(ABC):
    """
    An abstract base class for defining the interface of a web page.

    Attributes:
    -----------
    None

    Methods:
    --------
    get_title() -> str:
        Returns the title of the web page.

    save_html(dir: str):
        Saves the HTML content of the web page to a specified directory.

    extract_text(dir: str):
        Extracts the text content of the web page and saves it to a specified directory.

    get_state() -> dict:
        Returns the state of the web page.

    extract_links(dir: str = '') -> list:
        Extracts the links from the web page and returns them as a list.

    worker_func(**kwargs) -> tuple:
        A worker function that performs a specific task on the web page and returns the result as a tuple.
    """
    @abstractmethod
    def __init__(self, htm:str, url:str, tiitle='' , dir='',loger= None):
        pass
    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def save_html(self, dir: str):
        pass

    @abstractmethod
    def extract_text(self, dir: str):
        pass

    @abstractmethod
    def get_state(self) -> dict:
        pass

    @abstractmethod
    def extract_links(self, dir: str = '') -> list:
        pass

    @abstractmethod
    def worker_func(self, **kwargs) -> tuple:
        """
        Abstract method that defines the worker function for a subclass.
        
        Args:
        - **kwargs: keyword arguments that can be used by the subclass to define the worker function.
            usually, the keyword arguments are used to pass the parameters of the worker function.
            it will get by looper and pass to worker_func
        
        Returns:
        - A tuple containing the results of the worker function.
        """
        pass
    

import hashlib
import os
from bs4 import BeautifulSoup

class WebsitePage(PageInterface):
    """
    A class representing a website page.

    Attributes:
    -----------
    html : str
        The HTML content of the page.
    url : str
        The URL of the page.
    title : str
        The title of the page.
    soup : BeautifulSoup object
        A BeautifulSoup object representing the parsed HTML content.
    text : str
        The extracted text content of the page.
    extracted_pth : str
        The path where the extracted text content is saved.
    orginal_path : str
        The path where the original HTML content is saved.
    extracted : bool
        A flag indicating whether the text content has been extracted.
    dir : str
        The directory where the HTML and text content will be saved.
    uniqued_id : str
        A unique ID generated from the title of the page.

    Methods:
    --------
    get_title() -> str:
        Returns the title of the page.
    save_html(dir: str):
        Saves the HTML content of the page to a file.
    extract_text(dir: str):
        Extracts the text content of the page and saves it to a file.
    get_state() -> dict:
        Returns a dictionary containing the state of the object.
    """
    def __init__(self, htm, url, tiitle='', dir='',loggingfile= None):
        """
        Initializes a new instance of the WebsitePage class.

        Parameters:
        -----------
        htm : str
            The HTML content of the page.
        url : str
            The URL of the page.
        tiitle : str, optional
            The title of the page. If not provided, it will be extracted from the HTML content.
        dir : str, optional
            The directory where the HTML and text content will be saved.
        """
        self.html = htm
        self.url = url
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.text = ''
        self.extracted_pth = ''
        self.orginal_path = ''
        self.extracted = False
        self.dir = dir
        self.loggingfile = loggingfile
        self.islogging = True if loggingfile != '' else False
        if tiitle == '':
            ## extract title from html bt beautifulsoup
            self.title = self.soup.title.string
            ## remove all html / txt / jpg in title
            self.title = self.title.replace('.html','').replace('.txt','').replace('.jpg','')
            # remove space /n all space eement
            self.title = self.title.strip()
            self.title = self.title.replace('\n','')
            self.title = self.title.replace('\t','')
            ## remove invalid char for file name in Ubuntu and Windows
            self.title = re.sub(r'[\\/:*?"<>|]', '', self.title)
        else:
            self.title = tiitle

        ## init a unique id for titelname using 20 digits hash
        
        self.uniqued_id = str(hashlib.sha1(self.title.encode('utf-8')).hexdigest()[:20])
    def log_control(self,x,*args,**kwargs):
    ## fromat string linke print 
        x = str(x)
        x += ' '.join([str(i) for i in args]).replace('\n','')
        if 'end' in kwargs:
            x += kwargs['end']
        
        ## add time string
        x = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '  ' + x
        if self.islogging:
            with open(self.loggingfile,'a') as f:
                f.write(x+'\n')
        else:
            print(x)
    def get_title(self) -> str:
        """
        Returns the title of the page.

        Returns:
        --------
        str
            The title of the page.
        """
        return self.title

    def save_html(self, dir: str):
        """
        Saves the HTML content of the page to a file.

        Parameters:
        -----------
        dir : str
            The directory where the HTML content will be saved.
        """
        try:
            self.orginal_path = os.path.join(dir, str(self.title+'__'+self.uniqued_id) + '.html').strip().replace(' ', '')
            with open(self.orginal_path, 'w') as f:
                f.write(self.html)
        except Exception as e:
            self.log_control(e)
            self.log_control('fail to save html in base class: WebsitePage')

    def extract_text(self, dir: str):
        """
        Extracts the text content of the page and saves it to a file.

        Parameters:
        -----------
        dir : str
            The directory where the text content will be saved.
        """
        try:
            self.text = self.soup.get_text()
            self.extracted_pth = os.path.join(dir, str(self.title+'__'+self.uniqued_id) + '.txt').strip().replace(' ', '')
            with open(self.extracted_pth, 'w') as f:
                f.write(self.text)
            self.extracted = True
        except Exception as e:
            self.log_control(e)
            self.log_control('fail to extract text from base class: WebsitePage')

    def get_state(self) -> dict:
        """
        Returns a dictionary containing the state of the object.

        Returns:
        --------
        dict
            A dictionary containing the state of the object.
        """
        return {
            "url": self.url,
            "title": self.title,
            "extracted": self.extracted,
            "extracted_pth": self.extracted_pth,
            "orginal_path": self.orginal_path,
            "uniqued_id": self.uniqued_id
        }
    
class Controller:
    """
    A class that controls the web scraping process.

    Attributes:
    - init_url (str): The initial URL to start scraping from.
    - dir (str): The directory to save the scraped data.
    - thread_limit (int): The maximum number of threads to use for scraping.
    - link_csv (str): The path to the CSV file containing the scraped links.
    - driver (WebDriver): The Selenium WebDriver to use for scraping.
    - stop (threading.Event): An event to signal when to stop scraping.
    - page_class (WebsitePage): The class to use for parsing web pages.

    Methods:
    - __init__(self, init_url, dir, thread_limit=5, driver=None, page_class=WebsitePage):
        Initializes the Controller object with the given parameters.
    - get_unvisited(self, item=10, randomize=False):
        Returns a list of unvisited URLs.
    - save(self):
        Saves the Controller object to a file.
    - worker(self, input_queue, output_queue, wdata={}):
        The worker function for multithreading.
    - update_linkcsv(self, output_queue):
        The thread worker for updating the link CSV file.
    - analy_dir(self):
        Analyzes the total size and length of text files in the directory.
    - loop(self, no_target=2, batch=10, randomize=False, data={}):
        The main loop for the Controller object.

    """
    def log_control(self,x,*args,**kwargs):
        ## fromat string linke print 
        x = str(x)
        x += ' '.join([str(i) for i in args]).replace('\n','')
        if 'end' in kwargs:
            x += kwargs['end']
        
        ## add time string
        x = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '  ' + x
        if self.islogging:
            with open(self.loggingfile,'a') as f:
                f.write(x+'\n')
        else:
            print(x)
    def __init__(self, init_url, dir, thread_limit=5, driver=None, page_class=WebsitePage,loggingfile = ''):
        """
        Initializes the Controller object with the given parameters.

        Parameters:
        - init_url (str): The initial URL to start scraping from.
        - dir (str): The directory to save the scraped data.
        - thread_limit (int): The maximum number of threads to use for scraping.
        - driver (WebDriver): The Selenium WebDriver to use for scraping.
        - page_class (WebsitePage): The class to use for parsing web pages.
        """
        self.init_url = init_url
        self.dir = dir
        self.thread_limit = thread_limit
        self.link_csv = os.path.join(dir, 'link.csv')
        self.driver = driver
        self.stop  = threading.Event()
        self.page_class = page_class
        self.loggingfile = loggingfile
        self.islogging = True if loggingfile != '' else False
        ###
        if not os.path.isfile(self.link_csv):
            with open(self.link_csv, 'w') as f:
                self.log_control('create link.csv as cannot find it!')
                f.write('url,title,extracted,extracted_pth,orginal_path,uniqued_id\n')
                ### visit init url
                driver.get(self.init_url)
                driver.implicitly_wait(0.5)
                html = driver.page_source
                
                novel_page = self.page_class(html, self.init_url,loggingfile=self.loggingfile)
                novel_page.save_html(self.dir)
                link_t_be_added = novel_page.extract_links()
                #print(link_t_be_added)
                for link in link_t_be_added:
                    f.write(link+', ,F, , , \n')
    import random

    def get_unvisited(self, item=10, randomize=False):
        '''
        Returns a list of unvisited URLs.

        Parameters:
        - item (int): The maximum number of URLs to return.
        - randomize (bool): Whether to return URLs in random order.

        Returns:
        - unvisited (list): A list of unvisited URLs.
        '''
        try:
            unvisited = []
            self.log_control('getting unvisited url , file R')
            with open(self.link_csv, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    unvisited.append(dict(row))
                unvisited = [row['url'] for row in unvisited if row['extracted'] == 'F'  ]
            ## random sample
            #self.log_control('unvisited len: ', len(unvisited), 'item: ', unvisited)
            if randomize and len(unvisited) > item:
                unvisited = random.sample(unvisited, item)
            else:
                unvisited = unvisited[:item]
        except Exception as e:
            self.log_control(e)
            self.log_control('fail to get unvisited url sleep 3 sec')
            unvisited = []
            time.sleep(3)
        return unvisited

    def save(self):
        '''
        Saves the Controller object to a file.
        '''
        savedict = {
            'init_url': self.init_url,
            'dir': self.dir,
            'thread_limit': self.thread_limit,
            'link_csv': self.link_csv
        }
        with open(os.path.join(self.dir, 'controller.pkl'), 'wb') as f:
            pickle.dump(savedict, f)

    def worker(self, input_queue, output_queue, wdata={}):
        '''
        The worker function for multithreading.

        Parameters:
        - input_queue (queue.Queue): The input queue for the worker.
        - output_queue (queue.Queue): The output queue for the worker.
        - wdata (dict): The data to pass to the worker function.
        '''
        self.log_control(wdata)
        while not self.stop.is_set():
            try:
                if not self.stop.is_set():
                    sub_url, html = input_queue.get(timeout=5)
                else:
                    break             
                thispage = self.page_class(html, sub_url, dir=self.dir,loggingfile=self.loggingfile)
                link , state = thispage.worker_func(**wdata)
                output_queue.put((link, state))
                self.log_control('extracted: ', state["title"])
                input_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                self.log_control(e)
                self.log_control('fail to extract text')
                #input_queue.task_done()
                time.sleep(1)
        self.log_control('worker thread stop')

    def update_linkcsv(self,output_queue):
        '''
        The thread worker for updating the link CSV file.

        Parameters:
        - output_queue (queue.Queue): The output queue for the worker.
        '''
        while not self.stop.is_set():
            try:
                if not self.stop.is_set():
                    link, state = output_queue.get(timeout=5)
                else:
                    break
                self.log_control('update link.csv: ,file R')

                
                with open(self.link_csv, 'r') as f:
                    reader = csv.DictReader(f)
                    rows = [row for row in reader]
                for i in range(len(rows)):
                    if rows[i]['url'] == state['url']:
                        rows[i] = state
                        break
                ### insert unseen link to csv
                for i in link:
                    if i not in [row['url'] for row in rows]:
                        rows.append({'url': i, 'title': '', 'extracted': 'F', 'extracted_pth': '', 'orginal_path': '', 'uniqued_id': ''})
                self.log_control('update link.csv: ,file W')
                with open(self.link_csv, 'w') as f:
                    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                self.log_control('update link.csv: ,file W done')
                output_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                self.log_control(e)
                self.log_control('fail to update link.csv in worker2')
        self.log_control('update_linkcsv thread stop')

    def analy_dir(self):
        '''
        Analyzes the total size and length of text files in the directory.

        Returns:
        - total_size (int): The total size of the directory in bytes.
        - total_len (int): The total length of text files in the directory.
        '''
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(self.dir):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        # analy total len of *.txt
        total_len = 0
        for dirpath, dirnames, filenames in os.walk(self.dir):
            for f in filenames:
                if f.endswith('.txt'):
                    fp = os.path.join(dirpath, f)
                    with open(fp, 'r') as f:
                        total_len += len(f.read())
        self.log_control('total size: ', total_size)
        self.log_control('total len: ', total_len)
        return total_size, total_len

    def loop(self, no_target=2, batch=10, randomize=False, data={},wait_time=0,use_driver=True):
        '''
        The main loop for the Controller object.

        Parameters:
        - no_target (int): The number of targets to scrape.
        - batch (int): The number of URLs to scrape in each batch.
        - randomize (bool): Whether to scrape URLs in random order.
        - data (dict): The data to pass to the worker function.
        '''
        try:

            input_queue = queue.Queue()
            output_queue = queue.Queue()
            # strart worker
            thread_list = []
            for i in range(self.thread_limit):
                thread_list.append(threading.Thread(target=self.worker, args=(input_queue, output_queue), kwargs={"wdata": data}))

            
            # start update link.csv thread
            self.log_control("getting no_target: ", no_target)
            self.log_control("getting batch: ", batch)
            self.log_control("getting randomize: ", randomize)
            self.log_control("getting wait_time: ", wait_time)
            
            thread_list.append(threading.Thread(target=self.update_linkcsv, args=(output_queue,)))
            for i in thread_list:
                i.start()
            fail =0
            for i in range(no_target):
                unvisited = self.get_unvisited(batch, randomize)
                self.log_control("getting round: ", i)
                self.log_control("getting unvisited: ", len(unvisited))
                if len(unvisited) == 0:
                    fail +=1
                    time.sleep(60)
                if fail > 3:
                    self.log_control("fail to get unvisited url 3 times")
                    return False
                else:
                    self.log_control("last unvisited: ", unvisited[-1])
                for url in unvisited:
                    try:
                        if use_driver:

                            self.log_control('get url: ', url)
                            self.driver.get(url)
                            self.log_control('geted url: ', url)


                            # add to input queue
                            html = self.driver.page_source
                        else: 
                            ## use requests
                            self.log_control('get url: ', url)
                            html = requests.get(url).text
                            time.sleep(wait_time)
                        input_queue.put((url, html))
                        if wait_time == 0:
                            time.sleep(random.random())
                        else:
                            time.sleep(wait_time)
                    except Exception as e:
                        self.log_control(e)
                        self.log_control('fail to get url: ', url)
                        continue
            # close input queue if no more task
            input_queue.join()
            output_queue.join()
            
            self.log_control('input_queue join')
            self.log_control('output_queue join')
            self.stop.set()
        except Exception as e:
            self.log_control(e)
        # stop the thread
            return True