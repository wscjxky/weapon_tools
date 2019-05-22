import random
import time
from requests_html import HTMLSession
session = HTMLSession()
links_arr=[]
for i in range(20):
    i=str(i)
    url='http://img.ivsky.com/img/tupian/pre/201708/16/houzhongdefutoutupian-0%s.jpg'%(i.zfill(2))
    r = session.get(url)
    if r.status_code!=404:
        with open(str(random.randint(1,1000000))+str(i)+'.jpg','wb')as f :
            f.write(r.content)
    time.sleep(1)
