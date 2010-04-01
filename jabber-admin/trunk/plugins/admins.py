# -*- coding: utf-8 -*-
import xmpp

def init():
	return {'status':6,'descr':'Admins on-line','gc':2}

def run(bot,mess,mode='chat'):
	text = bot.phrases['ADMINS'] + ':'
	for i in bot.config['user_no_pass']:
		text += '\n' + i[0] + ':' + unicode(i[1])
	bot.send(xmpp.Message(mess.getFrom(),text,mode))

def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')