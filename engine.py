######################################################################################################################
# Программа "Заброшенный дом"
# Разработана для ItFest 2021
######################################################################################################################

import time
import random
import datetime as dt
import sqlite3
from sqlite3 import Error

from data import GameData, run_eval
from enumes import TypeLocation, Location
from texts import phrase, good_bay, start_text, my_info_text, my_loot_text


# Форматирование теста.
def format_text(text):
    res = []
    for string in text.split('\n'):
        s = string.strip()
        if len(s) == 0:
            s = ' '
        elif s[0].isdigit():
            s = ' ' * 6 + s
        res.append(s)
    res = '\n'.join(res)
    return res if len(res) > 0 else ' '


# Создание соединения с БД.
def create_connection():
    try:
        conn = sqlite3.connect("base.db")
        return conn

    except Error as e:
        print(e)
        return None


class GameEngine:
    # сколько у нас ключей
    keys = 0

    # мы уже забрали ключ из подвала?
    once_basement = False

    # мы уже забрали ключ из первой комнаты?
    once_first_room = False

    # мы уже подобрали отмычку для кухни?
    master_key = False

    # мы уже нашли рогатку?
    slingshot = False

    # запоминаем открытые замки
    complited_quests = set()

    current_location = Location.none

    count_run = 0

    count_finish = 0

    count_quest = 0

    user_id = 0
    user_name = 'Вы'

    bot = 0

    def __init__(self, bot, user_id, name):
        self.bot = bot
        self.user_name = name
        self.user_id = user_id

        # Проверяем пользователя в БД
        conn = create_connection()
        with conn:
            cur = conn.cursor()
            cur.execute('''SELECT count_run, count_finish, count_quest, location, keys, once_basement, 
                           once_first_room, master_key, slingshot, complited_quests, registration_date
                           FROM users WHERE user_id = ?''', (user_id,))
            rows = cur.fetchall()

            if len(rows) == 1:
                self.count_run = rows[0][0]
                self.count_finish = rows[0][1]
                self.count_quest = rows[0][2]
                self.current_location = Location(rows[0][3])
                self.keys = rows[0][4]
                self.once_basement = bool(rows[0][5])
                self.once_first_room = bool(rows[0][6])
                self.master_key = bool(rows[0][7])
                self.slingshot = bool(rows[0][8])
                self.complited_quests = list(map(int, str(rows[0][9]).split(', '))) if rows[0][9] != '' else []
                self.reg_date = rows[0][10]
            else:
                self.create_user(conn)

    # Начало игры при отправлении /start
    async def start_game(self):
        self.keys = 0
        self.once_basement = False
        self.once_first_room = False
        self.master_key = False
        self.slingshot = False
        self.current_location = Location.front_of_house
        self.complited_quests = list()

        await self.send("Начинаем игру!")
        time.sleep(1)

        await self.send(start_text[0])
        time.sleep(0.5)
        await self.send(start_text[1])
        time.sleep(0.5)

        await self.my_loot()
        await self.run_next_location()

    async def my_info(self):
        await self.send(my_info_text.format(self.user_name, self.reg_date, self.user_id,
                                            self.count_run, self.count_finish))

    async def my_loot(self):
        await self.send(my_loot_text.format(self.keys,
                                            'есть' if self.master_key else 'нет',
                                            'есть' if self.slingshot else 'нет'))

    async def send(self, text):
        await self.bot.send_message(self.user_id, text)

    # Завершение игры
    async def good_bay(self):
        await self.send(good_bay)
        self.count_run += 1
        self.count_finish += 1
        self.save_user()

    # Ввод ответа и перемещение на следующую локацию
    async def get_next_location(self, msg):
        location = GameData[self.current_location]
        # print("get ", location)

        type_location = location[0]
        variants = location[2]

        if type_location == TypeLocation.place:
            answer = await self.check_question(range(1, len(variants) + 1), msg)
            if answer is False:
                return False
            self.current_location = variants[answer - 1]

        if type_location == TypeLocation.quest:
            if self.current_location.value not in self.complited_quests:  # value
                self.complited_quests.append(self.current_location.value)

                params = location[3]
                if not await self.check_quest(params[2], params[3], msg):
                    return False

                await self.send("\tПолучилось!")
                if len(location) > 4 and location[4] != '':
                    await self.send(location[4])
                if len(location) == 6 and location[5] is True:
                    await self.my_loot()
                self.count_quest += 1

            self.current_location = variants[0]

        return True

    # Локации типа place - выбор выхода
    async def check_question(self, range_of, msg):
        results = list(map(str, range_of))
        if msg.text in results:
            return int(msg.text)
        else:
            await self.send('Некорректный ответ!')
            return False

    # Локации типа quest - обработка ответа
    async def check_quest(self, answer, x, msg):
        if msg.text == answer:
            return True
        elif msg.text.lower().strip() == 'answer' or msg.text.lower().strip() == 'ansver':
            await self.send('>>> Подключаем читы')
            await self.send(f'>>> Правильный ответ был: {x}{answer}')
            return True
        await self.send('\tНеверный ответ!')
        await self.send('\tПопробуйте другой ответ')
        return False

    # Печать текста локации, затем сохранение
    async def run_next_location(self):
        if self.current_location == Location.end:
            await self.good_bay()
            self.current_location = Location.none
            # await self.start_game()
            return

        location = GameData[self.current_location]
        # print("run ", location)

        type_location = location[0]

        if type_location == TypeLocation.place or \
                (type_location == TypeLocation.quest and self.current_location.value not in self.complited_quests):
            text = location[1]
            text = text.replace("%rnd%", random.choice(phrase))
            text = text.replace("%user%", self.user_name)
            texts = text.split("%pause%")
            # texts = parsing_text(text)
            for t in texts:
                await self.send(format_text(t))
                time.sleep(0.2)

        variants = location[2]

        if type_location == TypeLocation.place:
            if len(variants) == 1:
                self.current_location = variants[0]
                await self.run_next_location()
            else:
                await self.send('Введите ответ: ')

        if type_location == TypeLocation.quest:
            if self.current_location.value not in self.complited_quests:
                params = location[3]
                await self.send(params[0])
                await self.send(params[1])
            else:
                self.current_location = variants[0]
                await self.run_next_location()

        if type_location == TypeLocation.test:
            res = await run_eval(self.current_location.name, self)
            if res is True:
                self.current_location = variants[0]
            else:
                if len(location[1]) > 0:
                    await self.send(location[1])
                self.current_location = variants[1]
            await self.run_next_location()

        self.save_user()

    # Слздание новой записи в БД
    def create_user(self, conn):
        self.reg_date = dt.datetime.now().date().strftime('%Y %B-%d')
        sql = '''INSERT INTO users (user_id, name, count_run, count_finish, count_quest, location,
            keys, once_basement, once_first_room, master_key, slingshot, complited_quests, registration_date)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, (self.user_id, self.user_name, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', self.reg_date))
        conn.commit()

    # Созранение текущих результатов в БД
    def save_user(self):
        conn = create_connection()
        with conn:
            sql = ''' update users set count_run = ?, count_finish = ?, count_quest = ?, location = ?,
                keys = ?, once_basement = ?, once_first_room = ?, master_key = ?, slingshot = ?, complited_quests = ?
                where user_id = ? '''
            cur = conn.cursor()
            cur.execute(sql, (self.count_run, self.count_finish, self.count_quest, self.current_location.value,
                              self.keys, self.once_basement, self.once_first_room, self.master_key, self.slingshot,
                              ', '.join(map(str, self.complited_quests)), self.user_id))
            conn.commit()
