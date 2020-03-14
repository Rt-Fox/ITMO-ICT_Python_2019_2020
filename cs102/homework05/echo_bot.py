import telebot

access_token = '949981018:AAH6ApXBMfXK0YVvWIAmnn_zbeifloKVWfI'
telebot.apihelper.proxy = {'https': 'https://141.125.82.106:80'}
bot = telebot.TeleBot(access_token)

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)

