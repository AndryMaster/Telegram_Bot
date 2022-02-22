######################################################################################################################
# Программа "Заброшенный дом"
# Разработана для ItFest 2021
######################################################################################################################

TOKEN = '1749159339:AAFE1Fh8MBYn5oxEsYVX6TOI9MPDvcHSvuI'

t = '''Замок:  ________________________
                    |  ||  ||  ||| | ||'''

from emoji import emojize


class Emoji:  # Не работает!!!
    spider = emojize(':spider:')
    spider_web = emojize(':spider_web:')
    thunder_cloud = emojize(':thunder_cloud_and_rain:')
    rain = emojize(':sweat_drops:')
    mouse = emojize(':mouse:')
    moon = emojize(':full_moon:')
    hand_right = emojize(':point_right:')
    sleep = emojize(':sleeping:')

    freeze = '🥶'

def format_text(text):
    res = []
    for string in text.split('\n'):
        s = ''
        for i in range(len(string)):
            if string[i].isdigit():
                s = '\t' + string[i:]
                break
            if string[i].isalpha():
                s = string[i:]
                break
        res.append(s)
    return '\n'.join(res)


texti = '''
Это игра в которой вам предстоит иследовать двух этажный дом, где нужно исследовать все комнаты.
  Двери могут быть заперты на замки, ключи от которых потребуеться вам найти.

Основные команды:
1) "/start" - начинает игру сначала.
        2) "/help" - выводит эту информацию.

     В сюжетном ответе указывать только цифру ответа. Например "1" или "2".
    На мини_квесты давать нормальный ответ! (Чтобы система приняла).
Если вы не знаете ответ на миникест, то можете вместо ответа указать 
  "answer" - это чит-команда, даёт ответы на квесты;
'''

print(format_text(texti))
