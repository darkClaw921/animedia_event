import requests
import bs4
import re
from datetime import datetime
from pprint import pprint
from dotenv import load_dotenv
import os
import sqliteWork
# from aiogram import Bot
# from aiogram.client.bot import DefaultBotProperties
# from aiogram.enums.parse_mode import ParseMode
load_dotenv()
TOKEN = os.getenv('TOKEN_BOT_EVENT')
from workTelegram import sendMessage,sendVideo
# Функция для извлечения даты и времени из строки
def extract_date_time(set_interval_string):
    # Словарь для преобразования названий месяцев на русском языке в английские
    month_dict = {'января':'January','февраля':'February','марта':'March','апреля':'April','мая':'May','июня':'June','июля':'July','августа':'August','сентября':'September','октября':'October','ноября':'November','декабря':'December'}

    # Извлекаем дату и время из строки
    match = re.search(r"'(.*?)'", set_interval_string)
    if match:
        date_time_str = match.group(1)
        # Разделяем строку на день, месяц и время
        day, month, time = date_time_str.split()
        # Преобразуем название месяца в английское название
        month = month_dict[month]
        # Получаем текущий год
        current_year = datetime.now().year
        # Объединяем день, месяц, год и время обратно в строку
        date_time_str = f"{day} {month} {current_year} {time}"
        # Преобразуем строку в объект datetime
        date_time_obj = datetime.strptime(date_time_str, '%d %B %Y %H:%M')
        return date_time_obj

    return None





# with open('test.html', 'w') as file:
#     file.write(response.text)
def get_soup(url:str)->bs4.BeautifulSoup:
    reqUrl = url

    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }

    payload = ""


    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
    response=response.text

    # with open('test.html', 'w') as file:
    #     file.write(response)
    # with open('test.html', 'r') as file:
    #     response = file.read()
    soup = bs4.BeautifulSoup(response, 'html.parser')
    return soup

def get_date_new_serial(soup:bs4.BeautifulSoup)->datetime:
    # reqUrl = url

    # headersList = {
    # "Accept": "*/*",
    # "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    # }

    # payload = ""


    # # response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
    # # response=response.text
   
    
    # # print(response)
    # soup = bs4.BeautifulSoup(response, 'html.parser')
    # print(soup)
    animserii=soup.find_all('div', class_='pmovie__anime2')
    pprint(animserii)
    dateNewSerial=animserii[0].find('script').text
    setInterval=dateNewSerial.find('setInterval')
    dateNewSerial=dateNewSerial[setInterval:].strip()
    dateNewSerial = extract_date_time(dateNewSerial)
    print(dateNewSerial)

    return dateNewSerial


def get_title(soup:bs4.BeautifulSoup)->str:
    
    animeName=soup.find_all('header', class_='pmovie__header')[0].find('h1').text.strip()
    print(animeName)
    return animeName

def get_pre_last_serial(soup:bs4.BeautifulSoup)->str:
    animserii=soup.find_all('div', class_='kontaiher')
    preLastSerialUrl=animserii[0].find_all('a')[-2].attrs['data-vlnk']
    pprint(preLastSerialUrl)

    return preLastSerialUrl

def get_num_serial(soup:bs4.BeautifulSoup)->str:
    animserii=soup.find_all('div', class_='kontaiher')
    preLastSerialNum=animserii[0].find_all('a')[-2].attrs['data-vid']+' серия'
    pprint(preLastSerialNum)

    return preLastSerialNum


def check_time_exit_serial(date:datetime):
    date1=date-datetime.now()
    # print(date1)
    # dete1.da
    hour1=3600
    hour4=4*3600
    hour22=22*3600
    if date1.days>=7 and date1.seconds >= hour22:
        print(date-datetime.now())
        print('Сериал уже вышел')
        return True
    else:
        print('Сериал еще не вышел')
        print(date-datetime.now()) 
        return False
    
# print(animserii)
def check_new_serai(url):
    soup=get_soup(url)
    dateNewSeral=get_date_new_serial(soup)
    title=get_title(soup)
    preLastSerialUrl=get_pre_last_serial(soup)
    preLastSerialNum=get_num_serial(soup)
    print(dateNewSeral)
    print(title)
    print(preLastSerialUrl)
    print(preLastSerialNum)
    isNew=check_time_exit_serial(dateNewSeral)
    print(isNew)

    return dateNewSeral,title,preLastSerialUrl,preLastSerialNum,isNew

async def main():
    # bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    userID=400923372
    urls=sqliteWork.get_user_links(userID)
    for url in urls:
        try:
            dateNewSeral, title, preLastSerialUrl, preLastSerialNum, isNew= check_new_serai(url)
            if isNew:
                await sendMessage(userID, f'Вышла новая серия: {title}\n{preLastSerialNum}\n{preLastSerialUrl}\n{dateNewSeral}')
                # bot.send_message(userID, f'Вышла новая серия: {title}\n{preLastSerialNum}\n{preLastSerialUrl}\n{dateNewSeral}')
                # bot.send_video(userID, preLastSerialUrl)
                await sendVideo(userID,preLastSerialUrl)

        except:
            continue
if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
    
    # check_new_serai('https://amedia.site/1200-raskolotaja-bitvoj-sineva-nebes-5.html')
    # # soup=get_soup('https://amedia.site/1200-raskolotaja-bitvoj-sineva-nebes-5.html')
    # soup=get_soup('https://amedia.site/770-pogloschennaya-zvezda.html')
    # dateNewSeral=get_date_new_serial(soup)
    # title=get_title(soup)
    # preLastSerialUrl=get_pre_last_serial(soup)
    # preLastSerialNum=get_num_serial(soup)
    # print(dateNewSeral)
    # print(title)
    # print(preLastSerialUrl)
    # print(preLastSerialNum)
    # print(check_time_exit_serial(dateNewSeral))
    
    