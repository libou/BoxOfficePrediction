import requests
from .proxy_pool import Proxy


def test_proxy(proxy, https_url):
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'path': "/api/keyword_volumes/%23avengersendgame",
        'referer': "https://www.trendsmap.com/historical?q=avengersendgame", 'authority': "www.trendsmap.com",
        'accept': "application/json, text/javascript, */*; q=0.01", 'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9", 'origin': "https://www.trendsmap.com", 'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-origin", 'x-requested-with': "XMLHttpRequest"}
    try:
        proxies = {"http": proxy}
        res = requests.post(https_url, headers=headers, proxies=proxies)
        content = res.content.decode("utf-8")

        # print(res.status_code)
        # print(content)
        print(res.status_code)
        if res.status_code == 200:
            return True
        return False
    except Exception as e:
        msg = str(e)
        print(msg)
        return False


inst = Proxy('proxy.txt')
count = 0
for i in range(inst.get_proxies_num()):
    proxy = inst.get_proxy()
    url = "https://www.trendsmap.com/api/keyword_volumes/%23avengersendgame"
    if not test_proxy(proxy, url):
        count += 1
        print("Wrong Proxy: {}".format(proxy))
print("Total Count of Wrong Proxies: {}".format(count))

