"""
This module gives you a little bit less work to add new songs
"""
import sys, os

txtw = open(os.path.abspath(os.path.dirname(sys.argv[0])) + r'\songs_list.txt', mode='a', encoding='utf-8')
print('txtw =', txtw)

try:
	while True:
		new_song_names = input("\nWrite down names of new songs by using '/' to split:\n")
		if new_song_names == 'exit': break																# Break if you need to close the file

		new_song_names = new_song_names.split(sep='/')													# It makes lists of song's name
		song_names = "', '".join(new_song_names)

		song_url = input("\nWrite down the URL with 'https://telegra.ph/' :\n")							# Just url for a song

		new_song_example = input("\nWrite down lyrics example of the song by using '/' to split:\n")	# It makes lyrics
		new_song_example = new_song_example.split(sep='/')
		song_example = r'\n'.join(new_song_example)

		txtw.write("\n\n	{ 'song_name' : ['%s'],\n	'url' : '%s',\n	'example' : '%s'}," % (song_names, song_url, song_example))	# Write down config of songs
		txtw.flush()																												# into songs_list.txt
finally:
	txtw.close()