import os

# Render'da "Environment Variables" qismiga BOT_TOKEN qo'shing
BOT_TOKEN = os.getenv("BOT_TOKEN", "SIZNING_TOKENINGIZ")

# Majburiy obuna sozlamalari
IS_SUBSCRIPTION_REQUIRED = False  # Buni True qilsangiz, obuna majburiy bo'ladi
CHANNEL_ID = "@sizning_kanalingiz" # Kanal username'i
