import telebot
from telebot import types
import os
from config import MAIN_TEXT, RESPONSES, TRANSPORT_OPTIONS, MAP_IMAGES, TRANSPORT_LIST, MENU_OPTIONS, TRANSPORT_DIRECTIONS, number, help_text

BOT_TOKEN = "6906379683:AAESlzWrRQpaVMKU7QGaIy7P5rjc7NGFitk"
IMAGES_PATH = os.getcwd() + "\\images\\"
id_chat_admin = [5057474050, -1002218375130]

mes_op = False
pics_count = 0
bot = telebot.TeleBot(BOT_TOKEN)

def print_add_info(keyboard):
    for i in MENU_OPTIONS.keys():
        keyboard.add(types.InlineKeyboardButton(
            text=MENU_OPTIONS[i], callback_data=i))


def print_route_info(keyboard):
   but1 = types.InlineKeyboardButton(text=TRANSPORT_DIRECTIONS[0],
                                      callback_data='to_Riv')
   but2 = types.InlineKeyboardButton(text=TRANSPORT_DIRECTIONS[1],
                                      callback_data='back_Riv')
   but3 = types.InlineKeyboardButton(text=TRANSPORT_DIRECTIONS[2],
                                      callback_data='to_Yul')
   but4 = types.InlineKeyboardButton(text=TRANSPORT_DIRECTIONS[3],
                                      callback_data='back_Yul')
   # keyboard.add(but1,but2,but3,but4)
   keyboard.add(but1)
   keyboard.add(but2)
   keyboard.add(but3)
   keyboard.add(but4)
    
   key_back = types.InlineKeyboardButton(
      text='Назад', callback_data='back')
   keyboard.add(key_back)


@bot.message_handler(commands=['start'])
def start(message):
    print(message.chat.id, message.from_user.username)

    # Создание клавиатуры
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('Дополнительная информация')
    button2 = types.KeyboardButton('Наши соц.сети')
    button3 = types.KeyboardButton('Поддержка')
    button4 = types.KeyboardButton('Поделиться ботом')
    keyboard.add(button1, button2, button3, button4)

    bot.send_message(message.chat.id, MAIN_TEXT, reply_markup=keyboard)

    markup = types.InlineKeyboardMarkup()
    button4 = types.InlineKeyboardButton("Сайт СТЦ", url='https://www.stc-spb.ru/')
    button5 = types.InlineKeyboardButton("ТГК", url='https://t.me/stc_vesti')
    markup.add(button4, button5)
    bot.send_message(
        message.chat.id,
        "Переходите на наши информационные ресурсы:",
        reply_markup=markup
        )

# кнопки из нижнего меню:
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global mes_op, pics_count
    if message.text == 'Поддержка':
        markup = types.InlineKeyboardMarkup()
        
        key_yes = types.InlineKeyboardButton(text='Написать оператору', callback_data='yes')
        markup.add(key_yes)
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='back_main')
        markup.add(key_back)
        bot.send_message(
            message.chat.id,
            help_text,
            reply_markup=markup,
            parse_mode="HTML"
            )
        mes_op = True

    elif message.text == 'Дополнительная информация':
        keyboard = types.InlineKeyboardMarkup()
        print_add_info(keyboard)
        bot.send_message(message.chat.id, 'Вопросы:', reply_markup=keyboard)

    elif message.text == 'Наши соц.сети':
        markup = types.InlineKeyboardMarkup()
        button4 = types.InlineKeyboardButton(
            "Сайт СТЦ", url='https://www.stc-spb.ru/')
        button5 = types.InlineKeyboardButton(
            "Телеграм канал СТЦ", url='https://t.me/stc_vesti')
        markup.add(button4, button5)
        key_back = types.InlineKeyboardButton(
            text='Назад', callback_data='back_main')
        markup.add(key_back)
        bot.send_message(message.chat.id,
                         "Переходите на наши информационные ресурсы:", reply_markup=markup)

    elif message.text == 'Поделиться ботом':
        markup = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='back_main') #кнопка «Да»
        markup.add(key_back)
        bot.send_photo(message.chat.id, photo=open(IMAGES_PATH + 'QR.jpg', 'rb'),
                    caption=f'<code>@ooosts_info_bot</code>',parse_mode="HTML",reply_markup=markup)

    elif mes_op:
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.send_message(message.chat.id,"Спасибо за обращение, оператор ответит в ближайшее время")
        for i in id_chat_admin:
            bot.send_message(i,
                             'Сообщение -> ' +
                             str(message.text)+'\nchat id -> ' +
                             str(message.chat.id)
                             + '\n@'+str(message.from_user.username)+' '+str(message.from_user.first_name))
        mes_op = False

    else:
        # Действия при получении другого сообщения
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура

        key_yes = types.InlineKeyboardButton(
            text='Связаться с оператором', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes)
        key_back = types.InlineKeyboardButton(
            text='Назад', callback_data='back_main')
        keyboard.add(key_back)
        bot.send_message(
            message.chat.id,
            help_text,
            reply_markup=keyboard,
            parse_mode="HTML"
            )


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global mes_op, pics_count
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id,
                         'Напишите сообщение и мы направим его оператору')
        mes_op = True
    if call.data == "back_main":
        bot.delete_message(call.message.chat.id, call.message.message_id-1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        mes_op = False
    if call.data == "back":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        mes_op = False
        keyboard = types.InlineKeyboardMarkup()
        print_add_info(keyboard)
        bot.send_message(call.message.chat.id,
                         text="Вопросы:", reply_markup=keyboard)
    if call.data == "back_to":
        for id in range(pics_count+1):
            bot.delete_message(call.message.chat.id, call.message.message_id - id)
        mes_op = False
        keyboard = types.InlineKeyboardMarkup()
        text = "Путь следования:"
        print_route_info(keyboard)
        bot.send_message(call.message.chat.id, text, reply_markup=keyboard)

    for i in MENU_OPTIONS.keys():
        if call.data == i:
            keyboard = types.InlineKeyboardMarkup()
            if call.data == "transport_info":
                bot.delete_message(call.message.chat.id,
                                   call.message.message_id)
                text = "Путь следования:"
                print_route_info(keyboard)

            else:
                bot.delete_message(call.message.chat.id,
                                   call.message.message_id)
                text = RESPONSES[i]
                key_back = types.InlineKeyboardButton(
                    text='Назад', callback_data='back')
                keyboard.add(key_back)
            bot.send_message(call.message.chat.id, text, reply_markup=keyboard, parse_mode="HTML")

    if call.data in ["to_Riv", "back_Riv", 'to_Yul', 'back_Yul']:
        if 'ids' in locals():
            for id in ids:
                bot.delete_message(call.message.chat.id, id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(
            text='Назад', callback_data='back_to')
        keyboard.add(key_back)
        media = []
        pics_count = 0
        for x in MAP_IMAGES[call.data]:
            with open(IMAGES_PATH + x, 'rb') as img:
                file_data = img.read()
                media.append(types.InputMediaPhoto(file_data, caption=TRANSPORT_LIST[x]))
                pics_count += 1
        sent_pics = bot.send_media_group(media=media, chat_id=call.message.chat.id)
        ids = [mes.message_id for mes in sent_pics]
        bot.send_message(call.message.chat.id, text=TRANSPORT_OPTIONS[call.data], reply_markup=keyboard, parse_mode="HTML")

bot.polling(none_stop=True)