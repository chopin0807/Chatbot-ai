import requests
from bs4 import BeautifulSoup
import re

def web_crawling(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

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
                        word.append(t)
    # 내부링크는 이미 겹치고, 페이지가 있는 경우에만 해결(비동기)해야함
    return word

target_url = "https://startup.hanyang.ac.kr/introduce/introduce"
soup = web_crawling(target_url)
print(web_content(soup))