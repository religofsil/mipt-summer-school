import requests
from bs4 import BeautifulSoup
import urllib
import re

# здесь создаётся корпус
mar_pravda = 'http://www.marpravda.ru/news/'
def get_article(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(r.content, from_encoding = encoding)
    title = soup.find('h1').text
    try:
        author = soup.find('div', attrs={'class':'autor_name'}).find('a').text
    except AttributeError:
        author = ''
    topic = soup.find('a', attrs={'class':'rubric'}).text
    article = soup.find('article').text
    article = re.sub('\t', '', article)
    data = soup.find('span', attrs={'class':'date'}).text
    return author, title, data, topic, article

def create_corpus_doc(n, author, title, data, topic, url, article):
    file = open('text' + str(n) + '.txt', 'w', encoding='utf-8')
    file.write('@au ' + author + '\n@ti ' + title + '\n@da ' + data +
               '\n@topic ' + topic + '\n@url ' + url + '\n' + article)
    file.close

def get_articles(link, n):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')
    encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(r.content, from_encoding = encoding)
    arts = soup.find('div', attrs={'class':'news_list_tp1 clearfix'}).findAll('div', attrs={'class':'news_item'})
    for x in arts:
        n += 1
        ah = x.find('div', attrs={'class':'news_name'}).find('a')
        url = 'http://www.marpravda.ru' + str(ah['href'])
        author, title, data, topic, article = get_article(url)
        create_corpus_doc(n, author, title, data, topic, url, article)
    return n

def main(mar_pravda):
    n = 0
    n = get_articles(mar_pravda, n)
    page = 2
    while n < 1000:
        n = get_articles('http://www.marpravda.ru/news/?MUL_MODE=&PAGEN_1=' + str(page), n)
        page += 1

main(mar_pravda)
