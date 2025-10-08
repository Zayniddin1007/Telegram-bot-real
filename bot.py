from aiogram import Bot, Dispatcher, executor, types
import os

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN muhit o'zgaruvchisi topilmadi!")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def bosh_menyu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("⚽ O‘yin natijalari")
    keyboard.add("🧠 Viktorina")
    return keyboard

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("⚽ Salom! Men Real Madrid botiman!", reply_markup=bosh_menyu())

@dp.message_handler(lambda msg: msg.text == "⚽ O‘yin natijalari")
async def natija(message: types.Message):
    await message.answer(
        "🏟️ <b>So‘nggi o‘yin</b>: Real Madrid 3 - 1 Barcelona\n"
        "📅 <b>Sana</b>: 2025-04-05\n"
        "⚽ <b>To‘purarlar</b>: Vinícius (2), Bellingham\n"
        "🥇 <b>Natija</b>: G‘alaba! 🎉",
        parse_mode="HTML"
    )

VIKTORINA = [
    ("Real Madrid nechta Chempionlar Ligasi g‘alabasiga ega?", "14"),
    ("Kim 2022-yilda Ballon d’Orni qo‘lga kiritdi?", "Karim Benzema"),
    ("Santiago Bernabeu qaysi shaharda?", "Madrid"),
    ("Cristiano Ronaldo RMda nechta gol urgan?", "450"),
    ("Hozirgi kapitan kim?", "Nacho")
]

user_state = {}

@dp.message_handler(lambda msg: msg.text == "🧠 Viktorina")
async def viktorina_boshla(message: types.Message):
    user_id = message.from_user.id
    user_state[user_id] = {'savol': 0, 'to_gri': 0}
    await yubor_savol(message, user_id)

async def yubor_savol(message: types.Message, user_id):
    if user_id not in user_state:
        return
    idx = user_state[user_id]['savol']
    if idx >= len(VIKTORINA):
        to_gri = user_state[user_id]['to_gri']
        await message.answer(f"🧠 Siz {len(VIKTORINA)} savoldan {to_gri} tasiga to‘g‘ri javob berdingiz!")
        return
    savol = VIKTORINA[idx][0]
    await message.answer(f"❓ {idx+1}/{len(VIKTORINA)}: {savol}")

@dp.message_handler()
async def javob_tekshir(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_state or user_state[user_id]['savol'] >= len(VIKTORINA):
        return
    idx = user_state[user_id]['savol']
    to_gri_javob = VIKTORINA[idx][1].lower().strip()
    javob = message.text.lower().strip()
    if javob == to_gri_javob:
        await message.answer("✅ To‘g‘ri!")
        user_state[user_id]['to_gri'] += 1
    else:
        await message.answer(f"❌ Noto‘g‘ri. To‘g‘ri: {VIKTORINA[idx][1]}")
    user_state[user_id]['savol'] += 1
    await yubor_savol(message, user_id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
