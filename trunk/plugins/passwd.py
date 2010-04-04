# -*- coding: utf-8 -*-
import xmpp
import re


def init():
	return {'status':10,'usage':'<level> <password>','descr':'Changing level password','gc':0}

def run(bot,mess):
	passw = re.match('passwd ([^ ]*) (.*)', mess.getBody())
	level = 0
	password = ''
	try:
		level = int(passw.group(1))
		password = passw.group(2)
	except:
		return
	if (level <= bot.config['max_level']):
		for [passn,lvl] in bot.config['allow_password']:
			if (level == lvl):
				bot.config['allow_password'].remove([passn,level])
				bot.config['allow_password'].append([password,level])
				bot.send(xmpp.Message(mess.getFrom(),bot.phrases['LEVEL_PASSCHANGE']%(level,password)))
				break
	return