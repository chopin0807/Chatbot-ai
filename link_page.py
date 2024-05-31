import requests
from bs4 import BeautifulSoup
import json
import re

def crawling_end_page(url):
    response = requests.get(url.format('100000000')) # 끝 페이지 이후로 해야 정확한 끝지점 파악 가능
    data = response.json()
    return data['data']['page']['endPageNo']

def json_crawling(url, page_num):
    response = requests.get(url.format(str(page_num)))
    data = response.json()
    return data['data']['list']

# 9개에 대한 api uri 목록 추가
page_api = []
page_api.append("https://startup.hanyang.ac.kr/api/board/content?boardEnName=media_report&categoryCodeId&categoryId&page={}&pageSize=10&searchField&searchValue")
page_api.append("https://startup.hanyang.ac.kr/api/mentoring/mentor/list?counselField=&page={}&pageSize=6")
page_api.append("https://startup.hanyang.ac.kr/api/board/content?boardEnName=notice&categoryCodeId&categoryId&page={}&pageSize=10&searchField&searchValue")
page_api.append("https://startup.hanyang.ac.kr/api/board/content?boardEnName=startup_info&categoryCodeId&categoryId&page={}&pageSize=10&searchField&searchValue")
page_api.append("https://startup.hanyang.ac.kr/api/board/content?boardEnName=data_room&categoryCodeId&categoryId&page={}&pageSize=10&searchField&searchValue")
page_api.append("https://startup.hanyang.ac.kr/api/board/content?boardEnName=faq&categoryCodeId&categoryId&page={}&pageSize=10&searchField&searchValue")
page_api.append("https://startup.hanyang.ac.kr/api/board/content?boardEnName=corp_press&categoryCodeId&categoryId&page={}&pageSize=10&searchField&searchValue")

word = []
for i in page_api:
    print(i)
    for j in range(1, crawling_end_page(i) + 1):
        data = json_crawling(i, j)
        # word에 title 및 content 삽입
        for k in data:
            try:
                if k['title']:
                    print(k['title'])
                    word.append(k['title'])
                if k['content']:
                    t = k['content'].split("</")
                    for a in t:
                        keyword = re.findall("(?<=\>)[A-Z a-z 0-9 가-힣 /()!@#$%&*\-~+=?.,:;·]+", a)
                    if keyword:
                        for t in keyword:
                            if t not in word:
                                print(t)
                                word.append(t)
                    # print(k['content'])
                    # word.append(k['content'])
            except:
                print('맨토이름: ' + k['mentorName'])
                print('멘토 전화번호: ' + k['mentorPhoneNumber'])
                print('멘토 사무소: ' + k['mentorCompany'])
                print('멘토 소개: ' + k['mentorIntroduction'])
                word.append('맨토이름: ' + k['mentorName'] + '멘토 전화번호: ' + k['mentorPhoneNumber'] + '멘토 전화번호: ' + k['mentorPhoneNumber'] + '멘토 소개: ' + k['mentorIntroduction'])
print(word)