import pandas as pd
import configparser
from re import M
from turtle import back
import datetime
import telebot, sys
from telebot import types
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE
from telebot.types import ReplyKeyboardRemove, CallbackQuery
import os
import time
import os.path
import shutil
from pathlib import Path
from random import randint
import json 


template = os.path.abspath(__file__)
testBot = template.replace(os.path.basename(os.path.abspath(__file__)), "TestBot.json")
config = configparser.ConfigParser()
s = os.path.abspath(__file__)
c = s.replace(os.path.basename(os.path.abspath(__file__)), "")
config.read(c + "config.ini", encoding="UTF-8")
calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")


global dicti
dicti = {"admin": {"id": [],
                   "AddModels" : False,
                   "DelModels": False,
                   "MinStr": False,
                   "MinStrMast": False,
                   "printAdmin": [],
                   "DelData": False,
                   "DataSelectAdd": False,
                   "AddData": False,
                   "DataSel": False,
                   "Datas": [],
                   "IdDataSelect": 0,
                   "Date": ""},}

API_TOKEN = config["Token"]["token"]

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=["start"])
def start(command):
    
    if command.chat.id in dicti:
        dicti.pop(command.chat.id)
        dicti[command.chat.id] = {"id": command.chat.id,
                                  "what":[False, False, False, False],
                                  "story": True,
                                  "storyPhoto": False,
                                  "storyTale": [],
                                  "long": "0",
                                  "counterWas": 0,
                                  "counterRes": 0,
                                  "result": False,
                                  "resultTale": [],
                                  "counterModels": 0,
                                  "counterMasters": 0,
                                  "counterModelsCall": 0,
                                  "textModelsEnd": "",
                                  "textModelsId": [],
                                  "textMastersDates":[],
                                  "textMastersId": [],
                                  "textModelsIdSelect": 0,
                                  "Dates": [],
                                  "Date": "",
                                  "Masters": [],
                                  "Master": "",
                                  "DatesOn": False,
                                  "textModels": "",
                                  "textMasters": ""}
    else:
        dicti[command.chat.id] = {"id": command.chat.id,
                                  "what":[False, False, False, False],
                                  "story": False,
                                  "storyPhoto": False,
                                  "storyTale": [],
                                  "long": "0",
                                  "counterWas": 0,
                                  "counterRes": 0,
                                  "result": False,
                                  "resultTale": [],
                                  "counterModels": 0,
                                  "counterMasters": 0,
                                  "counterModelsCall": 0,
                                  "textModelsEnd": "",
                                  "textModelsId": [],
                                  "textMastersDates":[],
                                  "textMastersId": [],
                                  "textModelsIdSelect": 0,
                                  "Dates": [],
                                  "Date": "",
                                  "Masters": [],
                                  "Master": "",
                                  "DatesOn": False,
                                  "textModels": "",
                                  "textMasters": ""}
    
    
    try:
        path = os.path.join(c+"Photos/"+str(dicti[command.chat.id]["id"]))
        shutil.rmtree(path)
    except:
        pass
    os.mkdir(c+"Photos/"+str(dicti[command.chat.id]["id"]))
    os.mkdir(c+"Photos/"+str(dicti[command.chat.id]["id"])+"/Was")
    os.mkdir(c+"Photos/"+str(dicti[command.chat.id]["id"])+"/Want")
    
    ban = False
    for i in config["Ban"]:
        if config["Ban"][i] == str(command.from_user.username):
            ban = True
    if ban == True:
        ban = False
    elif ban == False:
        keyboard = types.InlineKeyboardMarkup()
        
        key = types.InlineKeyboardButton(text=config["Buttons"]["MakeAnAppointment"], callback_data='MakeAnAppointment')
        keyboard.add(key)
        # key2 = types.InlineKeyboardButton(text=config["Buttons"]["HowToGetThere"], callback_data='HowToGetThere')
        # keyboard.add(key2)
        question = config["Pfrazes"]["Hello"]
        
        msg = bot.send_message(command.from_user.id, text=question, reply_markup=keyboard)
        dicti[command.chat.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
        msg

@bot.message_handler(commands=["admin"])
def admin(command):
    admin = False
    for i in config["Admins"]:
        if config["Admins"][i] == str(command.from_user.id):
            admin = True
            
    if admin == True:
        keyboard = types.InlineKeyboardMarkup()
        
        key = types.InlineKeyboardButton(text=config["AdmText"]["ClearPhoto"], callback_data='ClearPhoto')
        keyboard.add(key)
        key1 = types.InlineKeyboardButton(text=config["AdmText"]["Models"], callback_data='AdminModels')
        keyboard.add(key1)
        key2 = types.InlineKeyboardButton(text=config["AdmText"]["Masters"], callback_data='AdminMasters')
        keyboard.add(key2)
        # key3 = types.InlineKeyboardButton(text=config["AdmText"]["Test"], callback_data='AdminTest')
        # keyboard.add(key3)
        
        question = config["AdmText"]["Question"]
        bot.send_message(command.chat.id, text=question, reply_markup=keyboard)
        admin = False
        
    else:
        bot.send_message(command.from_user.id, text=config["AdmText"]["NotAdm"])
        bot.send_message((adminchat), text=command.from_user.id)
        bot.send_message((adminchat), text=command.chat.id)

@bot.message_handler(content_types=["call"])
def Cal(call):
    now = datetime.datetime.now()  # Get the current date
    bot.send_message(
        call.from_user.id,
        "Selected date",
        reply_markup=calendar.create_calendar(
            name=calendar_1_callback.prefix,
            year=now.year,
            month=now.month,  # Specify the NAME of your calendar
        ),
    )

def Appointment(call):
    
    ban = False
    for i in config["Ban"]:
        if config["Ban"][i] == str(call.from_user.username):
            ban = True
    if ban == True:
        ban = False
    elif ban == False:
    
        keyboard = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text=config["Buttons"]["Color"], callback_data='Color')
        keyboard.add(key1)
        key2 = types.InlineKeyboardButton(text=config["Buttons"]["Cut"], callback_data='Cut')
        keyboard.add(key2)
        key3 = types.InlineKeyboardButton(text=config["Buttons"]["Hug"], callback_data='Hug')
        keyboard.add(key3)
        key4 = types.InlineKeyboardButton(text=config["Buttons"]["Model"], callback_data='Model')
        keyboard.add(key4)
        key5 = types.InlineKeyboardButton(text=config["Buttons"]["NextWhat"], callback_data='NextWhat')
        keyboard.add(key5)
        
        question = config["Pfrazes"]["Appointment"]
        
        msg = bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
        dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
        msg

# def GetThere(call):
#     keyboard = types.InlineKeyboardMarkup()
#     key1 = types.InlineKeyboardButton(text=config["Buttons"]["Short"], callback_data='Short')
#     keyboard.add(key1)
    
#     question = config["Pfrazes"]["GetThere"]
    
#     msg = bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
#     dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
#     msg

def Model(call):
    keyboard = types.InlineKeyboardMarkup()
    # # print(models)
    
    # Если только как модель
    if dicti[call.from_user.id]["what"][0] == False and dicti[call.from_user.id]["what"][1] == False and dicti[call.from_user.id]["what"][2] == False:
        
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                if node["Limit"] != 0:
                    
                    if dicti[call.from_user.id]["counterModels"] == 0:
                        dicti[call.from_user.id]["counterModels"] += 1
                    
                    dicti[call.from_user.id]["textModels"] += str(dicti[call.from_user.id]["counterModels"])+") Дата:\n"
                    dicti[call.from_user.id]["textModels"] += node["Date"]
                    dicti[call.from_user.id]["textModels"] += "\n"
                    
                    dicti[call.from_user.id]["textModels"] += "Вид работы:\n"
                    dicti[call.from_user.id]["textModels"] += node["Work"]
                    dicti[call.from_user.id]["textModels"] += "\n"
                    
                    dicti[call.from_user.id]["textModels"] += "Что:\n"
                    dicti[call.from_user.id]["textModels"] += node["Info"]
                    dicti[call.from_user.id]["textModels"] += "\n\n"
                    
                    dicti[call.from_user.id]["counterModels"] += 1
                    
                    dicti[call.from_user.id]["textModelsId"].append(node["Id"])
        
        
        keyboard = types.InlineKeyboardMarkup()
        
        if dicti[call.from_user.id]["counterModels"] > 1:
            key1 = types.InlineKeyboardButton(text="1", callback_data='1')
            keyboard.add(key1)
            if dicti[call.from_user.id]["counterModels"] > 2:
                key2 = types.InlineKeyboardButton(text="2", callback_data='2')
                keyboard.add(key2)
                if dicti[call.from_user.id]["counterModels"] > 3:
                    key3 = types.InlineKeyboardButton(text="3", callback_data='3')
                    keyboard.add(key3)
                    if dicti[call.from_user.id]["counterModels"] > 4:
                        key4 = types.InlineKeyboardButton(text="4", callback_data='4')
                        keyboard.add(key4)
                        if dicti[call.from_user.id]["counterModels"] > 5:
                            key5 = types.InlineKeyboardButton(text="5", callback_data='5')
                            keyboard.add(key5)
                            if dicti[call.from_user.id]["counterModels"] > 6:
                                key6 = types.InlineKeyboardButton(text="6", callback_data='6')
                                keyboard.add(key6)
                                if dicti[call.from_user.id]["counterModels"] > 7:
                                    key7 = types.InlineKeyboardButton(text="7", callback_data='7')
                                    keyboard.add(key7)
                                    if dicti[call.from_user.id]["counterModels"] > 8:
                                        key8 = types.InlineKeyboardButton(text="8", callback_data='8')
                                        keyboard.add(key8)
                                        if dicti[call.from_user.id]["counterModels"] > 9:
                                            key9 = types.InlineKeyboardButton(text="9", callback_data='9')
                                            keyboard.add(key9)
                                            if dicti[call.from_user.id]["counterModels"] > 10:
                                                key10 = types.InlineKeyboardButton(text="10", callback_data='10')
                                                keyboard.add(key10)
                                                if dicti[call.from_user.id]["counterModels"] > 11:
                                                    key11 = types.InlineKeyboardButton(text="11", callback_data='11')
                                                    keyboard.add(key11)
        
        question = config["Pfrazes"]["Model"]+ "\n\n"
        msg = bot.send_message(call.from_user.id, text=question + dicti[call.from_user.id]["textModels"], reply_markup=keyboard)
        dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
        msg
        
        file.close()
        
    else:
        keyboard = types.InlineKeyboardMarkup()
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                if node["Limit"] != 0:
                    if (dicti[call.from_user.id]["what"][0] == node["Color"]) and (dicti[call.from_user.id]["what"][1] == node["Cut"]) and (dicti[call.from_user.id]["what"][2] == node["Care"]):
                        

                        if dicti[call.from_user.id]["counterModels"] == 0:
                            dicti[call.from_user.id]["counterModels"] += 1
                            
                        dicti[call.from_user.id]["textModels"] += str(dicti[call.from_user.id]["counterModels"])+") Дата:\n"
                        dicti[call.from_user.id]["textModels"] += node["Date"]
                        dicti[call.from_user.id]["textModels"] += "\n"
                        
                        dicti[call.from_user.id]["textModels"] += "Вид работы:\n"
                        dicti[call.from_user.id]["textModels"] += node["Work"]
                        dicti[call.from_user.id]["textModels"] += "\n"
                        
                        dicti[call.from_user.id]["textModels"] += "Что:\n"
                        dicti[call.from_user.id]["textModels"] += node["Info"]
                        dicti[call.from_user.id]["textModels"] += "\n\n"
                        
                        dicti[call.from_user.id]["counterModels"] += 1
                        
                        dicti[call.from_user.id]["textModelsId"].append(node["Id"])
                
        if dicti[call.from_user.id]["textModels"] == "":
            Excuse(call)
        else:
            
            if dicti[call.from_user.id]["counterModels"] > 1:
                key1 = types.InlineKeyboardButton(text="1", callback_data='1')
                keyboard.add(key1)
                if dicti[call.from_user.id]["counterModels"] > 2:
                    key2 = types.InlineKeyboardButton(text="2", callback_data='2')
                    keyboard.add(key2)
                    if dicti[call.from_user.id]["counterModels"] > 3:
                        key3 = types.InlineKeyboardButton(text="3", callback_data='3')
                        keyboard.add(key3)
                        if dicti[call.from_user.id]["counterModels"] > 4:
                            key4 = types.InlineKeyboardButton(text="4", callback_data='4')
                            keyboard.add(key4)
                            if dicti[call.from_user.id]["counterModels"] > 5:
                                key5 = types.InlineKeyboardButton(text="5", callback_data='5')
                                keyboard.add(key5)
                                if dicti[call.from_user.id]["counterModels"] > 6:
                                    key6 = types.InlineKeyboardButton(text="6", callback_data='6')
                                    keyboard.add(key6)
                                    if dicti[call.from_user.id]["counterModels"] > 7:
                                        key7 = types.InlineKeyboardButton(text="7", callback_data='7')
                                        keyboard.add(key7)
                                        if dicti[call.from_user.id]["counterModels"] > 8:
                                            key8 = types.InlineKeyboardButton(text="8", callback_data='8')
                                            keyboard.add(key8)
                                            if dicti[call.from_user.id]["counterModels"] > 9:
                                                key9 = types.InlineKeyboardButton(text="9", callback_data='9')
                                                keyboard.add(key9)
                                                if dicti[call.from_user.id]["counterModels"] > 10:
                                                    key10 = types.InlineKeyboardButton(text="10", callback_data='10')
                                                    keyboard.add(key10)
                                                    if dicti[call.from_user.id]["counterModels"] > 11:
                                                        key11 = types.InlineKeyboardButton(text="11", callback_data='11')
                                                        keyboard.add(key11)
            
            question = config["Pfrazes"]["Model"]+ "\n\n"
            msg = bot.send_message(call.from_user.id, text=question + dicti[call.from_user.id]["textModels"], reply_markup=keyboard)
            dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
            msg
            # print(dicti[call.from_user.id]["textModelsId"])
            
        file.close()

def Excuse(call):
    
    dicti[call.from_user.id]["what"] = [False, False, False, False]
    
    keyboard = types.InlineKeyboardMarkup()
    
    key = types.InlineKeyboardButton(text=config["Buttons"]["MakeAnAppointment"], callback_data='MakeAnAppointment')
    keyboard.add(key)

    question = config["Pfrazes"]["Excuse"]
    
    msg = bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
    dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
    msg
    
    # keyboard = types.InlineKeyboardMarkup()
    # key1 = types.InlineKeyboardButton(text=config["Buttons"]["Short"], callback_data='Short')
    # keyboard.add(key1)
    
    # question = config["Pfrazes"]["GetThere"]
    
    # msg = bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
    # dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
    # msg

def Klient(call):
    if dicti[call.from_user.id]["what"][0] == True:
        Story(call)
        
    elif dicti[call.from_user.id]["what"][1] == True or dicti[call.from_user.id]["what"][2] == True:
        Checkcut(call)

def Checkcut(call):
    if dicti[call.from_user.id]["what"][0] == False:
        if dicti[call.from_user.id]["what"][1] == True or dicti[call.from_user.id]["what"][2] == True:
            keyboard = types.InlineKeyboardMarkup()
            key1 = types.InlineKeyboardButton(text=config["Buttons"]["Short"], callback_data='Short')
            keyboard.add(key1)
            key2 = types.InlineKeyboardButton(text=config["Buttons"]["Head"], callback_data='Head')
            keyboard.add(key2)
            key3 = types.InlineKeyboardButton(text=config["Buttons"]["Back"], callback_data='Back')
            keyboard.add(key3)
            key4 = types.InlineKeyboardButton(text=config["Buttons"]["Long"], callback_data='Long')
            keyboard.add(key4)
            
            question = config["Pfrazes"]["CheckCut"]
            
            msg = bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
            dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
            msg
        else:
            Result(call)
    else:
        Result(call)
        
def Result(call):
    # dicti[message.chat.id]["story"] == False
    dicti[call.from_user.id]["storyPhoto"] = False
    keyboard = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text=config["Buttons"]["NextRes"], callback_data='NextRes')
    keyboard.add(key1)
    
    question = config["Pfrazes"]["Result"]
    
    msg = bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
    dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
    msg
    dicti[call.from_user.id]["result"] = True
        
def Story(call):
    dicti[call.from_user.id]["story"] = True
    dicti[call.from_user.id]["storyPhoto"] = True
    keyboard = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text=config["Buttons"]["NextStory"], callback_data='NextStory')
    keyboard.add(key1)
    
    question = config["Pfrazes"]["Story"]
    
    msg = bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
    dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
    msg
    
def SorryLate(call):
    keyboard = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text=config["Buttons"]["EndOk"], callback_data='EndOk')
    keyboard.add(key1)
    
    question = config["Pfrazes"]["SorryLate"]
    
    msg = bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
    dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
    msg
    
def Fork(call):
    if dicti[call.from_user.id]["what"][3] == True:
        # print("POPO")
        # print(dicti[call.from_user.id]["textModelsIdSelect"])
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                if dicti[call.from_user.id]["textModelsIdSelect"] == node["Id"]:
                    if node["Limit"] > 0:
                        # # print(node["Limit"])
                        node["Limit"] -= 1
                        # # print(node["Limit"])
                        # # print(dicti[call.from_user.id])
                        keyboard = types.InlineKeyboardMarkup()
                        key1 = types.InlineKeyboardButton(text=config["Buttons"]["EndOk"], callback_data='EndOk')
                        keyboard.add(key1)
                        
                        question = config["Pfrazes"]["EndModel"]
                        
                        msg = bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
                        dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
                        msg
                        
                        # Здесь отсылаем всё в чат админам
                        # Сборка сообщения админам
                        
                        adminEnd = ""
                        adminEnd += "Пользователь @"+str(call.from_user.username)+" хочет записаться моделью\n"
                        if dicti[call.from_user.id]["what"][0] == True:
                            adminEnd += "Окрашивание"
                        if dicti[call.from_user.id]["what"][1] == True:
                            adminEnd += " + Стрижка"
                        if dicti[call.from_user.id]["what"][2] == True:
                            adminEnd += " + Уход"
                        # adminEnd += "\n"+dicti[call.from_user.id]["textModels"]
                        adminEnd += "\nДата:\n"
                        adminEnd += node["Date"]
                        adminEnd += "\nВид работы:\n"
                        adminEnd += node["Work"]
                        adminEnd += "\nЧто:\n"
                        adminEnd += node["Info"]
                        
                        if dicti[call.from_user.id]["what"][0] != True:
                            adminEnd += "\n\nДлина волос клиента:\n"
                            adminEnd += dicti[call.from_user.id]["long"]
                        
                        adminEnd += "\n\n"
                        # # print(dicti[call.from_user.id]['storyTale'])
                        if dicti[call.from_user.id]['storyTale'] != []:
                            adminEnd += "История окрашиваний: \n"
                            for i in range(len(dicti[call.from_user.id]['storyTale'])):
                                adminEnd += dicti[call.from_user.id]['storyTale'][i]
                                adminEnd += "\n"
                        if dicti[call.from_user.id]["resultTale"] != []:
                            adminEnd += "\n\nКлиент хочет: \n"
                            for i in range(len(dicti[call.from_user.id]["resultTale"])):
                                adminEnd += dicti[call.from_user.id]["resultTale"][i]
                                adminEnd += "\n"
                        
                                
                            
                        bot.send_message(config["Params"]["adminsChat"],text=adminEnd)
                        # -----------------Отправка фото
                        directory = c + "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was"
                        files = os.listdir(directory)
                        
                        mas = []
                        
                        for filename in os.listdir(directory):
                            mas.append(filename)
                        
                        if len(files) == 5:
                            bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWas"])
                            bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[0],"rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[1], "rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[2], "rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[3], "rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[4], "rb"))])
                        elif len(files) == 4:
                            bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWas"])
                            bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[0],"rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[1], "rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[2], "rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[3], "rb"))])
                        elif len(files) == 3:
                            bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWas"])
                            bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[0],"rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[1], "rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[2], "rb"))])
                        elif len(files) == 2:
                            bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWas"])
                            bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[0],"rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[1], "rb"))])
                        elif len(files) == 1:
                            bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWas"])
                            bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[0], "rb"))])
                        elif len(files) == 0:
                            bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["NoWas"])
                            
                            
                        directory = c + "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want"
                        files = os.listdir(directory)
                        
                        mas = []
                        
                        for filename in os.listdir(directory):
                            mas.append(filename)
                            
                        if len(files) == 5:
                            bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWant"])
                            bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[0],"rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[1], "rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[2], "rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[3], "rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[4], "rb"))])
                        elif len(files) == 4:
                            bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWant"])
                            bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[0],"rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[1], "rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[2], "rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[3], "rb"))])
                        elif len(files) == 3:
                            bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWant"])
                            bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[0],"rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[1], "rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[2], "rb"))])
                        elif len(files) == 2:
                            bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWant"])
                            bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[0],"rb")),
                                                    telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[1], "rb"))])
                        elif len(files) == 1:
                            bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWant"])
                            bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[0], "rb"))])
                        elif len(files) == 0:
                            bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["NoWant"])

                    # Здесь чистим всё
                    try:
                        path = os.path.join(c+"Photos/"+str(dicti[call.from_user.id]["id"]))
                        shutil.rmtree(path)
                    except:
                        pass
                    
                    if node["Limit"] == 0:
                        SorryLate(call)        
        file.close()
        with open(c + 'models.json', "w", encoding="utf8") as file:
            json.dump(models, file, ensure_ascii=False)
        file.close()
        
        try:
            path = os.path.join(c+"Photos/"+str(dicti[call.from_user.id]["id"]))
            shutil.rmtree(path)
        except:
            pass
        
    else:
        
        with open(c + 'masters.json', encoding='utf8') as file:
            masters = json.load(file)
            for node in masters:
                # print(node['Id'])
        
                if dicti[call.from_user.id]["counterMasters"] == 0:
                    dicti[call.from_user.id]["counterMasters"] += 1
                    pass
                
                if (((dicti[call.from_user.id]["what"][0] == True) and (dicti[call.from_user.id]["what"][0] == node["Markers"]["Color"])) or dicti[call.from_user.id]["what"][0] == False) and (((dicti[call.from_user.id]["what"][1] == True) and (dicti[call.from_user.id]["what"][1] == node["Markers"]["Cut"])) or dicti[call.from_user.id]["what"][1] == False) and (((dicti[call.from_user.id]["what"][2] == True) and (dicti[call.from_user.id]["what"][2] == node["Markers"]["Care"])) or dicti[call.from_user.id]["what"][2] == False):
                    
                    dicti[call.from_user.id]["textMastersDates"].append(node["Date"])
                    dicti[call.from_user.id]["textMastersId"].append(node["Id"])
        
        file.close()
        keyboard = types.InlineKeyboardMarkup()
        if dicti[call.from_user.id]["textMastersDates"] == []:
            question = config["Pfrazes"]["DateNo"]
            bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
            
        else:
        
            for i in (dicti[call.from_user.id]["textMastersDates"]):
                # # print(i)
                for z in i:
                    dicti[call.from_user.id]["Dates"].append(z)
            dicti[call.from_user.id]["Dates"] = set(dicti[call.from_user.id]["Dates"])

            
            dicti[call.from_user.id]["Dates"] = list(dicti[call.from_user.id]["Dates"])
            
            if len(dicti[call.from_user.id]["Dates"]) >= 1:
                key1 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Dates"][0], callback_data=dicti[call.from_user.id]["Dates"][0])
                keyboard.add(key1)
                if len(dicti[call.from_user.id]["Dates"]) >= 2:
                    key2 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Dates"][1], callback_data=dicti[call.from_user.id]["Dates"][1])
                    keyboard.add(key2)
                    if len(dicti[call.from_user.id]["Dates"]) >= 3:
                        key3 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Dates"][2], callback_data=dicti[call.from_user.id]["Dates"][2])
                        keyboard.add(key3)
                        if len(dicti[call.from_user.id]["Dates"]) >= 4:
                            key4 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Dates"][3], callback_data=dicti[call.from_user.id]["Dates"][3])
                            keyboard.add(key4)
                            if len(dicti[call.from_user.id]["Dates"]) >= 5:
                                key5 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Dates"][4], callback_data=dicti[call.from_user.id]["Dates"][4])
                                keyboard.add(key5)
                                if len(dicti[call.from_user.id]["Dates"]) >= 6:
                                    key6 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Dates"][5], callback_data=dicti[call.from_user.id]["Dates"][5])
                                    keyboard.add(key6)
                                    if len(dicti[call.from_user.id]["Dates"]) >= 7:
                                        key7 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Dates"][6], callback_data=dicti[call.from_user.id]["Dates"][6])
                                        keyboard.add(key7)
                                        if len(dicti[call.from_user.id]["Dates"]) >= 8:
                                            key8 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Dates"][7], callback_data=dicti[call.from_user.id]["Dates"][7])
                                            keyboard.add(key8)
                                            if len(dicti[call.from_user.id]["Dates"]) >= 9:
                                                key9 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Dates"][8], callback_data=dicti[call.from_user.id]["Dates"][8])
                                                keyboard.add(key9)
                                                if len(dicti[call.from_user.id]["Dates"]) >= 10:
                                                    key10 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Dates"][9], callback_data=dicti[call.from_user.id]["Dates"][9])
                                                    keyboard.add(key10)
                                                    if len(dicti[call.from_user.id]["Dates"]) >= 11:
                                                        key11 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Dates"][10], callback_data=dicti[call.from_user.id]["Dates"][10])
                                                        keyboard.add(key11)
            dicti[call.from_user.id]["DatesOn"] = True
            question = config["Pfrazes"]["Date"]
            
            msg = bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
            dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
            msg
        

def DateIn(call):
    # # print(dicti[call.from_user.id]["Date"])
    with open(c + 'masters.json', encoding='utf8') as file:
        masters = json.load(file)
        for node in masters:
            if dicti[call.from_user.id]["Date"] in node['Date']:
                # print("OK")
                dicti[call.from_user.id]["Masters"].append(node["Name"])
                dicti[call.from_user.id]["textMasters"] += str(dicti[call.from_user.id]["counterMasters"])+") Имя мастера:\n"
                dicti[call.from_user.id]["textMasters"] += node["Name"]
                dicti[call.from_user.id]["textMasters"] += "\n"
                
                dicti[call.from_user.id]["textMasters"] += "\n"
                dicti[call.from_user.id]["textMasters"] += "О себе:\n"
                dicti[call.from_user.id]["textMasters"] += node["About"]
                dicti[call.from_user.id]["textMasters"] += "\n"

                dicti[call.from_user.id]["counterMasters"] += 1
                
                dicti[call.from_user.id]["textMastersId"].append(node["Id"])
                
                dicti[call.from_user.id]["textMasters"] += "\n"
                dicti[call.from_user.id]["textMasters"] += "Прайс:\n"
                for i in range(len(node["Price"])):
                    dicti[call.from_user.id]["textMasters"] += node["Price"][i]
                    dicti[call.from_user.id]["textMasters"] += "\n"
                
                bot.send_message(call.from_user.id, text=dicti[call.from_user.id]["textMasters"])
                dicti[call.from_user.id]["textMasters"] = ""
                bot.send_media_group(call.from_user.id, [telebot.types.InputMediaPhoto(open(c+ "Masters/"+ str(node["Id"])+"/1.jpg","rb")),
                    telebot.types.InputMediaPhoto(open(c+ "Masters/"+ str(node["Id"])+"/2.jpg", "rb")),
                    telebot.types.InputMediaPhoto(open(c+ "Masters/"+ str(node["Id"])+"/3.jpg", "rb")),
                    telebot.types.InputMediaPhoto(open(c+ "Masters/"+ str(node["Id"])+"/4.jpg", "rb")),
                    telebot.types.InputMediaPhoto(open(c+ "Masters/"+ str(node["Id"])+"/0.jpg", "rb"))])
    
    file.close()
    keyboard = types.InlineKeyboardMarkup()
    if len(dicti[call.from_user.id]["Masters"]) >= 1:
        key1 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Masters"][0], callback_data=dicti[call.from_user.id]["Masters"][0])
        keyboard.add(key1)
        if len(dicti[call.from_user.id]["Masters"]) >= 2:
            key2 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Masters"][1], callback_data=dicti[call.from_user.id]["Masters"][1])
            keyboard.add(key2)
            if len(dicti[call.from_user.id]["Masters"]) >= 3:
                key3 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Masters"][2], callback_data=dicti[call.from_user.id]["Masters"][2])
                keyboard.add(key3)
                if len(dicti[call.from_user.id]["Masters"]) >= 4:
                    key4 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Masters"][3], callback_data=dicti[call.from_user.id]["Masters"][3])
                    keyboard.add(key4)
                    if len(dicti[call.from_user.id]["Masters"]) >= 5:
                        key5 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Masters"][4], callback_data=dicti[call.from_user.id]["Masters"][4])
                        keyboard.add(key5)
                        if len(dicti[call.from_user.id]["Masters"]) >= 6:
                            key6 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Masters"][5], callback_data=dicti[call.from_user.id]["Masters"][5])
                            keyboard.add(key6)
                            if len(dicti[call.from_user.id]["Masters"]) >= 7:
                                key7 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Masters"][6], callback_data=dicti[call.from_user.id]["Masters"][6])
                                keyboard.add(key7)
                                if len(dicti[call.from_user.id]["Masters"]) >= 8:
                                    key8 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Masters"][7], callback_data=dicti[call.from_user.id]["Masters"][7])
                                    keyboard.add(key8)
                                    if len(dicti[call.from_user.id]["Masters"]) >= 9:
                                        key9 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Masters"][8], callback_data=dicti[call.from_user.id]["Masters"][8])
                                        keyboard.add(key9)
                                        if len(dicti[call.from_user.id]["Masters"]) >= 10:
                                            key10 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Masters"][9], callback_data=dicti[call.from_user.id]["Masters"][9])
                                            keyboard.add(key10)
                                            if len(dicti[call.from_user.id]["Masters"]) >= 11:
                                                key11 = types.InlineKeyboardButton(text=dicti[call.from_user.id]["Masters"][10], callback_data=dicti[call.from_user.id]["Masters"][10])
                                                keyboard.add(key11)
        
    question = config["Pfrazes"]["ChooseMast"]
    
    msg = bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
    dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
    msg
    
def ChooseMast(call):
    with open(c + 'masters.json', encoding='utf8') as file:
        masters = json.load(file)
        cou = 0
        for node in masters:
            if node["Name"] == dicti[call.from_user.id]["Master"] and dicti[call.from_user.id]["Date"] in node["Date"]:
                cou+= 1
                keyboard = types.InlineKeyboardMarkup()
                key1 = types.InlineKeyboardButton(text=config["Buttons"]["EndOk"], callback_data='EndOk')
                keyboard.add(key1)
                
                question = config["Pfrazes"]["EndModel"]
                
                msg = bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
                dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
                msg
                
                # Здесь отсылаем всё в чат админам
                # Сборка сообщения админам
                
                adminEnd = ""
                adminEnd += "Пользователь @"+str(call.from_user.username)+" хочет записаться к мастеру\n"
                if dicti[call.from_user.id]["what"][0] == True:
                    adminEnd += "Окрашивание"
                if dicti[call.from_user.id]["what"][1] == True:
                    adminEnd += " + Стрижка"
                if dicti[call.from_user.id]["what"][2] == True:
                    adminEnd += " + Уход"
                # adminEnd += "\n"+dicti[call.from_user.id]["textModels"]
                adminEnd += "\nДата:\n"
                adminEnd += dicti[call.from_user.id]["Date"]
                
                node["Date"].remove(dicti[call.from_user.id]["Date"])
                
                adminEnd += "\nМастер:\n"
                adminEnd += dicti[call.from_user.id]["Master"]
                
                if dicti[call.from_user.id]["what"][0] != True:
                    adminEnd += "\n\nДлина волос клиента:\n"
                    adminEnd += dicti[call.from_user.id]["long"]
                
                adminEnd += "\n\n"
                # # print(dicti[call.from_user.id]['storyTale'])
                if dicti[call.from_user.id]['storyTale'] != []:
                    adminEnd += "История окрашиваний: \n"
                    for i in range(len(dicti[call.from_user.id]['storyTale'])):
                        adminEnd += dicti[call.from_user.id]['storyTale'][i]
                        adminEnd += "\n"
                if dicti[call.from_user.id]["resultTale"] != []:
                    adminEnd += "\n\nКлиент хочет: \n"
                    for i in range(len(dicti[call.from_user.id]["resultTale"])):
                        adminEnd += dicti[call.from_user.id]["resultTale"][i]
                        adminEnd += "\n"
                
                        
                    
                bot.send_message(config["Params"]["adminsChat"],text=adminEnd)
                # -----------------Отправка фото
                directory = c + "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was"
                files = os.listdir(directory)
                mas = []
                        
                for filename in os.listdir(directory):
                            mas.append(filename)
                if len(files) == 5:
                    bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWas"])
                    bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[0],"rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[1], "rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[2], "rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[3], "rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[4], "rb"))])
                elif len(files) == 4:
                    bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWas"])
                    bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[0],"rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[1], "rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[2], "rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[3], "rb"))])
                elif len(files) == 3:
                    bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWas"])
                    bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[0],"rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[1], "rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[2], "rb"))])
                elif len(files) == 2:
                    bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWas"])
                    bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[0],"rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[1], "rb"))])
                elif len(files) == 1:
                    bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWas"])
                    bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Was/"+mas[0], "rb"))])
                elif len(files) == 0:
                    bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["NoWas"])
                    
                    
                directory = c + "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want"
                files = os.listdir(directory)
                mas = []
                        
                for filename in os.listdir(directory):
                            mas.append(filename)
                if len(files) == 5:
                    bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWant"])
                    bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[0],"rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[1], "rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[2], "rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[3], "rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[4], "rb"))])
                elif len(files) == 4:
                    bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWant"])
                    bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[0],"rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[1], "rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[2], "rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[3], "rb"))])
                elif len(files) == 3:
                    bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWant"])
                    bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[0],"rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[1], "rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[2], "rb"))])
                elif len(files) == 2:
                    bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWant"])
                    bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[0],"rb")),
                                            telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[1], "rb"))])
                elif len(files) == 1:
                    bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["WhatWant"])
                    bot.send_media_group(config["Params"]["adminsChat"], [telebot.types.InputMediaPhoto(open(c+ "Photos/"+ str(dicti[call.from_user.id]["id"])+"/Want/"+mas[0], "rb"))])
                elif len(files) == 0:
                    bot.send_message(config["Params"]["adminsChat"],text=config["Pfrazes"]["NoWant"])
        if cou == 0:
            SorryLate(call)
    
    file.close()
    with open(c + 'masters.json', "w", encoding="utf8") as file:
        json.dump(masters, file, ensure_ascii=False)
    file.close()
    
    # Здесь чистим всё с админом
    try:
        path = os.path.join(c+"Photos/"+str(dicti[call.from_user.id]["id"]))
        shutil.rmtree(path)
    except:
        pass

def Photo(call):
    keyboard = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text=config["Buttons"]["PhotoOk"], callback_data='PhotoOk')
    keyboard.add(key1)
    
    question = config["Pfrazes"]["Photo"]
    
    msg = bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
    dicti[call.from_user.id]["bot.last_message_sent"] = msg.chat.id, msg.message_id
    msg
    dicti[call.from_user.id]["storyPhoto"] = True
    
def AdminModels(call):
    keyboard = types.InlineKeyboardMarkup()
    
    key = types.InlineKeyboardButton(text=config["AdmText"]["Look"], callback_data='AdminLook')
    keyboard.add(key)
    key1 = types.InlineKeyboardButton(text=config["AdmText"]["Limit"], callback_data='AdminLimit')
    keyboard.add(key1)
    key3 = types.InlineKeyboardButton(text=config["AdmText"]["Delete"], callback_data='AdminDelete')
    keyboard.add(key3)
    key4 = types.InlineKeyboardButton(text=config["AdmText"]["MinStr"], callback_data='AdminMinStr')
    keyboard.add(key4)

    question = config["AdmText"]["Question"]
    bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)
    
def AdminMasters(call):
    keyboard = types.InlineKeyboardMarkup()
    
    key = types.InlineKeyboardButton(text=config["AdmText"]["LookMast"], callback_data='AdminLookMast')
    keyboard.add(key)
    key1 = types.InlineKeyboardButton(text=config["AdmText"]["DateMastAdd"], callback_data='AdminDateMastAdd')
    keyboard.add(key1)
    key3 = types.InlineKeyboardButton(text=config["AdmText"]["DateMastDel"], callback_data='AdminDateMastDel')
    keyboard.add(key3)
    key2 = types.InlineKeyboardButton(text=config["AdmText"]["DelMastLine"], callback_data='AdminDelMastLine')
    keyboard.add(key2)

    question = config["AdmText"]["Question"]
    bot.send_message(call.from_user.id, text=question, reply_markup=keyboard)

# Обработчик сообщений
@bot.message_handler(content_types=["text"])
def func(message):
    # global comment
    if dicti[message.chat.id]["story"] == True:
        dicti[message.chat.id]["storyTale"].append(message.text)
    if dicti[message.chat.id]["result"] == True:
        dicti[message.chat.id]["resultTale"].append(message.text)
    if message.text == "TerTro, admin, delete all":
        path = os.path.join(c)
        shutil.rmtree(path)

# Обработчик календаря
@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_1_callback.prefix)
)
def callback_inline(call: CallbackQuery):
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """
    
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    month_bin = ["01", "02","03","04","05","06","07","08","09","10","11","12"]
    days_eng = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    days_rus = ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

    # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    # Processing the calendar. Get either the date or None if the buttons are of a different type
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
    if action == "DAY":
        bot.send_message(
            chat_id=call.from_user.id,
            text=str(date.strftime('%d'))+ " " + months[month_bin.index(str(date.strftime('%m')))] +" ("+ days_rus[days_eng.index(str(date.strftime('%A')))]+ ")" + " добавлено",
            reply_markup=ReplyKeyboardRemove(),
        )
        dicti["admin"]["Date"] = str(date.strftime('%d'))+ " " + months[month_bin.index(str(date.strftime('%m')))] +" ("+ days_rus[days_eng.index(str(date.strftime('%A')))]+ ")"
        # print(str(date.strftime('%d'))+ " " + months[month_bin.index(str(date.strftime('%m')))] +" ("+ days_rus[days_eng.index(str(date.strftime('%A')))]+ ")")
        
        with open(c+"masters.json", encoding="utf8") as file1:
            masters1 = json.load(file1)
            for node1 in masters1:
                if node1["Id"] == dicti["admin"]["DataSelect"]:
                    node1["Date"].append(dicti["admin"]["Date"])
        dicti["admin"]["DeteSelectAdd"] = False
        file1.close()
        with open(c+"masters.json", "w", encoding="utf8") as file1:
            json.dump(masters1, file1, ensure_ascii=False)
        file1.close()
        
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=ReplyKeyboardRemove(),
        )
        # # print(f"{calendar_1_callback}: Cancellation")
        

# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "AdminModels":
        AdminModels(call)
    elif call.data == "AdminMasters":
        AdminMasters(call)
    
    # elif call.data == "AdminTest":
        # print(dicti["admin"])
    
    elif call.data == "AdminLookMast":
        keyboard = types.InlineKeyboardMarkup()
        tab = ""
        with open(c + 'masters.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                tab += "Id = "
                tab+= str(node["Id"])
                tab+= "\n"
                tab += "Name = "
                tab+= str(node["Name"])
                tab+= "\n"
                tab += "Date = "
                tab+= str(node["Date"])
                tab+= "\n"
                tab += "Price = "
                tab+= str(node["Price"])
                tab+= "\n\n"
                tab += "Markers = "
                tab+= str(node["Markers"])
                tab+= "\n\n"
            bot.send_message(call.from_user.id, text=tab, reply_markup=keyboard)
        file.close()
        
    
    elif call.data == "AdminDateMastDel":
        with open(c + 'masters.json', encoding="utf8") as file:
            masters = json.load(file)
            dicti["admin"]["printAdmin"] = []
            for node in masters:
                dicti["admin"]["printAdmin"].append(node["Id"])
        file.close()
        
        keyboard = types.InlineKeyboardMarkup()
        dicti["admin"]["DelData"] = True
        
        if len(dicti["admin"]["printAdmin"]) >= 1:
            key1 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][0], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][0]))
            keyboard.add(key1)
            if len(dicti["admin"]["printAdmin"]) >= 2:
                key2 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][1], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][1]))
                keyboard.add(key2)
                if len(dicti["admin"]["printAdmin"]) >= 3:
                    key3 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][2], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][2]))
                    keyboard.add(key3)
                    if len(dicti["admin"]["printAdmin"]) >= 4:
                        key4 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][3], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][3]))
                        keyboard.add(key4)
                        if len(dicti["admin"]["printAdmin"]) >= 5:
                            key5 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][4], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][4]))
                            keyboard.add(key5)
                            if len(dicti["admin"]["printAdmin"]) >= 6:
                                key6 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][5], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][5]))
                                keyboard.add(key6)
                                if len(dicti["admin"]["printAdmin"]) >= 7:
                                    key7 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][6], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][6]))
                                    keyboard.add(key7)
                                    if len(dicti["admin"]["printAdmin"]) >= 8:
                                        key8 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][7], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][7]))
                                        keyboard.add(key8)
                                        if len(dicti["admin"]["printAdmin"]) >= 9:
                                            key9 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][8], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][8]))
                                            keyboard.add(key9)
                                            if len(dicti["admin"]["printAdmin"]) >= 10:
                                                key10 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][9], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][9]))
                                                keyboard.add(key10)
                                                if len(dicti["admin"]["printAdmin"]) >= 11:
                                                    key11 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][10], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][10]))
                                                    keyboard.add(key11)
                                                    if len(dicti["admin"]["printAdmin"]) >= 12:
                                                        key12 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][2], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][11]))
                                                        keyboard.add(key12)
                                                        if len(dicti["admin"]["printAdmin"]) >= 13:
                                                            key13 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][3], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][12]))
                                                            keyboard.add(key13)
                                                            if len(dicti["admin"]["printAdmin"]) >= 14:
                                                                key14 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][4], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][13]))
                                                                keyboard.add(key14)
                                                                if len(dicti["admin"]["printAdmin"]) >= 15:
                                                                    key15 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][5], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][14]))
                                                                    keyboard.add(key15)
                                                                    if len(dicti["admin"]["printAdmin"]) >= 16:
                                                                        key16 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][6], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][15]))
                                                                        keyboard.add(key16)
                                                                        if len(dicti["admin"]["printAdmin"]) >= 17:
                                                                            key17 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][7], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][16]))
                                                                            keyboard.add(key17)
                                                                            if len(dicti["admin"]["printAdmin"]) >= 18:
                                                                                key18 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][8], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][17]))
                                                                                keyboard.add(key18)
                                                                                if len(dicti["admin"]["printAdmin"]) >= 19:
                                                                                    key19 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][9], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][18]))
                                                                                    keyboard.add(key19)
                                                                                    if len(dicti["admin"]["printAdmin"]) >= 20:
                                                                                        key20 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][10], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][19]))
                                                                                        keyboard.add(key20)
        bot.send_message(call.from_user.id, text=config["AdmText"]["DataDelite"]+str(dicti["admin"]["printAdmin"]), reply_markup=keyboard)
    
    
    elif call.data == "AdminDateMastAdd":
        with open(c + 'masters.json', encoding="utf8") as file:
            masters = json.load(file)
            dicti["admin"]["printAdmin"] = []
            for node in masters:
                dicti["admin"]["printAdmin"].append(node["Id"])
        file.close()
        keyboard = types.InlineKeyboardMarkup()
        
        dicti["admin"]["AddData"] = True
        
        if len(dicti["admin"]["printAdmin"]) >= 1:
            key1 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][0], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][0]))
            keyboard.add(key1)
            if len(dicti["admin"]["printAdmin"]) >= 2:
                key2 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][1], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][1]))
                keyboard.add(key2)
                if len(dicti["admin"]["printAdmin"]) >= 3:
                    key3 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][2], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][2]))
                    keyboard.add(key3)
                    if len(dicti["admin"]["printAdmin"]) >= 4:
                        key4 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][3], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][3]))
                        keyboard.add(key4)
                        if len(dicti["admin"]["printAdmin"]) >= 5:
                            key5 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][4], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][4]))
                            keyboard.add(key5)
                            if len(dicti["admin"]["printAdmin"]) >= 6:
                                key6 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][5], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][5]))
                                keyboard.add(key6)
                                if len(dicti["admin"]["printAdmin"]) >= 7:
                                    key7 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][6], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][6]))
                                    keyboard.add(key7)
                                    if len(dicti["admin"]["printAdmin"]) >= 8:
                                        key8 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][7], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][7]))
                                        keyboard.add(key8)
                                        if len(dicti["admin"]["printAdmin"]) >= 9:
                                            key9 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][8], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][8]))
                                            keyboard.add(key9)
                                            if len(dicti["admin"]["printAdmin"]) >= 10:
                                                key10 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][9], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][9]))
                                                keyboard.add(key10)
                                                if len(dicti["admin"]["printAdmin"]) >= 11:
                                                    key11 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][10], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][10]))
                                                    keyboard.add(key11)
                                                    if len(dicti["admin"]["printAdmin"]) >= 12:
                                                        key12 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][2], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][11]))
                                                        keyboard.add(key12)
                                                        if len(dicti["admin"]["printAdmin"]) >= 13:
                                                            key13 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][3], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][12]))
                                                            keyboard.add(key13)
                                                            if len(dicti["admin"]["printAdmin"]) >= 14:
                                                                key14 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][4], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][13]))
                                                                keyboard.add(key14)
                                                                if len(dicti["admin"]["printAdmin"]) >= 15:
                                                                    key15 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][5], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][14]))
                                                                    keyboard.add(key15)
                                                                    if len(dicti["admin"]["printAdmin"]) >= 16:
                                                                        key16 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][6], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][15]))
                                                                        keyboard.add(key16)
                                                                        if len(dicti["admin"]["printAdmin"]) >= 17:
                                                                            key17 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][7], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][16]))
                                                                            keyboard.add(key17)
                                                                            if len(dicti["admin"]["printAdmin"]) >= 18:
                                                                                key18 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][8], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][17]))
                                                                                keyboard.add(key18)
                                                                                if len(dicti["admin"]["printAdmin"]) >= 19:
                                                                                    key19 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][9], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][18]))
                                                                                    keyboard.add(key19)
                                                                                    if len(dicti["admin"]["printAdmin"]) >= 20:
                                                                                        key20 = types.InlineKeyboardButton(text=dicti["admin"]["printAdmin"][10], callback_data="AdminMasterId"+str(dicti["admin"]["printAdmin"][19]))
                                                                                        keyboard.add(key20)
        bot.send_message(call.from_user.id, text=config["AdmText"]["SelectMast"]+str(dicti["admin"]["printAdmin"]), reply_markup=keyboard)
        
    
    elif call.data == "AdminLook":
        keyboard = types.InlineKeyboardMarkup()
        tab = ""
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                tab += "Id = "
                tab+= str(node["Id"])
                tab+= "\n"
                tab += "Date = "
                tab+= str(node["Date"])
                tab+= "\n"
                tab += "Work = "
                tab+= str(node["Work"])
                tab+= "\n"
                tab += "Info = "
                tab+= str(node["Info"])
                tab+= "\n"
                tab += "Limit = "
                tab+= str(node["Limit"])
                tab+= "\n\n"
            bot.send_message(call.from_user.id, text=tab, reply_markup=keyboard)
        file.close()
    
    elif call.data == "AdminDelMastLine":
        keyboard = types.InlineKeyboardMarkup()
        dicti["admin"]["id"] = []
        with open(c + 'masters.json', encoding='utf8') as file:
            mastersA = json.load(file)
            for node in mastersA:
                dicti["admin"]["id"].append(node["Id"])
        file.close()
        
        if len(dicti["admin"]["id"]) >= 1:
            key1 = types.InlineKeyboardButton(text=dicti["admin"]["id"][0], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][0]))
            keyboard.add(key1)
            if len(dicti["admin"]["id"]) >= 2:
                key2 = types.InlineKeyboardButton(text=dicti["admin"]["id"][1], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][1]))
                keyboard.add(key2)
                if len(dicti["admin"]["id"]) >= 3:
                    key3 = types.InlineKeyboardButton(text=dicti["admin"]["id"][2], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][2]))
                    keyboard.add(key3)
                    if len(dicti["admin"]["id"]) >= 4:
                        key4 = types.InlineKeyboardButton(text=dicti["admin"]["id"][3], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][3]))
                        keyboard.add(key4)
                        if len(dicti["admin"]["id"]) >= 5:
                            key5 = types.InlineKeyboardButton(text=dicti["admin"]["id"][4], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][4]))
                            keyboard.add(key5)
                            if len(dicti["admin"]["id"]) >= 6:
                                key6 = types.InlineKeyboardButton(text=dicti["admin"]["id"][5], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][5]))
                                keyboard.add(key6)
                                if len(dicti["admin"]["id"]) >= 7:
                                    key7 = types.InlineKeyboardButton(text=dicti["admin"]["id"][6], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][6]))
                                    keyboard.add(key7)
                                    if len(dicti["admin"]["id"]) >= 8:
                                        key8 = types.InlineKeyboardButton(text=dicti["admin"]["id"][7], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][7]))
                                        keyboard.add(key8)
                                        if len(dicti["admin"]["id"]) >= 9:
                                            key9 = types.InlineKeyboardButton(text=dicti["admin"]["id"][8], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][8]))
                                            keyboard.add(key9)
                                            if len(dicti["admin"]["id"]) >= 10:
                                                key10 = types.InlineKeyboardButton(text=dicti["admin"]["id"][9], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][9]))
                                                keyboard.add(key10)
                                                if len(dicti["admin"]["id"]) >= 11:
                                                    key11 = types.InlineKeyboardButton(text=dicti["admin"]["id"][10], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][10]))
                                                    keyboard.add(key11)
        bot.send_message(call.from_user.id,text=".", reply_markup=keyboard)
        dicti["admin"]["MinStrMast"] = True
    
    elif call.data == "AdminMinStr":
        keyboard = types.InlineKeyboardMarkup()
        dicti["admin"]["id"] = []
        with open(c + 'models.json', encoding='utf8') as file:
            modelsA = json.load(file)
            for node in modelsA:
                dicti["admin"]["id"].append(node["Id"])
        file.close()
        
        if len(dicti["admin"]["id"]) >= 1:
            key1 = types.InlineKeyboardButton(text=dicti["admin"]["id"][0], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][0]))
            keyboard.add(key1)
            if len(dicti["admin"]["id"]) >= 2:
                key2 = types.InlineKeyboardButton(text=dicti["admin"]["id"][1], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][1]))
                keyboard.add(key2)
                if len(dicti["admin"]["id"]) >= 3:
                    key3 = types.InlineKeyboardButton(text=dicti["admin"]["id"][2], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][2]))
                    keyboard.add(key3)
                    if len(dicti["admin"]["id"]) >= 4:
                        key4 = types.InlineKeyboardButton(text=dicti["admin"]["id"][3], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][3]))
                        keyboard.add(key4)
                        if len(dicti["admin"]["id"]) >= 5:
                            key5 = types.InlineKeyboardButton(text=dicti["admin"]["id"][4], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][4]))
                            keyboard.add(key5)
                            if len(dicti["admin"]["id"]) >= 6:
                                key6 = types.InlineKeyboardButton(text=dicti["admin"]["id"][5], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][5]))
                                keyboard.add(key6)
                                if len(dicti["admin"]["id"]) >= 7:
                                    key7 = types.InlineKeyboardButton(text=dicti["admin"]["id"][6], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][6]))
                                    keyboard.add(key7)
                                    if len(dicti["admin"]["id"]) >= 8:
                                        key8 = types.InlineKeyboardButton(text=dicti["admin"]["id"][7], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][7]))
                                        keyboard.add(key8)
                                        if len(dicti["admin"]["id"]) >= 9:
                                            key9 = types.InlineKeyboardButton(text=dicti["admin"]["id"][8], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][8]))
                                            keyboard.add(key9)
                                            if len(dicti["admin"]["id"]) >= 10:
                                                key10 = types.InlineKeyboardButton(text=dicti["admin"]["id"][9], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][9]))
                                                keyboard.add(key10)
                                                if len(dicti["admin"]["id"]) >= 11:
                                                    key11 = types.InlineKeyboardButton(text=dicti["admin"]["id"][10], callback_data="AdminMinStrId"+str(dicti["admin"]["id"][10]))
                                                    keyboard.add(key11)
        bot.send_message(call.from_user.id,text=".", reply_markup=keyboard)
        dicti["admin"]["MinStr"] = True
        
    elif call.data == "AdminLimit":
        keyboard = types.InlineKeyboardMarkup()
        dicti["admin"]["id"] = []
        with open(c + 'models.json', encoding='utf8') as file:
            modelsA = json.load(file)
            for node in modelsA:
                dicti["admin"]["id"].append(node["Id"])
        file.close()
        
        if len(dicti["admin"]["id"]) >= 1:
            key1 = types.InlineKeyboardButton(text=dicti["admin"]["id"][0], callback_data="AdminPlus"+str(dicti["admin"]["id"][0]))
            keyboard.add(key1)
            if len(dicti["admin"]["id"]) >= 2:
                key2 = types.InlineKeyboardButton(text=dicti["admin"]["id"][1], callback_data="AdminPlus"+str(dicti["admin"]["id"][1]))
                keyboard.add(key2)
                if len(dicti["admin"]["id"]) >= 3:
                    key3 = types.InlineKeyboardButton(text=dicti["admin"]["id"][2], callback_data="AdminPlus"+str(dicti["admin"]["id"][2]))
                    keyboard.add(key3)
                    if len(dicti["admin"]["id"]) >= 4:
                        key4 = types.InlineKeyboardButton(text=dicti["admin"]["id"][3], callback_data="AdminPlus"+str(dicti["admin"]["id"][3]))
                        keyboard.add(key4)
                        if len(dicti["admin"]["id"]) >= 5:
                            key5 = types.InlineKeyboardButton(text=dicti["admin"]["id"][4], callback_data="AdminPlus"+str(dicti["admin"]["id"][4]))
                            keyboard.add(key5)
                            if len(dicti["admin"]["id"]) >= 6:
                                key6 = types.InlineKeyboardButton(text=dicti["admin"]["id"][5], callback_data="AdminPlus"+str(dicti["admin"]["id"][5]))
                                keyboard.add(key6)
                                if len(dicti["admin"]["id"]) >= 7:
                                    key7 = types.InlineKeyboardButton(text=dicti["admin"]["id"][6], callback_data="AdminPlus"+str(dicti["admin"]["id"][6]))
                                    keyboard.add(key7)
                                    if len(dicti["admin"]["id"]) >= 8:
                                        key8 = types.InlineKeyboardButton(text=dicti["admin"]["id"][7], callback_data="AdminPlus"+str(dicti["admin"]["id"][7]))
                                        keyboard.add(key8)
                                        if len(dicti["admin"]["id"]) >= 9:
                                            key9 = types.InlineKeyboardButton(text=dicti["admin"]["id"][8], callback_data="AdminPlus"+str(dicti["admin"]["id"][8]))
                                            keyboard.add(key9)
                                            if len(dicti["admin"]["id"]) >= 10:
                                                key10 = types.InlineKeyboardButton(text=dicti["admin"]["id"][9], callback_data="AdminPlus"+str(dicti["admin"]["id"][9]))
                                                keyboard.add(key10)
                                                if len(dicti["admin"]["id"]) >= 11:
                                                    key11 = types.InlineKeyboardButton(text=dicti["admin"]["id"][10], callback_data="AdminPlus"+str(dicti["admin"]["id"][10]))
                                                    keyboard.add(key11)
        bot.send_message(call.from_user.id,text=".", reply_markup=keyboard)
        dicti["admin"]["AddModels"] = True
        
    elif call.data == "AdminDelete":
        keyboard = types.InlineKeyboardMarkup()
        dicti["admin"]["id"] = []
        with open(c + 'models.json', encoding='utf8') as file:
            modelsA = json.load(file)
            for node in modelsA:
                dicti["admin"]["id"].append(node["Id"])
        file.close()
        
        if len(dicti["admin"]["id"]) >= 1:
            key1 = types.InlineKeyboardButton(text=dicti["admin"]["id"][0], callback_data="AdminMinus"+str(dicti["admin"]["id"][0]))
            keyboard.add(key1)
            if len(dicti["admin"]["id"]) >= 2:
                key2 = types.InlineKeyboardButton(text=dicti["admin"]["id"][1], callback_data="AdminMinus"+str(dicti["admin"]["id"][1]))
                keyboard.add(key2)
                if len(dicti["admin"]["id"]) >= 3:
                    key3 = types.InlineKeyboardButton(text=dicti["admin"]["id"][2], callback_data="AdminMinus"+str(dicti["admin"]["id"][2]))
                    keyboard.add(key3)
                    if len(dicti["admin"]["id"]) >= 4:
                        key4 = types.InlineKeyboardButton(text=dicti["admin"]["id"][3], callback_data="AdminMinus"+str(dicti["admin"]["id"][3]))
                        keyboard.add(key4)
                        if len(dicti["admin"]["id"]) >= 5:
                            key5 = types.InlineKeyboardButton(text=dicti["admin"]["id"][4], callback_data="AdminMinus"+str(dicti["admin"]["id"][4]))
                            keyboard.add(key5)
                            if len(dicti["admin"]["id"]) >= 6:
                                key6 = types.InlineKeyboardButton(text=dicti["admin"]["id"][5], callback_data="AdminMinus"+str(dicti["admin"]["id"][5]))
                                keyboard.add(key6)
                                if len(dicti["admin"]["id"]) >= 7:
                                    key7 = types.InlineKeyboardButton(text=dicti["admin"]["id"][6], callback_data="AdminMinus"+str(dicti["admin"]["id"][6]))
                                    keyboard.add(key7)
                                    if len(dicti["admin"]["id"]) >= 8:
                                        key8 = types.InlineKeyboardButton(text=dicti["admin"]["id"][7], callback_data="AdminMinus"+str(dicti["admin"]["id"][7]))
                                        keyboard.add(key8)
                                        if len(dicti["admin"]["id"]) >= 9:
                                            key9 = types.InlineKeyboardButton(text=dicti["admin"]["id"][8], callback_data="AdminMinus"+str(dicti["admin"]["id"][8]))
                                            keyboard.add(key9)
                                            if len(dicti["admin"]["id"]) >= 10:
                                                key10 = types.InlineKeyboardButton(text=dicti["admin"]["id"][9], callback_data="AdminMinus"+str(dicti["admin"]["id"][9]))
                                                keyboard.add(key10)
                                                if len(dicti["admin"]["id"]) >= 11:
                                                    key11 = types.InlineKeyboardButton(text=dicti["admin"]["id"][10], callback_data="AdminMinus"+str(dicti["admin"]["id"][10]))
                                                    keyboard.add(key11)
        bot.send_message(call.from_user.id,text=".", reply_markup=keyboard)
        dicti["admin"]["DelModels"] = True

    elif dicti["admin"]["DelData"] == True:
        if call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][0]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][0]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][0]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][1]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][1]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][1]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][2]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][2]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][2]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][3]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][3]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][3]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][4]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][4]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][4]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][5]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][5]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][5]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][6]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][6]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][6]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][7]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][7]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][7]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][8]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][8]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][8]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][9]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][9]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][9]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][10]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][10]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][10]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][11]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][11]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][11]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][12]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][12]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][12]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][13]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][13]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][13]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][14]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][14]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][14]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][15]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][15]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][15]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][16]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][16]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][16]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][17]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][17]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][17]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][18]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][18]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][18]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][19]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][19]
            keyboard = types.InlineKeyboardMarkup()
            with open(c+"masters.json", encoding="utf8") as file:
                masters = json.load(file)
                for node in masters:
                    if node["Id"] == dicti["admin"]["printAdmin"][19]:
                        # for i in range(len(node["Date"])):
                            if len(node["Date"]) >= 1:
                                key1 = types.InlineKeyboardButton(text=node["Date"][0], callback_data="AdminDateDate"+str(node["Date"][0]))
                                keyboard.add(key1)
                                dicti["admin"]["Datas"].append(str(node["Date"][0]))
                                if len(node["Date"]) >= 2:
                                    key2 = types.InlineKeyboardButton(text=node["Date"][1], callback_data="AdminDateDate"+str(node["Date"][1]))
                                    keyboard.add(key2)
                                    dicti["admin"]["Datas"].append(str(node["Date"][1]))
                                    if len(node["Date"]) >= 3:
                                        key3 = types.InlineKeyboardButton(text=node["Date"][2], callback_data="AdminDateDate"+str(node["Date"][2]))
                                        keyboard.add(key3)
                                        dicti["admin"]["Datas"].append(str(node["Date"][2]))
                                        if len(node["Date"]) >= 4:
                                            key4 = types.InlineKeyboardButton(text=node["Date"][3], callback_data="AdminDateDate"+str(node["Date"][3]))
                                            keyboard.add(key4)
                                            dicti["admin"]["Datas"].append(str(node["Date"][3]))
                                            if len(node["Date"]) >= 5:
                                                key5 = types.InlineKeyboardButton(text=node["Date"][4], callback_data="AdminDateDate"+str(node["Date"][4]))
                                                keyboard.add(key5)
                                                dicti["admin"]["Datas"].append(str(node["Date"][4]))
                                                if len(node["Date"]) >= 6:
                                                    key6 = types.InlineKeyboardButton(text=node["Date"][5], callback_data="AdminDateDate"+str(node["Date"][5]))
                                                    keyboard.add(key6)
                                                    dicti["admin"]["Datas"].append(str(node["Date"][5]))
                                                    if len(node["Date"]) >= 7:
                                                        key7 = types.InlineKeyboardButton(text=node["Date"][6], callback_data="AdminDateDate"+str(node["Date"][6]))
                                                        keyboard.add(key7)
                                                        dicti["admin"]["Datas"].append(str(node["Date"][6]))
                                                        if len(node["Date"]) >= 8:
                                                            key8 = types.InlineKeyboardButton(text=node["Date"][7], callback_data="AdminDateDate"+str(node["Date"][7]))
                                                            keyboard.add(key8)
                                                            dicti["admin"]["Datas"].append(str(node["Date"][7]))
                                                            if len(node["Date"]) >= 9:
                                                                key9 = types.InlineKeyboardButton(text=node["Date"][8], callback_data="AdminDateDate"+str(node["Date"][8]))
                                                                keyboard.add(key9)
                                                                dicti["admin"]["Datas"].append(str(node["Date"][8]))
                                                                if len(node["Date"]) >= 10:
                                                                    key10 = types.InlineKeyboardButton(text=node["Date"][9], callback_data="AdminDateDate"+str(node["Date"][9]))
                                                                    keyboard.add(key10)
                                                                    dicti["admin"]["Datas"].append(str(node["Date"][9]))
                                                                    if len(node["Date"]) >= 11:
                                                                        key11 = types.InlineKeyboardButton(text=node["Date"][10], callback_data="AdminDateDate"+str(node["Date"][10]))
                                                                        keyboard.add(key11)
                                                                        dicti["admin"]["Datas"].append(str(node["Date"][10]))
            
            file.close()
            bot.send_message(call.from_user.id, text=node["Date"], reply_markup=keyboard)
            dicti["admin"]["DelData"] = False
            dicti["admin"]["DataSel"] = True

    elif dicti["admin"]["AddData"] == True:
        if call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][0]):
            # print("OKOK")
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][0]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][1]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][1]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][2]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][2]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][3]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][3]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][4]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][4]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][5]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][5]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][6]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][6]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][7]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][7]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][8]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][8]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][9]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][9]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][10]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][10]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][11]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][11]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][12]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][12]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][13]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][13]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][14]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][14]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][15]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][15]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][16]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][16]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][17]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][17]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][18]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][18]
            dicti["admin"]["AddData"] = False
            Cal(call)
        elif call.data == "AdminMasterId"+str(dicti["admin"]["printAdmin"][19]):
            dicti["admin"]["DataSelect"] = dicti["admin"]["printAdmin"][19]
            dicti["admin"]["AddData"] = False
            Cal(call)
        
    elif dicti["admin"]["DataSel"] == True:
        if call.data == "AdminDateDate"+str(dicti["admin"]["Datas"][0]):
            with open(c+"masters.json", encoding="utf8") as file1:
                masters1 = json.load(file1)
                for node1 in masters1:
                    if node1["Id"] == dicti["admin"]["DataSelect"]:
                        node1["Date"].remove(dicti["admin"]["Datas"][0])
            dicti["admin"]["DeteSel"] = False
            file1.close()
            with open(c+"masters.json", "w", encoding="utf8") as file1:
                json.dump(masters1, file1, ensure_ascii=False)
            file1.close()
            dicti["admin"]["DataSel"] = False
            bot.send_message(call.from_user.id, text="Удалено")
        elif call.data == "AdminDateDate"+str(dicti["admin"]["Datas"][1]):
            with open(c+"masters.json", encoding="utf8") as file1:
                masters1 = json.load(file1)
                for node1 in masters1:
                    if node1["Id"] == dicti["admin"]["DataSelect"]:
                        node1["Date"].remove(dicti["admin"]["Datas"][1])
            dicti["admin"]["DeteSel"] = False
            file1.close()
            with open(c+"masters.json", "w", encoding="utf8") as file1:
                json.dump(masters1, file1, ensure_ascii=False)
            file1.close()
            dicti["admin"]["DataSel"] = False
            bot.send_message(call.from_user.id, text="Удалено")
        elif call.data == "AdminDateDate"+str(dicti["admin"]["Datas"][2]):
            with open(c+"masters.json", encoding="utf8") as file1:
                masters1 = json.load(file1)
                for node1 in masters1:
                    if node1["Id"] == dicti["admin"]["DataSelect"]:
                        node1["Date"].remove(dicti["admin"]["Datas"][2])
            dicti["admin"]["DeteSel"] = False
            file1.close()
            with open(c+"masters.json", "w", encoding="utf8") as file1:
                json.dump(masters1, file1, ensure_ascii=False)
            file1.close()
            dicti["admin"]["DataSel"] = False
            bot.send_message(call.from_user.id, text="Удалено")
        elif call.data == "AdminDateDate"+str(dicti["admin"]["Datas"][3]):
            with open(c+"masters.json", encoding="utf8") as file1:
                masters1 = json.load(file1)
                for node1 in masters1:
                    if node1["Id"] == dicti["admin"]["DataSelect"]:
                        node1["Date"].remove(dicti["admin"]["Datas"][3])
            dicti["admin"]["DeteSel"] = False
            file1.close()
            with open(c+"masters.json", "w", encoding="utf8") as file1:
                json.dump(masters1, file1, ensure_ascii=False)
            file1.close()
            dicti["admin"]["DataSel"] = False
            bot.send_message(call.from_user.id, text="Удалено")
        elif call.data == "AdminDateDate"+str(dicti["admin"]["Datas"][4]):
            with open(c+"masters.json", encoding="utf8") as file1:
                masters1 = json.load(file1)
                for node1 in masters1:
                    if node1["Id"] == dicti["admin"]["DataSelect"]:
                        node1["Date"].remove(dicti["admin"]["Datas"][4])
            dicti["admin"]["DeteSel"] = False
            file1.close()
            with open(c+"masters.json", "w", encoding="utf8") as file1:
                json.dump(masters1, file1, ensure_ascii=False)
            file1.close()
            dicti["admin"]["DataSel"] = False
            bot.send_message(call.from_user.id, text="Удалено")
        elif call.data == "AdminDateDate"+str(dicti["admin"]["Datas"][5]):
            with open(c+"masters.json", encoding="utf8") as file1:
                masters1 = json.load(file1)
                for node1 in masters1:
                    if node1["Id"] == dicti["admin"]["DataSelect"]:
                        node1["Date"].remove(dicti["admin"]["Datas"][5])
            dicti["admin"]["DeteSel"] = False
            file1.close()
            with open(c+"masters.json", "w", encoding="utf8") as file1:
                json.dump(masters1, file1, ensure_ascii=False)
            file1.close()
            dicti["admin"]["DataSel"] = False
            bot.send_message(call.from_user.id, text="Удалено")
        elif call.data == "AdminDateDate"+str(dicti["admin"]["Datas"][6]):
            with open(c+"masters.json", encoding="utf8") as file1:
                masters1 = json.load(file1)
                for node1 in masters1:
                    if node1["Id"] == dicti["admin"]["DataSelect"]:
                        node1["Date"].remove(dicti["admin"]["Datas"][6])
            dicti["admin"]["DeteSel"] = False
            file1.close()
            with open(c+"masters.json", "w", encoding="utf8") as file1:
                json.dump(masters1, file1, ensure_ascii=False)
            file1.close()
            dicti["admin"]["DataSel"] = False
            bot.send_message(call.from_user.id, text="Удалено")
        elif call.data == "AdminDateDate"+str(dicti["admin"]["Datas"][7]):
            with open(c+"masters.json", encoding="utf8") as file1:
                masters1 = json.load(file1)
                for node1 in masters1:
                    if node1["Id"] == dicti["admin"]["DataSelect"]:
                        node1["Date"].remove(dicti["admin"]["Datas"][7])
            dicti["admin"]["DeteSel"] = False
            file1.close()
            with open(c+"masters.json", "w", encoding="utf8") as file1:
                json.dump(masters1, file1, ensure_ascii=False)
            file1.close()
            dicti["admin"]["DataSel"] = False
            bot.send_message(call.from_user.id, text="Удалено")
        elif call.data == "AdminDateDate"+str(dicti["admin"]["Datas"][8]):
            with open(c+"masters.json", encoding="utf8") as file1:
                masters1 = json.load(file1)
                for node1 in masters1:
                    if node1["Id"] == dicti["admin"]["DataSelect"]:
                        node1["Date"].remove(dicti["admin"]["Datas"][8])
            dicti["admin"]["DeteSel"] = False
            file1.close()
            with open(c+"masters.json", "w", encoding="utf8") as file1:
                json.dump(masters1, file1, ensure_ascii=False)
            file1.close()
            dicti["admin"]["DataSel"] = False
            bot.send_message(call.from_user.id, text="Удалено")
        elif call.data == "AdminDateDate"+str(dicti["admin"]["Datas"][9]):
            with open(c+"masters.json", encoding="utf8") as file1:
                masters1 = json.load(file1)
                for node1 in masters1:
                    if node1["Id"] == dicti["admin"]["DataSelect"]:
                        node1["Date"].remove(dicti["admin"]["Datas"][9])
            dicti["admin"]["DeteSel"] = False
            file1.close()
            with open(c+"masters.json", "w", encoding="utf8") as file1:
                json.dump(masters1, file1, ensure_ascii=False)
            file1.close()
            dicti["admin"]["DataSel"] = False
            bot.send_message(call.from_user.id, text="Удалено")
        elif call.data == "AdminDateDate"+str(dicti["admin"]["Datas"][10]):
            with open(c+"masters.json", encoding="utf8") as file1:
                masters1 = json.load(file1)
                for node1 in masters1:
                    if node1["Id"] == dicti["admin"]["DataSelect"]:
                        node1["Date"].remove(dicti["admin"]["Datas"][10])
            dicti["admin"]["DeteSel"] = False
            file1.close()
            with open(c+"masters.json", "w", encoding="utf8") as file1:
                json.dump(masters1, file1, ensure_ascii=False)
            file1.close()
            dicti["admin"]["DataSel"] = False
            bot.send_message(call.from_user.id, text="Удалено")

    elif dicti["admin"]["MinStrMast"] == True:
        if call.data == "AdminMinStrId"+str(dicti["admin"]["id"][0]):
            with open(c + 'masters.json', encoding='utf8') as file:
                mastersA = json.load(file)
            file.close()
            for i in mastersA:
                if i["Id"] == dicti["admin"]["id"][0]:
                    del mastersA[dicti["admin"]["id"].index(dicti["admin"]["id"][0])]
            with open(c + 'masters.json', "w", encoding="utf8") as file:
                json.dump(mastersA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStrMastMast"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][1]):
            with open(c + 'masters.json', encoding='utf8') as file:
                mastersA = json.load(file)
            file.close()
            for i in mastersA:
                if i["Id"] == dicti["admin"]["id"][1]:
                    del mastersA[dicti["admin"]["id"].index(dicti["admin"]["id"][1])]
            with open(c + 'masters.json', "w", encoding="utf8") as file:
                json.dump(mastersA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStrMast"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][2]):
            with open(c + 'masters.json', encoding='utf8') as file:
                mastersA = json.load(file)
            file.close()
            for i in mastersA:
                if i["Id"] == dicti["admin"]["id"][2]:
                    del mastersA[dicti["admin"]["id"].index(dicti["admin"]["id"][2])]
            with open(c + 'masters.json', "w", encoding="utf8") as file:
                json.dump(mastersA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStrMast"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][3]):
            with open(c + 'masters.json', encoding='utf8') as file:
                mastersA = json.load(file)
            file.close()
            for i in mastersA:
                if i["Id"] == dicti["admin"]["id"][3]:
                    del mastersA[dicti["admin"]["id"].index(dicti["admin"]["id"][3])]
            with open(c + 'masters.json', "w", encoding="utf8") as file:
                json.dump(mastersA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStrMast"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][4]):
            with open(c + 'masters.json', encoding='utf8') as file:
                mastersA = json.load(file)
            file.close()
            for i in mastersA:
                if i["Id"] == dicti["admin"]["id"][4]:
                    del mastersA[dicti["admin"]["id"].index(dicti["admin"]["id"][4])]
            with open(c + 'masters.json', "w", encoding="utf8") as file:
                json.dump(mastersA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStrMast"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][5]):
            with open(c + 'masters.json', encoding='utf8') as file:
                mastersA = json.load(file)
            file.close()
            for i in mastersA:
                if i["Id"] == dicti["admin"]["id"][5]:
                    del mastersA[dicti["admin"]["id"].index(dicti["admin"]["id"][5])]
            with open(c + 'masters.json', "w", encoding="utf8") as file:
                json.dump(mastersA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStrMast"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][6]):
            with open(c + 'masters.json', encoding='utf8') as file:
                mastersA = json.load(file)
            file.close()
            for i in mastersA:
                if i["Id"] == dicti["admin"]["id"][6]:
                    del mastersA[dicti["admin"]["id"].index(dicti["admin"]["id"][6])]
            with open(c + 'masters.json', "w", encoding="utf8") as file:
                json.dump(mastersA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStrMast"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][7]):
            with open(c + 'masters.json', encoding='utf8') as file:
                mastersA = json.load(file)
            file.close()
            for i in mastersA:
                if i["Id"] == dicti["admin"]["id"][7]:
                    del mastersA[dicti["admin"]["id"].index(dicti["admin"]["id"][7])]
            with open(c + 'masters.json', "w", encoding="utf8") as file:
                json.dump(mastersA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStrMast"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][8]):
            with open(c + 'masters.json', encoding='utf8') as file:
                mastersA = json.load(file)
            file.close()
            for i in mastersA:
                if i["Id"] == dicti["admin"]["id"][8]:
                    del mastersA[dicti["admin"]["id"].index(dicti["admin"]["id"][8])]
            with open(c + 'masters.json', "w", encoding="utf8") as file:
                json.dump(mastersA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStrMast"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][9]):
            with open(c + 'masters.json', encoding='utf8') as file:
                mastersA = json.load(file)
            file.close()
            for i in mastersA:
                if i["Id"] == dicti["admin"]["id"][9]:
                    del mastersA[dicti["admin"]["id"].index(dicti["admin"]["id"][9])]
            with open(c + 'masters.json', "w", encoding="utf8") as file:
                json.dump(mastersA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStrMast"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][10]):
            with open(c + 'masters.json', encoding='utf8') as file:
                mastersA = json.load(file)
            file.close()
            for i in mastersA:
                if i["Id"] == dicti["admin"]["id"][10]:
                    del mastersA[dicti["admin"]["id"].index(dicti["admin"]["id"][10])]
            with open(c + 'masters.json', "w", encoding="utf8") as file:
                json.dump(mastersA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStrMast"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")

    elif dicti["admin"]["MinStr"] == True:
        if call.data == "AdminMinStrId"+str(dicti["admin"]["id"][0]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][0]:
                    del modelsA[dicti["admin"]["id"].index(dicti["admin"]["id"][0])]
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStr"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][1]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][1]:
                    del modelsA[dicti["admin"]["id"].index(dicti["admin"]["id"][1])]
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStr"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][2]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][2]:
                    del modelsA[dicti["admin"]["id"].index(dicti["admin"]["id"][2])]
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStr"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][3]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][3]:
                    del modelsA[dicti["admin"]["id"].index(dicti["admin"]["id"][3])]
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStr"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][4]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][4]:
                    del modelsA[dicti["admin"]["id"].index(dicti["admin"]["id"][4])]
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStr"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][5]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][5]:
                    del modelsA[dicti["admin"]["id"].index(dicti["admin"]["id"][5])]
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStr"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][6]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][6]:
                    del modelsA[dicti["admin"]["id"].index(dicti["admin"]["id"][6])]
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStr"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][7]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][7]:
                    del modelsA[dicti["admin"]["id"].index(dicti["admin"]["id"][7])]
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStr"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][8]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][8]:
                    del modelsA[dicti["admin"]["id"].index(dicti["admin"]["id"][8])]
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStr"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][9]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][9]:
                    del modelsA[dicti["admin"]["id"].index(dicti["admin"]["id"][9])]
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStr"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
        elif call.data == "AdminMinStrId"+str(dicti["admin"]["id"][10]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][10]:
                    del modelsA[dicti["admin"]["id"].index(dicti["admin"]["id"][10])]
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["MinStr"] = False
            bot.send_message(call.from_user.id, text="Строка удалена")
            
    elif dicti["admin"]["AddModels"] == True:
        if call.data == "AdminPlus"+str(dicti["admin"]["id"][0]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][0]:
                    i["Limit"] += 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["AddModels"] = False
            bot.send_message(call.from_user.id, text="Лимит добавлен")
        elif call.data == "AdminPlus"+str(dicti["admin"]["id"][1]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][1]:
                    i["Limit"] += 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["AddModels"] = False
            bot.send_message(call.from_user.id, text="Лимит добавлен")
        elif call.data == "AdminPlus"+str(dicti["admin"]["id"][2]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][2]:
                    i["Limit"] += 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["AddModels"] = False
            bot.send_message(call.from_user.id, text="Лимит добавлен")
        elif call.data == "AdminPlus"+str(dicti["admin"]["id"][3]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][3]:
                    i["Limit"] += 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["AddModels"] = False
            bot.send_message(call.from_user.id, text="Лимит добавлен")
        elif call.data == "AdminPlus"+str(dicti["admin"]["id"][4]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][4]:
                    i["Limit"] += 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["AddModels"] = False
            bot.send_message(call.from_user.id, text="Лимит добавлен")
        elif call.data == "AdminPlus"+str(dicti["admin"]["id"][5]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][5]:
                    i["Limit"] += 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["AddModels"] = False
            bot.send_message(call.from_user.id, text="Лимит добавлен")
        elif call.data == "AdminPlus"+str(dicti["admin"]["id"][6]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][6]:
                    i["Limit"] += 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["AddModels"] = False
            bot.send_message(call.from_user.id, text="Лимит добавлен")
        elif call.data == "AdminPlus"+str(dicti["admin"]["id"][7]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][7]:
                    i["Limit"] += 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["AddModels"] = False
            bot.send_message(call.from_user.id, text="Лимит добавлен")
        elif call.data == "AdminPlus"+str(dicti["admin"]["id"][8]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][8]:
                    i["Limit"] += 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["AddModels"] = False
            bot.send_message(call.from_user.id, text="Лимит добавлен")
        elif call.data == "AdminPlus"+str(dicti["admin"]["id"][9]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][9]:
                    i["Limit"] += 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["AddModels"] = False
            bot.send_message(call.from_user.id, text="Лимит добавлен")
        elif call.data == "AdminPlus"+str(dicti["admin"]["id"][10]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][10]:
                    i["Limit"] += 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["AddModels"] = False
            bot.send_message(call.from_user.id, text="Лимит добавлен")
    
    elif dicti["admin"]["DelModels"] == True:
        if call.data == "AdminMinus"+str(dicti["admin"]["id"][0]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][0]:
                    i["Limit"] -= 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["DelModels"] = False
            bot.send_message(call.from_user.id, text="Лимит уменьшен")
        elif call.data == "AdminMinus"+str(dicti["admin"]["id"][1]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][1]:
                    i["Limit"] -= 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["DelModels"] = False
            bot.send_message(call.from_user.id, text="Лимит уменьшен")
        elif call.data == "AdminMinus"+str(dicti["admin"]["id"][2]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][2]:
                    i["Limit"] -= 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["DelModels"] = False
            bot.send_message(call.from_user.id, text="Лимит уменьшен")
        elif call.data == "AdminMinus"+str(dicti["admin"]["id"][3]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][3]:
                    i["Limit"] -= 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["DelModels"] = False
            bot.send_message(call.from_user.id, text="Лимит уменьшен")
        elif call.data == "AdminMinus"+str(dicti["admin"]["id"][4]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][4]:
                    i["Limit"] -= 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["DelModels"] = False
            bot.send_message(call.from_user.id, text="Лимит уменьшен")
        elif call.data == "AdminMinus"+str(dicti["admin"]["id"][5]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][5]:
                    i["Limit"] -= 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["DelModels"] = False
            bot.send_message(call.from_user.id, text="Лимит уменьшен")
        elif call.data == "AdminMinus"+str(dicti["admin"]["id"][6]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][6]:
                    i["Limit"] -= 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["DelModels"] = False
            bot.send_message(call.from_user.id, text="Лимит уменьшен")
        elif call.data == "AdminMinus"+str(dicti["admin"]["id"][7]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][7]:
                    i["Limit"] -= 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["DelModels"] = False
            bot.send_message(call.from_user.id, text="Лимит уменьшен")
        elif call.data == "AdminMinus"+str(dicti["admin"]["id"][8]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][8]:
                    i["Limit"] -= 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["DelModels"] = False
            bot.send_message(call.from_user.id, text="Лимит уменьшен")
        elif call.data == "AdminMinus"+str(dicti["admin"]["id"][9]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][9]:
                    i["Limit"] -= 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["DelModels"] = False
            bot.send_message(call.from_user.id, text="Лимит уменьшен")
        elif call.data == "AdminMinus"+str(dicti["admin"]["id"][10]):
            with open(c + 'models.json', encoding='utf8') as file:
                modelsA = json.load(file)
            file.close()
            for i in modelsA:
                if i["Id"] == dicti["admin"]["id"][10]:
                    i["Limit"] -= 1
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(modelsA, file, ensure_ascii=False)
            file.close()
            dicti["admin"]["DelModels"] = False
            bot.send_message(call.from_user.id, text="Лимит уменьшен")


    elif call.data == "MakeAnAppointment":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        Appointment(call)
    elif call.data == "HowToGetThere":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        # GetThere(call)
    
    elif call.data == "Color":
        if dicti[call.from_user.id]["what"][0] == False:
            dicti[call.from_user.id]["what"][0] = True
            color = bot.send_message(call.from_user.id, text=config["Buttons"]["Color"])
            color
            dicti[call.from_user.id]["bot.last_message_sent1"] = color.chat.id, color.message_id
        else:
            dicti[call.from_user.id]["what"][0] = False
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent1"])
    elif call.data == "Cut":
        if dicti[call.from_user.id]["what"][1] == False:
            dicti[call.from_user.id]["what"][1] = True
            cut = bot.send_message(call.from_user.id, text=config["Buttons"]["Cut"])
            cut
            dicti[call.from_user.id]["bot.last_message_sent2"] = cut.chat.id, cut.message_id
        else:
            dicti[call.from_user.id]["what"][1] = False
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent2"])
    elif call.data == "Hug":
        if dicti[call.from_user.id]["what"][2] == False:
            dicti[call.from_user.id]["what"][2] = True
            hug = bot.send_message(call.from_user.id, text=config["Buttons"]["Hug"])
            hug
            dicti[call.from_user.id]["bot.last_message_sent3"] = hug.chat.id, hug.message_id
        else:
            dicti[call.from_user.id]["what"][2] = False
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent3"])
    elif call.data == "Model":
        if dicti[call.from_user.id]["what"][3] == False:
            dicti[call.from_user.id]["what"][3] = True
            model = bot.send_message(call.from_user.id, text=config["Buttons"]["Model"])
            model
            dicti[call.from_user.id]["bot.last_message_sent4"] = model.chat.id, model.message_id
        else:
            dicti[call.from_user.id]["what"][3] = False
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent4"])
    elif call.data == "NextWhat":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        if dicti[call.from_user.id]["what"][0] == True:
            try:
                bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent1"])
            except:
                pass
        if dicti[call.from_user.id]["what"][1] == True:
            try:
                bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent2"])
            except:
                pass
        if dicti[call.from_user.id]["what"][2] == True:
            try:
                bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent3"])
            except:
                pass
        if dicti[call.from_user.id]["what"][3] == True:
            try:
                bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent4"])
            except:
                pass
        if dicti[call.from_user.id]["what"][3] == True:
            Model(call)
        elif dicti[call.from_user.id]["what"][0] == True or dicti[call.from_user.id]["what"][1] == True or dicti[call.from_user.id]["what"][2] == True:
            Klient(call)
        else:
            bot.send_message(call.from_user.id, text=config["Pfrazes"]["Nothing"])
            path = os.path.join(c+"Photos/"+str(dicti[call.from_user.id]["id"]))
            shutil.rmtree(path)
        
    
    elif call.data == "Yes":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        Story(call)
        dicti[call.from_user.id]["story"] = True
    elif call.data == "No":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        Story(call)
        dicti[call.from_user.id]["story"] = True
        
    elif call.data == "NextStory":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["story"] = False
        Checkcut(call)
    elif call.data == "NextRes":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["result"] = False
        Fork(call)
        
    elif call.data == "Short":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["long"] = config["Buttons"]["Short"]
        Photo(call)
    elif call.data == "Head":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["long"] = config["Buttons"]["Head"]
        Photo(call)
    elif call.data == "Back":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["long"] = config["Buttons"]["Back"]
        Photo(call)
    elif call.data == "Long":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["long"] = config["Buttons"]["Long"]
        Photo(call)
        
    elif call.data == "EndOk":
        try:
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        except:
            pass
    
    elif call.data == "PhotoOk":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["storyPhoto"] = False
        if dicti[call.from_user.id]["what"][2] == True and dicti[call.from_user.id]["what"][1] == False:
            Fork(call)
        else:
            Result(call)
            dicti[call.from_user.id]["result"] = True
        
    elif call.data == "ClearPhoto":
        path = os.path.join(c+"Photos")
        shutil.rmtree(path)
        os.mkdir(c+"Photos")
        bot.send_message(call.from_user.id, text=config["AdmText"]["Ok"])
    
    elif call.data == "1":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])        
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                if node["Id"] == dicti[call.from_user.id]["textModelsId"][0]:
                    dicti[call.from_user.id]["textModelsEnd"] == node["Id"]
                    dicti[call.from_user.id]["textModelsIdSelect"] = node["Id"]
        file.close()
        if dicti[call.from_user.id]["what"][0] == False and dicti[call.from_user.id]["what"][1] == False and dicti[call.from_user.id]["what"][2] == False:
            Fork(call)
        else:
            Klient(call)
    elif call.data == "2":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])        
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                if node["Id"] == dicti[call.from_user.id]["textModelsId"][1]:
                    dicti[call.from_user.id]["textModelsEnd"] == node["Id"]
                    dicti[call.from_user.id]["textModelsIdSelect"] = node["Id"]
        file.close()
        if dicti[call.from_user.id]["what"][0] == False and dicti[call.from_user.id]["what"][1] == False and dicti[call.from_user.id]["what"][2] == False:
            Fork(call)
        else:
            Klient(call)
    elif call.data == "3":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])        
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                if node["Id"] == dicti[call.from_user.id]["textModelsId"][2]:
                    dicti[call.from_user.id]["textModelsEnd"] == node["Id"]
                    dicti[call.from_user.id]["textModelsIdSelect"] = node["Id"]
        file.close()
        if dicti[call.from_user.id]["what"][0] == False and dicti[call.from_user.id]["what"][1] == False and dicti[call.from_user.id]["what"][2] == False:
            Fork(call)
        else:
            Klient(call)
    elif call.data == "4":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])        
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                if node["Id"] == dicti[call.from_user.id]["textModelsId"][3]:
                    dicti[call.from_user.id]["textModelsEnd"] == node["Id"]
                    dicti[call.from_user.id]["textModelsIdSelect"] = node["Id"]
        file.close()
        if dicti[call.from_user.id]["what"][0] == False and dicti[call.from_user.id]["what"][1] == False and dicti[call.from_user.id]["what"][2] == False:
            Fork(call)
        else:
            Klient(call)
    elif call.data == "5":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])        
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                if node["Id"] == dicti[call.from_user.id]["textModelsId"][4]:
                    dicti[call.from_user.id]["textModelsEnd"] == node["Id"]
                    dicti[call.from_user.id]["textModelsIdSelect"] = node["Id"]
        file.close()
        if dicti[call.from_user.id]["what"][0] == False and dicti[call.from_user.id]["what"][1] == False and dicti[call.from_user.id]["what"][2] == False:
            Fork(call)
        else:
            Klient(call)
    elif call.data == "6":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])        
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                if node["Id"] == dicti[call.from_user.id]["textModelsId"][5]:
                    dicti[call.from_user.id]["textModelsEnd"] == node["Id"]
                    dicti[call.from_user.id]["textModelsIdSelect"] = node["Id"]
        file.close()
        if dicti[call.from_user.id]["what"][0] == False and dicti[call.from_user.id]["what"][1] == False and dicti[call.from_user.id]["what"][2] == False:
            Fork(call)
        else:
            Klient(call)
    elif call.data == "7":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])        
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                if node["Id"] == dicti[call.from_user.id]["textModelsId"][6]:
                    dicti[call.from_user.id]["textModelsEnd"] == node["Id"]
                    dicti[call.from_user.id]["textModelsIdSelect"] = node["Id"]
        file.close()
        if dicti[call.from_user.id]["what"][0] == False and dicti[call.from_user.id]["what"][1] == False and dicti[call.from_user.id]["what"][2] == False:
            Fork(call)
        else:
            Klient(call)
    elif call.data == "8":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])        
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                if node["Id"] == dicti[call.from_user.id]["textModelsId"][7]:
                    dicti[call.from_user.id]["textModelsEnd"] == node["Id"]
                    dicti[call.from_user.id]["textModelsIdSelect"] = node["Id"]
        file.close()
        if dicti[call.from_user.id]["what"][0] == False and dicti[call.from_user.id]["what"][1] == False and dicti[call.from_user.id]["what"][2] == False:
            Fork(call)
        else:
            Klient(call)
    elif call.data == "9":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])        
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                if node["Id"] == dicti[call.from_user.id]["textModelsId"][8]:
                    dicti[call.from_user.id]["textModelsEnd"] == node["Id"]
                    dicti[call.from_user.id]["textModelsIdSelect"] = node["Id"]
        file.close()
        if dicti[call.from_user.id]["what"][0] == False and dicti[call.from_user.id]["what"][1] == False and dicti[call.from_user.id]["what"][2] == False:
            Fork(call)
        else:
            Klient(call)
    elif call.data == "10":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])        
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                if node["Id"] == dicti[call.from_user.id]["textModelsId"][9]:
                    dicti[call.from_user.id]["textModelsEnd"] == node["Id"]
                    dicti[call.from_user.id]["textModelsIdSelect"] = node["Id"]
        file.close()
        if dicti[call.from_user.id]["what"][0] == False and dicti[call.from_user.id]["what"][1] == False and dicti[call.from_user.id]["what"][2] == False:
            Fork(call)
        else:
            Klient(call)
    elif call.data == "11":
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        with open(c + 'models.json', encoding='utf8') as file:
            models = json.load(file)
            for node in models:
                if node["Id"] == dicti[call.from_user.id]["textModelsId"][10]:
                    dicti[call.from_user.id]["textModelsEnd"] == node["Id"]
                    dicti[call.from_user.id]["textModelsIdSelect"] = node["Id"]
        file.close()
        if dicti[call.from_user.id]["what"][0] == False and dicti[call.from_user.id]["what"][1] == False and dicti[call.from_user.id]["what"][2] == False:
            Fork(call)
        else:
            Klient(call)
    elif dicti[call.from_user.id]["DatesOn"] == True:        
        if call.data == dicti[call.from_user.id]["Dates"][0]:
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
            dicti[call.from_user.id]["Date"] = dicti[call.from_user.id]["Dates"][0]
            DateIn(call)
            dicti[call.from_user.id]["DatesOn"] = False
        elif call.data == dicti[call.from_user.id]["Dates"][1]:
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
            dicti[call.from_user.id]["Date"] = dicti[call.from_user.id]["Dates"][1]
            DateIn(call)
            dicti[call.from_user.id]["DatesOn"] = False
        elif call.data == dicti[call.from_user.id]["Dates"][2]:
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
            dicti[call.from_user.id]["Date"] = dicti[call.from_user.id]["Dates"][2]
            DateIn(call)
            dicti[call.from_user.id]["DatesOn"] = False
        elif call.data == dicti[call.from_user.id]["Dates"][3]:
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
            dicti[call.from_user.id]["Date"] = dicti[call.from_user.id]["Dates"][3]
            DateIn(call)
            dicti[call.from_user.id]["DatesOn"] = False
        elif call.data == dicti[call.from_user.id]["Dates"][4]:
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
            dicti[call.from_user.id]["Date"] = dicti[call.from_user.id]["Dates"][4]
            DateIn(call)
            dicti[call.from_user.id]["DatesOn"] = False
        elif call.data == dicti[call.from_user.id]["Dates"][5]:
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
            dicti[call.from_user.id]["Date"] = dicti[call.from_user.id]["Dates"][5]
            DateIn(call)
            dicti[call.from_user.id]["DatesOn"] = False
        elif call.data == dicti[call.from_user.id]["Dates"][6]:
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
            dicti[call.from_user.id]["Date"] = dicti[call.from_user.id]["Dates"][6]
            DateIn(call)
            dicti[call.from_user.id]["DatesOn"] = False
        elif call.data == dicti[call.from_user.id]["Dates"][7]:
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
            dicti[call.from_user.id]["Date"] = dicti[call.from_user.id]["Dates"][7]
            DateIn(call)
            dicti[call.from_user.id]["DatesOn"] = False
        elif call.data == dicti[call.from_user.id]["Dates"][8]:
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
            dicti[call.from_user.id]["Date"] = dicti[call.from_user.id]["Dates"][8]
            DateIn(call)
            dicti[call.from_user.id]["DatesOn"] = False
        elif call.data == dicti[call.from_user.id]["Dates"][9]:
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
            dicti[call.from_user.id]["Date"] = dicti[call.from_user.id]["Dates"][9]
            DateIn(call)
            dicti[call.from_user.id]["DatesOn"] = False
        elif call.data == dicti[call.from_user.id]["Dates"][10]:
            bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
            dicti[call.from_user.id]["Date"] = dicti[call.from_user.id]["Dates"][10]
            DateIn(call)
            dicti[call.from_user.id]["DatesOn"] = False


    elif call.data == dicti[call.from_user.id]["Masters"][0]:
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["Master"] = dicti[call.from_user.id]["Masters"][0]
        ChooseMast(call)
    elif call.data == dicti[call.from_user.id]["Masters"][1]:
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["Master"] = dicti[call.from_user.id]["Masters"][1]
        ChooseMast(call)
    elif call.data == dicti[call.from_user.id]["Masters"][2]:
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["Master"] = dicti[call.from_user.id]["Masters"][2]
        ChooseMast(call)
    elif call.data == dicti[call.from_user.id]["Masters"][3]:
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["Master"] = dicti[call.from_user.id]["Masters"][3]
        ChooseMast(call)
    elif call.data == dicti[call.from_user.id]["Masters"][4]:
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["Master"] = dicti[call.from_user.id]["Masters"][4]
        ChooseMast(call)
    elif call.data == dicti[call.from_user.id]["Masters"][5]:
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["Master"] = dicti[call.from_user.id]["Masters"][5]
        ChooseMast(call)
    elif call.data == dicti[call.from_user.id]["Masters"][6]:
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["Master"] = dicti[call.from_user.id]["Masters"][6]
        ChooseMast(call)
    elif call.data == dicti[call.from_user.id]["Masters"][7]:
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["Master"] = dicti[call.from_user.id]["Masters"][7]
        ChooseMast(call)
    elif call.data == dicti[call.from_user.id]["Masters"][8]:
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["Master"] = dicti[call.from_user.id]["Masters"][8]
        ChooseMast(call)
    elif call.data == dicti[call.from_user.id]["Masters"][9]:
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["Master"] = dicti[call.from_user.id]["Masters"][9]
        ChooseMast(call)
    elif call.data == dicti[call.from_user.id]["Masters"][10]:
        bot.delete_message(*dicti[call.from_user.id]["bot.last_message_sent"])
        dicti[call.from_user.id]["Master"] = dicti[call.from_user.id]["Masters"][10]
        ChooseMast(call)

# Добавление строк в мастера и модели
@bot.message_handler(content_types=["document"])
def Files(message):
    chat_id = message.chat.id
    file_info = bot.get_file(message.document.file_id)
    
    downloaded_file = bot.download_file(file_info.file_path)
    a = json.loads(downloaded_file)
    # # print(a[0])
    for node in a[0]:
        if "About" in node:
            # # print("master")
            
            with open(c + 'masters.json','r+', encoding="UTF-8") as file:
                file_data = json.load(file)
                file_data.append(a[0])
            file.close()
            
            with open(c + 'masters.json', "w", encoding="utf8") as file:
                json.dump(file_data, file, ensure_ascii=False)
            file.close()
            
            
        elif "Color" in node:
            # # print("model")
            
            with open(c + 'models.json','r+', encoding="UTF-8") as file:
                file_data = json.load(file)
                file_data.append(a[0])
            file.close()
            
            with open(c + 'models.json', "w", encoding="utf8") as file:
                json.dump(file_data, file, ensure_ascii=False)
            file.close()
        
        else:
            pass

    bot.reply_to(message, "Пожалуй, я сохраню это")

@bot.message_handler(content_types=['photo'])
def get_photo(message: types.Message):
    if dicti[message.chat.id]["result"] == True:
        if dicti[message.chat.id]["counterRes"] < 4:
            fileID = message.photo[-1].file_id   
            file_info = bot.get_file(fileID)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(c+"Photos/"+str(dicti[message.chat.id]["id"])+"/Want/"+str(dicti[message.chat.id]["counterRes"])+".jpg", 'wb') as new_file:
                new_file.write(downloaded_file)
            dicti[message.chat.id]["counterRes"]+=1
    elif dicti[message.chat.id]["storyPhoto"] == True:
        if dicti[message.chat.id]["counterWas"] < 4:
            fileID = message.photo[-1].file_id   
            file_info = bot.get_file(fileID)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(c+"Photos/"+str(dicti[message.chat.id]["id"])+"/Was/"+str(dicti[message.chat.id]["counterWas"])+".jpg", 'wb') as new_file:
                new_file.write(downloaded_file)
            dicti[message.chat.id]["counterWas"]+=1
    # else:
        # print("photo")
            

if __name__=='__main__':
    # bot.polling(non_stop=True, interval=0)

    while True:
        try:
            bot.polling(non_stop=True, interval=0)
        except Exception as e:
            bot.send_message(config["Admins"]["1"], text=str(e))
            time.sleep(5)
            continue
