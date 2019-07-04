import requests
import base64
import time
import random

url = 'http://114.214.176.61/uploadImg/'
file = open('1.jpg', 'rb')
img = base64.b64encode(file.read())
file.close()
headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", 'Connection': 'close'}
# 客户端发送请求报文服务端
for k in range(10):
    for i in range(1, 10):
        j = random.randint(1,10)
        if(j >= 1 and j <= 6):
            data = {'info': '1', 'img': img}
        else:
            data = {'info': '0', 'img': img}
        ret = requests.post(url, data=data, headers=headers)
        time.sleep(1)
print("finsh!")
