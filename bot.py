import os
from flask import Flask, request
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Твой домен на Render (например, https:// твой-проект.onrender.com)
# Render автоматически передает имя хоста или можно прописать вручную
WEBHOOK_URL_BASE = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_URL_PATH = f"/{TOKEN}"

app = Flask(__name__)


@app.route(WEBHOOK_URL_PATH, methods=["POST"])
def webhook():
  if request.headers.get("content-type") == "application/json":
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200
  else:
    return "Invalid content type", 403


# Удаляем старый вебхук и ставим новый при старте
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)


# Здесь твои обработчики сообщений (handlers), как и были:
@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(message, "Привет, режиссёр!")


# Запуск Flask-сервера на порту, который требует Render
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)
