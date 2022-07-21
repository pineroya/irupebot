from asyncore import dispatcher
import os
import logging
import telegram
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    level = logging.INFO, format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
logger = logging.getLogger()

TOKEN = os.getenv("TOKEN")

eventos = "Los eventos son:"

def event(update, context):
    chatId = update.message.chat_id
    userName = update.effective_user['first_name']
    bot = context.bot

    logger.info(f'El usuario {userName} ha solicitado los eventos')
    bot.sendMessage(
        chat_id = chatId,
        text = eventos
    )

def addEvent(update, context):
    global eventos
    bot = context.bot
    chatId = update.message.chat_id
    userName = update.effective_user["first_name"]
    userId = update.effective_user['id']
    args = context.args

    if len(args) == 0:
        logger.info(f'El usuario {userName} no ha ingresado argumentos')
        bot.sendMessage(
            chat_id = chatId,
            text = f'{userName} porfavor ingresa más información para agregar al evento'
        )
    else:
        evento = ' '.join(args)
        eventos = eventos + '\n>>' + evento

        logger.info(f'El usuario {userName} ha ingresado un nuevo evento')

        bot.sendMessage(
            chat_id = chatId,
            text = f'{userName} has ingresado un evento correctamente'
        )

def deleteMessage(bot, chatId, messageId, userName):
    try:
        bot.delete_message(chatId, messageId)
        logger.info(f'El mensaje de {userName} se eliminó')
    except Exception as e:
        print(e)

def delEvent(update, context):
    global eventos
    bot = context.bot
    chatId = update.message.chat_id
    userName = update.effective_user["first_name"]
    userId = update.effective_user['id']
    args = context.args

    evento = ' '.join(args(''))

    bot.sendMessage(
        chat_id = chatId,
        text = f'{userName} ha borrado los eventos correctamente'
    )