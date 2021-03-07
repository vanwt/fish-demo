import requests
import threading
from time import clock


data = {'POST': 'AAA', 'key': 'Ezsdfssdfafas23ed323e2sfsfdafa', 'account': 'admin', 'password': 'xinshang123',
            'save': '1', 'tz': '5637', 'email': '1213@qwew.com', 'url': 'www.baidu.com', 'content': '你好'}
sl = []
s = clock()
for i in range(10000):
    sl.append(requests.post(
        "http://127.0.0.1:8000/index?a=1&word=baidu&key=t67t7T7Tut76t78T87tuy8T78T78ygyuy67RTG",
        data=data).status_code)
e = clock()
print(e - s)
num = 0
for i in sl:
    if i != "200":
        num += 1
print(num)