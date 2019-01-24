import os, time
from pptx import Presentation
from songs.PPTX import convp
from telegraph import Telegraph
import string, pickle

def _get_text(path, name):
	l_text = convp.words_prs(Presentation(path + '\\' + name))
	textw_pptx = open(path + '\\[s4G]Temp\\' + name + '.txt', mode='w', encoding='utf-8')
	textw_pptx.write('names:\n' + name + '\n\n')
	for x in l_text:
		textw_pptx.write(x + '\n')
	textw_pptx.close()

	os.system('subl "' + path + '\\[s4G]Temp\\' + name + '.txt"')
	mtime = os.path.getmtime(path + '\\[s4G]Temp\\' + name + '.txt')
	while True:
		time.sleep(0.5)
		if os.path.getmtime(path + '\\[s4G]Temp\\' + name + '.txt') != mtime:
			break
	os.remove('%s\\%s' % (path, name))

def get_list_song(text_fp):
	text_fp = text_fp.split('\n\n')
	for x in range(len(text_fp)):
		text_fp[x] = text_fp[x].split('\n')

	text_fp[0] = text_fp[0][1:]
	text_fp[0].append(text_fp[0][0])
	exlude = set(string.punctuation)
	for x in range(len(text_fp[0])):
		if x == 0:
			text_fp[0][0] = text_fp[0][0].rstrip()
			continue
		text_fp[0][x] = ''.join(ch for ch in text_fp[0][x] if ch not in exlude)
		temp1 = text_fp[0][x].split()
		text_fp[0][x] = ' '.join(temp1)
		text_fp[0][x] = text_fp[0][x].lower().rstrip()
		if text_fp[0][x].startswith('єп'):
			text_fp[0].append(text_fp[0][x].replace('єп','євангельські пісні'))
		elif text_fp[0][x].startswith('пхм'):
			text_fp[0].append(text_fp[0][x].replace('пхм','пісні християнської молоді'))
		elif text_fp[0][x].startswith('пв'):
			text_fp[0].append(text_fp[0][x].replace('пв','песнь возрождения'))
		elif text_fp[0][x].startswith('чк'):
			text_fp[0].append(text_fp[0][x].replace('чк','чудный край'))
			text_fp[0].append(text_fp[0][x].replace('чк','4k'))
		elif text_fp[0][x].startswith('пх'):
			text_fp[0].append(text_fp[0][x].replace('пх','пісні хвали'))
	for x1 in range(len(text_fp)):
		for x2 in range(len(text_fp[x1])):
			text_fp[x1][x2] = text_fp[x1][x2].rstrip()
	return text_fp

def list_to_html(songs_list):
	song_html = ''
	for couplet in songs_list:
		if couplet[0] == '*':
			chorus = True
		else:
			chorus = False

		for stroke in couplet:
			if stroke == '*':
				continue
			elif chorus:
				song_html += '<aside><strong>'
				song_html += stroke + '</strong></aside>'
			else:
				song_html += '<aside>'
				song_html += stroke + '</aside>'

		song_html += '<aside><br></aside>'
	return song_html[:-19]

def add_telegraph(tele_acc, song_h, song_l):
	info = tele_acc.get_account_info()
	responce = tele_acc.create_page(title=song_l[0][0], html_content=song_h, author_name=info['author_name'], author_url=info['author_url'])
	return responce

def add_new_songs(path, amount=None):
	if not amount: amount = len(os.listdir(path))
	pptx_files = sorted(os.listdir(path))[:amount]
	number = 1
	if not os.path.exists(path + '\\[s4G]Temp'): os.mkdir(path + '\\[s4G]Temp')
	for x in pptx_files:
		if not os.path.isfile(path + '\\' + x) or (not x.endswith('.pptx') and not x.endswith('.PPTX')):
			continue
		song_l = _get_text(path, x)
		print('[%s] added: %s' % (number, x))
		number += 1

def push(path, path_pkl, token='YOUR TOKEN'):
	try:
		tele_bot = Telegraph(token)
		songsr_pkl = open(path_pkl + '\\songs.pickle', mode='rb')
		songs = pickle.load(songsr_pkl)
		songsr_pkl.close()
		amount = 0
		for file in os.listdir(path + '\\[s4G]Temp'):
			song_file = open(path + '\\[s4G]Temp\\' + file, mode='r', encoding='utf-8')
			song_l = get_list_song(song_file.read())
			song_file.close()
			song_h = list_to_html(song_l[1:])
			responce = add_telegraph(tele_bot, song_h, song_l)
			songs.append({ 'song_name' : [name for name in song_l[0]], 'url' : responce['url'], 'example' : '\n'.join(song_l[1]).strip()})
			os.remove(path + '\\[s4G]Temp\\' + file)
			amount += 1
	except ConnectionError:
		print('###########')
		print('#  ERROR  #')
		print('###########')
		print('\n\nCheck your internet connection or try later\n\n')

	finally:
		os.rmdir(path + '\\[s4G]Temp')
		songsw_pkl = open(path_pkl + '\\songs.pickle', mode='wb')
		pickle.dump(songs, songsw_pkl)
		songsw_pkl.close()
		print('done: pushed %s songs' % (amount))

def add_new_song_t(song_text, path_pkl, token='YOUR TOKEN'):
	try:
		tele_bot = Telegraph(token)
		songsr_pkl = open(path_pkl + '\\songs.pickle', mode='rb')
		songs = pickle.load(songsr_pkl)
		songsr_pkl.close()
		#songs = []
		
		song_l = get_list_song(song_text)
		song_h = list_to_html(song_l[1:])
		responce = add_telegraph(tele_bot, song_h, song_l)
		songs.append({ 'song_name' : [name for name in song_l[0]], 'url' : responce['url'], 'example' : '\n'.join(song_l[1])})
	finally:
		songsw_pkl = open(path_pkl + '\\songs.pickle', mode='wb')
		pickle.dump(songs, songsw_pkl)
		songsw_pkl.close()