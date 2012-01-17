# -*- coding: utf-8 -*-
import xmpp

def init(bot):
	return {'status':6,'descr':bot.phrases['DESCR_ADMINS'],'gc':2}

def run(bot,mess,mode='chat'):
	text = bot.phrases['ADMINS'] + ':'
	for i in bot.config['permissions']['private_users']:
		text += '\n' + i[0] + ':' + unicode(i[1])
	bot.send(xmpp.Message(mess.getFrom(),text,mode))

def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')