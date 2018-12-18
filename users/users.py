# The users.py file
import shelve

def initdir(dirname):
	'''
	initdir(dirname)
	send me a path to a file of user list
	and I`ll initialize all necessary arguments
	'''
	global users_list
	users_list = shelve.open(dirname)

users_list = None