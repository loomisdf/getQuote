import requests
import time
import shlex
import os

# Get filepath relative to project folder
basepath = os.path.dirname(__file__)
config_filepath = os.path.abspath(os.path.join(basepath, 'config.txt'))

# Config file parameters
previous_day = ''
cached_quote = ''
cached_author = ''

# Get today's date
today = time.strftime('%m/%d/%Y')

# Parse config file
with open(config_filepath, 'r') as f:
    previous_day = f.readline().split()[1]
    cached_quote = shlex.split(f.readline())[1]
    cached_author = f.readline().split('\t')[1]

# If today is a new day ping the qod API, otherwise use the cached config data
if today == previous_day:
    print('{0}\n - {1}'.format(cached_quote, cached_author))
else:
    previous_day = today
    r = requests.get('https://quotes.rest/qod')
    quote_str = r.json()['contents']['quotes'][0]['quote'] 
    quote_author = r.json()['contents']['quotes'][0]['author'] 
    print("{0}\n - {1}".format(quote_str, quote_author))
    with open(config_filepath, 'r+') as f:
        f.seek(0)
        f.write("previous_day:\t{0}\nquote:\t\"{1}\"\nauthor:\t{2}".format(previous_day, quote_str, quote_author))
        f.truncate()
