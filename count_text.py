for i in range(1,2):
    y = []
    with open("textfiles\pat_{0}.text".format(i), 'r') as file:
    #with open("textfiles\pat_1.txt", 'r') as file:
        for line in file.readlines():  # 예외 사항이 너무 많다. text 6,7,8 비교.
            x = line.split() # 각 줄 - 띄어쓰기로 구분해서 리스트에 각각 넣고

            for i in range(len(x)):
                count=0
                for j in range(len(x)):
                    if x[i] == x[j]:
                            count += 1
                z = [x[i],count]
                y.append(z)


    print(y)
    with open("textfiles\words{0}.text".format(i), 'w') as file:
        for i in range(len(y)):
            x = str(y[i])  #  +"\n"
            file.write(x+ "\n")

# 2열의 count 수로 오름차순하기 ( sort? ) / 필요 없는 문자 빼는 방법? 

