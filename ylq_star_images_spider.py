import os
import requests
import pandas as pd
from fake_useragent import UserAgent

df = pd.read_csv('ylq_star_infos.csv', encoding='utf-8')
print(df.head())

names = df.name.tolist()
image_urls = df.image.tolist()
print(len(image_urls)) # 1282

images_folder = 'webapp/static/images/star/'

if not os.path.exists(images_folder):
    os.makedirs(images_folder)

# http://img.ylq.com/2017/1113/thumb_300_400_20171113111422402.png
# 骆达华 http://img.ylq.com/2014/1203/thumb_300_400_20141203190237562.jpg
for i in range(0, len(image_urls)):
    ua = UserAgent()
    headers ={"User-Agent": ua.random}
    url = image_urls[i]
    pic_name = names[i]
    try:
        pic = requests.get(url=url, headers=headers)
        with open(images_folder+'%s.jpg'% (pic_name),'wb') as fp:
            fp.write(pic.content)
    except:
        pass
    print(i, pic_name, url)