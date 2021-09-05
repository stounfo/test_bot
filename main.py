from aiogram import Bot, Dispatcher, executor, types
from states import state_machine, states, MachineError


TOKEN = '1847090296:AAGl6cvi9cARXupoEhrRy8QG58LCfw-ZCDM'

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler()
async def echo(message: types.Message):
    try:
        await state_machine.change_state(states.get(message.text), message)
    except MachineError:
        await message.answer("ты чото не то делаешь")
        await state_machine.change_state(states['menu'], message)


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
