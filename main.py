# Sing4God Bot 1.1.3 Early Access (17.12.2018)
# Website: https://t.me/sing4god_bot


from telepot.loop import MessageLoop
from users import users
from songs import songs
import bot_control, sys, os
import time, console

log_file = None
def init_log_file(file_log_name):                   # Initialize log_file
    global log_file
    log_file = open(file_log_name, mode='w', encoding='utf-8')
    bot_control.log_file = log_file

if __name__ == '__main__':
	print('Sing4God Bot 1.1.3 Early Access (17.12.2018)\nWebsite: https://t.me/sing4god_bot\n')

	print('initializating...: database of users')
	users.initdir(os.path.abspath(os.path.dirname(sys.argv[0])) + r'\users\users_list')
	print('done: database of users\n')

	print('initializating...: database of songs')
	songs.initdir(os.path.abspath(os.path.dirname(sys.argv[0])) + r'\songs')
	print('done: database of songs\n')

	bot_control.init_bot('788030920:AAH22J1w44kOI_y9ZM3RYmGaqGiGYu7Dga8')
	MessageLoop(bot_control.bot, {'chat' : bot_control.chat_handler,
									'callback_query' : bot_control.callback_handler}).run_as_thread()
	while True:
		command = input('>>> ')
		if command.split(' ')[0].lower() in console.commands.keys():
			console.commands[command.split(' ')[0].lower()](command.split(' ')[1:])
		else:
			print('No such command')