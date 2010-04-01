# -*- coding: utf-8 -*-
import xmpp


def init():
	return {'status':10,'descr':'Turns off bot','gc':2}

def run(bot,mess,mode='chat'):
	bot.send(xmpp.Message(mess.getFrom(),bot.phrases['BOT_SD'],mode))
	bot.online = 0

def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')