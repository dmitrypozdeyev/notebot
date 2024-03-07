import telebot 
import json

TOKEN = ('TOKEN')


bot = telebot.TeleBot(TOKEN)
input_state = {}
with open('notes.json', 'r') as file:
    notes = json.load(file)
note = {}

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message) -> None:
    input_state[message.chat.id] = 'default'
    bot.send_message(message.chat.id, 'Hello!')

@bot.message_handler(commands=['addnote'])
def add_note(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, "Введите текст заметки!")
    input_state[message.chat.id] = 'add_note'

@bot.message_handler(commands=['shownotes'])
def show_notes(message: telebot.types.Message) -> None:
    for note in notes:
        bot.send_message(message.chat.id, f"Заметка: {note['text']}\nДата: {note['date']}\nВажность: {note['imp']}")

@bot.message_handler(content_types=['text'])
def action(message: telebot.types.Message) -> None:
    if input_state[message.chat.id] == 'add_note':
        note['text'] = message.text
        bot.send_message(message.chat.id, "Введите дату")
        input_state[message.chat.id] = 'add_date'
    elif input_state[message.chat.id] == 'add_date':
        note['date'] = message.text
        bot.send_message(message.chat.id, "Введите важность")
        input_state[message.chat.id] = 'add_imp'
    elif input_state[message.chat.id] == 'add_imp':
        note['imp'] = message.text
        bot.send_message(message.chat.id, "Заметка добавлена")
        input_state[message.chat.id] = 'default'
        notes.append(note)
        with open('notes.json', 'w') as file: 
            json.dump(notes, file, indent=4)


    

bot.polling()