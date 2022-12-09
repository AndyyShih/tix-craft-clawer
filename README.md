# 針對拓元售票網站的自動化購票程式

## 自動登入的方式為抓取Session
    先從擴充功能中增加EditThisCoockie，接著登入拓元之後，從擴充功能中找到
    EditThisCoockie選擇匯出，建立一個json檔貼上，留下name跟value即可。
    注意:Session的有效期限約莫一天

## 使用的套件
    selenium
    pillow
    time
    os
    json
    numpy
    tensorflow

## 更新紀錄
    11/28
    新增驗證碼仿生程式，取代抓取驗證碼。
    12/09
    新增模型訓練程式，改寫資料讀取方式。
