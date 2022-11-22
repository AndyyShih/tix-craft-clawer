from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from PIL import Image
import time
import json
from keras import models
from keras_preprocessing.image import img_to_array
from keras_preprocessing.image import load_img
import numpy as np
import os
import transfer

if not os.path.isdir("./target_captcha"):
    os.mkdir("./target_captcha")

with open('cookie_tix.json') as j_file:
    cookies = json.load(j_file)
    
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach",True) #保持瀏覽器開啟
driver = webdriver.Chrome(options=chrome_option)
#driver.maximize_window() #視窗最大化
driver.get('https://tixcraft.com/activity/detail/23_mamamoo')

for cookie in cookies:
    driver.add_cookie(cookie)
driver.refresh()

"""節目資訊頁"""
##立即購票
info = driver.find_element(By.XPATH,"/html/body/div[1]/section/div/div/div/ul/li[1]/a")
info.click()
time.sleep(1)

##選擇場次
game= Select(driver.find_element(By.ID,'dateSearchGameList'))
game.select_by_value('2023/01/14 (六)')
time.sleep(1)

##立即訂購
info = driver.find_element(By.XPATH,"/html/body/div[1]/section/div/div/div/div[2]/div[2]/div/table/tbody/tr/td[4]/input")
info.click()
time.sleep(2)

"""選擇位置頁"""
seat = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/div[2]/div[2]/div[2]/ul[2]/li[10]/font')
seat.click()
time.sleep(2)

"""選擇張數頁"""
##設定購買張數2
select = Select(driver.find_element(By.ID,"TicketForm_ticketPrice_02"))
select.select_by_value("2")

##閱讀條款無腦打勾
agree = driver.find_element(By.ID,"TicketForm_agree")
agree.click()

##處理驗證碼
###截取驗證碼
scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
driver.set_window_size(scroll_width,scroll_height)
driver.save_screenshot('./target_captcha/tmp.png')

element = driver.find_element(By.ID,'yw0')
left = element.location['x']
right = element.location['x'] + element.size['width']
top = element.location['y']
bottom = element.location['y'] + element.size['height']

img = Image.open('./target_captcha/tmp.png')
img = img.crop((left,top,right,bottom))
img.save(f'./target_captcha/target.png')

###驗證碼辨識
####切開圖形驗證碼
def split_digits_in_img(img_array):
    x_list = list()
    for i in range(digits_in_img):
        step = img_cols // digits_in_img
        x_list.append(img_array[:, i * step:(i + 1) * step] / 255)
    return x_list

####初始化參數
img_rows = None #驗證碼影像檔的高
img_cols = None #驗證碼影像檔的寬
digits_in_img = 4 #驗證碼碼數
model = None
np.set_printoptions(suppress=True, linewidth=150, precision=9, formatter={'float': '{: 0.9f}'.format})

####如果沒有找到模型即終止程式
if os.path.isfile('cnn_captcha_model.h5'):
    model = models.load_model('cnn_captcha_model.h5')
else:
    print('No trained model found.')
    exit(-1)

target = os.path.basename('./target_captcha/target.png') #驗證碼檔名全名
img_filename = f'./target_captcha/{target}'
img = load_img(img_filename, color_mode='grayscale')
img_array = img_to_array(img)
img_rows, img_cols, _ = img_array.shape
x_list = split_digits_in_img(img_array)

result = ''
for i in range(digits_in_img):
    confidences = model.predict(np.array([x_list[i]]), verbose=0)
    result_class = np.argmax(model.predict(np.array([x_list[i]])), axis=-1)
    #result_class = model.predict_classes(np.array([x_list[i]]), verbose=0)
    #將數字轉回英文
    result_class = transfer.num_to_en(result_class)
    result = result + result_class[0]

###輸入驗證碼
captcha = driver.find_element(By.ID,'TicketForm_verifyCode')
captcha.send_keys(result)
time.sleep(1)

##確認送出
submit = driver.find_element(By.ID,"ticketPriceSubmit")
submit.click()
time.sleep(2)

"""確認訂票頁"""
payment = driver.find_element(By.ID,'PaymentForm_payment_id_54')
payment.click()
check = driver.find_element(By.ID,"submitButton")
check.click()