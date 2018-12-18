import bot_control
from songs import songs
commands = {}

commands['/start'] = (lambda chat_id: bot_control.bot.sendMessage(chat_id, "Привет. Я *Sing4God Bot*, напиши мне название христианской песни и я найду её текст для тебя.", parse_mode='Markdown'))
commands['/about'] = (lambda chat_id: bot_control.bot.sendMessage(chat_id, '*Sing4God Bot\n\nVersion: 1.1.3 Early Access (17.12.2018)*\nКоличество добавленых песен: %s' % (songs.songs_amount), parse_mode='Markdown'))
commands['/all'] = (lambda chat_id: bot_control.sendSongs(chat_id, songs.songs_list, '/all'))