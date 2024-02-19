import os
import sys
import telebot
from telebot import types
import database.manger as db
import json

with open('src/config.json') as file:
    token =json.load(file)
    bot = telebot.TeleBot(token['token'])

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Menu ⚙️")
    markup.add(item1)
    if (not db.ifUserExist(message.chat.id)):
        db.createUser(message.chat.id)
        bot.send_message(message.chat.id, "Hello there!",reply_markup=markup)

    else:
        bot.send_message(message.chat.id, "User already exists!",reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def message_reply(message):
    userId=message.chat.id
    if message.text=="Menu ⚙️":
         showMenu(userId)
    elif message.text=="Account data 🔒":
        getAccountdata(userId)

    elif message.text=="Create trade offer💵":
        db.createTrade(userId)
        db.changeUserPosition(userId,"selecting_type")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buyButton = types.KeyboardButton("BUY 🟢")
        sellButton = types.KeyboardButton("SELL 🔴")
        markup.add(buyButton,sellButton)
        bot.send_message(userId,"Select the type of order",reply_markup=markup)

    elif db.getUserPosition(userId)=="creating_description":
        description=message.text
        db.AddDescription(description,userId)
        print(f'des = {description}')
        bot.send_message(userId,"Enter how much it costs")
        db.changeUserPosition(userId,"order_creation")

    elif db.getUserPosition(userId)=="selecting_type":
        if message.text == "BUY 🟢":
            order_type = "buy"
            bot.send_message(message.chat.id, "Describe an order",reply_markup=types.ReplyKeyboardRemove())
            db.changeUserPosition(userId,"creating_description")
        elif message.text == "SELL 🔴":
            order_type = "sell"
            bot.send_message(message.chat.id, "Describe an order",reply_markup=types.ReplyKeyboardRemove())
            db.changeUserPosition(userId,"creating_description")
        else:
            bot.send_message(userId, "Oops...Something went wrong :(")
            showMenu(userId)
        db.AddType(order_type,userId)   
        print(f'Type = {order_type}')
    elif db.getUserPosition(userId)=="order_creation":
        amount=message.text
        print(f'Amount = {amount}')
        if amount.isdigit():
            amount=float(message.text)
            db.AddAmonunt(amount,userId)
            bot.send_message(userId,f"Order succesfully created!\nOrder id:{db.FindCurrentId()}")
        else:
            bot.send_message(userId, "Oops...Something went wrong :(")
            showMenu(userId)
    else:
        bot.send_message(message.chat.id,"Oops...Something went wrong :(")
    
def showMenu(userId):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    getProfileInfo = types.KeyboardButton("Account data 🔒")
    startTrade = types.KeyboardButton("Create trade offer💵")
    markup.add(getProfileInfo,startTrade)
    db.changeUserPosition(userId,"menu")
    bot.send_message(userId, "Choose an option:", reply_markup=markup)

def getAccountdata(userId):
    bot.send_message(userId,f"Account id: {userId}\nMoney: {db.getProfileInfo(userId)}\nTrades number: {len(db.getTradeList(userId))}")

def getOrderDescription(text):
    description=text
    return description
