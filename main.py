# Sing4God Bot 1.2 Early Access (24.01.2019)
# Website: https://t.me/sing4god_bot

import sys, os, time
from log import logs
logs.init_log_file('{0}\\Log\\{1}-{2}-{3}.{4}-{5}-{6}.log'.format(
                            os.path.abspath(os.path.dirname(sys.argv[0])),
                            *time.strftime('%D/%H/%M/%S').split('/')))
from telepot.loop import MessageLoop
from users import users
from songs import songs
import bot_control, console

log_file = None
def init_log_file(file_log_name):                   # Initialize log_file
    global log_file
    log_file = open(file_log_name, mode='w', encoding='utf-8')
    bot_control.log_file = log_file

if __name__ == '__main__':

	print('Sing4God Bot 1.2 Early Access (24.01.2019)\nWebsite: https://t.me/sing4god_bot\n')

	print('initializating...: database of users')
	users.initdir(os.path.abspath(os.path.dirname(sys.argv[0])) + r'\users\users_list')
	print('done: database of users\n')

	print('initializating...: database of songs')
	songs.initdir(os.path.abspath(os.path.dirname(sys.argv[0])) + r'\songs')
	print('done: database of songs\n')

	bot_control.init_bot('YOUR BOT TOKEN')
	MessageLoop(bot_control.bot, {'chat' : bot_control.chat_handler,
									'callback_query' : bot_control.callback_handler}).run_as_thread()
	while True:
		command = input('>>> ')
		if command.split(' ')[0].lower() in console.commands.keys():
			console.commands[command.split(' ')[0].lower()](command.split(' ')[1:])
		else:
			print('No such command')