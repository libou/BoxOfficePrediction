"""
Crawl free proxy ip address and Create proxy pool
"""
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests


class Proxy(object):
    _instance = None

    def __new__(cls, proxyfile):
        if not isinstance(cls._instance, cls):
            cls._instance = super(Proxy, cls).__new__(cls)
            with open(proxyfile) as f:
                content = f.read()
                lines = content.split("\n")
                cls._instance._proxies = lines[:-1]
                cls._instance._curr = 0
        return cls._instance

    def get_proxy(self):
        idx = self._curr % len(self._proxies)
        proxy = self._proxies[idx]
        self._curr += 1
        return proxy


def get_proxy(page_no):
    url = "https://www.xicidaili.com/nn/{}".format(page_no)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'})
    response = urlopen(req)
    assert (response.getcode() == 200)
    response = response.read()

    result = []

    container = BeautifulSoup(response, 'html.parser')
    proxy_ips = container.table.find_all('tr')[1:]
    for proxy_ip in proxy_ips:
        elements = proxy_ip.find_all('td')
        protocol = elements[5].text
        if protocol != 'HTTPS':
            continue
        ip = elements[1].text
        port = elements[2].text
        proxy = "https://{}:{}".format(ip, port)
        result.append(proxy)

    return result


def test_proxy(proxy):
    https_url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start=0&limit=100"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    try:
        proxies = {"https": proxy}
        r = requests.get(https_url, headers=headers, proxies=proxies, timeout=10)
        content = r.content.decode("utf-8")

        print(r.status_code)
        print(content)
        if r.status_code == 200:
            return True
        return False
    except Exception as e:
        msg = str(e)
        print(msg)
        return False


