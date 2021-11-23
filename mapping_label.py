import pandas as pd
import re

total  = pd.read_csv('detail_review_data/total.csv')
print(total.head)
print(total.columns)

label = pd.read_csv('label_table.csv')
print(label)

def change(str):
    return re.sub('[^A-Za-z0-9가-힣]', '', str)

def change_1(str):
    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', str)

# 특수문자 및 공백 제거
total['lecture_name'] = total['lecture_name'].apply(change)
total['professor_name'] = total['professor_name'].apply(change_1)
# pattern = re.compile(r'\s+')
# total['professor_name'] = re.sub(pattern, '', total['professor_name'])
# total['professor_name'] = total['professor_name'].replace(' ', '')
label = label.iloc[3:130,:]
for i in range(3, 130):
    label['category'][i] = label['category'][i][5:]

# total의 id에 label추가
# label의 category에서 total의 lecture_name과 professor name 에서 문자열 찾기 

total = pd.DataFrame(total)
total['id']=[-1]*len(total)
print(total)

for i in range(3, 130):
    for j in range(len(total)):
        if total['professor_name'][j] == 'X':
            if label['category'][i].find(total['lecture_name'][j]) != -1 :
                break
        if label['category'][i].find(total['lecture_name'][j]) != -1 and label['category'][i].find(total['professor_name'][j]) != -1:
            break
    total['id'][j] = label['label'][i] - 3

print(total)
print(total.loc[total['id']==-1])
total.to_csv('mappind_label.csv')