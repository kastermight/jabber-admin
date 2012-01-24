# -*- coding: utf-8 -*-
import xmpp

def init(bot):
	return {'status':0,'usage':'<nick>','descr':bot.phrases['DESCR_SEEN'],'gc':1}

def run(bot,mess,mode='chat'):
	command = mess.getBody()[5:].strip()
	asker = unicode(mess.getFrom()).split('/')[1]
	conf = unicode(mess.getFrom()).split('/')[0]
	if command == 'help':
		mes = u'Выводит информацию о последнем посещении участника с указанным ником конференции, при условии, что его нету в данный момент'
	else:
		nick = command
		if command == '':
			mes = u'Может введешь ник того, кого ищещь? :-/'
		elif command == bot.config['conferences']['nick']:
			mes = u'Зачем, интересно, тебе понадобилось меня искать? :-/'
		elif nick == asker:
			mes = u'Сам себя искать? Тебе к Зигмунду, который Фрейд :)'
		elif bot.visitors[conf].has_key(nick.lower()):
			mes = u'Разуй зенки, ' + nick + u' же тут :)'
		else:
			try:
				mes = open('users/' + nick).read()
				mes = u'Последний раз ' + nick + u' был тут замечен ' + mes
			except:
				mes = u'На моей памяти, ' + nick + u' тут не появлялся'
		mes = asker + ': ' + mes
	bot.send(xmpp.Message(conf,mes,mode))

def rungc(bot,mess):
	#mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')
