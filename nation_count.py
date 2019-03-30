%matplotlib inline
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

df = pd.read_csv("data1[original].csv", encoding='euc-kr')
df[["출원번호", "국가코드", "출원일"]]

kr_count, jp_count, us_count, ep_count = 0, 0, 0, 0
for i in range(len(df.index):  
    if df.loc[i, "국가코드"] == "KR":
        kr_count += 1
    if df.loc[i, "국가코드"] == "JP":
        jp_count += 1
    if df.loc[i, "국가코드"] == "US":
        us_count += 1
    if df.loc[i, "국가코드"] == "EP":
        ep_count += 1
        
        
        
print(kr_count)
print(jp_count)
print(us_count)
print(ep_count)


# 확인 : csv 안 각 셀안에도 "," 가 있을수 있어 split(',') 사용 하지 말것
