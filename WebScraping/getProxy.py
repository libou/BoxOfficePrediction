from WebScraping.proxyPool import get_proxy

with open("proxy.txt", 'a+') as file:
    for i in range(5):
        proxy_list = get_proxy(i+1)
        file.writelines("%s\n" % proxy for proxy in proxy_list)