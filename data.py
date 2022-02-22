######################################################################################################################
# Программа "Заброшенный дом"
# Разработана для ItFest 2021
######################################################################################################################

import random

from enumes import Location, TypeLocation
from texts import TextFinal, TextNotGoodEnd, TextGoodEnd

######################################################################################################################
# Engine Data

# Основное описание локаций, в зависимости от типа локации могут иметь переменную длину списка с параметрами
# {ключ = [тип локации, текст, варианты исхода, данные для квестов (необязательно)]}
# Локация типа place - просто описывает место и предлагает варианты выходов
# Локация типа quest - иемет только один выход, но выйти можно решив только задачу или остаться там умирать с голоду
# Локация типа test - иемет 2 выхода, но выход выбирает не пользователь, а "одноименная" функция (скрипт)
#                 для упрошщения тело скрипта вынесено из GameData, хотя можно было его вызвать через eval полностью

GameData = {
    Location.front_of_house: [
        TypeLocation.place,
        '''
    Вот Я перед домом.
    Дом действительно очень старый и не менее страшный.
    Дааа, и тут мне придётся ночевать.
    
    Мне нужно решить, что мне делать:
        1) Попытаться войти в дом.
        2) Обойти дом по кругу.''',
        [Location.first_floor_quest, Location.next_house]],

    Location.first_floor_quest: [
        TypeLocation.quest,
        'На двери замок!',
        [Location.first_floor], ['Надо вскрыть замок:', '(2 + 3) * 5 - 2 = x', '23', 'x = ']],

    Location.next_house: [
        TypeLocation.place,
        '''
    Я нахожусь около дома, под окном на второй этаж.
    %rnd%
    Тут очень сыро и холодно 🥶.
    Я вижу что к окну идут лианы!
    
    Мне нужно решить, что мне делать:
        1) Попытаться залезть на второй этаж.
        2) Подойти ко входу в дом.''',
        [Location.first_room_quest, Location.front_of_house]],

    Location.first_room_quest: [
        TypeLocation.quest,
        '''
    Квест: Некоторые лианы засохли!
    Надо найти свежие лианы.''',
        [Location.first_room_test_inner], ['Найди закономерность!\nВставь вместо пропусков ответ:',
                                           '101100111000____0000', '1111', '____ = ']],

    Location.first_floor: [
        TypeLocation.place,
        '''
    Я на первом этаже этого дома.
    Надо тут осмотреться, убедиться в безопасности дома, как ночлега. 😴
    Ливень снаружи, к сожалению, всё никак не прекращался.
    
    Мне нужно решить, что мне предпринять:
        1) Подняться на второй этаж.
        2) Посмотреть что есть в подвале.
        3) Зайти в комнату похожую на кухню.
        4) Выйти из дома.''',
        [Location.second_floor_1, Location.basement_test_inner, Location.kitchen_test_slingshot,
         Location.front_of_house]],

    Location.second_floor_1: [
        TypeLocation.place,
        '''
    Я на втором этаже этого странного дома.
    Но тут более приятное место для ночлега.
    %rnd%
    Надо осмотреть каждую комнату этого этажа.
    
    Мне нужно решить, куда мне пойти:
        1) Попытаться зайти в 1-ую комнату.
        2) Попытаться зайти во 2-ую комнату.
        3) Попытаться зайти в 3-ую комнату вроде "самую уютную".
        4) Спуститься на первый этаж.''',
        [Location.first_room_test, Location.second_room, Location.final_room_test, Location.first_floor]],

    Location.second_floor_2: [
        TypeLocation.place,
        '''
    Второй этаж этого "неблагоприятного" дома.
    %rnd%
    
    Мне нужно решить, куда мне пойти:
        1) Попытаться зайти в 1-ую комнату.
        2) Попытаться зайти во 2-ую комнату.
        3) Попытаться зайти в 3-ую комнату вроде "самую уютную".
        4) Спуститься на первый этаж.''',
        [Location.first_room_test, Location.second_room, Location.final_room_test, Location.first_floor]],

    Location.final_room_test: [
        TypeLocation.test,
        '   Здесь замок, для которого нужно 2 ключа!',
        [Location.final_room_quest, Location.second_floor_2]],

    Location.final_room_quest: [
        TypeLocation.quest,
        '\tКвест: Осталось подобрать ключи\n\tНадо только узнать как?',
        [Location.final_room_test_inner], ['\tДля этого реши систему уравнений:',
                                           '\t2k + x = 1\nk + y = 13\ny + x = 2\n2k = ...', '8', '2k = ']],

    Location.first_room_test: [
        TypeLocation.test,
        '   Эта комната заперта с другой стороны!',
        [Location.first_room_test_inner, Location.second_floor_2]],

    Location.first_room_test_inner: [
        TypeLocation.test,
        '',
        [Location.first_room_2, Location.first_room_quest_open]],

    Location.first_room_quest_open: [
        TypeLocation.quest,
        '''
    в этой комнате в первый раз. Она необычная и немного жутковатая!
    В большом шкафу Я нашёл мистическую "математическую" шкатулку.
    Квест: Хорошо, что Я люблю математику!''',
        [Location.first_room_1],
        ['Откроем её!', 'x = sin(30) * 4', '2', 'x = '],
        'Здесь лежит ключ!',
        True],

    Location.first_room_1: [
        TypeLocation.place,
        '''
    Мне нужно решить, что мне делать:
        1) Попытаться слезть по лиане с окна на улицу!
        2) Выйти в коридор второго этажа.''',
        [Location.next_house, Location.second_floor_1]],

    Location.first_room_2: [
        TypeLocation.place,
        '''
    В этой комнате Я уже всё осмотрел и открыл шкатулку.
    Зачем я хожу кругами?
    %rnd%
    Надо действовать быстрее, а то Я здесь буду до утра всё проверять!
    
    Мне нужно решить, что мне делать:
        1) Попытаться слезть по лиане с окна на улицу!
        2) Выйти в коридор второго этажа.''',
        [Location.next_house, Location.second_floor_1]],

    Location.second_room: [
        TypeLocation.place,
        '''
    Эта комната открылась довольно дружелюбно.
    Комната была небольшая, но здесь была лестница на чердак.
    
    %rnd%
    
    В комнате Я не нашёл ни одной вещи, которая мне могла бы пригодиться.
    Тут-же Я заметил, что крыжа протекает, так себе ночлег!
    
    Мне нужно решить, куда идти:
        1) Подняться на чердак.
        2) Вернуться обратно в коридор.''',
        [Location.attic, Location.second_floor_1]],

    Location.attic: [
        TypeLocation.place,
        '''
    Пока Я лез на пыльный чердак, наглотался паутины 🕸!
    %rnd%
    Тут было довольно просторно.
    Надо изучить всё пространство.
    
    Мне нужно решить, что мне делать:
        1) Спустится обратно, через пауков 🕷.
        2) Вылезть через щель в 1-ую комнату.
        3) Зайти в дальний конец чердака.''',
        [Location.second_room, Location.first_room_test_inner, Location.attic_test_inner]],

    Location.attic_test_inner: [
        TypeLocation.test,
        '',
        [Location.attic_down]],

    Location.attic_down: [
        TypeLocation.place,
        '''
    В чердаке оказалась "пробоина", Я громко свалился на первый этаж.
    Когда пришёл в сознание, всё ужасно болело, мне было страшно.
    Хорошо, что Я выжил после такого. Ведь мог бы и не выжить!''',
        [Location.first_floor]],

    Location.basement_test_inner: [
        TypeLocation.test,
        '',
        [Location.basement_2, Location.basement_quest]],

    Location.basement_quest: [
        TypeLocation.quest,
        '''
    Вот я уже в тёмном подвале этого дома.
    %rnd%
    Тут уж точно место не для ночлега.
    
    Стоп, тут есть какая-то шкатулка.''',
        [Location.basement_1],
        ['Эта шкатулка хитро закрыта, попробую открыть:', '2x + 3 = 3x - 4\nx = ...', '7', 'x = '],
        '\tВ шкатулке был ключ! Возьму вдруг пригодиться.',
        True],

    Location.basement_1: [
        TypeLocation.place,
        '''
    Мне нужно решить, что мне делать дальше:
    1) Вернуться в этот дом.
    2) Вылезть через маленькое окно в подвале "Попытаться".''',
        [Location.first_floor, Location.small_window_quest]],

    Location.basement_2: [
        TypeLocation.place,
        '''
    Вот я уже в тёмном подвале этого дома.
    %rnd%
    Тут уж точно место не для ночлега.
        
    Эту шкатулку я уже видел!
    Зачем я хожу кругами?
    
    Мне нужно решить, что мне делать дальше:
        1) Вернуться в этот дом.
        2) Вылезть через маленькое окно в подвале "Попытаться".''',
        [Location.first_floor, Location.small_window_quest]],

    Location.small_window_quest: [
        TypeLocation.quest,
        ''' 
    Ну что-ж, попытка не пытка! Надеюсь)''',
        [Location.next_house], ['Надо пролезть, подбери минимальное значение:',
                                'Минимальное "n" если (n > 16) и (n - чётное число)', '16', 'n = '],
        '\tНаконец-то!'],  # 'min(n) if n > 14 and n % 2 == 0'

    Location.kitchen_test_slingshot: [
        TypeLocation.test,
        '',
        [Location.kitchen_1, Location.kitchen_2]],

    Location.kitchen_1: [
        TypeLocation.place,
        '''
    А вспомнил, я тут уже был и взял рогатку, возвращаемся обратно.
      ''',
        [Location.first_floor]],

    Location.kitchen_3: [
        TypeLocation.place,
        '''
    Остается только вернуться в хол и поискать ключ.
      ''',
        [Location.first_floor]],

    Location.kitchen_4: [
        TypeLocation.place,
        '''
    Ящик открылся, я был сильно напуган увидев череп какого-то лесного животного-хищника,
    Ещё тут было много тараканов и пахло не очень. Зато тут была хорошая рогатка.
    Она была стальная с бронзовыми шариками-снарядами, ладно возьму с собой.
    Тут где-то в доме упала стеклянная ваза. Может это крысы бегают по столам?
    Возвращаемся в комнату, тут больше делать нечего.
      ''',
        [Location.first_floor]],

    Location.kitchen_2: [
        TypeLocation.place,
        '''
    Я зашёл в комнату, похожую на кухню.
    Выглядела она ужасно, везде пахло гноем.
    Во всей комнате не было ничего дельного.
    Комната была пуста, хоть тут и было много различных шкафов!
    Один, кстати, закрыт, может хоть в нём что-то есть!
    %rnd%
    
    Похоже придётся возвращаться или ... :
        1) Вернуться обратно.
        2) Осмотреть шкаф.   ''',
        [Location.first_floor, Location.kitchen_test_key]],

    Location.kitchen_test_key: [
        TypeLocation.test,
        '''
    Упс. Шкаф закрыт! Мне нужен ключ для шкафа.''',
        [Location.kitchen_quest, Location.kitchen_3]],

    Location.kitchen_quest: [
        TypeLocation.quest,
        '''
    У меня как-раз есть отмычка, придётся потрудиться!''',
        [Location.kitchen_4],
        ['Надо настроить нашу отмычку!', '|(4 * 2 - 6) ** 3 - 3| * 111 = ...', '555', 'Ответ: '],
        '',
        True],
    # ['Надо настроить отмычку под форму замка:"_" - пропуск, а "|" - палочка!',
    #     'Замок:  ________________________\n            |  ||  ||  ||| | || ',  # Не работает!!!
    #     '_||__||__||___|_|__|', 'Ключик: ____', True],

    Location.final_room_test_inner: [
        TypeLocation.test,
        '',
        [Location.final_room_1, Location.final_room_2]],

    Location.final_room_1: [
        TypeLocation.place,
        TextFinal + '''
        3) Оглушить ударом снаряда рогатки,  и кинуться по лестнице на улицу! (активно - вы нашли рогатку)''',
        [Location.end_test_1, Location.end_2, Location.end_3]],

    Location.final_room_2: [
        TypeLocation.place,
        TextFinal + '''
        3) [блок] Оглушить ударом снаряда рогатки,  и кинуться по лестнице на улицу! (вы не нашли рогатку)''',
        [Location.end_test_1, Location.end_2]],

    Location.end_2: [
        TypeLocation.place,
        '''
    Я бросился, что есть мочи к выходу! Оно не отставало.
    Я вышиб старую дверь ногой и собирался бежать в лес... ''' + TextNotGoodEnd,
        [Location.end]],

    Location.end_3: [
        TypeLocation.place,
        '''
    Я не знаю как, но я "случайно" попал ему в грудь!
    Я бросился, что есть мочи к выходу! Бросив несчастную рогатку на лестнице.
    Я вышиб старую дверь ногой и собирался бежать далеко-далеко в лес...''' + TextGoodEnd,
        [Location.end]],

    Location.end_test_1: [
        TypeLocation.test,
        '',
        [Location.end_1_a, Location.end_1_b]],

    Location.end_1_a: [
        TypeLocation.place,
        '''
    Я в считанные секунды выпрыгнул в окно, думая, что это не худшее, что могло случиться!
    В эти секунды моё сердце чуть не лопнуло от страха...
    Мне кажется повезло, что под оком были кусты, смягчившие падение!
    %pause%
    Мне правда повезло! Я поранился о ветки, но мог бежать...''' + TextGoodEnd,
        [Location.end]],

    Location.end_1_b: [
        TypeLocation.place,
        '''
    Я в считанные секунды выпрыгнул в окно, думая, что это не худшее, что могло случиться!
    В эти секунды моё сердце чуть не лопнуло от страха...
    Мне кажется повезло, что под оком были кусты, смягчившие падение!
    %pause%
    Случилось худшее, что можно представить, Я упал и сломал ногу, Я обречён.
    Оно уже было у выхода!''' + TextNotGoodEnd,
        [Location.end]]
}


#############################################################################################################
# Активные тесты в локациях


async def first_room_test(user):
    return user.once_first_room


async def final_room_test(user):
    if user.keys == 0:
        await user.send("\tУ вас нет ключей, поищите в доме.")
    if user.keys == 1:
        await user.send("\tУ вас 1 ключ, поищите второй в доме.")
    return user.keys == 2


async def first_room_test_inner(user):
    if not user.once_first_room:
        user.once_first_room = True
        user.keys += 1
        # await user.my_loot()
        return False
    else:
        return True


async def attic_test_inner(user):
    if not user.master_key:
        user.master_key = True
        await user.send('\tТак, я тут нашёл "отмычку", она может пригодиться!')
        await user.send('\tМожет тут есть ещё "сокровища"?')
        await user.my_loot()
    return True


async def basement_test_inner(user):
    if not user.once_basement:
        user.once_basement = True
        user.keys += 1
        # await user.my_loot()
        return False
    else:
        return True


async def kitchen_test_slingshot(user):
    return user.slingshot


async def kitchen_test_key(user):
    if user.master_key:
        user.slingshot = True
        # await user.my_loot()
        return True
    else:
        return False


async def final_room_test_inner(user):
    return user.slingshot


async def end_test_1(user):
    return bool(random.randrange(0, 3))


async def run_eval(fn, user):
    return await eval(fn + "(user)", globals(), locals())
