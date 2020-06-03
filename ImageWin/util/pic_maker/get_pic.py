import requests
from bs4 import BeautifulSoup
import shutil
import time

def soup_go_to(url:str):
    r = requests.get(url)
    content = (r.text)

    soup = BeautifulSoup(content, 'html.parser')
    #print(soup.prettify())
    return soup
'''
def get_photo(url:str) -> None :
    def download_pic(img_set_url:str,label:str):
         r = requests.get(img_set_url, stream=True)
         if r.status_code == 200:
            with open("./img/"+label+".png", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

    photo_page_soup = soup_go_to(url)
    img_tags = photo_page_soup.find_all('img')
    for tag in img_tags:
        if tag.get("src") is not None and tag.get("alt") is not None:
            tag_url = tag.get("src")
            label = str(tag.get("alt"))
            if label[:2]!="Go":
                print(tag_url, label)
                download_pic(img_set_url=tag_url,label=label)
                break




topic=[ "climb-person",
        "Lonely-person",
       ]
for t in topic:
    labels = []
    home_page_soup = soup_go_to('https://unsplash.com/search/photos/'+t)
    a_tags = home_page_soup.find_all('a')
    for tag in a_tags:
        if tag.get("class") is None: continue
        if "_2Mc8_" not in tag.get("class"): continue
        labels.append(tag.get("href")[tag.get("href").rfind("/")+1:])

    for i, label in enumerate(labels):
        print(i)
        get_photo("https://unsplash.com/photos/"+label)
        time.sleep(3)
'''
    

