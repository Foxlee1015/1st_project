from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

#  https://lsjsj92.tistory.com/304 참고

def convert_pdf_to_txt(num):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open('documents\sample{0}.pdf'.format(num), 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password =""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    with open("textfiles\pat_{0}.text".format(num), 'w') as file:
        file.write(text)
    fp.close()
    device.close()
    retstr.close()
    return text

for i in range (1, 13):                # 특허 전문 12개 = range(1,13)
    v = convert_pdf_to_txt(i)
# 함수 안에서 x
data = []
for i in range(1,13):
    with open("textfiles\pat_{0}.text".format(i), 'r') as file:

        for line in file.readlines():
            if "(19)" in line and ("KR" in line or "JP" in line or "US" in line):
                x = (line[-4:-2])
            if "(21)" in line and "출원번호" in line:
                y = (line[15:-3])
            if "(54)" in line and "발명의 명칭" in line:
                z = (line[12:-3])
                data.append([x, y, z])

with open("report1.csv", 'w') as file:
    file.write('국가, 출원번호, 발명의 명칭\n')
    for i in data:
        print(i[0], i[1], i[2])
        file.write("{0},{1},{2}\n".format(i[0], i[1], i[2]))

words = []

# Test - 특정 text 파일에서 단어 추출 
for i in range(1,2):
    with open("textfiles\pat_{0}.text".format(i), 'r') as file:
#with open("textfiles\sample00.txt", 'r') as file:
        for line in file.readlines():  # 예외 사항이 너무 많다. text 6,7,8 비교.
            x = line.split() # 각 줄 - 띄어쓰기로 구분해서 리스트에 각각 넣고
            for i in range(len(x)):
                if x[i] in words:
                    pass
                else:
                    words.append(x[i])

    with open("textfiles\words{0}.text".format(i), 'w') as file:
        for i in range(len(words)):
            x = words[i]+"\n"
            file.write(x)