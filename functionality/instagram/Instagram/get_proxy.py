import requests
import random



try:


    country = ["http://gimmeproxy.com/api/getProxy?country=CA", "http://gimmeproxy.com/api/getProxy?country=US"]
    url = random.choice(country)
    r = requests.get(url, timeout=10).json()
    ip = r['ip']
    port = r['port']
    print(ip + ':' + port)
    f = open('proxy_file.txt', 'w')
    f.write(ip + ':' + port)
    f.close()
except Exception as e:
    print("Error requesting proxy because: ", e)
    f = open('proxy_file.txt', 'w')
    f.write('0')
    f.close()