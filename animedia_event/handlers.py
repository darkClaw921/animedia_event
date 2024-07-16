import asyncio
from aiogram import types, F, Router, html, Bot
from aiogram.types import (Message, CallbackQuery,
                           InputFile, FSInputFile,
                            MessageEntity, InputMediaDocument,
                            InputMediaPhoto, InputMediaVideo, Document)
from aiogram.filters import Command, StateFilter,ChatMemberUpdatedFilter
from aiogram.types.message import ContentType
from pprint import pprint
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from typing import Any, Dict
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER

from aiogram.types import ChatMemberUpdated
# from aiogram.dispatcher.filters import ChatMemberUpdatedFilter
# from helper import (get_all_user_list, get_dates, 
#                     timestamp_to_date, time_epoch,
#                     get_future_events, prepare_message_event,
#                     get_today_pracktik,prepare_message_pracktik,
#                     langList, langListKeybord, typeFiles)
# # from createKeyboard import *
# from payments import *
from dotenv import load_dotenv
import os
# from chat import GPT
# import postgreWork 
# import chromaDBwork
from loguru import logger
# from workRedis import *
# from calendarCreate import create_calendar
# from helper import create_db,convert_text_to_variables,create_db2,get_next_weekend,find_and_format_date,find_patterns_date,create_db_for_user
from datetime import datetime,timedelta
# from workGS import Sheet
import uuid
import time
# import speech_recognition as sr
# from promt import clasificatorPromt

load_dotenv()
TOKEN = os.getenv('TOKEN_BOT_EVENT')
# PAYMENTS_TOKEN = os.getenv('PAYMENTS_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK')
SECRECT_KEY = os.getenv('SECRET_CHAT')

# sql = Ydb()

router = Router()

bot = Bot(token=TOKEN,)

import requests
import hashlib
import base64
import json
import hmac
# import loguru
from loguru import logger
import sqliteWork
# logger.add("file_{time}.log",format="{time} - {level} - {message}", rotation="100 MB", retention="10 days", level="DEBUG")
# Define the secret key and other required information

# task_code = "sub"
# user_id = "your_telegram_user_id"
# action = True  # or False depending on your requirement

# Prepare the body of the request


# Define the headers
# headers = {
#     "Content-Type": "application/json",
#     "X-Api-Signature-Sha256": signature
# }

# Define the URL
# url = "https://gql.aibetrade.com/hook/task"

# Make the POST request
# response = requests.post(url, headers=headers, data=body_json)

# # Print the response
# print("Status Code:", response.status_code)
# print("Response Body:", response.json())
@router.message(Command("help"))
async def help_handler(msg: Message, state: FSMContext):
    mess="/start - начало работы\n/add добавление нового отслеживания сразу ссылкой add http://"
    await msg.answer(mess)
    return 0

@router.message(Command("add"))
async def help_handler(msg: Message, state: FSMContext):
    url=msg.text
    userID=msg.from_user.id
    sqliteWork.add_link(user_id=userID,url=url)
    await msg.answer('Добавлено')
    return 0

@router.message(Command("start"))
async def help_handler(msg: Message, state: FSMContext):
    mess="Каждый час проверяет вышла ли серия"
    userID=msg.from_user.id
    sqliteWork.create_user(userID, 'telegram')

    await msg.answer(mess)
    return 0


#Обработка калбеков
@router.callback_query()
async def message(msg: CallbackQuery):
    pprint(msg.message.message_id)
    userID = msg.from_user.id
    await msg.answer()
    callData = msg.data
    # pprint(callData)
    logger.debug(f'{callData=}')

           
    return 0




@router.message()
async def message(msg: Message, state: FSMContext):
    # pprint(msg.__dict__)
    # 241 реф ссылки #240
    userID = msg.from_user.id
    # print(msg.chat.id)
    print(f"{msg.chat.id=}")
    print(f'{userID=}')
    
    



if __name__ == '__main__':
    
    

    pass
