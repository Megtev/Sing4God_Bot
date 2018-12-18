# The console.py file
import sys, os
from songs import songs

def update_songs():
	print('[update_songs] initializating: database of songs')
	songs.initdir(os.path.abspath(os.path.dirname(sys.argv[0])) + r'\songs')
	print('[update_songs] done: database of songs')

commands = {}

commands['exit'] = (lambda *x: exec('raise KeyboardInterrupt'))
commands['stop'] = (lambda *x: exec('raise KeyboardInterrupt'))
commands['update_songs'] = (lambda *x: update_songs())
commands['help'] = (lambda *x: print('EXIT\t\t\tTo stop bot.\nSTOP\t\t\tTo stop bot.\nUPDATE_SONGS\t\tTo upload new songs to the bot without stopping.'))