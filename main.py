from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
from aiogram.types import ParseMode, InputFile

token = "6736514904:AAEBpUdXIhQKt4_5jTBfrdAGCxgtDR9qHbw"
bot = Bot(token)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_handler(message: types.Message):
    text = f"Assalamu alaykum\n\nSiz Qur'on oyatlarining tarjimasini topib beruvchi botdasiz\n\nBotdan foydalanish uchun tafsir tilini tanlang, keyin avval Sura raqamini va Oyat raqamini kiriting:\nMisol uchun: 1-4 ko'rinishida"
    await message.answer(text)


@dp.message_handler()
async def surah_handler(message: types.Message):
    try:
        text_msg = message.text
        text_msg = text_msg.split('-')
        surah = int(text_msg[0])
        ayah = int(text_msg[1])

        # editionName = 'uzb-alauddinmansour'
        editionName = 'uzb-muhammadsodikmu'
        url_res = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{editionName}/{surah}/{ayah}.json"
        res = requests.get(url_res).json()

        url_new_res = f"https://api.alquran.cloud/v1/surah/{surah}"
        new_res = requests.get(url_new_res).json()
        surah_name = new_res['data']['englishName']

        url_new_res = f"https://quranenc.com/api/v1/translation/aya/english_saheeh/{surah}/{ayah}"
        new_res = requests.get(url_new_res).json()
        arabic_text = new_res['result']['arabic_text']

        url_mp3 = f"https://api.alquran.cloud/v1/surah/{surah}/ar.alafasy"

        res_mp3 = requests.get(url_mp3).json()
        ayah_mp3 = res_mp3['data']['ayahs'][ayah - 1]['audio']
        #audio = InputFile.from_url(ayah_mp3)

        text = f"\n*Sura nomi:* {surah_name}\n\n*Oyat raqami:* {ayah}\n\n*Arabcha matni:* \n_{arabic_text}_\n\n*Tarjima:* {res['text']}"
        # await message.answer(text, parse_mode=ParseMode.MARKDOWN)
        await message.answer_audio(audio=InputFile.from_url(ayah_mp3), caption=text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await message.answer(
            f"Kechirasiz, sizning so'rovingizga ko'ra ma'lumot topilmadi\nIltimos qaytadan kiriting:\tSura_raqami-Oyat_raqami\nMasalan: 1-4")
        #await message.answer(e)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
