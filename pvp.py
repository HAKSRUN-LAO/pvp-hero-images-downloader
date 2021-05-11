import os
import requests
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

print('loading Firefox driver...')
DRIVER = webdriver.Firefox(executable_path = r'geckodriver.exe')

def get_hero_info():
    print('connecting 王者荣耀 hero list page...')
    global DRIVER
    DRIVER.get('https://pvp.qq.com/web201605/herolist.shtml')
    print('getting all hero information...')
    try:
        ul = WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'herolist')))
        lis = ul.find_elements_by_tag_name('li')
        hero_info = {}
        for li in lis:
            a = li.find_element_by_tag_name('a')
            hero_info[a.text] = a.get_attribute('href')
        return hero_info
    except:
        print('getting all hero information error, retrying...')
        get_hero_info()

def get_img_info(hero_name, hero_add):
    print('getting image addresses from ' + hero_name + '...')
    global DRIVER
    DRIVER.get(hero_add)
    try:
        ul = WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pic-pf-list')))
        lis = ul.find_elements_by_tag_name('li')
        skin_info = {}
        for li in lis:
            skin_info[hero_name + '-' + li.text] = 'https:' + li.find_element_by_tag_name('i').find_element_by_tag_name('img').get_attribute('data-imgname')
        return skin_info
    except:
        print('getting image addresses from ' + hero_name + ' error, retrying...')
        get_img_info(hero_name, hero_add)

def get_img(img_name, img_add):
    print('getting ' + img_name + '.jpg...')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    try:
        with requests.get(img_add, headers = headers) as img_res, open(img_name + '.jpg', 'wb') as img:
            img.write(img_res.content)
        print(img_name + '.jpg downloaded')
    except:
        print('getting ' + img_name + '.jpg error, retrying...')
        time.sleep(1.5)
        get_img(img_name, img_add)

def main():
    global DRIVER
    hero_info = get_hero_info()
    for hero_name in hero_info:
        DRIVER.execute_script('window.open("");')
        DRIVER.switch_to.window(DRIVER.window_handles[1])
        img_info = get_img_info(hero_name, hero_info[hero_name])
        for img_name in img_info:
            if not os.path.exists(img_name + '.jpg'):
                get_img(img_name, img_info[img_name])
        DRIVER.close()
        DRIVER.switch_to.window(DRIVER.window_handles[0])
    DRIVER.quit()

if __name__ == '__main__':
    main()