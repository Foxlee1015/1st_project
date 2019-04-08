from selenium import webdriver
from bs4 import BeautifulSoup

# a = keywords, b = number of patents
def Get_patent_data(): #def Get_patent_data(a , b):
    driver = webdriver.Chrome('chromedriver_win32\chromedriver')
    driver.implicitly_wait(3)
    driver.get('https://www.google.com/?tbm=pts')
    # put a instead of 자기부상
    driver.find_element_by_name('q').send_keys("자기부상")
    driver.find_element_by_xpath('//*[@id="lga"]').click()  #자동완성 없애기 위해 바탕 클릭
    driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div/div[3]/center/input[1]').click()
    # 일단 테스트로 하나만, range 변경 필요!
    t = []
    da = []
    for i in range(1, 2):
        driver.find_element_by_xpath('//*[@id="rso"]/div/div/div[{0}]/div/div/div[1]/a/h3'.format(i)).click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select('#title')
        for content in title:
            con = content.text
            title_list = con.split('\n')
        t.append(title_list[-2])
        #abstract = soup.find('abstract')
        #abs = abstract.text
        date = soup.find('div', {'class' : 'publication style-scope application-timeline'})
        da.append(date.text)
        print(t)
        print(da)
        # 출원인 부분 수정 필요함
        #inventor = soup.find('data-inventor')

Get_patent_data()