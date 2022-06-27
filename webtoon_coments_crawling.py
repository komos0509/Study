import os
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt

base_url = 'https://comic.naver.com/webtoon/weekday.nhn'
os.chdir('F:\Crawling_1')

def drive(url):
    driver = webdriver.Chrome('./chromedriver')
    driver.implicitly_wait(3)
    driver.get(url)
    html =  driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return driver, soup

driver, soup = drive(base_url)
driver.close()

title = soup.select('.title')
t_IDs = list(map(lambda x: x.get('href').split('titleId=')[1].split('&')[0],title))
t_weekdays = list(map(lambda x: x.get('href').split('weekday=')[1],title))
t_names = list(map(lambda x: x.text, title))

def find_id_weekday(name):
    try:
        idx = t_names.index(name)
    except:
        print('찾는 웹툰이 없습니다.')
        return
    return t_IDs[idx], t_weekdays[idx]

def episode_count(ID, weekday):
    url = base_url.split('weekday')[0] + 'list.nhn?titleId={0}&weekday={1}'.format(ID, weekday)
    driver, soup = drive(url)
    driver.close()
    res = soup.select('.title')[0].select('a')[0].get('href').split('no=')[1].split('&')[0]
    return res

def coment_crawler(name):
    id_num, weekday = find_id_weekday(name)
    cnt = int(episode_count(id_num, weekday))
    coments = []
    proceed = -1

    driver, _ = drive(base_url)
    print('진행중...')
    
    for i in range(1, cnt+1):
        percentage = int((1/cnt)*100)
        if percentage%10 == 0 and percentage > proceed:
            proceed = percentage
            print(proceed, '% 완료')
        url = 'https://comic.naver.com/comment/comment.nhn?titleId={0}&no={1}#'.format(id_num, str(i))
        time.sleep(1.5)
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        coments += list(map(lambda x: x.text, soup.select('.u_cbox_contents')))
        
    driver.close()
    print('crawling finished')

    return coments

print('찾으려는 웹툰의 이름을 입력하세요. : ')
a = input()
c = coment_crawler(a)

wordcloud = WordCloud(font_path='C:\\windows\\Fonts\\NanumGothic.ttf', max_font_size=100).generate(c)
plt.imshow(wordcloud, interpolation='biniear')
plt.axis('off')
plt.show()
plt.savefig('wordcloud.png')




