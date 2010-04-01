# -*- coding: utf-8 -*-
import xmpp
from __main__ import get_priv


def init():
	return {'status':1,'descr':'Admin session closing','gc':0}

def run(bot,mess):
	user=unicode(mess.getFrom())
	priv = get_priv(user)
	if priv != 0:
		bot.config['user_no_pass'].remove([user,priv])
		bot.send(xmpp.Message(mess.getFrom(),bot.phrases['SESS_CLOSE']))