# -*- coding: utf-8 -*-
import xmpp


def init(bot):
	return {'status':0,'usage':'<text>','descr':bot.phrases['DESCR_ECHO'],'gc':2}

def run(bot,mess,mode='chat'):
	full = unicode(mess.getFrom())
	afull = full.split('/')
	try:
		nick = afull[1]
	except:
		nick = ''
	conf = afull[0]
	command = mess.getBody()[5:].strip()
	mes = command
	if command == 'help':
		mes = u'Данный плагин делает простое повторение набранного вами сообщения исключив саму команду. Повтор выдается в том чате, в котором была вызвана команда. Исключение составляет команда, с ключевым словом hide набранном в личке. В этом случае, бот перенаправит сообщение в общий чат без указания автора.'
	if mode == 'chat':
		if command.startswith('hide'):
			mode = 'groupchat'
			full = conf
			mes = command[5:]
	else:
		full = conf
	bot.send(xmpp.Message(full,mes,mode))

def rungc(bot,mess):
	#mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')
