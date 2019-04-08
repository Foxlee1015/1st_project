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
    for i in range(0, 10): # 검새하고자하는 특허의 수  //  # 일단 테스트로 하나만, range 변경 필요!
        element = driver.find_element_by_xpath('//*[@id="rso"]/div/div/div[{0}]/div/div/div[1]/a/h3'.format(i+1))
        ActionChains(driver) \
        .key_down(Keys.CONTROL) \
        .click(element) \
        .key_up(Keys.CONTROL) \
        .perform()

        # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        # driver.find_element_by_xpath('//*[@id="rso"]/div/div/div[{0}]/div/div/div[1]/a/h3'.format(i+1)).click()  #// 1, 5, 10 번째 특허 데이터 가져오기 성공

        #print(driver.window_handles)
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
        abs_text = abstract.text[1:-2]     # abstract.text 앞의 \n 제거
        abs.append(abs_text)

        print("Title :", t[i], sep=" ")
        print("Publication date :", da[i], sep=" ")
        print("Application filed by :", inv[i], sep=" ")
        print("Abstract :", abs[i], sep=" ")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        # driver.back()
        #driver.execute_script("window.history.go(-1)")
        print("Loop", str(i))

    print(t)
    print(da)
    print(inv)
    print(abs)

Get_patent_data()
