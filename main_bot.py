######################################################################################################################
# Программа "Заброшенный дом"
# Разработана для ItFest 2021
######################################################################################################################

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from enumes import Location
from engine import GameEngine
from texts import help_text


TOKEN = '1749159339:AAFE1Fh8MBYn5oxEsYVX6TOI9MPDvcHSvuI'

bot = Bot(token=TOKEN)

dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def process_help_command(msg: types.Message):
    await msg.reply(help_text)


@dp.message_handler(commands=['restart'])
async def process_start_command(msg: types.Message):
    await bot.send_photo(msg.from_user.id, photo=open('static/house.jpg', 'rb'))
    await bot.send_message(msg.from_user.id, help_text)
    user = GameEngine(bot, msg.from_user.id, msg.from_user.first_name)
    await user.start_game()


@dp.message_handler(commands=['info'])
async def process_start_command(msg: types.Message):
    user = GameEngine(bot, msg.from_user.id, msg.from_user.first_name)
    await user.my_info()


@dp.message_handler(commands=['loot'])
async def process_start_command(msg: types.Message):
    user = GameEngine(bot, msg.from_user.id, msg.from_user.first_name)
    await user.my_loot()


@dp.message_handler()
async def bot_messaging(msg: types.Message):
    user = GameEngine(bot, msg.from_user.id, msg.from_user.first_name)

    if user.current_location == Location.none:
        await msg.reply(help_text)
        await user.start_game()
        return

    if await user.get_next_location(msg):
        await user.run_next_location()


if __name__ == '__main__':
    executor.start_polling(dp)
