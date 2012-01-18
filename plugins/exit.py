# -*- coding: utf-8 -*-
import xmpp


def init(bot):
	return {'status':1,'descr':bot.phrases['DESCR_EXIT'],'gc':0}

def run(bot,mess):
	user=unicode(mess.getFrom())
	priv = bot.get_priv(user)
	if priv != 0:
		bot.config['permissions']['private_users'].remove([user,priv])
		bot.send(xmpp.Message(mess.getFrom(),bot.phrases['SESS_CLOSE']))