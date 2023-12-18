from bs4 import BeautifulSoup #соберает ссылки в гугле
import requests, lxml
import argparse #передача аргументов запроса в скрипт
import sys
import shutil # save img locally
import time

def createParser ():

    parser = argparse.ArgumentParser()
    parser.add_argument ('-u', '--url',help = 'запрос в гугл',type=str)  #Запрос в гугл
    parser.add_argument ('-d', '--dir',help='каталог сохранения', default='~/getgoogle/',type=str) #Каталог сохранения
    parser.add_argument ('-p', '--print', help ='печать url',default=False) #Каталог сохранения
    parser.add_argument ('-e', '--end', help ='количество url',default=20) #Каталог сохранения
    
    return parser


def get_query(namespace):
    
    #Поиск в гуглы
    text = None
        
    if namespace.url != None:
        text = namespace.url
    
    if text== None:
        text="site:https://gekkk.co"

    text.replace(" ","+")
    return text


def get_urls(namespace):

    s = requests.session()
    s.cookies.clear()

    googleTrendsUrl = 'https://google.com'

    text = get_query(namespace)

    response = s.get(googleTrendsUrl)
    g_cookies = None
    if response.status_code == 200:
        g_cookies = response.cookies.get_dict()

    headers =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
            AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}

    params = {
    'q': text,
    'gl': 'en',
    'hl': 'us',
    }

    start = 1
    urls = list
    time.sleep(15)
    while start<=namespace.end:

        html = s.get(googleTrendsUrl+'/search', headers=headers,cookies=g_cookies, params=params)
          
            
        soup = BeautifulSoup(html.text, 'lxml')

        for result in soup.select('.tF2Cxc'):
            link = result.select_one('.yuRUbf a')['href']
            urls.append(link)
            print(link, sep='\n')

        start = start + 10
        params['start'] = start
        time.sleep(15)
    return urls

def save_urls(namespace,urls):
   
   for i in urls:
       if namespace.print == True:
            print(i)         


if __name__ == '__main__':
      
    parser = createParser()    
    namespace = parser.parse_args(sys.argv[1:])  
    
    urls = get_urls(namespace)
