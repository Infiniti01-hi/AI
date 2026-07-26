import os
import telebot
from flask import Flask, request

# Получаем токены из переменных окружения
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(message, "Здравствуйте, чем могу помочь?")


# Обработчик обычных текстовых сообщений
@bot.message_handler(content_types=["text"])
def handle_text(message):
  # Здесь можно добавить логику ответа от Gemini или эхо-ответ для проверки
  user_text = message.text
  bot.reply_to(message, f"Вы написали: {user_text}")


# Маршрут для вебхуков от Telegram
@server.route(f"/{TOKEN}", methods=["POST"])
def redirect_webhook():
  json_string = request.get_data().decode("utf-8")
  update = telebot.types.Update.de_json(json_string)
  bot.process_new_updates([update])
  return "!", 200


# Главная страница (проверка, что сервер живой)
@server.route("/")
def index():
  return "Bot is running!", 200


if __name__ == "__main__":
  # Настройка вебхука при старте (замени свой домен на render на актуальный)
  bot.remove_webhook()
  bot.set_webhook(url=f"https://gemini-ai-2026.onrender.com/{TOKEN}")

  # Запуск Flask-сервера на порту от Render
  port = int(os.environ.get("PORT", 10000))
  server.run(host="0.0.0.0", port=port)
