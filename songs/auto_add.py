import os, time
from pptx import Presentation
from songs.PPTX import convp
from telegraph import Telegraph
import string, pickle

def _get_text(path, name):
	l_text = convp.words_prs(Presentation(path + '\\' + name))
	textw_pptx = open(path + '\\' + name + '.txt', mode='w', encoding='utf-8')
	textw_pptx.write('names:\n' + name + '\n\n')
	for x in l_text:
		textw_pptx.write(x + '\n')
	textw_pptx.close()

	os.system('subl "' + path + '\\' + name + '.txt"')
	mtime = os.path.getmtime(path + '\\' + name + '.txt')
	while True:
		time.sleep(0.5)
		if os.path.getmtime(path + '\\' + name + '.txt') != mtime:
			break

	textr_pptx = open(path + '\\' + name + '.txt', mode='r', encoding='utf-8')
	text_fp = textr_pptx.read()
	textr_pptx.close()
	return text_fp


def get_list_song(path, name, from_file=True):
	if from_file:
		text_fp = _get_text(path, name)
	else:
		text_fp = path

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

	if from_file:
		os.system('del "'+ path + '\\' + name + '.txt"')
		print('added:', text_fp[0][0])

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

def add_new_songs(path, path_pkl, token='b9f7f14cbeaf0c7ee2710265b99c9baafae2cdf7baea2be8803020ba34e7', amount=1):
	try:
		pptx_files = os.listdir(path)[:amount]
		tele_bot = Telegraph(token)
		songsr_pkl = open(path_pkl + '\\songs.pickle', mode='rb')
		songs = pickle.load(songsr_pkl)
		songsr_pkl.close()
		#songs = []
		
		for x in pptx_files:
			song_l = get_list_song(path, x)
			song_h = list_to_html(song_l[1:])
			responce = add_telegraph(tele_bot, song_h, song_l)
			songs.append({ 'song_name' : [name for name in song_l[0]], 'url' : responce['url'], 'example' : '\n'.join(song_l[1]).strip()})
			os.system('del "' + path + '\\' + x + '"')
	finally:
		songsw_pkl = open(path_pkl + '\\songs.pickle', mode='wb')
		pickle.dump(songs, songsw_pkl)
		songsw_pkl.close()
		print('done: added songs[%s]' % (amount))

def add_new_song_t(song_text, path_pkl, token='b9f7f14cbeaf0c7ee2710265b99c9baafae2cdf7baea2be8803020ba34e7'):
	try:
		tele_bot = Telegraph(token)
		songsr_pkl = open(path_pkl + '\\songs.pickle', mode='rb')
		songs = pickle.load(songsr_pkl)
		songsr_pkl.close()
		#songs = []
		
		song_l = get_list_song(song_text, '', from_file=False)
		song_h = list_to_html(song_l[1:])
		responce = add_telegraph(tele_bot, song_h, song_l)
		songs.append({ 'song_name' : [name for name in song_l[0]], 'url' : responce['url'], 'example' : '\n'.join(song_l[1])})
	finally:
		songsw_pkl = open(path_pkl + '\\songs.pickle', mode='wb')
		pickle.dump(songs, songsw_pkl)
		songsw_pkl.close()


#if __name__ == '__main__':
#	songs_pkl = open(r'E:\Python\MyProject\Sing4God_Bot\songs\songs.pkl', mode='wb')
#b9f7f14cbeaf0c7ee2710265b99c9baafae2cdf7baea2be8803020ba34e7