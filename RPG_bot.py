import random
import telebot
from telebot import types

token = '5613937045:AAH2S4Y37q_uXeOvAYXPU6QZLE8sgYXiqZk'
bot = telebot.TeleBot(token)
hp = 0
damage = 0
exp = 0
balance = 0
lvl = 1
potions = {'Здоровья': 0, 'Замедления': 0, 'Тумана': 0, 'Урона': 0}
potions_price = {'Здоровья': 17, 'Замедления': 5, 'Тумана': 13, 'Урона': 15}
plan = -1  # сможет ли сбежать игрок, выбирается рандомно; 1 - да, 2 - нет; становится 0 при применении з. Тумана
can = 1  # может ли атаковать монстр, обнуляется при применении зелья Замедления

race_db = {
    'Ангел': {'hp': 200, 'damage': 41},
    'Фея': {'hp': 126, 'damage': 74},
    'Эльф': {'hp': 150, 'damage': 65},
    'Кот': {'hp': 174, 'damage': 57}
}
prof_database = {
    'Некромант': {'hp': 35, 'damage': 15},
    'Лекарь': {'hp': 30, 'damage': 20},
    'Ведьма': {'hp': 25, 'damage': 30}
}


def reply(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton('Атаковать')
    button_2 = types.KeyboardButton('Бежать')
    button_3 = types.KeyboardButton('Использовать зелье')
    keyboard.add(button_1, button_2, button_3)
    bot.send_message(message.chat.id,
                     text=f'Вы успешно использовали зелье {message.text}', reply_markup=keyboard)


def make_prof_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for prof in prof_database.keys():
        markup.add(types.KeyboardButton(text=prof))
    return markup


def make_race_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for race in race_db:
        keyboard.add(types.KeyboardButton(text=race))
    return keyboard


def main_menu():
    global hp, damage, exp, lvl, balance
    hp = damage = exp = balance = 0
    lvl = 1
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Начать игру')
    btn2 = types.KeyboardButton('Об игре...')
    markup.add(btn1, btn2)
    return markup


def start_quest():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = 'В путь!'
    btn2 = 'Магазин'
    markup.add(btn1, btn2)
    return markup


def combat():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = 'Атаковать'
    btn2 = 'Бежать'
    btn3 = 'Использовать зелье'
    markup.add(btn1, btn2, btn3)
    return markup


def create_monster(lvl):
    rnd_name = random.choice(monster_name)
    rnd_hp = random.randint(150 * lvl, 260 * lvl)
    rnd_damage = random.randint(60 * lvl, 110 * lvl)
    rnd_cost = random.randint(10, 17)
    return [rnd_name, rnd_hp, rnd_damage, rnd_cost]


def buy(message, potion):
    global balance, potions_price, potions
    if balance >= potions_price[potion]:
        balance -= potions_price[potion]
        potions[potion] += 1
        bot.send_message(message.chat.id, text=f'Вы преобрели зелье {message.text}', reply_markup=start_quest())
    else:
        bot.send_message(message.chat.id, text='Вам не хватило денег(\n'
                                               'P.S. Надеюсь в жизни такого не было', reply_markup=start_quest())


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Начать игру!')
    button2 = types.KeyboardButton('Об игре...')
    button3 = types.KeyboardButton('Магазин')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, text='Приветствую!! Вы готовы начать игру?', reply_markup=keyboard)


def potionkeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton('Атаковать')
    button_2 = types.KeyboardButton('Бежать')
    button_3 = types.KeyboardButton('Использовать зелье')
    keyboard.add(button_1, button_2, button_3)
    return keyboard


@bot.message_handler(content_types=['text'])
def main(message):
    global hp, damage, exp, lvl, plan, can, potions, balance, keyboard
    global mns0, mns1, mns2, mns3  # имя, hp, урон
    # global mns1, mns2
    if message.text == 'Начать игру!':
        # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # button1 = types.KeyboardButton('Ангел')
        # button2 = types.KeyboardButton('Фея')
        # button3 = types.KeyboardButton('Эльф')
        # keyboard.add(button1, button2, button3)
        bot.send_message(message.chat.id, text='Выберите расу', reply_markup=make_race_menu())
    elif message.text == 'Об игре...':
        hp = damage = exp = balance = 0
        lvl = 1
        bot.send_message(message.chat.id, text='Это лучшая ролевая игра, которую Вы когда-лтбо видели! '
                                               'Надеюсь, она Вам понравится :3')
    if message.text == 'Ангел':
        hp += race_db['Ангел']['hp']
        damage += race_db['Ангел']['damage']
        img = open('img/Angel.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        bot.send_message(message.chat.id,
                         text=f'Вы умопомрачительный ангел!\nВаше здоровье = {hp}, a ваш урон = {damage}.'
                              f'\nВыберите профессию', reply_markup=make_prof_menu())

    elif message.text == 'Фея':
        hp += race_db['Фея']['hp']
        damage += race_db['Фея']['damage']
        img = open('img/Fairy.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        bot.send_message(message.chat.id, text=f'Вы прекраснейшая фея!\nВаше здоровье = {hp}, a ваш урон = {damage}.'
                                               f'\nВыберите профессию', reply_markup=make_prof_menu())
    elif message.text == 'Эльф':
        hp += race_db['Эльф']['hp']
        damage += race_db['Эльф']['damage']
        img = open('img/Elf.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        bot.send_message(message.chat.id, text=f'Вы велиполепный эльф!\nВаше здоровье = {hp}, a ваш урон = {damage}.'
                                               f'\nВыберите профессию', reply_markup=make_prof_menu())
    elif message.text == 'Кот':
        hp += race_db['Кот']['hp']
        damage += race_db['Кот']['damage']
        img = open('img/Cat.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        bot.send_message(message.chat.id, text=f'Вы милейший котик!\nВаше здоровье = {hp}, a ваш урон = {damage}.'
                                               f'\nВыберите профессию', reply_markup=make_prof_menu())

    if message.text == 'Некромант':
        hp += prof_database['Некромант']['hp']
        damage += prof_database['Некромант']['damage']
        img = open('img/Necromancer.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        bot.send_message(message.chat.id,
                         text=f'Вы вмогилуположительный неромант!\nВаше здоровье = {hp}, a ваш урон = {damage}.'
                              f'\nВперед к приключениям', reply_markup=start_quest())
    elif message.text == 'Лекарь':
        hp += prof_database['Лекарь']['hp']
        damage += prof_database['Лекарь']['damage']
        img = open('img/Doctor.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        bot.send_message(message.chat.id, text=f'Вы лекарь на все руки!\nВаше здоровье = {hp}, a ваш урон = {damage}.'
                                               f'\nВперед к приключениям', reply_markup=start_quest())
    elif message.text == 'Ведьма':
        hp += prof_database['Ведьма']['hp']
        damage += prof_database['Ведьма']['damage']
        img = open('img/Witch.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        bot.send_message(message.chat.id,
                         text=f'Вы многочегомогущая ведьма!!\nВаше здоровье = {hp}, a ваш урон = {damage}.'
                              f'\nВперед к приключениям', reply_markup=start_quest())
    if message.text == 'В путь!':
        event = random.randint(0, 1)
        if event == 0:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            bot.send_message(message.chat.id,
                             text=f'Пока никто не встретился.'
                                  f'\nИдем дальше?', reply_markup=keyboard)
        else:
            mns0, mns1, mns2, mns3 = create_monster(lvl)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_1 = types.KeyboardButton('Атаковать')
            button_2 = types.KeyboardButton('Бежать')
            button_3 = types.KeyboardButton('Использовать зелье')
            keyboard.add(button_1, button_2, button_3)
            img = open(f'img/{mns0}.jpg', 'rb')
            bot.send_photo(message.chat.id, img)
            bot.send_message(message.chat.id,
                             text=f'А вот и монстр! Его имя {mns0}.\nУ него здоровья {mns1}, '
                                  f'урон {mns2}\nНадеюсь, он Вам понравится', reply_markup=keyboard)
    elif message.text == 'Магазин':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Здоровья')
        button2 = types.KeyboardButton('Замедления')
        button3 = types.KeyboardButton('Урона')
        button4 = types.KeyboardButton('Тумана')
        button5 = types.KeyboardButton('Инфо')
        button6 = types.KeyboardButton('Выйти')
        keyboard.add(button1, button2, button3, button4, button5, button6)
        bot.send_message(message.chat.id, text='Какое зелье вы хотели бы приобрести?\n'
                                               'Зелье Урона - 15 карт\n'
                                               'Зелье Тумана - 13 карт\n'
                                               'Зелье Здоровья - 17 карт\n'
                                               'Зелья Замедления - 5 карт\n'
                                               'Если не знаете, как они действуют, нажмите "Инфо"',
                         reply_markup=keyboard)
    if message.text == 'Инфо':
        bot.send_message(message.chat.id, text='Зелье Урона наносит урон монстру равный пятикратному уровню\n'
                                               'Зелье Тумана позволяет сбежать от монстра со стопроцентоной '
                                               'вероятностью\n'
                                               'Зелье Здоровья восстанавливает количество очков жизни, раных '
                                               'пятикратному уровню\n'
                                               'Зелье Замедления останавливает одну атаку монстра')
    elif message.text in ['Здоровья', 'Замедления', 'Тумана', 'Урона']:
        buy(message, potion=message.text)
    elif message.text == 'Выйти':
        bot.send_message(message.chat.id, text=f'Вы вышли из магазина.',
                         reply_markup=start_quest())
    if message.text == 'Атаковать':
        mns1 -= damage
        if mns1 <= 0:
            exp += 10 * lvl
            balance += mns3
            if exp >= lvl * 30:
                lvl += 1
                hp += 25 * lvl
                damage += 15 * lvl
                bot.send_message(message.chat.id,
                                 text=f'Твой уровень повысился. Теперь у тебя {lvl} уровень\nТвое здоровье: {hp}, '
                                      f'твой урон: {damage}')
            bot.send_message(message.chat.id,
                             text=f'Враг повержен! За это ты получаешь {10 * lvl} очков опыта и {mns3} карт, теперь у '
                                  f'тебя {exp} очков и {balance} карт.\n'
                                  f'Идем дальше?', reply_markup=start_quest())
        elif mns1 > 0:
            hp -= mns2 * can
            if can == 1:
                bot.send_message(message.chat.id,
                                 text='Монстр атакует!\n'
                                      'P.S. Надеюсь, Вам понравится XD')
            elif can == 0:
                can = 1
                bot.send_message(message.chat.id, text='Монстра остановило зелье Замедления')
            if hp <= 0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                bot.send_message(message.chat.id,
                                 text='Вы были бравым воином, но погибли...\nНапишите "/start", чтобы попробовать '
                                      'заново')
                bot.send_message(message.chat.id,
                                 text='Победа осталась за монстром(', reply_markup=main_menu())
            elif hp > 0:
                bot.send_message(message.chat.id,
                                 text=f'Теперь у многоуважаемого монстра {mns1} очков здоровья и {mns2} урона.\n'
                                      f'У Вас {hp} очков здоровья.\n Что будете делать?', reply_markup=combat())
    elif message.text == 'Бежать':
        if plan != 0:
            plan = random.randint(1, 2)
        if plan == 1:
            bot.send_message(message.chat.id, text=f'Вы сумели сбежать от монстра! Продожаем путешествие?',
                             reply_markup=start_quest())
        elif plan == 0:
            plan = -1
            bot.send_message(message.chat.id, text=f'Вы сумели сбежать от монстра с помощью зелья Тумана!'
                                                   f'Продожаем путешествие?',
                             reply_markup=start_quest())
        elif plan == 2:
            hp -= mns2
            bot.send_message(message.chat.id, text=f'О ужас! Побег не удался и монстр атакаует!')
            if hp <= 0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                bot.send_message(message.chat.id,
                                 text='Вы были бравым воином, но погибли...\nНапишите "/start", чтобы попробовать '
                                      'заново')
                bot.send_message(message.chat.id,
                                 text='Победа осталась за монстром(', reply_markup=main_menu())
            elif hp > 0:
                bot.send_message(message.chat.id, text=f' Теперь у многоуважаемого монстра {mns1} '
                                                       f'очков здоровья и {mns2} урон, а у Вас {hp} очков здоровья. '
                                                       f'Что будете делать?',
                                 reply_markup=combat())
    elif message.text == 'Использовать зелье':
        counthp = potions['Здоровья']
        countdem = potions['Урона']
        countslow = potions['Замедления']
        countfog = potions['Тумана']
        if counthp + countfog + countdem + countslow == 0:
            bot.send_message(message.chat.id, text='У вас нет зельев :(',
                             reply_markup=potionkeyboard())
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('Здoровья')
            button2 = types.KeyboardButton('Зaмедления')
            button3 = types.KeyboardButton('Урoна')
            button4 = types.KeyboardButton('Тумaна')
            button5 = types.KeyboardButton('Bыйти')
            keyboard.add(button1, button2, button3, button4, button5)
            bot.send_message(message.chat.id, text='Что бы Вы хотели использовать?', reply_markup=keyboard)

    if message.text == 'Здoровья':
        if potions['Здоровья'] > 0:
            hp += 5 * lvl
            potions['Здоровья'] -= 1
            reply(message)
        else:
            bot.send_message(message.chat.id, text='У вас нет зелья Здоровья :(',
                             reply_markup=potionkeyboard())
    elif message.text == 'Урoна':
        if potions['Урона'] > 0:
            mns1 -= 5 * lvl
            potions['Урона'] -= 1
            reply(message)
        else:
            bot.send_message(message.chat.id, text='У вас нет зелья Урона :(',
                             reply_markup=potionkeyboard())
    elif message.text == 'Тумaна':
        if potions['Тумана'] > 0:
            plan = 0
            potions['Тумана'] -= 1
            reply(message)
        else:
            bot.send_message(message.chat.id, text='У вас нет зелья Тумана :(',
                             reply_markup=potionkeyboard())
    elif message.text == 'Зaмедления':
        if potions['Замедления'] > 0:
            can = 0
            potions['Замедления'] -= 1
            reply(message)
        else:
            bot.send_message(message.chat.id, text='У вас нет зелья Замедления :(',
                             reply_markup=potionkeyboard())
    elif message.text == 'Bыйти':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton('Атаковать')
        button_2 = types.KeyboardButton('Бежать')
        button_3 = types.KeyboardButton('Использовать зелье')
        keyboard.add(button_1, button_2, button_3)
        bot.send_message(message.chat.id, text='Вы решили не использовать зелья...',
                         reply_markup=keyboard)


monster_name = ['Шоколадный заяц', 'Резиновая уточка - убийца', 'Иван Грозный', 'Дама черви', 'Разбойник',
                'Гоголь-моголь', 'Мстя', 'Дилер', 'Стоматолог', '10 копеек', 'Пельмешка', 'Опричник',
                'Каракуля',
                'Цуцик', 'Боевой стул', 'Сессия']

bot.polling(non_stop=True)
