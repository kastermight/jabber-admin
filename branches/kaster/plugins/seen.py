# -*- coding: utf-8 -*-
import xmpp
import sqlite3

def init(bot):
	return {'status':0,'usage':'<nick>','descr':bot.phrases['DESCR_SEEN'],'gc':1}

def run(bot,mess,mode='chat'):
	command = mess.getBody()[5:].strip()
	asker = unicode(mess.getFrom()).split('/')[1]
	conf = unicode(mess.getFrom()).split('/')[0]
	if command == 'help':
		mes = u'Выводит информацию о последнем посещении участника с указанным ником конференции, при условии, что его нету в данный момент\n'
		mes += u'Версия используемой библиотеки SQL - SQLite v' + sqlite3.version
	else:
		nick = command
		if command == '':
			mes = u'Может введешь ник того, кого ищешь? :-/'
		elif command == bot.config['conferences']['nick']:
			mes = u'Зачем, интересно, тебе понадобилось меня искать? :-/'
		elif nick.lower() == asker.lower():
			mes = u'Сам себя искать? Тебе к Зигмунду, который Фрейд :)'
		elif bot.visitors[conf].has_key(nick.lower()):
			mes = u'Разуй зенки, ' + nick + u' же тут :)'
		else:
			conn = sqlite3.connect('maindb')
			cur = conn.cursor()
			st = "SELECT lastdate FROM users WHERE username = '%s'" % nick.lower()
			ans = cur.execute(st).fetchone()
			if ans:
				lasttime = ans[0]
				mes = u'Последний раз ' + nick + u' был тут замечен ' + lasttime
			else:
				mes = u'На моей памяти, ' + nick + u' тут не появлялся'
			cur.close()
			conn.close()
		mes = asker + ': ' + mes
	bot.send(xmpp.Message(conf,mes,mode))

def rungc(bot,mess):
	#mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')
