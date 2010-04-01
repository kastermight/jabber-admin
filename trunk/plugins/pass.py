# -*- coding: utf-8 -*-
import xmpp
import re
from __main__ import get_priv


def init():
	return {'status':0,'usage':'<level> <password>','descr':'Joining level','gc':0}

def run(bot,mess):
	user=unicode(mess.getFrom())
	priv = get_priv(user)
	passw = re.match('pass (\d{1,2}) (.*)', mess.getBody())
	level = ''
	password = ''
	try:
		level = int(passw.group(1))
		password = passw.group(2)
	except:
		return
	if level <= bot.config['max_level']:
		if priv != 0:
			bot.config['user_no_pass'].remove([user,priv])
		if [password,level] in bot.config['allow_password']:
				bot.config['user_no_pass'].append([user,level])
				bot.send(xmpp.Message(mess.getFrom(),bot.phrases['LOGGED_IN']%level))