# -*- coding: utf-8 -*-
import xmpp


def init(bot):
	return {'status':0,'usage':'<text>','descr':bot.phrases['DESCR_ECHO'],'gc':2}

def run(bot,mess,mode='chat'):
	import subprocess as sp
	import re
	command = mess.getBody()[4:].strip()
	if command == 'help':
		mes = u'Эта команда выводит версию бота'
	else:
		version = re.search("Revision:\s(\d+)", sp.check_output(["svn", "info"])).group(1)
		mes = u'JAdmin V.%s' % version
	bot.send(xmpp.Message(mess.getFrom(),mes,mode))

def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')
