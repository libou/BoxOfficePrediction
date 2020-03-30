import requests
from WebScraping.proxy.proxy_pool import Proxy


def test_proxy(proxy, https_url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    try:
        proxies = {"https": proxy}
        res = requests.get(https_url, headers=headers, proxies=proxies, timeout=10)
        content = res.content.decode("utf-8")

        # print(res.status_code)
        # print(content)
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
    url = "https://www.imdb.com/search/title/?release_date=2019-01-01,2019-12-31&sort=num_votes,desc&ref_=adv_prv"
    if not test_proxy(proxy, url):
        count += 1
        print("Wrong Proxy: {}".format(proxy))
print("Total Count of Wrong Proxies: {}".format(count))

