import requests
from bs4 import BeautifulSoup
import re

def web_crawling(url):  # 동기 방식 크롤링
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def tag(soup, tag):
    target = soup.select(tag)
    # 원할한 키워드 추출을 위해 정규표현식 사용및 리스트에 키워드 추가
    word = []
    for i in target:
        k = str(i).split("</")
        for j in k:
            keyword = re.findall("(?<=\>)[A-Z a-z 0-9 가-힣 /()!@#$%&*\-~+=?.,:;·]+", j)
            if keyword:
                for t in keyword:
                    if t not in word:
                        if t[0] == ' ':
                            word.append(t)
                        else:
                            word.append(' ' + t)
    # 내부 링크 추출
    # 홈페이지 링크 추출(a href)
    if tag == "a":
        a_tag = soup.select("a")
    else:
        a_tag = soup.select(tag + " a")
    # 추출된 링크에 대한 최종 url링크 생성 후 리스트 저장
    link_url = []
    for i in a_tag:
        try:
            link = i.attrs["href"]
            if "//" not in link and len(link) != 1 and link != "/en" and "https://startup.hanyang.ac.kr" + link not in link_url:
                link_url.append("https://startup.hanyang.ac.kr" + link)
        except:
            pass
    return [word, link_url]

def web_content(soup):
    target = soup.select("div.container")
    # 원할한 키워드 추출을 위해 정규표현식 사용및 리스트에 키워드 추가
    word = []
    for i in target:
        k = str(i).split("</")
        for j in k:
            keyword = re.findall("(?<=\>)[A-Z a-z 0-9 가-힣 /()!@#$%&*\-~+=?.,:;·]+", j)
            if keyword:
                for t in keyword:
                    if t not in word:
                        if t[0] == ' ':
                            word.append(t)
                        else:
                            word.append(' ' + t)
    
    return word

def crawling_end_page(url):
    response = requests.get(url.format('100000000')) # 끝 페이지 이후로 해야 정확한 끝지점 파악 가능
    data = response.json()
    return data['data']['page']['endPageNo']

def json_crawling(url, page_num):
    response = requests.get(url.format(str(page_num)))
    data = response.json()
    return data['data']['list']

# 홈페이지(https://startup.hanyang.ac.kr)에 대한 키워드 및 내부 링크 추출
keyword, linkurl = [], []
target_url = "https://startup.hanyang.ac.kr"
soup = web_crawling(target_url)
result1 = tag(soup, 'div.header_header_inner__fzmrt') # 상단 배너
result2 = tag(soup, 'section.footer_wrap') # 하단 배너
result3 = tag(soup, 'a') # 전체페이지
banner_link_url = result1[1] + result2[1]

# 웹 사이트 텍스트 파일로 기록
f = open("keyword.txt", 'w', encoding='utf-8')
for i in result3[0]:
    print(i)
    f.write(i)

# 내부링크에 대한 키워드(페이지가 있는 목록 제외) 추출
for i in banner_link_url:
    soup = web_crawling(i)
    for j in web_content(soup):
        print(j)
        f.write(j)

# api(비동기) crawling
page_api, api_keyword = [], []
page_api.append("https://startup.hanyang.ac.kr/api/board/content?boardEnName=media_report&categoryCodeId&categoryId&page={}&pageSize=10&searchField&searchValue")
page_api.append("https://startup.hanyang.ac.kr/api/mentoring/mentor/list?counselField=&page={}&pageSize=6")
page_api.append("https://startup.hanyang.ac.kr/api/board/content?boardEnName=notice&categoryCodeId&categoryId&page={}&pageSize=10&searchField&searchValue")
page_api.append("https://startup.hanyang.ac.kr/api/board/content?boardEnName=startup_info&categoryCodeId&categoryId&page={}&pageSize=10&searchField&searchValue")
page_api.append("https://startup.hanyang.ac.kr/api/board/content?boardEnName=data_room&categoryCodeId&categoryId&page={}&pageSize=10&searchField&searchValue")
page_api.append("https://startup.hanyang.ac.kr/api/board/content?boardEnName=faq&categoryCodeId&categoryId&page={}&pageSize=10&searchField&searchValue")
page_api.append("https://startup.hanyang.ac.kr/api/board/content?boardEnName=corp_press&categoryCodeId&categoryId&page={}&pageSize=10&searchField&searchValue")

api_keyword.append("언론보도")
api_keyword.append("멘토단 소개")
api_keyword.append("공지사항")
api_keyword.append("신규사업공고")
api_keyword.append("자료실")
api_keyword.append("질의응답(FAQ)")
api_keyword.append("기업 언론보도")
word = []
for i, api_k in zip(page_api, api_keyword):
    print(i, api_k)
    word.append(api_k)
    for j in range(1, crawling_end_page(i) + 1):
        data = json_crawling(i, j)
        # word에 title 및 content 삽입
        for k in data:
            try:
                if k['title']:
                    print(api_k + ': ' + k['title'])
                    word.append(api_k + ': ' + k['title'])
                if k['content']:
                    t = k['content'].split("</")
                    for a in t:
                        keyword = re.findall("(?<=\>)[A-Z a-z 0-9 가-힣 /()!@#$%&*\-~+=?.,:;·]+", a)
                    if keyword:
                        for t in keyword:
                            print(api_k + ': ' + t)
                            word.append(api_k + ': ' + t)
            except:
                print('맨토이름: ' + k['mentorName'])
                print('멘토 전화번호: ' + k['mentorPhoneNumber'])
                print('멘토 사무소: ' + k['mentorCompany'])
                print('멘토 소개: ' + k['mentorIntroduction'])
                word.append('맨토이름: ' + k['mentorName'] + '멘토 전화번호: ' + k['mentorPhoneNumber'] + '멘토 전화번호: ' + k['mentorPhoneNumber'] + '멘토 소개: ' + k['mentorIntroduction'])

# 비동기방식인 목록에서 제목을 클릭하면 볼 수 있는 내용
content_link = "https://startup.hanyang.ac.kr/board/notice/view/38"

def json_content(url, page_num):
    response = requests.get(url.format(str(page_num)))
    data = response.json()
    return [data['response'], data['data']['content']] if data['response'] == "success" else []

content_link = "https://startup.hanyang.ac.kr/api/board/content/{}"

for i in word:
    f.write(i)

word = []
for i in range(38, 3350):
    target = json_content(content_link, i)
    if target:
        try:
            content = target[1]['content'].split("</")
            for x in content:
                content_keyword = re.findall("(?<=\>)[A-Z a-z 0-9 가-힣 /()!@#$%&*\-~+=?.,:;·]+", x)
                if content_keyword:
                    for t in content_keyword:
                        t = t.replace('&nbsp;', '')
                        if t.replace(' ', ''):
                            print(t)
                            word.append(t)
        except:
            if target[1]['content']:
                paste = target[1]['content']
                paste = paste.replace('&nbsp;', '')
                print(paste)
                word.append(paste)

for i in word:
    f.write(i)
f.close()