# EaseScrap
The web scraping process begins from the initial URL. It retrieves URLs from the web, filters unwanted URLs, and stores the remaining URLs in a database. Then, a random batch of URLs is selected from the database for further scraping. Multiple threads are used to handle the scraping work efficiently.

There are two main classes involved in this process: "Controller" and "Demo". The "Controller" class manages threading and database operations, while the "Demo" class handles text extraction and link filtering for scraped pages.

This project is a demo of how to use a Python script for fault-tolerant web scraping.
Currently, no package is provided. Start from `demo.py`.

## Installation

1. Clone the repository to your local machine.
2. Create a virtual environment using `python -m venv venv`.
3. Activate the virtual environment using `source venv/bin/activate`
4. Install the required packages using `pip install -r requirements.txt`.
5. Create one output directory per website/script for extracted data.
6. Install Firefox and geckodriver. Other WebDrivers should also work.

## Usage

1. Modify the paths in the script to point to the correct `.db` and `.log` locations.
2. Run the script using `python demo.py` with or without arguments.
3. The demo writes output, log, and database files into `scrapped/` by default. The directory is included with a placeholder; generated files inside it are ignored by git.


## Modifying the demo.py to your target web

1. Modify the TODO list as needed in `demo.py`, including the URL and output directory.
2. Save the file and run `python demo.py [rounds] [batch] [wait_time]` to see the updated list.
<br>    rounds     : number of rounds, default `4` <br>   batch     : pages per round, default `10` <br>   wait_time     : seconds between page loads, default `1.0`



## Working In Batch
Use the `.sh` files in the `scrip/` directory to run jobs in the background with `nohup`.
