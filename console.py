# The console.py file
import sys, os
from songs import songs
from log import logs

def update_songs():
	last_amount = songs.songs_amount
	print('[update_songs] initializating: database of songs')
	songs.initdir(os.path.abspath(os.path.dirname(sys.argv[0])) + r'\songs')
	print('[update_songs] done: database of songs\t-added %s songs' % (songs.songs_amount - last_amount))

commands = {}

commands['exit'] = (lambda *x: exec('raise KeyboardInterrupt'))
commands['stop'] = (lambda *x: exec('raise KeyboardInterrupt'))
commands['update_songs'] = (lambda *x: update_songs())
commands['log_file'] = (lambda *x: os.system(r'subl ' + os.path.abspath(os.path.realpath(logs.log_file.name))))
commands['help'] = (lambda *x: print(help_c))

help_c = '''
EXIT\t\t\tTo stop bot.
STOP\t\t\tTo stop bot.
UPDATE_SONGS\t\tTo upload new songs to the bot without stopping.
LOG_FILE\t\tTo open a log file associated with current session.
'''