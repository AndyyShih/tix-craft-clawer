from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
import time
import os

if not os.path.isdir("./tmp"):
    os.mkdir("./tmp")

if not os.path.isdir("./captcha_img"):
    os.mkdir("./captcha_img")

for i in range(0,5):#抓取張數可自行調整
#開啟瀏覽器
    chrome_options = Options()
    chrome_options.add_argument("--headless")#不開視窗，在背景下處理
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://tixcraft.com/ticket/ticket/22_eaj/13413/1/48')#網頁可能因到期失效

    #抓取整頁截圖
    scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(scroll_width,scroll_height)
    driver.save_screenshot('./tmp/tmp.png')

    #抓取驗證碼圖形位置
    element = driver.find_element(By.ID,'yw0')
    left = element.location['x']
    right = element.location['x'] + element.size['width']
    top = element.location['y']
    bottom = element.location['y'] + element.size['height']

    #切下圖形驗證碼
    img = Image.open('./tmp/tmp.png')
    img = img.crop((left,top,right,bottom))
    img.save(f'./captcha_img/{i}.png')
