# Function for sending messages right out to the bot

from telepot.namedtuple import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from songs import songs
from users import users
from commands_m import commands
import math, telepot, time,string
from log import logs

bot = None
def init_bot(api_token):			# init bot by a token
	global bot
	bot = telepot.Bot(api_token)

def chat_handler(msg):				# Messages handler
	content_type, chat_type, chat_id, message_date, message_id = telepot.glance(msg, long=True)

	if not str(chat_id) in users.users_list.keys():
		if 'username' in msg['from']:				# Checking for new users and addting them to users_list
			users.users_list[str(chat_id)] = msg['from']['username']
		else:
			users.users_list[str(chat_id)] = None
		logs.log_file.write('%s-%s-%s.%s:%s:%s: [%s(%s)] new user\n' %  (*time.strftime('%D/%H/%M/%S').split('/'), str(chat_id), users.users_list[str(chat_id)]))

	if content_type == 'text':
		command = msg['text']
		logs.log_file.write('%s-%s-%s.%s:%s:%s: [%s(%s)] got command: %s\n' % (*time.strftime('%D/%H/%M/%S').split('/'), str(chat_id), users.users_list[str(chat_id)], command))
		
		comm_b = command.split('\n')
		if comm_b[0] in commands.keys():
			comm_e = command[len(comm_b[0]):]
			commands[comm_b[0]](chat_id=chat_id, other=comm_e)
		elif command.startswith('/'):
			bot.sendMessage(chat_id, "Упс. Нет такой команды.")
		else:
			exclude = set(string.punctuation)
			command = ' '.join(''.join(ch for ch in command if ch not in exclude).split())		# remove all punctuation and double white-space
			users_songs = songs.look4song(command)
			if users_songs:
				sendSongs(chat_id, users_songs, command)
			else:
				songs.new_users_songs.write('%s %s\n' % (str(chat_id), command))
				songs.new_users_songs.flush()
				bot.sendMessage(chat_id, text="Простите, но мы ничего не нашли. Возможно в нашей базе ещё нету песни которую вы ищете, но вы всегда можете попробывать ввести другое имя.\nМы записали название этой песни и в будущем постараемся её добавить.")
				logs.log_file.write("%s-%s-%s.%s:%s:%s: [%s(%s)] can't found: %s\n" % (*time.strftime('%D/%H/%M/%S').split('/'), str(chat_id), users.users_list[str(chat_id)], command))
	else:
		bot.sendMessage(chat_id, 'Простите, но я не понимаю вас (пока что).')
	logs.log_file.flush()

def callback_handler(msg):			# callback quiry handler
	query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
	if query_data != 'this':
		action, *command, part = query_data.split(' ')
		command = ' '.join(command)
		if command == '/all':
			songs2 = songs.songs_list
		else:
			songs2 = songs.look4song(command)
		songs_part = songs2[0+4*int(part):4+4*int(part)]

		counter = 1
		if part != '0':
			counter = int(part)*4 + 1

		parse_md = ''
		for x in songs_part:
			stext = '' + x['example'].replace('\n', '\n')
			parse_md += '' + str(counter) + '. [{song_name}]({url})\n{example}\n\n'.format(
																url=x['url'], song_name=x['song_name'][0], example=stext)
			counter += 1

		inline_keyboard =[[]]

		if int(part) > 0:
			inline_keyboard[0].append(InlineKeyboardButton(text='<', callback_data='last '+command+' '+ str(int(part) - 1)))
		inline_keyboard[0].append(InlineKeyboardButton(text=str(int(part) + 1), callback_data='this'))
		if int(part) < math.ceil(len(songs2) / 4) - 1:
			inline_keyboard[0].append(InlineKeyboardButton(text='>', callback_data='next '+command+' '+ str(int(part) + 1)))

		origin_identifier = telepot.origin_identifier(msg)
		bot.editMessageText(msg_identifier=origin_identifier, text=parse_md, parse_mode='Markdown', disable_web_page_preview=True, reply_markup=
						InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
		logs.log_file.write('%s-%s-%s.%s:%s:%s: [%s(%s)] edited: %s [%s]\n' % (*time.strftime('%D/%H/%M/%S').split('/'), origin_identifier[0], users.users_list[str(origin_identifier[0])], origin_identifier[1], query_data))
		logs.log_file.flush()

def sendSongs(chat_id, songs, command, part=0):											# Send founded songs to a user of Telegram
	parse_md = ''
	counter = 1
	parts = math.ceil(len(songs) / 4)
	songs_part = songs[0:4]
	for x in songs_part:
		stext = '' + x['example'].replace('\n', '\n')
		parse_md += '' + str(counter) + '. [{song_name}]({url})\n{example}\n\n'.format(
															url=x['url'], song_name=x['song_name'][0], example=stext)
		counter += 1
	#print('\n\n', parse_md, '\n\n')
	inline_keyboard = [[InlineKeyboardButton(text=str(1), callback_data='this'),
						InlineKeyboardButton(text='>', callback_data='next '+command+' '+str(1))]]
	if parts > 1:
		bot.sendMessage(chat_id=chat_id, text=parse_md, parse_mode='Markdown', disable_web_page_preview=True, reply_markup=
					InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
	else:
		bot.sendMessage(chat_id=chat_id, text=parse_md, parse_mode='Markdown', disable_web_page_preview=True)
	logs.log_file.write('%s-%s-%s.%s:%s:%s: [%s(%s)] sended %s song(s)\n' % (*time.strftime('%D/%H/%M/%S').split('/'), chat_id, users.users_list[str(chat_id)], len(songs)))
	logs.log_file.flush()