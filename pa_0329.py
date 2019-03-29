text_words = [] # 특허 전문을 띄어쓰기 기준으로 나눈 리스트
count_n = [] # [ word, count of the word]
words_count = []
# 텍스트파일에서 단어 사전 (분야별?)    # 단어 추가 필요 -> 수작업... -> 사전 만들기?
words = ["차량", "실내", "공간", "바닥", "벤틸레이터", "흡입구", "감지부", "통로", "배치", "하우징", "신호", "감지", "정화" ]
with open("textfiles\pat_0329.text", 'r') as file:
    for line in file.readlines():
        x = line.split()
        text_words = text_words + x
#    print(text_words)   # y 에 다들어감
for word in words:
    count = 0
    for text in text_words:
        if word in text:
            count += 1
    count_n = [word, count]
    words_count.append(count_n)
#print(words_count)
#
with open("report0329.csv", 'w') as file:
    file.write('단어, 횟수\n')
    for i in words_count:
        #print(i[0], i[1])
        file.write("{},{}\n".format(i[0], i[1]))