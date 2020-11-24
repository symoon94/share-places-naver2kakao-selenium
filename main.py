# Author: Sooyoung Moon
# -*- coding: utf-8 -*-

from collections import defaultdict

import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pyperclip

import time


def clipboard_input(driver, xpath, user_input, os):
    pyperclip.copy(user_input)
    driver.find_element_by_xpath(xpath).click()
    if os == "window":
        ActionChains(driver).key_down(Keys.CONTROL).send_keys(
            'v').perform()
    else:
        ActionChains(driver).key_down(Keys.COMMAND).send_keys(
            'v').perform()


def sign_in_naver(driver, args):
    driver.get("https://map.naver.com/v5/favorite/myPlace/folder/")
    time.sleep(1)
    clipboard_input(driver, '//*[@id="id"]', args.naver_id, args.os)
    clipboard_input(driver, '//*[@id="pw"]', args.naver_pw, args.os)
    driver.find_element_by_id("log.login").click()


def sign_in_kakao(driver, args):
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


def get_naver_places(driver, naver_folder, total_list):
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'list_place')))

    num_places = driver.find_element_by_xpath(
        '// *[@id="container"]/shrinkable-layout/div/favorite-layout/favorite-list/favorite-list-option-area/div/span/span').text

    elem = driver.find_elements_by_class_name('item_place')
    i = 0
    while True:
        try:
            time.sleep(0.1)
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", elem[i])
            if elem[i].text.split("\n")[0] == naver_folder:
                elem[i].click()
                break
        except:
            pass
        i += 1

    time.sleep(5)

    address_list = driver.find_elements_by_class_name("item_result")
    len_address_list = len(address_list)

    for i in range(len_address_list):
        infos = address_list[i].text.split("\n")
        dic = defaultdict(str)
        dic["name"] = infos[0]
        dic["address"] = infos[1]
        total_list.append(dic)

    print(f'네이버 "{naver_folder}"에서 가져온 장소 토탈 {len_address_list}개')
    return total_list


def search(driver, keyword):
    driver.find_element_by_id("search.keyword.query").clear()
    words = keyword.split()
    for word in words:
        driver.find_element_by_id("search.keyword.query").send_keys(word + " ")
    ActionChains(driver).key_down(Keys.ENTER).perform()


def get_color(color):
    if color == "red":
        return 'favoriteColor1'
    elif color == "yellow":
        return 'favoriteColor2'
    elif color == "orange":
        return 'favoriteColor3'
    elif color == "green":
        return 'favoriteColor5'
    elif color == "purple":
        return 'favoriteColor6'
    elif color == "pink":
        return 'favoriteColor7'
    else:  # color=="light green"
        return 'favoriteColor4'


def lookup(driver, folder_name, count, new_added, shape, color):
    try:
        saved = driver.find_elements_by_class_name("SAVED")
        len_saved = len(saved)
        i = 0
        while i < len_saved:
            if saved[i].text == folder_name:
                # 이미 즐겨찾기에 추가되어있는 place일 경우 스킵한다.
                driver.find_element_by_link_text("레이어 닫기").click()
                return count + 1, new_added
            i += 1
    except:
        pass

    folderExist = False
    folders = driver.find_elements_by_class_name("txt_folder")
    for folder in folders:
        if folder.text == folder_name:
            folder.click()
            folderExist = True
            break

    if not folderExist:
        driver.find_element_by_link_text('새 폴더 추가').click()
        time.sleep(3)
        driver.find_element_by_class_name('btn_option').click()
        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.LINK_TEXT, shape)))
        element.click()
        time.sleep(3)
        driver.find_element_by_id('folderName').send_keys(folder_name)
        time.sleep(3)
        driver.find_element_by_xpath(
            '/html/body/div[20]/div[4]/form/fieldset/div[3]/button').click()

    element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, color)))
    element.click()
    driver.find_elements_by_class_name('btn_submit')[0].click()
    return count + 1, new_added + 1


def main(args):
    kakao_folder = args.kakao_folder
    color = get_color(args.color)

    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=option)

    sign_in_naver(driver, args)

    total = []
    for naver_folder in args.naver_list:
        total = get_naver_places(driver, naver_folder, total)
        driver.back()

    num_restaurant = len(total)
    print(f'네이버에서 가져온 장소 토탈 {num_restaurant}개')

    sign_in_kakao(driver, args)

    count = 0
    new_added = 0
    for i in range(num_restaurant):
        if i % 10 == 0:
            print(f"{int((i/num_restaurant)*100)}% 진행 중...")
        if count % 100 == 0 and count != 0:
            kakao_folder = args.kakao_folder + str(i//100)
        keyword = f"{total[i]['address']} {total[i]['name']}"
        time.sleep(2)
        search(driver, keyword)
        time.sleep(2)
        if driver.find_element_by_class_name("message").is_displayed() and driver.find_element_by_class_name("addrtitle").text == "주소":
            # invalid place
            continue

        try:
            # 가끔 즐겨찾기 추가하라고 파란색 이미지 뜨는거 꺼주기
            driver.find_element_by_class_name("layer_body").click()
        except:
            pass

        if driver.find_element_by_class_name("retry").is_displayed():
            time.sleep(2)
            keyword = total[i]['name']
            search(driver, keyword)

        try:
            element = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "fav")))
            element.click()
            time.sleep(1)
            count, new_added = lookup(
                driver, kakao_folder, count, new_added, args.shape, color)
            time.sleep(1)
        except:
            pass

    time.sleep(3)
    driver.quit()
    print(f'카카오 "{kakao_folder}"에 공유된 장소 토탈 {count}개')
    print(f'그 중 새롭게 공유된 장소 {new_added}개')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--naver_id', type=str, required=True)
    parser.add_argument('--naver_pw', type=str, required=True)
    parser.add_argument('--naver_folder', type=str,
                        action='append', dest='naver_list', required=True)
    parser.add_argument('--kakao_id', type=str, required=True)
    parser.add_argument('--kakao_pw', type=str, required=True)
    parser.add_argument('--kakao_folder', type=str)
    parser.add_argument('--shape', type=str, default="like",
                        help='star, heart, thunder, check, eye, smile, shine, clover, rect, like')
    parser.add_argument('--color', type=str, default="red",
                        help='red, yellow, orange, light green, green, purple, pink')
    parser.add_argument('--os', type=str, required=True, help='mac, window')
    args = parser.parse_args()

    if args.kakao_folder == None:
        args.kakao_folder = args.naver_list[0]

    main(args)
    print("Sharing completed")
