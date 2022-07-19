from asyncore import dispatcher
import telebot
import os
import logging
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    level = logging.INFO, format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
logger = logging.getLogger()

TOKEN = os.getenv("TOKEN")

eventos = "Los eventos son:"

def getBotInfo(update, context):
    bot = context.bot
    chatId = update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f'El usuario {userName} ha solicitado información sobre el bot')
    bot.sendMessage(
        chat_id = chatId,
        parse_mode = "HTML",
        text = f'Hola soy un bot creado por <b>Yamil</b>'
    )

def start(update, context):
    bot = context.bot
    userName = update.effective_user["first_name"]
    update.message.reply_text(f'Hola {userName} gracias por activarme, bolsa de cuernos')

def wellcomeMsg(update, context):
    bot = context.bot
    chatId = update.message.chat_id
    updateMsg = getattr(update, "message", None)
    for user in updateMsg.new_chat_members:
        userName = user.first_name

    logger.info(f'El usuario {userName} ha ingresado al grupo')

    bot.sendMessage(
        chat_id = chatId,
        parse_mode = "HTML",
        text = f'<b>Bienvenido al grupo {userName}</b> \n Esperamos que disfrutes de esta comunidad bien chistosa, sentite a gusto y sentate en la torta'
    )

def deleteMessage(bot, chatId, messageId, userName):
    try:
        bot.delete_message(chatId, messageId)
        logger.info(f'El mensaje de {userName} se eliminó')
    except Exception as e:
        print(e)

def echo(update, context):
    bot = context.bot
    updateMsg = getattr(update, 'message', None)
    messageId = updateMsg.message_id #obtiene el ide del mensaje
    chatId = update.message.chat_id
    userName = update.effective_user['first_name']
    text = update.message.text #obtener el texto que envió el usuario al chat
    logger.info(f'El usuario {userName} ha enviado un nuevo mensaje al grupo {chatId}')

    badWord = 'Yamil'

    if badWord in text:
        deleteMessage(bot, chatId, messageId, userName)
        bot.sendMessage(
            chat_id = chatId,
            text = f'El mensaje de {userName} ha sido eliminado porque habló de Yamil sin su divino consentimiento'
        )
    elif 'Hola' in text and 'Martina' in text:
        bot.sendMessage(
            chat_id = chatId,
            text = f'Hola {userName}, lindo día, que mierda queres?!'
        )

def userisAdmin(chatId, userId, bot):
    try:
        groupAdmins = bot.get_chat_administrators(chatId)
        for admin in groupAdmins:
            if admin.user.id == userId:
                isAdmin = True
            else:
                isAdmin = False
        return isAdmin
    except Exception as e:
        print(e)

def addEvent(update, context):
    global eventos
    bot = context.bot
    chatId = update.message.chat_id
    userName = update.effective_user["first_name"]
    userId = update.effective_user['id']
    args = context.args

    if userisAdmin(chatId, userId, bot) == True:
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
    else:
        logger.info(f'{userName} ha intentado agregar un evento pero no tiene permisos')
        bot.sendMessage(
            chat_id = chatId,
            text = f'{userName} no tienes permisos para agregar un evento'
        )

def event(update, context):
    chatId = update.message.chat_id
    userName = update.effective_user['first_name']
    bot = context.bot

    logger.info(f'El usuario {userName} ha solicitado los eventos')
    bot.sendMessage(
        chat_id = chatId,
        text = eventos
    )



if __name__ == "__main__":
    #obtener la informacion del bot
    myBot = telegram.Bot(token = TOKEN)
    #print(myBot.getMe())

#updated se conecta y recibe los mensajes
updater = Updater(myBot.token, use_context = True)

#create dispatcher
dp = updater.dispatcher

#create command
dp.add_handler(CommandHandler("botInfo", getBotInfo))
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("addEvent", addEvent, pass_args=True))
dp.add_handler(CommandHandler("event", event))
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, wellcomeMsg))
dp.add_handler(MessageHandler(Filters.text, echo)) #con esto lee los mensajes del chat


updater.start_polling() #esto pregunta por mensajes entrantes
print("BOT RUNNING")
updater.idle()# terminar bot con ctrl + c