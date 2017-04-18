import ctypes
import os
from PIL import Image
import requests
from bs4 import BeautifulSoup, SoupStrainer
from datetime import date
import urllib.request


def img_url():
    home_page = "http://thepaperwall.com"
    source_code = requests.get(home_page)
    plain_text = source_code.text
    soup_filter = SoupStrainer("div", class_="active", style="display:block;")
    soup = BeautifulSoup(plain_text, "html.parser", parse_only=soup_filter)
    link = home_page + "/" + soup.a.get("href")
    return get_img_url(link, home_page)


def get_img_url(link, home_page):
    source_code = requests.get(link)
    plain_text = source_code.text
    soup_filter = SoupStrainer("a", {"class": "wall_img_a", "style": "cursor:pointer;"})
    soup = BeautifulSoup(plain_text, "html.parser", parse_only=soup_filter)
    img_source = home_page + "/" + soup.img.get("src")
    return img_source


def set_wallpaper():
    url = img_url()
    image_path = os.getcwd() + "\\" + "wallpapers\\" + str(date.today()) + ".jpeg"
    urllib.request.urlretrieve(url, filename=image_path)
    resize_img(image_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    return None


def resize_img(file):
    user32 = ctypes.windll.user32
    sys_l, sys_w = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    with Image.open(file) as img_obj:
        img_obj = img_obj.resize((sys_l, sys_w), Image.ANTIALIAS)
        img_obj.save(file, "JPEG")
    return None


if __name__ == "__main__":
    set_wallpaper()
