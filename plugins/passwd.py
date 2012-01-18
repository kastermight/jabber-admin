# -*- coding: utf-8 -*-
import xmpp
import re


def init(bot):
	return {'status':10,'usage':'<level> <password>','descr':bot.phrases['DESCR_PASSWD'],'gc':0}

def run(bot,mess):
	passw = re.match('passwd ([^ ]*) (.*)', mess.getBody())
	level = 0
	password = ''
	try:
		level = int(passw.group(1))
		password = passw.group(2)
	except:
		return
	if (level <= bot.config['permissions']['max_level']):
		for [passn,lvl] in bot.config['permissions']['level_passwords']:
			if (level == lvl):
				bot.config['permissions']['level_passwords'].remove([passn,level])
				bot.config['permissions']['level_passwords'].append([password,level])
				bot.send(xmpp.Message(mess.getFrom(),bot.phrases['LEVEL_PASSCHANGE']%(level,password)))
				break
	return