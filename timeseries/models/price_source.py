from common.constants import DOMAIN
from common.utils import get_soup

import datetime
import re
import ast
import requests


class PriceSource:

    def get_source(self, source):
        get_price_method = False
        if source == 'jajum':
            get_price_method = self.get_price_jajum
        elif source == 'beetracker':
            get_price_method = self.get_price_beetracker
        return get_price_method


    def _process_raw_url(self, raw_url):
        if 'http' in raw_url:
            raw_url = raw_url.split('/', 3)[-1]
        if '.html' in raw_url:
            raw_url = raw_url.split('.html')[0]

        return raw_url

    def get_price_jajum(self, platform, raw_url):
        processed_url = self._process_raw_url(raw_url)
        jajum_url = "https://jajum.com/products/{domain}/{product_url}". \
            format(domain=DOMAIN[platform], product_url=processed_url)

        soup = get_soup(jajum_url)
        res = {}

        if soup:
            pattern = re.compile('datasets.*borderColor')
            script = soup.find("script", text=pattern).text
            datasets = re.search(r'\[{(.*?)}\]', script, re.MULTILINE | re.DOTALL)

            if datasets:
                datasets = datasets.group(0).strip()
                datasets = datasets.split('\"data\":')[1]
                data_list = json.loads(datasets)

                for record in data_list:
                    timestamp = record.get('x')
                    price = record.get('y')
                    date_time = datetime.datetime.fromtimestamp(float(timestamp) / 1e3)
                    only_date = date_time.strftime("%d-%m-%Y")
                    only_time = str(date_time.time()).split(".")[0]

                    if res.get(only_date):
                        res[only_date].update({only_time: price})
                    else:
                        res[only_date] = {only_time: price}

        return res

    def get_price_beetracker(self, platform, url):
        res = {}
        get_pid_url = "https://www.beetracker.org/process.php"
        try:
            pid_res = requests.post(get_pid_url, {"q": url})

            if pid_res:
                pid = pid_res.json().get('pid')
                if pid:
                    beetracker_url = "https://www.beetracker.org/data/?id=%s" % pid
                    soup = get_soup(beetracker_url)
                    if soup:
                        pattern = re.compile('.*Highcharts.*')
                        script = soup.find("script", text=pattern)
                        if script:
                            datasets = re.search(r'\[\[(.*?)\]\]', script.text, re.MULTILINE | re.DOTALL)

                            if datasets:
                                datasets = datasets.group(0).strip()
                                data_list = ast.literal_eval(datasets)

                                for record in data_list:
                                    timestamp = record[0]
                                    price = record[1]
                                    date_time = datetime.datetime.fromtimestamp(float(timestamp) / 1e3)
                                    only_date = date_time.strftime("%d-%m-%Y")
                                    only_time = str(date_time.time()).split(".")[0]

                                    if res.get(only_date):
                                        res[only_date].update({only_time: price})
                                    else:
                                        res[only_date] = {only_time: price}
                                print("Requesting %s:" % beetracker_url)
        except Exception as err:
            print("Error requesting to BeeTracker")
            print(err)
        return res
