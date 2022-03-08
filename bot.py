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
from datetime import date
import re
#requests.post('https://api.telegram.org/bot5134551401:AAGsCzW7j9mTBX8aNC3HRyZX2j68wR4Y5KY/sendMessage?chat_id=@transport_helo_vienna&text='+)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, Contact
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.ext import MessageHandler, Filters

logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def reset_button():
	keyboard = [
		[
			InlineKeyboardButton("🔄 Начать заново", callback_data='Button_Restart'),
		],
	]
	return InlineKeyboardMarkup(keyboard)

def get_contact():
	keyboard = [
		[
			KeyboardButton("Поделиться контактом", request_contact=True),
		],
	]
	return ReplyKeyboardMarkup(keyboard, resize_keyboard=True,one_time_keyboard=True)

def get_phone_number(update: Update, context: CallbackContext):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, поделитесь вашим контактом.", reply_markup=get_contact())


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

def remove_markdown(string):
		return string.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")

def send_message(update: Update, context: CallbackContext, button):
	
	def phone_number(update: Update, context: CallbackContext):
		tel_number = user_info[update.effective_user.id]["phone_number"]
		def check_plus(tel_number):
			if '+' not in tel_number:
				telephone_number = '+' + str(tel_number)
				print(telephone_number)
				return telephone_number
			else:
				return tel_number
		
		if len(tel_number) > 0:
			return ' (номер телефона ' + check_plus(tel_number) + ')'

	if button == 'Button_MaterialAid':
		
		message = (
		'✅ Новая заявка от ' + remove_markdown(user_info[update.effective_user.id]["user_name"]) + phone_number(update, context) + ' на вещи и медикаменты\n' +
		'- - - - - - - - - - - - - - -\n' +
		'*Список необходимого:* \n' +
		user_info[update.effective_user.id]["reply1"] + '\n' +
		'*На когда нужно:* \n' +
		user_info[update.effective_user.id]["reply2"] + '\n' +
		'*Куда доставить:* \n' +
		user_info[update.effective_user.id]["reply3"])
		msg = context.bot.send_message(chat_id="@material_aid_in_vienna", text=message, parse_mode="Markdown")
		return msg
	elif button == 'Button_Transport':
		message = (
		'✅ Новая заявка от ' + remove_markdown(user_info[update.effective_user.id]["user_name"]) + phone_number(update, context) + ' на транспортировку\n' +
		'- - - - - - - - - - - - - - -\n' +
		'*Откуда:* \n' +
		user_info[update.effective_user.id]["reply1"] + '\n' +
		'*Куда:* \n' +
		user_info[update.effective_user.id]["reply2"] + '\n' +
		'*Когда:* \n' +
		user_info[update.effective_user.id]["reply3"]	+'\n' +
		'*Информация о поездке:* \n' +
		user_info[update.effective_user.id]["reply4"])
		
		keyboard = [
			[
				InlineKeyboardButton("Взять заявку 👍", callback_data='take_request')
			]
		]
		markup = InlineKeyboardMarkup(keyboard)
		msg = context.bot.send_message(chat_id="@transport_in_vienna", text=message, parse_mode="Markdown", reply_markup=markup) 
		return msg
	elif button == 'Button_Translation':
		message = (
		'✅ Новая заявка от ' + remove_markdown(user_info[update.effective_user.id]["user_name"]) + phone_number(update, context) + ' на языковую помощь\n' +
		'- - - - - - - - - - - - - - -\n' +
		'*Что необходимо перевести:* \n' +
		user_info[update.effective_user.id]["reply1"] + '\n' +
		'*РУС-НЕМ или НЕМ-РУС:* \n' +
		user_info[update.effective_user.id]["reply2"] + '\n' +
		'*На когда:* \n' +
		user_info[update.effective_user.id]["reply3"])
		msg = context.bot.send_message(chat_id="@translations_in_vienna", text=message, parse_mode="Markdown")
		return msg
	elif button == 'Button_Accomponation':
		message = (
		'✅ Новая заявка от ' + remove_markdown(user_info[update.effective_user.id]["user_name"]) + phone_number(update, context) + ' на сопровождение\n' +
		'- - - - - - - - - - - - - - -\n' +
		'*Куда необходимо сопроводить:* \n' +
		user_info[update.effective_user.id]["reply1"] + '\n' +
		'*Когда:* \n' +
		user_info[update.effective_user.id]["reply2"] + '\n' +
		'*Доп. информация:* \n' +
		user_info[update.effective_user.id]["reply3"])		
		msg = context.bot.send_message(chat_id="@accomponation_in_vienna", text=message, parse_mode="Markdown")
		return msg

def update_message(update: Update, context: CallbackContext, button):
	
	if button == 'take_request':
		user_id = update.effective_user.id
		msg_id  = update.callback_query.message.message_id

		db_conn = open_db()
		cursor = db_conn[0]
		conn = db_conn[1]
		cursor.execute('SELECT * FROM users WHERE (user_id, message_id) = (?, ?)', (user_id, msg_id))
		user_created = cursor.fetchall()
		cursor.execute('SELECT * FROM volunteers WHERE (user_id, message_id) = (?, ?)', (user_id, msg_id))
		volunteer_took = cursor.fetchall()
		close_db(conn)
		the_same_user = len(user_created)
		taken_flag = len(volunteer_took) 

		if the_same_user > 0:
			context.bot.send_message(chat_id=user_id, text="Извините, но Вы не можете взять в работу свою заявку.")
		elif taken_flag > 0:
			keyboard = [
				[
					InlineKeyboardButton("Отказаться от заявки 👎", callback_data='cancel_request')
				]
			]
			markup = InlineKeyboardMarkup(keyboard)
			msg_txt  = update.callback_query.message.text
			user_name = update.effective_user.first_name + " " + update.effective_user.last_name
			word_arr = re.findall("[А-я ]+\:", msg_txt)
			new_arr = []
			for word in word_arr:
				new_word = "*" + word + "*"
				new_arr.append(new_word)
				msg_txt = msg_txt.replace(word, new_word)
			#print(new_arr)
			taken_text = "\n\n*----- Заявку номер " + str(msg_id) + " взял(а) в работу " + user_name + " -----*\n\n" + msg_txt
			query = update.callback_query
			query.edit_message_text(text=taken_text, reply_markup=markup, parse_mode="Markdown")
	if button == 'cancel_request':
		keyboard = [
			[
				InlineKeyboardButton("Взять заявку 👍", callback_data='take_request')
			]
		]
		markup = InlineKeyboardMarkup(keyboard)
		msg_txt  = update.callback_query.message.text
		user_name = update.effective_user.first_name + " " + update.effective_user.last_name
		word_arr = re.findall("[А-я ]+\:", msg_txt)
		new_arr = []
		for word in word_arr:
			new_word = "*" + word + "*"
			new_arr.append(new_word)
			msg_txt = msg_txt.replace(word, new_word)
		new_txt = msg_txt.split("-----")
		query = update.callback_query
		query.edit_message_text(text=new_txt[2], reply_markup=markup, parse_mode="Markdown")

def db_table_val(user_id: int, user_name: str, phone_number: str, got_contact: bool, role: str, status: int, reply1: str, reply2: str, reply3: str, reply4: str, chosen_button: str, message_id: int):
	db_conn = open_db()
	cursor = db_conn[0]
	conn = db_conn[1]
	cursor.execute('INSERT INTO users (user_id,user_name,phone_number,got_contact,role,status,reply1,reply2,reply3,reply4,chosen_button, message_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, user_name, phone_number, got_contact, role, status, reply1, reply2, reply3, reply4, chosen_button, message_id))
	conn.commit()
	close_db(conn)
	
'''
def before_start(update: Update, context: CallbackContext):
	button = [[KeyboardButton("Press me!")]]
	#keyboard = ReplyKeyboardMarkup(button, one_time_keyboard=True)

	keyboard = [
		[
			InlineKeyboardButton("Взять заявку 👍", callback_data='take_request'),
		]
	]

	reply_markup = InlineKeyboardMarkup(keyboard)
	
	msg = context.bot.send_message(chat_id="@transport_helo_vienna", text="Текст сообщения", reply_markup=reply_markup)
	print(msg.message_id)
	#context.bot.edit_message_text(text=f"Пожалуйста, напишите, откуда вас нужно перевезти: ", chat_id="@transport_helo_vienna",message_id=500)
	#context.bot.copyMessage(chat_id="@dead_channel_test", from_chat_id="@transport_helo_vienna", message_id=1)
	'''
		

def start(update: Update, context: CallbackContext):
	"""Sends a message with three inline buttons attached."""
	user_info[update.effective_user.id] = {"user_id":"", "user_name":"", "phone_number":"", "got_contact":False, "role":"", "status":-1, "chosen_button":"", "reply1":"", "reply2":"", "reply3":"", "reply4":"", "category":""}
	

	keyboard = [
		[
			InlineKeyboardButton("🙏 Получить помощь", callback_data='Button_NeedHelp'),
			InlineKeyboardButton("🤝 Оказать помощь", callback_data='Button_ProvideHelp')
		]
	]

	reply_markup = InlineKeyboardMarkup(keyboard)

	context.bot.send_message(chat_id=update.effective_chat.id, text="Этот бот был создан для поиска и оказания взаимопомощи людям, оказавшимся в Вене из-за войны в Украине 🇺🇦 \nПожалуйста, укажите, хотите ли вы получить помощь или ее оказать:", reply_markup=(reply_markup))

def handleButton_need_help(update: Update, context: CallbackContext):
	keyboard = [
		[
			InlineKeyboardButton("⛑ Вещи / Mедикаменты", callback_data='Button_MaterialAid'),
			InlineKeyboardButton("🚙 Транспорт", callback_data='Button_Transport'),
		],
		[
			InlineKeyboardButton("💬 Языковые Переводы", callback_data='Button_Translation'),
			InlineKeyboardButton("🧍🏻 Сопровождение", callback_data='Button_Accomponation'),
		],
		[
			InlineKeyboardButton("💡 Информация", callback_data='Button_Info', url="https://ukrainians-in-vienna.at/"),
			InlineKeyboardButton("🔄 Начать заново", callback_data='Button_Restart'),
		],
	]

	reply_markup = InlineKeyboardMarkup(keyboard)

	query = update.callback_query
	query.edit_message_text(text="Пожалуйста, выберите вид помощи, в которой вы нуждаетесь:", reply_markup=reply_markup)


def handleButton_provide_help(update: Update, context: CallbackContext):
	message = (
			'Ссылки на группы: \n' +
			'- - - - - - - - - - - - - - -\n' +
			'*Вещи и медикаменты:* \n' +
			remove_markdown('https://t.me/material_aid_in_vienna') + '\n' +
			'*Транспорт:* \n' +
			remove_markdown('https://t.me/transport_in_vienna') + '\n' +
			'*Языковая помощь:* \n' +
			remove_markdown('https://t.me/translations_in_vienna') + '\n' +
			'*Сопровождение:* \n' +
			remove_markdown('https://t.me/accomponation_in_vienna'))
	
	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="Markdown", reply_markup=reset_button())


def callbackHandler(update: Update, context: CallbackContext) -> None:
	"""Parses the CallbackQuery and updates the message text."""
	query = update.callback_query
	# CallbackQueries need to be answered, even if no notification to the user is needed
	# Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
	query.answer()

	userInput = query.data

	if userInput == "take_request":
		# first of all, check takes limit
		today = date.today()
		db_conn = open_db()
		cursor = db_conn[0]
		conn = db_conn[1]
		user_id = update.effective_user.id
		cursor.execute('SELECT * FROM volunteers WHERE user_id = (?) AND date_taken = (?)', (user_id, today)) #COUNT(message_id)
		records = cursor.fetchall()
		taken_num = len(records) 
		# if ok, take the request
		if taken_num < 5:
			msg_id  = update.callback_query.message.message_id
			user_name = update.effective_user.name
			cursor.execute('INSERT INTO volunteers (user_id, user_name, message_id, date_taken) VALUES (?, ?, ?, ?)', (user_id, user_name, msg_id, today))
			conn.commit()
			update_message(update, context, userInput)
			return
		else:
			context.bot.send_message(chat_id=user_id, text="Извините, но Вы исчерпали максимальное количество взятых заявок.")
		close_db(conn)

	if userInput == "cancel_request":
		user_id = update.effective_user.id
		msg_id  = update.callback_query.message.message_id
		db_conn = open_db()
		cursor = db_conn[0]
		conn = db_conn[1]
		cursor.execute('SELECT * FROM volunteers WHERE (user_id, message_id) = (?, ?)', (user_id, msg_id))
		records = cursor.fetchall()
		taken_flag = len(records) 
		if taken_flag > 0:
			cursor.execute('DELETE FROM volunteers WHERE message_id = (?)', (msg_id,))
			conn.commit()
			close_db(conn)
			update_message(update, context, userInput)
		return

	if userInput == "Button_Restart":
		start(update, context)
		return
	
	if ((userInput == "Button_ProvideHelp") and (user_info[update.effective_user.id]["role"] == "Button_NeedHelp")):
		start(update, context)
		return

	if ((userInput == "Button_NeedHelp") and (user_info[update.effective_user.id]["role"] == "Button_ProvideHelp")):
		start(update, context)
		return

	user_info[update.effective_user.id]["user_id"] = update.effective_user.id
	user_info[update.effective_user.id]["user_name"] = update.effective_user.name
	if user_info[update.effective_user.id]["status"] == -1:
		user_info[update.effective_user.id]["role"] = userInput
		if (user_info[update.effective_user.id]["role"] == "Button_ProvideHelp"):
			handleButton_provide_help(update, context)
		elif (user_info[update.effective_user.id]["role"] == "Button_NeedHelp"):
			handleButton_need_help(update, context)
	else:
		user_info[update.effective_user.id]["chosen_button"] = userInput
		if userInput == 'Button_MaterialAid':
			handleButton_MaterialAid(update, context)
		elif userInput == 'Button_Transport':
			handleButton_Transport(update, context)
		elif userInput == 'Button_Translation':
			handleButton_Translation(update, context)
		elif userInput == 'Button_Accomponation':
			handleButton_Accomponation(update, context)

	user_info[update.effective_user.id]["status"] += 1
   

def handleButton_MaterialAid(update: Update, context: CallbackContext) -> None:
	query = update.callback_query
	query.edit_message_text(text=f"Пожалуйста, напишите, какие предметы вам нужны (если вещей несколько, то перечислите их через запятую): ", reply_markup=reset_button())

def handleButton_Transport(update: Update, context: CallbackContext) -> None:
	query = update.callback_query
	query.edit_message_text(text=f"Пожалуйста, напишите, откуда вас нужно перевезти: ", reply_markup=reset_button())

def handleButton_Translation(update: Update, context: CallbackContext) -> None:
	query = update.callback_query
	query.edit_message_text(text=f"Пожалуйста, напишите, что нужно перевести: ", reply_markup=reset_button())

def handleButton_Accomponation(update: Update, context: CallbackContext) -> None:
	query = update.callback_query
	query.edit_message_text(text=f"Пожалуйста, напишите, куда вас нужно сопроводить: ", reply_markup=reset_button())

#def handleButton_Take(update: Update, context: CallbackContext) -> None:
#	query = update.callback_query
#	query.edit_message_text(text=f"Пожалуйста, напишите, куда вас нужно сопроводить: ", reply_markup=reset_button())

#def handleButton_Cancel(update: Update, context: CallbackContext) -> None:
#	query = update.callback_query
#	query.edit_message_text(text=f"Пожалуйста, напишите, куда вас нужно сопроводить: ", reply_markup=reset_button())

def handle_message(update: Update, context: CallbackContext) -> None:
	if user_info[update.effective_user.id]["chosen_button"] == 'Button_MaterialAid':
		handleResponse_MaterialAid(update, context)
	if user_info[update.effective_user.id]["chosen_button"] == 'Button_Transport':
		handleResponse_Transport(update, context)
	if user_info[update.effective_user.id]["chosen_button"] == 'Button_Translation':
		handleResponse_Translation(update, context)
	if user_info[update.effective_user.id]["chosen_button"] == 'Button_Accomponation':
		handleResponse_Accomponation(update, context)
	
	if user_info[update.effective_user.id]["status"] != 0:
		user_info[update.effective_user.id]["status"] += 1

def handle_contacts(update: Update, context: CallbackContext) -> None:
	user_info[update.effective_user.id]["phone_number"] = update.message.contact.phone_number
	user_info[update.effective_user.id]["got_contact"] = True
	handle_message(update, context)

def handleResponse_MaterialAid(update: Update, context: CallbackContext) -> None:
	if user_info[update.effective_user.id]["status"] == 1:
		user_info[update.effective_user.id]["reply1"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите, на когда вам нужны эти предметы (дата и время, например: 01.01.2022, 12:00): ", reply_markup=reset_button())
	if user_info[update.effective_user.id]["status"] == 2:
		user_info[update.effective_user.id]["reply2"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите, куда их необходимо доставить: ", reply_markup=reset_button())
	if user_info[update.effective_user.id]["status"] == 3:
		user_info[update.effective_user.id]["reply3"] = update.message.text
		user_info[update.effective_user.id]["status"] = 4
	if user_info[update.effective_user.id]["status"]>3:
		if not(user_info[update.effective_user.id]["got_contact"]):
			get_phone_number(update, context)
		else:
			msg = send_message(update, context, user_info[update.effective_user.id]["chosen_button"])
			db_table_val(user_id=user_info[update.effective_user.id]["user_id"], user_name=user_info[update.effective_user.id]["user_name"], phone_number=user_info[update.effective_user.id]["phone_number"], got_contact=user_info[update.effective_user.id]["got_contact"], role=user_info[update.effective_user.id]["role"], status=user_info[update.effective_user.id]["status"], reply1=user_info[update.effective_user.id]["reply1"], reply2=user_info[update.effective_user.id]["reply2"], reply3=user_info[update.effective_user.id]["reply3"], reply4=user_info[update.effective_user.id]["reply4"], chosen_button=user_info[update.effective_user.id]["chosen_button"], message_id = msg.message_id )
			context.bot.send_message(chat_id=update.effective_chat.id, text="Ваша заявка была создана! Волонтёры свяжутся с вами через Telegram. Ссылка на ваш запрос: https://t.me/material_aid_in_vienna/" + str(msg.message_id), reply_markup=reset_button())


def handleResponse_Transport(update: Update, context: CallbackContext) -> None:
	if user_info[update.effective_user.id]["status"] == 1:
		user_info[update.effective_user.id]["reply1"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите, куда вам необходимо поехать: ", reply_markup=reset_button())
	if user_info[update.effective_user.id]["status"] == 2:
		user_info[update.effective_user.id]["reply2"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите, когда должна состояться поездка (дата и время, например: 01.01.2022, 12:00): ", reply_markup=reset_button())
	if user_info[update.effective_user.id]["status"] == 3:
		user_info[update.effective_user.id]["reply3"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Коротко опишите цель поездки и важные на ваш взгляд детали: ", reply_markup=reset_button())
	if user_info[update.effective_user.id]["status"] == 4:
		user_info[update.effective_user.id]["reply4"] = update.message.text
		user_info[update.effective_user.id]["status"] = 5
	if user_info[update.effective_user.id]["status"]>4:
		if not(user_info[update.effective_user.id]["got_contact"]):
			get_phone_number(update, context)
		else:
			msg = send_message(update, context, user_info[update.effective_user.id]["chosen_button"])
			db_table_val(user_id=user_info[update.effective_user.id]["user_id"], user_name=user_info[update.effective_user.id]["user_name"], phone_number=user_info[update.effective_user.id]["phone_number"], got_contact=user_info[update.effective_user.id]["got_contact"], role=user_info[update.effective_user.id]["role"], status=user_info[update.effective_user.id]["status"], reply1=user_info[update.effective_user.id]["reply1"], reply2=user_info[update.effective_user.id]["reply2"], reply3=user_info[update.effective_user.id]["reply3"], reply4=user_info[update.effective_user.id]["reply4"], chosen_button=user_info[update.effective_user.id]["chosen_button"], message_id = msg.message_id )
			context.bot.send_message(chat_id=update.effective_chat.id, text="Ваша заявка была создана! Волонтёры свяжутся с вами через Telegram. Ссылка на ваш запрос: https://t.me/transport_in_vienna/" + str(msg.message_id), reply_markup=reset_button())


def handleResponse_Translation(update: Update, context: CallbackContext) -> None:
	if user_info[update.effective_user.id]["status"] == 1:
		user_info[update.effective_user.id]["reply1"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите, с какого языка на какой необходим перевеод (используйте сочетание УКР-НЕМ или НЕМ-УКР): ", reply_markup=reset_button())
	if user_info[update.effective_user.id]["status"] == 2:
		user_info[update.effective_user.id]["reply2"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите, на когда вам нужен перевод (дата и время, например: 01.01.2022, 12:00): ", reply_markup=reset_button())
	if user_info[update.effective_user.id]["status"] == 3:
		user_info[update.effective_user.id]["reply3"] = update.message.text
		user_info[update.effective_user.id]["status"] = 4
	if user_info[update.effective_user.id]["status"]>3:
		if not(user_info[update.effective_user.id]["got_contact"]):
			get_phone_number(update, context)
		else:
			msg = send_message(update, context, user_info[update.effective_user.id]["chosen_button"])
			db_table_val(user_id=user_info[update.effective_user.id]["user_id"], user_name=user_info[update.effective_user.id]["user_name"], phone_number=user_info[update.effective_user.id]["phone_number"], got_contact=user_info[update.effective_user.id]["got_contact"], role=user_info[update.effective_user.id]["role"], status=user_info[update.effective_user.id]["status"], reply1=user_info[update.effective_user.id]["reply1"], reply2=user_info[update.effective_user.id]["reply2"], reply3=user_info[update.effective_user.id]["reply3"], reply4=user_info[update.effective_user.id]["reply4"], chosen_button=user_info[update.effective_user.id]["chosen_button"], message_id = msg.message_id )
			context.bot.send_message(chat_id=update.effective_chat.id, text="Ваша заявка была создана! Волонтёры свяжутся с вами через Telegram. Ссылка на ваш запрос: https://t.me/translations_in_vienna/" + str(msg.message_id), reply_markup=reset_button())


def handleResponse_Accomponation(update: Update, context: CallbackContext) -> None:
	if user_info[update.effective_user.id]["status"] == 1:
		user_info[update.effective_user.id]["reply1"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите, когда вам необходимо сопровождение (дата и время, например: 01.01.2022, 12:00): ", reply_markup=reset_button())
	if user_info[update.effective_user.id]["status"] == 2:
		user_info[update.effective_user.id]["reply2"] = update.message.text
		context.bot.send_message(chat_id=update.effective_chat.id, text="Коротко опишите цель сопровождения и важные на ваш взгляд детали: ", reply_markup=reset_button())
	if user_info[update.effective_user.id]["status"] == 3:
		user_info[update.effective_user.id]["reply3"] = update.message.text
		user_info[update.effective_user.id]["status"] = 4	
	if user_info[update.effective_user.id]["status"]>3:
		if not(user_info[update.effective_user.id]["got_contact"]):
			get_phone_number(update, context)
		else:
			msg = send_message(update, context, user_info[update.effective_user.id]["chosen_button"])
			db_table_val(user_id=user_info[update.effective_user.id]["user_id"], user_name=user_info[update.effective_user.id]["user_name"], phone_number=user_info[update.effective_user.id]["phone_number"], got_contact=user_info[update.effective_user.id]["got_contact"], role=user_info[update.effective_user.id]["role"], status=user_info[update.effective_user.id]["status"], reply1=user_info[update.effective_user.id]["reply1"], reply2=user_info[update.effective_user.id]["reply2"], reply3=user_info[update.effective_user.id]["reply3"], reply4=user_info[update.effective_user.id]["reply4"], chosen_button=user_info[update.effective_user.id]["chosen_button"], message_id = msg.message_id )
			context.bot.send_message(chat_id=update.effective_chat.id, text="Ваша заявка была создана! Волонтёры свяжутся с вами через Telegram. Ссылка на ваш запрос: https://t.me/accomponation_in_vienna/" + str(msg.message_id), reply_markup=reset_button())


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
	updater = Updater("5229228704:AAEAsJ5DZ0Zs_PEw7Y0Ub--sPOoG98Tr8MY")

	global user_info
	user_info = {}
	
	updater.dispatcher.add_handler(CommandHandler('start', start))
	#updater.dispatcher.add_handler(CommandHandler('before_start', before_start))
	updater.dispatcher.add_handler(CommandHandler('help', help_command))
	updater.dispatcher.add_handler(CallbackQueryHandler(callbackHandler))
	updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))
	updater.dispatcher.add_handler(MessageHandler(Filters.contact, handle_contacts))
    
	# Start the Bot
	updater.start_polling()

	
	# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT
	updater.idle()


if __name__ == '__main__':
	main()