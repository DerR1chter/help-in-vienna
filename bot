#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://git.io/JOmFw.
"""
import logging
import time
import sqlite3
import requests
#requests.post('https://api.telegram.org/bot5134551401:AAGsCzW7j9mTBX8aNC3HRyZX2j68wR4Y5KY/sendMessage?chat_id=@transport_helo_vienna&text='+)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.ext import MessageHandler, Filters

logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

#Writing to DB and sending the message
def open_db():
	try:
		conn = sqlite3.connect('bot_database.db', check_same_thread=False)
		cursor = conn.cursor()
		return cursor, conn

	except sqlite3.Error as error:
		print("Can't connect to DB", error)

def close_db(conn):
	conn.close()

user_info = {"user_id":"", "user_name":"", "status":0, "chosen_button":"", "reply1":"", "reply2":"", "reply3":"", "reply4":""}
def send_message(button):

		def remove_markdown(string):
			return string.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")

		if button == 'Button_MaterialAid':
			message = (
			'✅ Новая заявка от ' + remove_markdown(user_info["user_name"]) + ' на вещи и медикаменты\n' +
			'- - - - - - - - - - - - - - -\n' +
			'*Список необходимого:* \n' +
			user_info["reply1"] + '\n' +
			'*На когда нужно:* \n' +
			user_info["reply2"] + '\n' +
			'*Куда доставить:* \n' +
			user_info["reply3"])
			requests.post('https://api.telegram.org/bot5134551401:AAGsCzW7j9mTBX8aNC3HRyZX2j68wR4Y5KY/sendMessage?chat_id=@transport_helo_vienna&text='+ message + '&parse_mode=Markdown')
		elif button == 'Button_Transport':
			message = (
			'✅ Новая заявка от ' + remove_markdown(user_info["user_name"]) + ' на транспортировку\n' +
			'- - - - - - - - - - - - - - -\n' +
			'*Откуда:* \n' +
			user_info["reply1"] + '\n' +
			'*Куда:* \n' +
			user_info["reply2"] + '\n' +
			'*Когда:* \n' +
			user_info["reply3"]	+'\n' +
			'*Информация о поездке:* \n' +
			user_info["reply4"])
			requests.post('https://api.telegram.org/bot5134551401:AAGsCzW7j9mTBX8aNC3HRyZX2j68wR4Y5KY/sendMessage?chat_id=@transport_helo_vienna&text='+ message + '&parse_mode=Markdown')
		elif button == 'Button_Translation':
			message = (
			'✅ Новая заявка от ' + remove_markdown(user_info["user_name"]) + ' на перевод с/на немецкий\n' +
			'- - - - - - - - - - - - - - -\n' +
			'*Что необходимо перевести:* \n' +
			user_info["reply1"] + '\n' +
			'*РУС-НЕМ или НЕМ-РУС:* \n' +
			user_info["reply2"] + '\n' +
			'*На когда:* \n' +
			user_info["reply3"])
			requests.post('https://api.telegram.org/bot5134551401:AAGsCzW7j9mTBX8aNC3HRyZX2j68wR4Y5KY/sendMessage?chat_id=@transport_helo_vienna&text='+ message + '&parse_mode=Markdown')
		elif button == 'Button_Accomponation':
			message = (
			'✅ Новая заявка от ' + remove_markdown(user_info["user_name"]) + ' на сопровождение\n' +
			'- - - - - - - - - - - - - - -\n' +
			'*Куда необходимо сопроводить:* \n' +
			user_info["reply1"] + '\n' +
			'*Когда:* \n' +
			user_info["reply2"] + '\n' +
			'*Доп. информация:* \n' +
			user_info["reply3"])		
			requests.post('https://api.telegram.org/bot5134551401:AAGsCzW7j9mTBX8aNC3HRyZX2j68wR4Y5KY/sendMessage?chat_id=@transport_helo_vienna&text='+ message + '&parse_mode=Markdown')


def db_table_val(user_id: int, user_name: str, status: int, reply1: str, reply2: str, reply3: str, reply4: str):
	db_conn = open_db()
	cursor = db_conn[0]
	conn = db_conn[1]
	cursor.execute('INSERT INTO our_table (user_id,user_name,status,reply1,reply2,reply3,reply4) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id,user_name,status,reply1,reply2,reply3,reply4,))
	conn.commit()
	close_db(conn)
	

def before_start(update: Update, context: CallbackContext):
	button = [[KeyboardButton("Press me!")]]
	#keyboard = ReplyKeyboardMarkup(button, one_time_keyboard=True)

	keyboard = [
		[
			InlineKeyboardButton("Взять заявку 👍", callback_data='take_request'),
		]
	]

	reply_markup = InlineKeyboardMarkup(keyboard)
	
	context.bot.send_message(chat_id="@transport_helo_vienna", text="Текст сообщения", reply_markup=reply_markup)
	update.channel_post 
	

def start(update: Update, context: CallbackContext):
	"""Sends a message with three inline buttons attached."""
	keyboard = [
		[
			InlineKeyboardButton("Вещи и медикаменты", callback_data='Button_MaterialAid'),
			InlineKeyboardButton("Поиск транспорта", callback_data='Button_Transport'),
		],
		[
			InlineKeyboardButton("Перевод с/на немецкий", callback_data='Button_Translation'),
			InlineKeyboardButton("Сопровождение", callback_data='Button_Accomponation'),
		],
	]

	reply_markup = InlineKeyboardMarkup(keyboard)

	context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, выберите услугу, в которой вы нуждаетесь.", reply_markup=reply_markup)
	#update.message.reply_text('Please choose:', reply_markup=reply_markup)

def callbackHandler(update: Update, context: CallbackContext) -> None:
	"""Parses the CallbackQuery and updates the message text."""
	query = update.callback_query
	# CallbackQueries need to be answered, even if no notification to the user is needed
	# Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
	query.answer()

	userInput = query.data

	user_info["user_id"] = update.effective_user.id
	user_info["user_name"] = update.effective_user.name

	
	user_info["chosen_button"] = userInput
	if userInput == 'Button_MaterialAid':
		handleButton_MaterialAid(update, context)
	elif userInput == 'Button_Transport':
		handleButton_Transport(update, context)
	elif userInput == 'Button_Translation':
		handleButton_Translation(update, context)
	elif userInput == 'Button_Accomponation':
		handleButton_Accomponation(update, context)

	user_info["status"] = 1


def handleButton_MaterialAid(update: Update, context: CallbackContext) -> None:
	query = update.callback_query
	query.edit_message_text(text=f"Пожалуйста, напишите, какие предметы вам нужны (если вещей несколько, то перечислите их через запятую): ")

def handleButton_Transport(update: Update, context: CallbackContext) -> None:
	query = update.callback_query
	query.edit_message_text(text=f"Пожалуйста, напишите, откуда вас нужно перевезти: ")

def handleButton_Translation(update: Update, context: CallbackContext) -> None:
	query = update.callback_query
	query.edit_message_text(text=f"Пожалуйста, напишите, что нужно перевести: ")

def handleButton_Accomponation(update: Update, context: CallbackContext) -> None:
	query = update.callback_query
	query.edit_message_text(text=f"Пожалуйста, напишите, куда вас нужно сопроводить: ")


def handle_message(update: Update, context: CallbackContext) -> None:
	if user_info["chosen_button"] == 'Button_MaterialAid':
		handleResponse_MaterialAid(update, context)
	if user_info["chosen_button"] == 'Button_Transport':
		handleResponse_Transport(update, context)
	if user_info["chosen_button"] == 'Button_Translation':
		handleResponse_Translation(update, context)
	if user_info["chosen_button"] == 'Button_Accomponation':
		handleResponse_Accomponation(update, context)
	
	if user_info["status"] != 0:
		user_info["status"] += 1


def handleResponse_MaterialAid(update: Update, context: CallbackContext) -> None:
	if user_info["status"] == 1:
		user_info["reply1"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите, на когда вам нужны эти предметы (дата и время, например: 01.01.2022, 12:00): ")
	if user_info["status"] == 2:
		user_info["reply2"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите, куда их необходимо доставить: ")
	if user_info["status"] == 3:
		user_info["reply3"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Ваша заявка была создана! Волонтёры свяжутся с вами через Telegram.")
		db_table_val(user_id=user_info["user_id"], user_name=user_info["user_name"], status=user_info["status"], reply1=user_info["reply1"], reply2=user_info["reply2"], reply3=user_info["reply3"], reply4=user_info["reply4"])
		send_message(user_info["chosen_button"])


def handleResponse_Transport(update: Update, context: CallbackContext) -> None:
	if user_info["status"] == 1:
		user_info["reply1"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите, куда вам необходимо поехать: ")
	if user_info["status"] == 2:
		user_info["reply2"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите, когда должна состояться поездка (дата и время, например: 01.01.2022, 12:00): ")
	if user_info["status"] == 3:
		user_info["reply3"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Коротко опишите цель поездки и важные на ваш взгляд детали: ")
	if user_info["status"] == 4:
		user_info["reply4"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Ваша заявка была создана! Волонтёры свяжутся с вами через Telegram.")
		db_table_val(user_id=user_info["user_id"], user_name=user_info["user_name"], status=user_info["status"], reply1=user_info["reply1"], reply2=user_info["reply2"], reply3=user_info["reply3"], reply4=user_info["reply4"])
		send_message(user_info["chosen_button"])

def handleResponse_Translation(update: Update, context: CallbackContext) -> None:
	if user_info["status"] == 1:
		user_info["reply1"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите, необходим ли перевод с русского на немецкий или наоборот (используйте сочетание РУС-НЕМ или НЕМ-РУС): ")
	if user_info["status"] == 2:
		user_info["reply2"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите, на когда вам нужен перевод (дата и время, например: 01.01.2022, 12:00): ")
	if user_info["status"] == 3:
		user_info["reply3"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Ваша заявка была создана! Волонтёры свяжутся с вами через Telegram.")
		db_table_val(user_id=user_info["user_id"], user_name=user_info["user_name"], status=user_info["status"], reply1=user_info["reply1"], reply2=user_info["reply2"], reply3=user_info["reply3"], reply4=user_info["reply4"])
		send_message(user_info["chosen_button"])

def handleResponse_Accomponation(update: Update, context: CallbackContext) -> None:
	if user_info["status"] == 1:
		user_info["reply1"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите, когда вам необходимо сопровождение (дата и время, например: 01.01.2022, 12:00): ")
	if user_info["status"] == 2:
		user_info["reply2"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Коротко опишите цель сопровождения и важные на ваш взгляд детали: ")
	if user_info["status"] == 3:
		user_info["reply3"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Ваша заявка была создана! Волонтёры свяжутся с вами через Telegram.")
		db_table_val(user_id=user_info["user_id"], user_name=user_info["user_name"], status=user_info["status"], reply1=user_info["reply1"], reply2=user_info["reply2"], reply3=user_info["reply3"], reply4=user_info["reply4"])
		send_message(user_info["chosen_button"])

'''
def handleResponse_Accomponation(update: Update, context: CallbackContext) -> None:
	query = update.callback_query
	query.edit_message_text(text=f"Selected option: Material Aid")
'''

def help_command(update: Update, context: CallbackContext) -> None:
	"""Displays info on how to use the bot."""
	update.message.reply_text("Use /start to test this bot.")

def main() -> None:
	"""Run the bot."""
	# Create the Updater and pass it your bot's token.
	updater = Updater("5134551401:AAGsCzW7j9mTBX8aNC3HRyZX2j68wR4Y5KY")

	updater.dispatcher.add_handler(CommandHandler('before_start', before_start))
	updater.dispatcher.add_handler(CommandHandler('help', help_command))
	updater.dispatcher.add_handler(CommandHandler('start', start))
	updater.dispatcher.add_handler(CallbackQueryHandler(callbackHandler))
	updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))


	# Start the Bot
	updater.start_polling()

	# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT
	updater.idle()


if __name__ == '__main__':
	main()
