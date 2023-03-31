import telebot
from telebot import types
import sqlite3
import random

from telebot.types import ReplyKeyboardRemove

import config

bot = telebot.TeleBot("6272826586:AAFOF5CqpjYnNbngm0jE2G5NlbH7pMhtiSQ")
bot.send_message('354398142', 'Alive /start')
print('Бот запущен!')
connection = None
randlist = random.sample(range(1, 21), k=20)
guessed = 0
loosed = 0
stage = 0


def get_connection():
    global connection
    if connection is None:
        connection = sqlite3.connect('main.db', check_same_thread=False)
    return connection


def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS questions')
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions(
        id        INTEGER PRIMARY KEY AUTOINCREMENT
                  UNIQUE,
        text      TEXT NOT NULL,
        first     TEXT NOT NULL,
        second    TEXT,
        third     TEXT,
        fourth    TEXT,
        correct   TEXT NOT NULL
        )
    ''')
    conn.commit()


def getrandquiz():
    conn = get_connection()
    c = conn.cursor()
    global randlist
    randid = randlist.pop()
    get_rand_quiz_sql = 'SELECT * FROM questions WHERE id = ?'
    c.execute(get_rand_quiz_sql, (randid,))
    quiz_sql = c.fetchone()
    # (2, 'Мое любимое блюдо в маке?', 'Биг мак', 'Биг тейсти', 'Дабл роял чизбургер', 'Наггетсы', 'Биг тейсти')
    quiz = {
        'quest_id': quiz_sql[0],
        'question_text': quiz_sql[1],
        'first_ans': quiz_sql[2],
        'second_ans': quiz_sql[3],
        'third_ans': quiz_sql[4],
        'fourth_ans': quiz_sql[5],
        'correct_ans': quiz_sql[6]
    }
    # print(quiz)  # TODO: Убрать
    return quiz


@bot.message_handler(commands=['start'])
def start(message):
    if stage == 0:
        if message.chat.id == 354398142 or message.chat.id == 450940602:
            bot.send_message(message.chat.id, 'Привет Тасюник, этот бот поможет тебе в решении моих загадок\n'
                                              'Раз ты нашла этого бота, значит ты смогла решить первую мою загадку\n'
                                              'Я тебя подзравляю, умничка!')
            bot.send_message(message.chat.id, 'И так, начнем с самого простого, небольшой тест)\n'
                                              'Набери 8 правильных ответов что-бы продолжить!')
            bot.send_message(354398142, 'Начался квест с вопросами')
            main(message)
        else:
            bot.send_message(message.chat.id, 'Бот создан не для вас')
    else:
        bot.send_message(message.chat.id, 'Начинать заново нельзя)')


def main(message):
    if stage == 0:
        quizes(message)
    if stage == 1:
        bot.send_message(354398142, 'Тася дошла до 1 стадии с майа')
        maya(message)
    if stage == 2:
        bot.send_message(354398142, 'Тася дошла до 2 стадии с детек')
        dethek(message)
        # TODO: В книге нарисовать символы языка детека
    if stage == 3:
        bot.send_message(message.chat.id, 'Это последний квест для тебя!')
        bot.send_message(message.chat.id, 'Кажется кто-то спрятал его у тебя в комнате')
        bot.send_message(message.chat.id, 'Если будет сильно трудно, обратись за помощью к Наде')


def quizes(message):
    quiz = getrandquiz()
    ReplyMarkup(message, text=quiz['question_text'], first=quiz['first_ans'], second=quiz['second_ans'],
                third=quiz['third_ans'], fourth=quiz['fourth_ans'], correct=quiz['correct_ans'])


def maya(message):
    bot.send_message(message.chat.id, 'Тебе предстоит разгадать загадку!')
    photo = open('maya.png', 'rb')
    bot.send_photo(message.chat.id, photo)


def dethek(message):
    bot.send_message(message.chat.id, 'Окей, эта загадка будет интереснее!')
    photo = open('dethek.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, 'Тебе прийдется вернуться к книге, на страницах есть спрятанные символы\n'
                                      'Тебе нужно найти их и расшифровать с помощью этой таблицы')


@bot.message_handler(content_types=['text'])
def check_answer(message):
    global stage
    if stage == 1:
        if message.text == '17082021':
            stage = 2
            bot.send_message(message.chat.id, 'Совершенно верно!')
            main(message)
        else:
            bot.send_message(message.chat.id, 'Не правильно)')
    elif stage == 2:
        text = message.text.lower()
        if text == 'infinity':
            stage = 3
            bot.send_message(message.chat.id, 'Отлично, ответ правильный)\nТы ещё на шаг ближе к цели!')
            main(message)
        else:
            bot.send_message(message.chat.id, 'Извини, но ответ не правильный')


class ReplyMarkup:
    global stage

    def __init__(self, message, text=None, first=None, second=None, third=None, fourth=None, correct=None,
                 force_clear: [bool] = False):
        self.text = text
        self.force_clear = force_clear
        self.First = first
        self.Second = second
        self.Third = third
        self.Fourth = fourth
        self.chat_id = message.chat.id
        self.correct = correct
        self.markup()

    def markup(self):
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        if self.First is not None and self.Second is not None and self.Third is not None and self.Fourth is not None:
            itembtn1 = types.KeyboardButton(self.First)
            itembtn2 = types.KeyboardButton(self.Second)
            itembtn3 = types.KeyboardButton(self.Third)
            itembtn4 = types.KeyboardButton(self.Fourth)
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        elif self.First is not None and self.Second is not None and self.Third is not None:
            itembtn1 = types.KeyboardButton(self.First)
            itembtn2 = types.KeyboardButton(self.Second)
            itembtn3 = types.KeyboardButton(self.Third)
            markup.add(itembtn1, itembtn2, itembtn3)
        elif self.First is not None and self.Second is not None:
            itembtn1 = types.KeyboardButton(self.First)
            itembtn2 = types.KeyboardButton(self.Second)
            markup.add(itembtn1, itembtn2)
        elif self.First is not None:
            itembtn1 = types.KeyboardButton(self.First)
            markup.add(itembtn1)
        msg = bot.send_message(self.chat_id, self.text, reply_markup=markup)
        bot.register_next_step_handler(msg, self.check)

    def check(self, message):
        global loosed
        global guessed
        global stage
        if message.text == self.correct:
            guessed += 1
            if guessed < 8:
                bot.send_message(message.chat.id, config.nice[guessed])
                bot.send_message(354398142, f'QUIZ: Ещё один правильный ответ, текущее количество: {guessed}')
                main(message)
            else:
                bot.send_message(message.chat.id, 'Поздравляю, ты прошла первую часть)',
                                 reply_markup=ReplyKeyboardRemove())
                stage = 1
                bot.send_message(354398142, f'QUIZ: Закончен, количество правильных/неправильный: {guessed}/{loosed}')
                main(message)
        else:
            loosed += 1
            bot.send_message(354398142, f'QUIZ: Ещё одна ошибка, текущее количество: {loosed}')
            bot.send_message(message.chat.id, config.bads[loosed])
            main(message)


bot.polling(none_stop=True)

# bot.send_message(message.chat.id, 'Поздравляю, ты победила!')
# photo = open('qr-code.png', 'rb')
# bot.send_photo(message.chat.id, photo)
# bot.send_message(message.chat.id, 'Сканируй!')
