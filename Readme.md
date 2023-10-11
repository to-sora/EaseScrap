# EaseScrap
The web scraping process will begin in the "initurl" . It will retrieve all URLs from the web, filter out any unwanted URLs, and store them in a database. Then, a batch of random URLs will be selected from the database for further scraping. To handle this process efficiently, multiple threads will be utilized.

There are two classes involved in this process: "Controller" and "Demo". The "Controller" class is responsible for managing the threading operations and db manage, while the "Demo" class handles the extraction of text and the filtering of links from the scraped data which is ina function called by "Controller"

This project is a demo of how to use a Python script to do webscrap with  fault tolerance.

## Installation

1. Clone the repository to your local machine.
2. Create a virtual environment using `python -m venv venv`.
3. Activate the virtual environment using `source venv/bin/activate`
4. Install the required packages using `pip install -r requirements.txt`.
5. Create a dir for storage all data you wish to extracted. One dir per one websiter per one .py script
6. download firefox and web driver (other webdriver also should be work)

## Usage

1. Modify the path in `script` to point to the correct file location of .db .log 
2. Run the script using `python demo.py` with or without args
3. The output will be saved in dir and log and db 


## Modifying the demo.py to your target web

1. Modify the TODO list as needed in demo.py (refering to the url, dir .etc)
2. Save the file and run `python demo.py arg1 arg2 arg3` to see the updated list.
<br>    arg1     : number of round <br>   arg2     : page per round <br>   arg3     : time interval



## Working in batch
Make use of script in scrip directory to run job in background and in batch by `nohup`

