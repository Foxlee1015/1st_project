import csv
import matplotlib.pyplot as plt

# 연도별 // 국가별 그래프

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

f = open("report_country_count.csv", 'r')
lines = csv.reader(f)
country_count = []
for line in lines:
    country_count.append(line[1])
KR = [country_count[0]]
US = [country_count[1]]
JP = [country_count[2]]
EP = [country_count[3]]

colors = ['#AA2848', '#28AA48', '2848AA', 'K']
categoies = ['KR', 'US', 'JP', 'EP']
plt.title("THE NUMBER OF PATENTS FROM DIFFERENT COUNTRIES")
slice =[KR, US, JP, EP]
plt.pie(slice, labels=categoies, startangle=90, shadow =True, explode=(0, 0, 0.1, 0), autopct='%1.1f%%')

#fig2, ax1 = plt.subplots()
#ax1.pie(sizes, explode=explode, labels=labels, autopact='%1.1f%%', shadow=True, startangle=90)
#ax1.axis('equal')
plt.show()