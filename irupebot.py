from asyncore import dispatcher
import fn
import os
import logging
import threading
import telegram
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
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
    update.message.reply_text(f'Hola {userName} gracias por activarme. Te dejo a continuación la lista de comandos que hizo el vago de Yamil: \n /start , /botinfo, /addevent , /event , /f1, /dados')
    button1 = InlineKeyboardButton(
        text = 'El origen de RamiMeMe',
        url = 'https://www.instagram.com/p/BO2KkXqA7jswGgv-TYP26Bclf7ino4w0gzu5hk0/'
    )
    button2 = InlineKeyboardButton(
        text = 'Chatea conmigo',
        url = 'https://t.me/YamilPi'
    )
    update.message.reply_text(
        text = 'Haz click en un botón',
        reply_markup = InlineKeyboardMarkup([
            [button1, button2]
        ])
    )

def F1(update, context):
    bot = context.bot
    userName = update.effective_user["first_name"]
    update.message.reply_text(f'{userName} a continuación te dejo información sobre la Formula 1: \nNoticias, siguiente gran premio y más:')
    button1 = InlineKeyboardButton(
        text = 'Noticias',
        url = 'https://www.formula1.com/en/latest.html'
    )
    button2 = InlineKeyboardButton(
        text = 'Calendario 2022',
        url = 'https://www.formula1.com/en/racing/2022.html'
    )
    button3 = InlineKeyboardButton(
        text = 'Conoce a los pilotos',
        url = 'https://www.formula1.com/en/drivers.html'
    )
    button4 = InlineKeyboardButton(
        text = 'Futuro campeón',
        url = 'https://www.instagram.com/charles_leclerc/'
    )
    button5 = InlineKeyboardButton(
        text = 'F1 Instagram',
        url = 'https://www.instagram.com/f1/'
    )
    button6 = InlineKeyboardButton(
        text = 'G.O.A.T',
        url = 'https://www.instagram.com/lewishamilton/'
    )
    update.message.reply_text(
        text = 'Click para información',
        reply_markup = InlineKeyboardMarkup([
            [button1, button2],
            [button3, button4],
            [button5, button6]
        ])
    )

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
        text = f'<b>Bienvenido al grupo {userName}</b>'
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
            text = f'Hola {userName}, que tengas un lindo día!'
        )
    elif 'Formula 1' in text or 'formula 1' in text:
        bot.sendMessage(
            chat_id = chatId,
            text = f'{userName} si te gusta la Formula 1 puedes clickear en /f1'
        )
    elif 'charo' in text:
        chard = fn.get_chard()
        chatId = update.message.chat_id
        context.bot.send_animation(chatId, chard)

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

    # if userisAdmin(chatId, userId, bot) == True:
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
    # else:
    #     logger.info(f'{userName} ha intentado agregar un evento pero no tiene permisos')
    #     bot.sendMessage(
    #         chat_id = chatId,
    #         text = f'{userName} no tienes permisos para agregar un evento'
    #     )

def event(update, context):
    chatId = update.message.chat_id
    userName = update.effective_user['first_name']
    bot = context.bot

    logger.info(f'El usuario {userName} ha solicitado los eventos')
    bot.sendMessage(
        chat_id = chatId,
        text = eventos
    )

def mibreak(update, context):
    def send_alert(msg):
        update.message.reply_text(msg)
    minutos = float(context.args[0])
    userName = update.effective_user["first_name"]
    msg = (f'{userName} se terminó tu break, pestañaste')
    timer = threading.Timer(minutos, send_alert, [msg])
    timer.start()

def cmd_roll_d6(update, context):
    result = fn.roll_d6()
    context.bot.send_message(update.message.chat_id, str(result))

def cmd_animated_d6(update, context):
    result = fn.roll_d6()
    animation = fn.get_d6_img(result)
    chatId = update.message.chat_id
    context.bot.send_animation(chatId, animation)

if __name__ == "__main__":
    #obtener la informacion del bot
    myBot = telegram.Bot(token = TOKEN)
    #print(myBot.getMe())

#updated se conecta y recibe los mensajes
updater = Updater(myBot.token, use_context = True)

#create dispatcher
dp = updater.dispatcher

#create command
dp.add_handler(CommandHandler("botinfo", getBotInfo))
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("f1", F1))
dp.add_handler(CommandHandler("addevent", addEvent, pass_args=True))
dp.add_handler(CommandHandler("event", event))
dp.add_handler(CommandHandler("rolld6", cmd_roll_d6))
dp.add_handler(CommandHandler("dados", cmd_animated_d6))
dp.add_handler(CommandHandler("break", mibreak))
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, wellcomeMsg))
dp.add_handler(MessageHandler(Filters.text, echo)) #con esto lee los mensajes del chat


updater.start_polling() #esto pregunta por mensajes entrantes
print("BOT RUNNING")
updater.idle()# terminar bot con ctrl + c