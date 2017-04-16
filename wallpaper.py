import ctypes
import os
from PIL import Image
import requests
from bs4 import BeautifulSoup, SoupStrainer
from datetime import date
import urllib.request
import sys


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
    temp_img_path = resize_img(image_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, temp_img_path, 3)
    os.remove(temp_img_path)
    return None


def resize_img(file):
    temp_img_path = file
    img_obj = Image.open(file)
    img_l, img_w = img_obj.size
    user32 = ctypes.windll.user32
    sys_l, sys_w = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if img_l > sys_l and img_w > sys_w:
        x = min(img_l-sys_l, img_w-sys_w)
        img_obj2 = img_obj.resize((img_l-x, img_w-x))
        temp_img_path = os.getcwd() + "\\" + "wallpapers\\" + "temp.jpeg"
        img_obj2.save(temp_img_path)
    return temp_img_path


set_wallpaper()
