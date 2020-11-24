# -*- coding: utf-8 -*- 

from collections import defaultdict

import pickle
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import pyperclip

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from datetime import datetime


def clipboard_input(driver, xpath, user_input, os):
    pyperclip.copy(user_input)
    driver.find_element_by_xpath(xpath).click()
    if os == "window":
        ActionChains(driver).key_down(Keys.CONTROL).send_keys(
            'v').perform()
    else:
        ActionChains(driver).key_down(Keys.COMMAND).send_keys(
            'v').perform()

def lookup(driver, folder_name):
    try:
        saved = driver.find_elements_by_class_name("SAVED")
        len_saved = len(saved)
        i=0
        while i<len_saved:
            if saved[i].text == folder_name:
                # 이미 즐겨찾기에 추가되어있는 place일 경우 스킵한다.
                driver.find_element_by_link_text("레이어 닫기").click()
                return
            i +=1
    except:
        pass
    try:
        driver.find_element_by_link_text(folder_name).click()
    except:
        driver.find_element_by_link_text('새 폴더 추가').click()
        driver.find_element_by_id('folderName').send_keys(folder_name)
        driver.find_element_by_xpath(
            '/html/body/div[20]/div[4]/form/fieldset/div[3]/button').click()
    time.sleep(1)
    ActionChains(driver).key_down(Keys.ENTER).perform()

def main(args):
    folder_name = args.folder

    option = Options()

    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=option)

    driver.get("https://map.naver.com/v5/favorite/myPlace/folder/")

    time.sleep(1)
    clipboard_input(driver, '//*[@id="id"]', args.naver_id, args.os)
    clipboard_input(driver, '//*[@id="pw"]', args.naver_pw, args.os)
    driver.find_element_by_id("log.login").click()

    time.sleep(5)
    categ_list = driver.find_element_by_class_name('list_place').text.split("\n")
    categ_size = len(categ_list)

    for i in range(categ_size):
        try:
            folder = driver.find_element_by_xpath(f'//*[@id="container"]/shrinkable-layout/div/favorite-layout/favorite-list/div/favorite-place-folder-list/ul/li[{i}]/a/div/span[1]')
            if folder_name == folder.text:
                folder.click()
        except:
            pass

    time.sleep(5)

    address_list = driver.find_element_by_xpath(
        '//*[@id="container"]/shrinkable-layout/div/favorite-layout/favorite-list/favorite-place-bookmark-list/div[2]/place-list-item/ul').text

    address_list = address_list.split("\n")
    total = []
    
    for i in range(0, len(address_list), 3):
        dic = defaultdict(str)
        dic["name"] = address_list[i]
        dic["address"] = address_list[i+1]
        total.append(dic)

    driver.get("https://map.kakao.com/")
    driver.find_element_by_css_selector("img")
    try:
        driver.find_element_by_class_name("layer_body").click()
    except:
        pass
    driver.find_element_by_id("btnLogin").click()

    clipboard_input(
        driver, '//*[@id="loginEmailField"]', args.kakao_id, args.os)
    clipboard_input(
        driver, '//*[@id="login-form"]/fieldset/div[3]', args.kakao_pw, args.os)
    driver.find_element_by_class_name("submit").click()

    num_restaurant = len(total)
    for i in range(num_restaurant):
        if i % 100 == 0 and i != 0:
            folder_name = folder_name + str(i//100)
        keyword = f"{total[i]['address']} {total[i]['name']}"
        time.sleep(1)
        driver.find_element_by_id("search.keyword.query").clear()
        driver.find_element_by_id("search.keyword.query").send_keys(keyword)
        time.sleep(1)
        submit = driver.find_element_by_id("search.keyword.submit")
        driver.execute_script("arguments[0].click();", submit)
        
        time.sleep(2)

        if (driver.find_element_by_class_name("noPlace").is_displayed()) or (driver.find_element_by_class_name("message").is_displayed() and driver.find_element_by_class_name("addrtitle").text == "주소"):
            # invalid place
            continue

        if driver.find_element_by_class_name("retry").is_displayed():
            time.sleep(1)
            try:
                # 가끔 즐겨찾기 추가하라고 파란색 이미지 뜨는거 꺼주기
                driver.find_element_by_class_name("layer_body").click()
            except:
                pass
            keyword = total[i]['name']
            driver.find_element_by_id("search.keyword.query").clear()
            driver.find_element_by_id("search.keyword.query").send_keys(keyword)
            ActionChains(driver).key_down(Keys.ENTER).perform()

        time.sleep(1)
        driver.find_element_by_class_name("fav").click()

        time.sleep(3)
        lookup(driver, folder_name)
        time.sleep(1)

    time.sleep(3)
    driver.quit()





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--naver_id', type=str, required=True)
    parser.add_argument('--naver_pw', type=str, required=True)
    parser.add_argument('--kakao_id', type=str, required=True)
    parser.add_argument('--kakao_pw', type=str, required=True)
    parser.add_argument('--folder', type=str, required=True)
    parser.add_argument('--os', type=str, required=True)
    args = parser.parse_args()

    main(args)
    print("Sharing completed")
