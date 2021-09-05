from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def test_action(state, message):
    await message.reply('work?', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).row(
        *[KeyboardButton(state.name) for state in state.get_destinations()]
    ))
