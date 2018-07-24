import requests
from bs4 import BeautifulSoup
import os
import _thread
import vthread

def get_page(url):
    response = requests.get(url).content.decode('gbk')
    soup = BeautifulSoup(response,'lxml')
    return soup
	
def get_all_links(url):
	soup = get_page(url)
	link_list_dome=soup.select(".mulu_list a")
	return link_list_dome
@vthread.pool(6)
def download_article(url,title):
    try:
        soup = get_page(url)
        #获取class为contentbox的dome
        article_dome = soup.find('div',class_="contentbox")
        #获取dome的内容
        article=article_dome.text
        title=title.replace('*','')
        title=title.replace('\\','')
        title=title.replace('?','')
        title=title.replace('<','')
        title=title.replace('>','')
        title=title.replace('|','')
        with open(title+".txt",'w+',encoding='utf-8') as f:
            f.write(article)
        print(title+'sucess')
    except:
        print("!!!error-->"+title)


def get_article_links(types):
    soup=get_page("https://www.ybdu.com/book"+str(types)+"/0/1/")
    type_name=soup.find('div',class_="rec_rtit").h2.text
    os.makedirs("E:/BOOK/"+type_name)
    first_page=int(soup.select('.first')[0].text)
    last_page=int(soup.select('.last')[0].text)
    for page in range(first_page,last_page+1):
        soup=get_page("https://www.ybdu.com/book"+types+"/0/"+str(page)+"/")
        links=soup.select('.rec_rullist .two')
        links = [i.a.get('href') for i in links]
        for article in links:
            article_name=get_page(article).find('div',class_="mu_h1").h1.text
            os.makedirs("E:/BOOK/"+type_name+'/'+article_name)
            for i in get_all_links(article):
                download_article(article+i.get('href'),'E:/BOOK/'+type_name+'/'+article_name+'/'+i.text.replace('/',''))



for types in range(1,10):
    get_article_links(str(types),)
