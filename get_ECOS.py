# 한국은행 통계 자료를 정상적으로 받아올 수 있는지 테스트 해보는 것(official)
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom

# 한국은행 자료 제대로 받아올 수 있는지 테스트 해보는 구간
authorized_key = '5H6P7H8QSOH3MNPO08UZ'

url = f"http://ecos.bok.or.kr/api/StatisticItemList/{authorized_key}/xml/kr/1/1/901Y009"
response = requests.get(url)

if response.status_code == 200:
    try:
        contents = response.text
        ecosRoot = ET.fromstring(contents)

        if ecosRoot[0].text[:4] in ("INFO", "ERRO"):
            print(ecosRoot[0].text + ":" + ecosRoot[1].text)
        else:
            dom = xml.dom.minidom.parseString(contents)
            pretty_xml_as_string = dom.toprettyxml(indent="    ")
            print(pretty_xml_as_string)
    except Exception as e:
        print(str(e))


# 본격적으로 필요한 한국은행 자료 받아오는 구간임
# 필요한 라이브러리 로드
import pandas as pd
from pandas.io.json import json_normalize
from bs4 import BeautifulSoup
import requests

key = "5H6P7H8QSOH3MNPO08UZ" # 한국은행 ECOS에서 인증받은 키값
n = '10' # 최대한으로 나열할 열의 크기
date1 = '1990'
date2 = '2022'


def get_ECOS(key, n, date1, date2, item_code1, interval, item_code2, item_code3):
    url = f"http://ecos.bok.or.kr/api/StatisticSearch/{key}/xml/kr/1/{n}/{item_code1}/{interval}/{date1}/{date2}/{item_code2}/{item_code3}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'xml')
    item_list = soup.findAll('row')

    stat_code1 = []
    stat_code2 = []
    stat_code3 = []
    stat_name = []
    item_name1 = []
    item_name2 = []
    unit_name = []
    time = []
    value = []

    for item in item_list:
        stat_code1.append(item.find('STAT_CODE').text)
        stat_code2.append(item.find('ITEM_CODE1').text)
        stat_code3.append(item.find('ITEM_CODE2').text)
        stat_name.append(item.find('STAT_NAME').text)
        item_name1.append(item.find('ITEM_NAME1').text)
        item_name2.append(item.find('ITEM_NAME2').text)
        unit_name.append(item.find('UNIT_NAME').text)
        time.append(item.find('TIME').text)
        value.append(item.find('DATA_VALUE').text)

    data = pd.concat([pd.DataFrame(stat_code1),
                      pd.DataFrame(stat_code2),
                      pd.DataFrame(stat_code3),
                      pd.DataFrame(stat_name),
                      pd.DataFrame(item_name1),
                      pd.DataFrame(item_name2),
                      pd.DataFrame(time),
                      pd.DataFrame(value),
                      pd.DataFrame(unit_name)], axis = 1)

    data.columns = ['항목코드', '통계코드', '세부통계코드', '항목명', '세부통계명', '국가', '조회시점', '값', '단위']
    return data




# 이제 위의 정의된 함수에 따라서 받아올 수 있는 값들을 정의한 자료 더미들을 만든다.
# 연간으로 조회할 지표
combination_ECOS_A = [['902Y015', 'A', 'KOR', ''], # 경제성장률
                      ['901Y027', 'A', 'I61E', 'I28A'],
                      ['731Y004', 'A', '0000001', '0000100'],
                      ['801Y002', 'A', '401000A', ''],
                      ['901Y054', 'A', 'MO3AB', 'AB'],
                      ['901Y054', 'A', 'MO3AA', 'AB'],
                      ['902Y002', 'A', '3010101', ''],
                      ['722Y001', 'A', '0101000', ''],
                      ['121Y006', 'A', 'BECBLA0202', '']
                      ]


df_ecos_a = pd.DataFrame()
df_ecos_a.to_excel('C:/Users/chmiw/Desktop/Programming/Finance/ECOS.xlsx', sheet_name='Sheet0')
a = 1

for i in combination_ECOS_A:
    data = get_ECOS(key, n, date1, date2, i[0], i[1], i[2], i[3])
    data["값"] = pd.to_numeric(data['값'])
    df_ecos_a = df_ecos_a.append(data, ignore_index=True)
    with pd.ExcelWriter('C:/Users/chmiw/Desktop/Programming/Finance/ECOS.xlsx', mode = 'a') as writer:
        data.to_excel(writer, sheet_name=f'Sheet{a}')
    a = a + 1
print(df_ecos_a)