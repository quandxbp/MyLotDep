from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from inspect import getmodule

def get_soup(url):
    soup = False
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, verify=False, timeout=7)
        raw = response.content
        soup = BeautifulSoup(raw, 'lxml')
    except Exception as error:
        print("Error when requesting to %s" % url)
        print(error)
    return soup
