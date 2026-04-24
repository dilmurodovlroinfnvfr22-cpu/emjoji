import logging
import io
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from PIL import Image, ImageDraw, ImageFont
from config import BOT_TOKEN, IS_SUBSCRIPTION_REQUIRED, CHANNEL_ID

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Majburiy obuna tekshiruvi
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status != 'left'
    except:
        return False

# Rasm -> Emoji sticker konvertori
def create_emoji_sticker(photo_bytes):
    img = Image.open(io.BytesIO(photo_bytes)).convert('RGB')
    img = img.resize((20, 20)) # Kichraytiramiz
    sticker = Image.new('RGB', (512, 512), color='white')
    draw = ImageDraw.Draw(sticker)
    
    # Oddiy emoji mapping (yorqinlikka qarab)
    emojis = ['🌑', '🌚', '🌝', '⚪']
    
    for y in range(20):
        for x in range(20):
            r, g, b = img.getpixel((x, y))
            brightness = (r + g + b) / 3
            emoji = emojis[int(brightness / 64)]
            draw.text((x * 25, y * 25), emoji, fill='black')
            
    output = io.BytesIO()
    sticker.save(output, format='WEBP')
    output.seek(0)
    return output

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Salom! Rasm yuboring, uni emoji-stickerga aylantirib beraman.")

@dp.message(F.photo)
async def photo_handler(message: types.Message):
    # Majburiy obuna tekshiruvi
    if IS_SUBSCRIPTION_REQUIRED:
        if not await check_sub(message.from_user.id):
            await message.answer(f"Botdan foydalanish uchun {CHANNEL_ID} ga obuna bo'ling!")
            return

    # Rasmni yuklash
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    
    buffer = io.BytesIO()
    await bot.download_file(file.file_path, buffer)
    buffer.seek(0)
    
    # Sticker yaratish
    sticker_buffer = create_emoji_sticker(buffer.read())
    
    await message.answer_sticker(sticker=types.BufferedInputFile(sticker_buffer.read(), filename="sticker.webp"))

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
