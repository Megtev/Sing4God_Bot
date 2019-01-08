import bot_control, os, sys
from songs import songs
from songs import auto_add as auto_add
commands = {}
vip = []

def update_songs(chat_id, other):
	if str(chat_id) not in vip:
		bot_control.bot.sendMessage(chat_id, "Упс. Нет такой команды.")
		return

	last_amount = songs.songs_amount
	bot_control.bot.sendMessage(chat_id, '[update_songs] initializating: database of songs')
	songs.initdir(os.path.abspath(os.path.dirname(sys.argv[0])) + r'\songs')
	bot_control.bot.sendMessage(chat_id, '[update_songs] done: database of songs\n-added %s songs' % (songs.songs_amount - last_amount))

def add_new_song(chat_id, other):
	if str(chat_id) not in vip:
		bot_control.bot.sendMessage(chat_id, "Упс. Нет такой команды.")
		return

	auto_add.add_new_song_t(song_text=other[1:], path_pkl=r'E:\Python\MyProject\Sing4God_Bot\songs')
	bot_control.bot.sendMessage(chat_id, '[add_new_song] done: added new songs, use /update_songs to update')

commands['/start'] = (lambda chat_id, other: bot_control.bot.sendMessage(chat_id, "Привет. Я *Sing4God Bot*, напиши мне название христианской песни и я найду её текст для тебя.", parse_mode='Markdown'))
commands['/about'] = (lambda chat_id, other: bot_control.bot.sendMessage(chat_id, '*Sing4God Bot\n\nVersion: 1.1.3 Early Access (17.12.2018)*\nКоличество добавленых песен: %s' % (songs.songs_amount), parse_mode='Markdown'))
commands['/all'] = (lambda chat_id, other: bot_control.sendSongs(chat_id, songs.songs_list, '/all'))
commands['/update_songs'] = update_songs
commands['/add_new_song'] = add_new_song