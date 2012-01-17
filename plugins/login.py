# -*- coding: utf-8 -*-
import xmpp
import re


def init(bot):
	return {'status':0,'usage':'<level> <password>','descr':bot.phrases['DESCR_LOGIN'],'gc':0}

def run(bot,mess):
	user=unicode(mess.getFrom())
	priv = bot.get_priv(user)
	passw = re.match('login (\d{1,2}) (.*)', mess.getBody())
	level = ''
	password = ''
	try:
		level = int(passw.group(1))
		password = passw.group(2)
	except:
		return
	if level <= bot.config['permissions']['max_level']:
		if priv != 0:
			bot.config['permissions']['private_users'].remove([user,priv])
		if [password,level] in bot.config['permissions']['level_passwords']:
				bot.config['permissions']['private_users'].append([user,level])
				bot.send(xmpp.Message(mess.getFrom(),bot.phrases['LOGGED_IN']%level))