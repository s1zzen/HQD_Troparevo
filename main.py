import telebot
from telebot import types
from keyboa import Keyboa

with open('Token.txt', 'r') as token_file:
    Token = token_file.read()

bot = telebot.TeleBot(Token)

print("      _/_/_/  _/                                         ")
print("   _/            _/_/_/_/  _/_/_/_/    _/_/    _/_/_/    ")
print("    _/_/    _/      _/        _/    _/_/_/_/  _/    _/   ")
print("       _/  _/    _/        _/      _/        _/    _/    ")
print("_/_/_/    _/  _/_/_/_/  _/_/_/_/    _/_/_/  _/    _/     ")

count_digit = {}
list_of_tastes = {}
cart = {}
taste = {}
counter_id = {}
message_of_taste = {}
exit_cart = {}
ireturner = {1: 'HQD', 2: 'IZI'}

adress_delivery = {}
comment_courier = {}
end_order = {}
user_name = {}


@bot.message_handler(commands=["admchgbase"])
def adm_chengebase(message):
    bot.send_message(chat_id=message.chat.id, text='Отправьте данные для csv файла:')
    bot.register_next_step_handler(message, change_base)


def change_base(message):
    with open('ink.csv', 'w') as ink:
        ink.write(message.text)
    bot.send_message(chat_id=message.chat.id, text='Done')


@bot.message_handler(commands=["start"])
def start_msg(message):
    global exit_cart
    global count_digit
    global taste
    global counter_id
    global list_of_tastes
    global message_of_taste
    cht_id = message.chat.id
    user_name[message.chat.id] = message.from_user.username
    count_digit[cht_id] = 0
    list_of_tastes[cht_id] = []
    cart[cht_id] = []
    taste[cht_id] = ''
    counter_id[cht_id] = 0
    message_of_taste[cht_id] = 0
    with open('ink.csv', 'r') as ink:
        k = ink.readlines()
        a = k[0].replace(';\n', '').split(';')
        b = k[1].replace(';\n', '').split(';')
        c = k[2].replace(';\n', '').split(';')
        d = k[3].replace(';\n', '').split(';')
        HQDic = {}
        BackHQD = {}
        IZIc = {}
        BackIZI = {}
        for i in range(0, len(a)):
            HQDic[i] = [a[i], b[i]]
        for i in range(0, len(a)):
            BackHQD[a[i]] = i
        for i in range(0, len(c)):
            IZIc[i] = [c[i], d[i]]
        for i in range(0, len(c)):
            BackIZI[c[i]] = i
    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    HQD_button = types.InlineKeyboardButton(text="HQD", callback_data="HQD")
    IZI_button = types.InlineKeyboardButton(text="IZI", callback_data="IZI")
    keyboardmain.add(HQD_button, IZI_button)
    with open('photo/Troparevo.jpeg', 'rb') as logo:
        bot.send_photo(message.chat.id, logo, caption="Здравствуйте!\nВыберите товар", reply_markup=keyboardmain)

    def hand_digit(message):
        global count_digit
        global message_of_taste
        if message.text.isdigit():
            if counter_id[message.chat.id] == 1:
                Nid = int(HQDic[BackHQD[taste[message.chat.id]]][1])
                if int(message.text) <= Nid:
                    count_digit[message.chat.id] = int(message.text)
                    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                    bot.edit_message_caption(chat_id=message.chat.id, message_id=message_of_taste[message.chat.id],
                                             caption='Сколько вы хотите заказать?',
                                             reply_markup=plsminkboard(message.chat.id))
                else:
                    count_digit[message.chat.id] = Nid
                    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                    bot.edit_message_caption(chat_id=message.chat.id, message_id=message_of_taste[message.chat.id],
                                             caption='У нас нет больше',
                                             reply_markup=plsminkboard(message.chat.id))

            elif counter_id[message.chat.id] == 2:
                Nid = int(IZIc[BackIZI[taste[message.chat.id]]][1])
                if int(message.text) <= Nid:
                    count_digit[message.chat.id] = int(message.text)

                    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                    bot.edit_message_caption(chat_id=message.chat.id, message_id=message_of_taste[message.chat.id],
                                             caption='Сколько вы хотите заказать?',
                                             reply_markup=plsminkboard(message.chat.id))
                else:
                    count_digit[message.chat.id] = Nid
                    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                    bot.edit_message_caption(chat_id=message.chat.id, message_id=message_of_taste[message.chat.id],
                                             caption='У нас нет больше',
                                             reply_markup=plsminkboard(message.chat.id))

        else:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            bot.edit_message_caption(chat_id=message.chat.id, message_id=message_of_taste[message.chat.id],
                                     caption='Вы ввели не число!!!',
                                     reply_markup=plsminkboard(message.chat.id))

    def com_adress(message):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        adress_delivery[message.chat.id] = message.text
        ynkeyboard = types.InlineKeyboardMarkup()
        y_button = types.InlineKeyboardButton(text='Да', callback_data='yadress')
        n_button = types.InlineKeyboardButton(text='Нет', callback_data='order')
        ynkeyboard.add(y_button, n_button)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_of_taste[message.chat.id],
                              text=f'Правильно?\n{message.text}',
                              reply_markup=ynkeyboard)

    def com_kuriy(message):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        comment_courier[message.chat.id] = message.text
        ynkeyboard = types.InlineKeyboardMarkup()
        y_button = types.InlineKeyboardButton(text='Да', callback_data='nocoments')
        n_button = types.InlineKeyboardButton(text='Нет', callback_data='comentyes')
        ynkeyboard.add(y_button, n_button)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_of_taste[message.chat.id],
                              text=f'Правильно?\n{message.text}',
                              reply_markup=ynkeyboard)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        global adress_delivery
        global exit_cart
        global count_digit
        global taste
        global counter_id
        global list_of_tastes
        global message_of_taste
        if call.data == 'HQD':
            count_digit[call.message.chat.id] = 0
            counter_id[call.message.chat.id] = 1

            for i in HQDic:
                list_of_tastes[call.message.chat.id].append(HQDic[i][0])
            list_of_tastes[call.message.chat.id].append('<-')
            HQDkeyboard = Keyboa(items=list_of_tastes[call.message.chat.id], items_in_row=1)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            with open('photo/HQDlogo.jpg', 'rb') as logo:
                bot.send_photo(chat_id=call.message.chat.id, photo=logo, caption='HQD\nВыберите вкус',
                               reply_markup=HQDkeyboard())
            del list_of_tastes[call.message.chat.id][-1]
        if call.data == 'IZI':
            count_digit[call.message.chat.id] = 0
            counter_id[call.message.chat.id] = 2
            for i in IZIc:
                list_of_tastes[call.message.chat.id].append(IZIc[i][0])
            list_of_tastes[call.message.chat.id].append('<-')
            IZIkeyboard = Keyboa(items=list_of_tastes[call.message.chat.id], items_in_row=1)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            with open('photo/izilogo.jpeg', 'rb') as logo:
                bot.send_photo(chat_id=call.message.chat.id, photo=logo, caption='IZI\nВыберите вкус',
                               reply_markup=IZIkeyboard())
            del list_of_tastes[call.message.chat.id][-1]
        if call.data == '<-':
            backmenu(call)
        if call.data == "plus":
            if counter_id[call.message.chat.id] == 1:
                Nid = int(HQDic[BackHQD[taste[call.message.chat.id]]][1])
                if count_digit[call.message.chat.id] + 1 <= Nid:
                    count_digit[call.message.chat.id] += 1
                    bot.edit_message_reply_markup(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        reply_markup=plsminkboard(call.message.chat.id))
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                              text="К сожалению, больше нет")
            elif counter_id[call.message.chat.id] == 2:
                Nid = int(IZIc[BackIZI[taste[call.message.chat.id]]][1])
                if count_digit[call.message.chat.id] + 1 <= Nid:
                    count_digit[call.message.chat.id] += 1
                    bot.edit_message_reply_markup(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        reply_markup=plsminkboard(call.message.chat.id))
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                              text="К сожалению, больше нет")
        if call.data == "digid":

            message_of_taste[call.message.chat.id] = call.message.message_id
            if counter_id[call.message.chat.id] == 1:
                backbut = "HQD"
            else:
                backbut = "IZI"

            keyboard = types.InlineKeyboardMarkup(row_width=1)
            tastebutton = types.InlineKeyboardButton(text=taste[call.message.chat.id], callback_data=backbut)
            rele2 = types.InlineKeyboardButton(text=str(count_digit[call.message.chat.id]), callback_data='digid')
            cartbutton = types.InlineKeyboardButton(text="отправте количество", callback_data="None")
            keyboard.add(tastebutton, rele2, cartbutton)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     caption='Сколько вы хотите заказать?',
                                     reply_markup=keyboard)

            bot.register_next_step_handler(call.message, hand_digit)
        if call.data == "minus":
            if count_digit[call.message.chat.id] > 0:
                count_digit[call.message.chat.id] -= 1
                bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=plsminkboard(call.message.chat.id))
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="нельзя")
                plsminkboard(call.message.chat.id)
        for i in list_of_tastes[call.message.chat.id]:
            if call.data == i:
                taste[call.message.chat.id] = i
                bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                         caption='Сколько вы хотите заказать?',
                                         reply_markup=plsminkboard(call.message.chat.id))
        if call.data == "cart":
            if count_digit[call.message.chat.id] != 0:
                if call.message.chat.id in exit_cart:
                    if ireturner[counter_id[call.message.chat.id]] + " " + taste[call.message.chat.id] in exit_cart[
                        call.message.chat.id]:
                        exit_cart[call.message.chat.id][
                            ireturner[counter_id[call.message.chat.id]] + " " + taste[call.message.chat.id]] += \
                        count_digit[
                            call.message.chat.id]
                    else:
                        exit_cart[call.message.chat.id][
                            ireturner[counter_id[call.message.chat.id]] + " " + taste[call.message.chat.id]] = \
                        count_digit[
                            call.message.chat.id]
                else:
                    exit_cart[call.message.chat.id] = {
                        ireturner[counter_id[call.message.chat.id]] + " " + taste[call.message.chat.id]: count_digit[
                            call.message.chat.id]}
                if counter_id[call.message.chat.id] == 1:
                    if int(HQDic[BackHQD[taste[call.message.chat.id]]][1]) - count_digit[call.message.chat.id] == 0:
                        del HQDic[BackHQD[taste[call.message.chat.id]]]
                    else:
                        HQDic[BackHQD[taste[call.message.chat.id]]][1] = str(
                            int(HQDic[BackHQD[taste[call.message.chat.id]]][1]) - count_digit[call.message.chat.id])
                elif counter_id[call.message.chat.id] == 2:
                    if int(IZIc[BackIZI[taste[call.message.chat.id]]][1]) - count_digit[call.message.chat.id] == 0:
                        del IZIc[BackIZI[taste[call.message.chat.id]]]
                    else:
                        IZIc[BackIZI[taste[call.message.chat.id]]][1] = str(
                            int(IZIc[BackIZI[taste[call.message.chat.id]]][1]) - count_digit[call.message.chat.id])
                writebase()

                backmenu(call)
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                          text="Хотяб одну")
        if call.data == "clearcart":
            for i in exit_cart[call.message.chat.id]:
                a_id = i.split(' ')[0]
                b_tst = i.split(' ')[1]
                if a_id == 'HQD':
                    HQDic[BackHQD[b_tst]][1] = str(int(HQDic[BackHQD[b_tst]][1]) + exit_cart[call.message.chat.id][i])
                else:
                    IZIc[BackIZI[b_tst]][1] = str(int(IZIc[BackIZI[b_tst]][1]) + exit_cart[call.message.chat.id][i])
            del exit_cart[call.message.chat.id]
            backmenu(call)
        if call.data == "order":
            if call.message.chat.id in exit_cart:
                if call.message.chat.id in adress_delivery:
                    del adress_delivery[call.message.chat.id]
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                backkeybord = types.InlineKeyboardMarkup()
                backkeybord.add(types.InlineKeyboardButton(text='Главное меню', callback_data='<-'))
                message_of_taste[call.message.chat.id] = bot.send_message(chat_id=call.message.chat.id,
                                                                          text='Отправте, пожалуйста, адрес\nна который будет произведена доставка',
                                                                          reply_markup=backkeybord).message_id
                bot.register_next_step_handler(call.message, com_adress)


            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                          text="Хотяб одну")
        if call.data == "yadress":
            comentkeyboard = types.InlineKeyboardMarkup()
            y_button = types.InlineKeyboardButton(text='Да', callback_data='comentyes')
            n_button = types.InlineKeyboardButton(text='Нет', callback_data='nocoments')
            nendbutton = types.InlineKeyboardButton(text='Главное меню', callback_data='<-')
            comentkeyboard.add(y_button, n_button)
            comentkeyboard.add(nendbutton)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Хотите оставить комментарий для курьера?', reply_markup=comentkeyboard)
        if call.data == "comentyes":
            if call.message.chat.id in comment_courier:
                del comment_courier[call.message.chat.id]
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            message_of_taste[call.message.chat.id] = bot.send_message(chat_id=call.message.chat.id,
                                                                      text='Комментарий: ').message_id
            bot.register_next_step_handler(call.message, com_kuriy)
        if call.data == "nocoments":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            end_order[call.message.chat.id] = 'Ваш заказ:\n'
            for i in exit_cart[call.message.chat.id]:
                end_order[call.message.chat.id] += f'{i} x {str(exit_cart[call.message.chat.id][i])}\n'
            end_order[call.message.chat.id] += f'\n Адрес доставки:\n{adress_delivery[call.message.chat.id]}'
            if call.message.chat.id in comment_courier:
                end_order[call.message.chat.id] += f'\n\nКомментарий:\n{comment_courier[call.message.chat.id]}'
            end_order[call.message.chat.id] += f'\nКак с Вами связаться:\n@{user_name[call.message.chat.id]}'
            endkboard = types.InlineKeyboardMarkup()
            yendbutton = types.InlineKeyboardButton(text='Все верно', callback_data='endoftheends')
            nendbutton = types.InlineKeyboardButton(text='Главное меню', callback_data='<-')
            endkboard.add(yendbutton, nendbutton)
            bot.send_message(chat_id=call.message.chat.id, text=end_order[call.message.chat.id], reply_markup=endkboard)
        if call.data == "endoftheends":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(chat_id=call.message.chat.id,
                             text='спасибо за заказ!\nОжидайте курьера\nДля повторного заказа\nпропишите /start')
            bot.send_message(chat_id='-1001721728601', text=end_order[call.message.chat.id])

            if call.message.chat.id in count_digit:
                del count_digit[call.message.chat.id]
            if call.message.chat.id in list_of_tastes:
                del list_of_tastes[call.message.chat.id]
            if call.message.chat.id in cart:
                del cart[call.message.chat.id]
            if call.message.chat.id in taste:
                del taste[call.message.chat.id]
            if call.message.chat.id in counter_id:
                del counter_id[call.message.chat.id]
            if call.message.chat.id in message_of_taste:
                del message_of_taste[call.message.chat.id]
            if call.message.chat.id in exit_cart:
                del exit_cart[call.message.chat.id]
            if call.message.chat.id in adress_delivery:
                del adress_delivery[call.message.chat.id]
            if call.message.chat.id in comment_courier:
                del comment_courier[call.message.chat.id]
            if call.message.chat.id in end_order:
                del end_order[call.message.chat.id]
            if call.message.chat.id in user_name:
                del user_name[call.message.chat.id]

    def backmenu(call):
        count_digit[call.message.chat.id] = 0
        taste[call.message.chat.id] = ''
        list_of_tastes[call.message.chat.id] = []
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        if call.message.chat.id in exit_cart:
            cart_to_str = ''
            for i in exit_cart[call.message.chat.id]:
                cart_to_str += f'{i} {str(exit_cart[call.message.chat.id][i])}\n'

            keyboardmain = types.InlineKeyboardMarkup(row_width=2)
            HQD_button = types.InlineKeyboardButton(text="HQD", callback_data="HQD")
            IZI_button = types.InlineKeyboardButton(text="IZI", callback_data="IZI")
            offer_button = types.InlineKeyboardButton(text='Оформить заказ', callback_data='order')
            clearcart_button = types.InlineKeyboardButton(text='Очистить корзину', callback_data='clearcart')
            keyboardmain.add(HQD_button, IZI_button)
            keyboardmain.add(clearcart_button)
            keyboardmain.add(offer_button)
            with open('photo/Troparevo.jpeg', 'rb') as logo:
                bot.send_photo(call.message.chat.id, logo, caption=(f"В корзине:\n{cart_to_str}"),
                               reply_markup=keyboardmain)
        else:
            keyboardmain = types.InlineKeyboardMarkup(row_width=2)
            HQD_button = types.InlineKeyboardButton(text="HQD", callback_data="HQD")
            IZI_button = types.InlineKeyboardButton(text="IZI", callback_data="IZI")
            keyboardmain.add(HQD_button, IZI_button)
            with open('photo/Troparevo.jpeg', 'rb') as logo:
                bot.send_photo(call.message.chat.id, logo, caption=("Здравствуйте!\nВыберите товар"),
                               reply_markup=keyboardmain)

    def writebase():
        a = ''
        b = ''
        c = ''
        d = ''
        for i in HQDic:
            a += HQDic[i][0] + ';'
            b += HQDic[i][1] + ';'
        for i in IZIc:
            c += IZIc[i][0] + ';'
            d += IZIc[i][1] + ';'
        with open('ink.csv', 'w') as ink:
            ink.write(a)
            ink.write('\n')
            ink.write(b)
            ink.write('\n')
            ink.write(c)
            ink.write('\n')
            ink.write(d)

    def plsminkboard(msgchtid):
        global taste
        global counter_id
        global count_digit
        global list_of_tastes
        if counter_id[msgchtid] == 1:
            backbut = "HQD"
        else:
            backbut = "IZI"
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        tastebutton = types.InlineKeyboardButton(text=taste[msgchtid], callback_data=backbut)
        rele1 = types.InlineKeyboardButton(text="+", callback_data="plus")
        rele2 = types.InlineKeyboardButton(text=str(count_digit[msgchtid]), callback_data='digid')
        rele3 = types.InlineKeyboardButton(text="-", callback_data="minus")
        cartbutton = types.InlineKeyboardButton(text="Добавить в заказ", callback_data="cart")
        keyboard.add(tastebutton)
        keyboard.add(rele1, rele2, rele3, cartbutton)
        list_of_tastes[msgchtid] = []
        return keyboard


if __name__ == "__main__":
    bot.polling(none_stop=True)
