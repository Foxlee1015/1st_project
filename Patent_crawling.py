# -*- coding:utf-8 -*-
import csv
import matplotlib.pyplot as plt
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

# a = keywords, b = number of patents
def Get_patent_data(): #def Get_patent_data(a , b):
    driver = webdriver.Chrome('chromedriver_win32\chromedriver')
    driver.implicitly_wait(3)
    driver.get('https://www.google.com/?tbm=pts') # 구글특허 접속
    driver.find_element_by_name('q').send_keys("자기부상") # Keyword = 자기부상
    driver.find_element_by_xpath('//*[@id="lga"]').click()  # 자동완성 없애기 위해 바탕 클릭
    driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div/div[3]/center/input[1]').click()

    t = [] # 명칭
    da = [] # 출원일
    inv = []  # 출원인
    abs = [] # 요약
    for j in range(1, 3): # pages  -> start from j+1 = 2
        for i in range(0, 10): # 검새하고자하는 특허의 수  //  # 일단 테스트로 하나만, range 변경 필요!
            element = driver.find_element_by_xpath('//*[@id="rso"]/div/div/div[{0}]/div/div/div[1]/a/h3'.format(i+1))
            ActionChains(driver) \
            .key_down(Keys.CONTROL) \
            .click(element) \
            .key_up(Keys.CONTROL) \
            .perform()
            print('test')
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(5)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.select('#title')   # 타이틀
            for content in title:
                con = content.text
                title_list = con.split('\n')
            t.append(title_list[-2])

            date = soup.find('div', {'class' : 'publication style-scope application-timeline'}) # 출원일
            da.append(date.text)

            inventors = soup.select('#link') # 출원인
            for inventor in inventors:
                invent = inventor.text
                invent_list = invent.split('\n')
                if invent_list[0].find("Application filed by") == 0:
                    names = invent_list[0][21:]
                    inv.append(names)
            driver.implicitly_wait(10)

            abstract = soup.find('abstract')  # 요약
            if abstract == None:
                abs_text = "None"
            else:
                abs_text = abstract.text[1:-2]     # abstract.text 앞의 \n 제거
            abs.append(abs_text)
            x = (j-1)*10 + i

            print("Title :", t[x], sep=" ")
            print("Publication date :", da[x], sep=" ")
            print("Application filed by :", inv[x], sep=" ")
            print("Abstract :", abs[x], sep=" ")

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print("Loop_page_", str(j), "_",str(i+1) )
        driver.find_element_by_xpath('// *[ @ id = "nav"] / tbody / tr / td[{0}] / a'.format(j + 2)).click()
        time.sleep(5)
    print(t)
    print(da)
    print(inv)
    print(abs)
    
    with open("report.csv", 'w') as file:  # -> 오류 뜨는 부분 전까지 출력됨
    #with open("report.csv", 'w', encoding: "utf-9")  ->  오류는 안뜨나 한글이 다 꺠짐
        file.write('명칭, 출원일, 출원인, 요약\n')
        for k in range(len(t)):
            if "," in t[k]:
                t[k] = t[k].replace(","," ")
            if "," in da[k]:
                da[k] = da[k].replace(",", " ")
            if "," in inv[k]:
                inv[k] = inv[k].replace(",", " ")
            if "," in abs[k]:
                abs[k] = abs[k].replace(","," ")
            file.write("{0},{1},{2},{3}\n".format(t[k], da[k], inv[k], abs[k]))
    

    #출원일에서 출원년도만 저장하기
    with open("report_year.csv", 'w') as file:
        for s in range(len(da)):
            file.write("{0},{1}\n".format(s+1,da[s][:4]))

Get_patent_data()

# 연도 파일 열어서 횟수로 다시 저장
f = open("report_year.csv", 'r')
lines = csv.reader(f)
years = list(range(1960,2020))
year_count = [0 for i in range(1960,2020)]
for line in lines:
    for i in range(len(years)):
        if int(line[1]) == years[i]:
            year_count[i] += 1

with open("report_year_count.csv", 'w') as file:
    file.write('년도, 횟수\n')
    for i in range(len(years)):
        file.write("{0},{1}\n".format(years[i], year_count[i]))

# 그래프
plt.plot(years, year_count)
plt.axis([1960, 2020, 0, 8])
plt.show()

# t, da, inv, abs -> 우분투 mysql 에 저장하기

