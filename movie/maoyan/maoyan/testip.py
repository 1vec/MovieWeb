import requests

# 要访问的目标页面
headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) " 
                          "Chrome/66.0.3359.139 Safari/537.36 " }
targetUrl = "https://maoyan.com/films?showType=3&yearId=10&sortI"
#targetUrl = "http://proxy.abuyun.com/switch-ip"
#targetUrl = "http://proxy.abuyun.com/current-ip"

# 代理服务器
proxyHost = "http-pro.abuyun.com"
proxyPort = "9010"

    # 代理隧道验证信息
proxyUser = "HU0PGV22PUNAMOXP"
proxyPass = "4B0B5460D5425072"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
  "host" : proxyHost,
  "port" : proxyPort,
  "user" : proxyUser,
  "pass" : proxyPass,
}

proxies = {
    "http"  : proxyMeta,
    "https" : proxyMeta,
}

resp = requests.get(targetUrl, proxies=proxies, headers=headers)

print(resp.text)