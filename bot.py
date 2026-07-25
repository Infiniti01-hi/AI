import os
import threading
from flask import Flask
import telebot
import google.generativeai as genai

# Чтение ключей из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# Модель Gemini 1.5 Flash (быстрая и бесплатная)
model = genai.GenerativeModel("gemini-1.5-flash")

# Flask-сервер для поддержки активности на Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot status: OK"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Логика бота
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "Привет! Я бот с подключенным ИИ Gemini. Задай мне любой вопрос.")

@bot.message_handler(func=lambda message: True)
def handle_prompt(message):
    try:
        # Визуальный статус "печатает..."
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Запрос к нейросети
        response = model.generate_content(message.text)
        
        # Отправка ответа
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Ошибка Gemini API: {e}")
        bot.reply_to(message, "Не удалось получить ответ от ИИ. Попробуй позже.")

if __name__ == "__main__":
    # Запуск фонового веб-сервера
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Запуск бота
    print("Бот успешно запущен...")
    bot.polling(none_stop=True)
