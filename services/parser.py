from aiogram import Bot
from aiogram.types import Message
from bs4 import BeautifulSoup as BS
import lxml 
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from services.services import cut_url, load_from_file, save_json_file
import time
import datetime

#Парсер должен находить нужную иформацию на сайтах по ключевым словам


# Словарь в котором ключи -- название сайта, обрезанное
# значения -- словарь, 
# url -- ссылка на сайт
# function -- функция с помощью которой будет парсится сайта (requests, selenium)
# site_targets -- словарь в котором находятся ключевые слова для поиска
# path_to_file -- путь до скаченного сайта для парсинга
# urls: dict[str, dict['url', str, 
#                      'function', str, 
#                      'site_targets', list[str], 
#                      'path_to_file', str]] = {}



def get_file_with_requests(name_site: str):
    # Заголовки моих данных чтобы сайт думал что пользуется человек а не парсер сайтом
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept': '*/*'
    }

    response = requests.get(url=table_parse[name_site]['url'])
    
    with open(f'services/data/index_{name_site}.html', 'w', encoding='utf-8') as file:
        file.write(response.text)

    return f'services/data/index_{name_site}.html'
        


# Если через requests происходит ошибка или неверная кодировка
def get_file_with_selenium(name_site: str):
    service = Service(executable_path='D:\\Python\\Python_projects\\Python_bots\\News aggregator bot\\services\\chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    try:
        driver.maximize_window()

        driver.get(url=table_parse[name_site]['url'])

        with open(f'services/data/index_{name_site}.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

        return f'services/data/index_{name_site}.html'

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def get_data_from_file(name_site: str, path_to_file: str):
    with open(file=path_to_file, encoding='utf-8') as file:
        src = file.read()

    today_month, today_day = str(datetime.datetime.now().date().month), str(datetime.datetime.now().date().day)

    soup = BS(src, 'lxml')
    # print(soup.title)

    if name_site == 'www_rbc':
        bring_news = []
        all_news = soup.find_all(class_='item_image-mob')
        # print('In RBC')
        for news in all_news:
            news_title = news.find(class_='item__title rm-cm-item-text js-rm-central-column-item-text').text.strip()
            news_url = news.find(class_='item__wrap l-col-center').find('a').get('href')
            news_date = news.find(class_='item__category').text.split()[0]
            
            if news_date == f'{today_day}.{today_month}':    
                bring_news.append((news_title, news_url))
                # print(f'Title: {news_title}')
                # print(news_url)
                # print('-' * 30)
            else:
                return bring_news
            

    if name_site == 'journal_tinkoff':
        bring_news = []
        all_news = soup.find_all(class_='item--HhAuM')
        # print(all_news)
        for news in all_news:
            try:
                news_title = news.find(class_='title--eHNn2').text
            except AttributeError as ex:
                continue

            news_url = 'https://journal.tinkoff.ru' + news.find(class_='link--r6yOY').get('href')

            news_date = news.find(class_='date--oLk5c').text

            if news_date == f'{today_day}.{today_month}':
                bring_news.append((news_title, news_url))

                # print(news_title)
                # print(news_url)
                # print('-' * 30)
            else:
                return bring_news
    
    if name_site == 'rb':
        bring_news = []
        all_news = soup.find_all(class_='news-item__text')
        # print('In RB')
        for news in all_news:
            news_title = news.find(class_='news-item__title').text.strip()
            news_url = 'https://rb.ru' + news.find(class_='news-item__title').get('href')
            news_date = news.find(class_='news-item__date').text.strip().split()[0]
            
            if news_date == today_day:
                bring_news.append((news_title, news_url))
                
                # print(news_title)
                # print(news_url)
                # print('-' * 30)
            else:
                return bring_news


    if name_site == 'www_kommersant':
        bring_news = []
        all_news = soup.find_all(class_='uho__text rubric_lenta__item_text')
        # print('In KOMMERSANT')
        for news in all_news:
            news_title = news.find('span', class_='vam').text.strip()
            news_url = 'https://www.kommersant.ru' + news.find(class_='uho__link uho__link--overlay').get('href')
            news_date = news.find(class_='uho__tag rubric_lenta__item_tag hide_mobile').text.strip().split('.')[0]

            if news_date == today_day:
                bring_news.append((news_title, news_url))

                # print(news_title)
                # print(news_url)
                # print('-' * 30)
            else:
                return bring_news


    if name_site == 'skillbox':
        bring_news = []
        all_news = soup.find_all(class_='card-articles')
        # print('In SKILLBOX')
        for news in all_news:
            news_title = news.find(class_='card-articles__body-title').text.strip()
            news_url = 'https://skillbox.ru' + news.find(class_='card-articles__body-link').get('href')
            news_date = news.find(class_='info-text').text.strip().split()[0]
            
            if news_date == today_day:
                bring_news.append((news_title, news_url))

                # print(news_title)
                # print(news_url)
                # print('-' * 30)
            else:
                return bring_news

table_parse: dict = {
    'www_rbc': {
        'url': 'https://www.rbc.ru/economics/?utm_source=topline',
        'function': get_file_with_requests,
        'path_to_file': ''
    },
    'journal_tinkoff': {
        'url': 'https://journal.tinkoff.ru/flows/economics/',
        'function': get_file_with_selenium,
        'path_to_file': ''
    },
    'rb': {
        'url': 'https://rb.ru/news/',
        'function': get_file_with_requests,
        'path_to_file': ''
    },
    'www_kommersant': {
        'url': 'https://www.kommersant.ru/rubric/3?from=burger',
        'function': get_file_with_requests,
        'path_to_file': ''
    },
    'skillbox': {
        'url': 'https://skillbox.ru/media/topic/articles/design/',
        'function': get_file_with_requests,
        'path_to_file': ''
    }
}


# Функция которая парсит выбранные пользователем сайты
def parse_user_sites(user_id: str):
    all_news = []
    
    users = load_from_file()
    # print(user_id)
    # print(users)

    dict_pressed_sites = [site for site in users[str(user_id)]['pressed_sites'].keys()]
    # print(dict_pressed_sites)
    for site_name in dict_pressed_sites:
        name_site = '_'.join(site_name.split('_')[2:])
        
        # name_site = '_'.join(name_site.split('.'))
        # print(name_site)
        # print(users[str(user_id)]['pressed_sites'])
        # print(table_parse[name_site])

        users[str(user_id)]['pressed_sites'][name_site] = table_parse[name_site]
        function = users[str(user_id)]['pressed_sites'][name_site]['function']

        # Парсим сайт с помощью requests или selenium
        users[str(user_id)]['pressed_sites'][name_site]['path_to_file'] = users[str(user_id)]['pressed_sites'][name_site]['function'](name_site=name_site)

        # news_title, news_url = get_data_from_file(
        #     name_site=name_site,
        #     path_to_file=users[user_id]['pressed_sites'][name_site]['path_to_file'])

        # get_data_from_file(
        #     name_site=name_site,
        #     path_to_file=users[str(user_id)]['pressed_sites'][name_site]['path_to_file'])
        
        new_news = get_data_from_file(
            name_site=name_site,
            path_to_file=users[str(user_id)]['pressed_sites'][name_site]['path_to_file'])

        if new_news:
            if len(new_news) > 1:
                for news in new_news:
                    all_news.append(news)
            else:
                all_news.append(new_news)

    return all_news
        







# if __name__ == '__main__':
    


#     # urls[cut_url(url=url)] = {'url': url,
#     #                           'function': function,
#     #                           'site_targets': site_targets,
#     #                           'path_to_file': ''}

#     for name_site, list_values in urls.items():
#         list_values['function'](name_site=name_site)
#         get_data_from_file(name_site=name_site)