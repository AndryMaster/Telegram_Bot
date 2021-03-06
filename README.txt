Об игре
Основная цель создать игру в виде чат-бота Telegram. Свою игру я назвал “Страшный дом”. Это хорор игра, в которой вы заблудились в мрачном лесу и решаете укрыться в старом заброшен-ном доме, заодно исследуя его мрачные комнаты и решая разные загадки и ребусы.
В этой игре 10 локаций-комнат, по которым можно перемещаться, некоторые из них закры-ты и вам нужно будет найти ключи в доме или как-то туда попасть, а в некоторые чтобы попасть надо будет решить задачку-квест, их в игре целых 6 штук, поэтому будет не скучно. В игре есть иг-ровые предметы 2 ключа, 1 мастер ключ и рогатка, так же игре есть разные варианты завершения – хороший и плохой.

Реализация
Для создания бота использован язык программирования Python и 3 сторонние библиотеки:
•	Aiogram – библиотека для создания бота в Telegram.
•	SQLite(sqlite3) – не сложная, удобная база данных, в самый раз для этого проекта.
При переделке игры из первого этапа пришлось разделить логику игры и содержимое, по-тому что вопрос игроку и ответ на него разделены во времени, использовать код первой игры не получилось. Главные данные для игры получилось оформить в виде большого словаря, где ключ — это код локации, а значение это кортеж с параметрами, описывающими место.

Может быть 3 вида локаций:
•	Место – это просто развилка, например комната с не сколькими выходами и нужно пользователю выбрать вариант
•	Квест – это место с одним входом, одним выходом (например дверь, или отрываем шкатулку), но для продвижения нужно решить задачу.
•	Тест – это развилка (ветвление) где функция на основании игровых предметов, выбира-ет дальнейший путь.

Для удобства разработки проект разбит на несколько файлов:
•	main_bot.py – стартовый файл игры для бота, с помощь его происходит запуск игры.
•	engine.py – движок игры совмещённый с информацией о пользователе, отвечает за иг-ровой процесс. Он отвечает за работу с данными пользователя и сохранением из БД. А также содержит две самых главных функции:
o	get_next_location - на основании сообщения от пользователя выбирает индекс следующей локации
o	run_next_location – используя данные из главного словаря с настройками выдает сообщение пользователю соответствующее текущей локации
•	enumes.py – перечисления для удобства работы со словарём локаций.
•	data.py – главный словарь – описывающий места действия и их свойства.
•	texts.py –большие тексты блоки из сюжета, для удобства отделены от словаря.
