# -*- coding: utf-8 -*-
import xmpp


def init():
	return {'status':0,'usage':'<text>','descr':'Echo test plugin','gc':2}

def run(bot,mess,mode='chat'):
	bot.send(xmpp.Message(mess.getFrom(),mess.getBody()[5:],mode))

def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')