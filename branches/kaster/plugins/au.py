# -*- coding: utf-8 -*-
import xmpp

def init(bot):
	return {'status':0,'usage':'<func_name|func_shortcut>','descr':bot.phrases['DESCR_AUHELP'],'gc':2}

def run(bot,mess,mode='chat'):
	command = mess.getBody()[3:]
	full = unicode(mess.getFrom())
	afull = full.split('/')
	try:
		nick = afull[1]
	except:
		nick = ''
	conf = afull[0]
	funcs = getfuncs()
	if command == 'help':
		mes = u'Этот плагин отображет раздел справки по введенной функции или ее сокращению. '
		mes += u'Если хотите узнать сокращение той или иной функции наберите !au sh <func_name>. '
		mes += u'Если же наоборот, хотите узнать, что обозначает то или иное сокращение, наберите !au full <shortcut> (Угловые скобки не нужны)'
	else:
		if command[:2] == 'sh':
			subcommand = command[3:]
			mes = get_key(funcs, subcommand.lower())
			if not mes: mes = u'В моей базе такой функции или ее сокращения нет'
		elif command[:4] == 'full':
			subcommand = command[5:]
			try:
				mes = funcs[subcommand.lower()]
			except:
				mes = u'В моей базе такой функции или ее сокращения нет'
		elif (command.lower() == 'sre') or (command.lower() == 'stringregexp'):
				mes = u'Спаравка для функции StringRegExp слишком объемная и вызывает нестабильность в работе бота, и поэтому не может быть вызвана. И потом, конференция не самое удачное место для изучения такого сложного механизма как Регулярные выражения. Рекомендую почитать классический учебник Фридла по данной тематике'
		else:
			try:
				func = funcs[command.lower()]
				mes = open('auhelp/' + func + '.txt').read().decode('cp1251')
			except:
				mes = u'В моей базе такой функции или ее сокращения нет'
			if (len(mes) > 400) and (mode == 'groupchat'):
				mode = 'chat'
				conf = full
	bot.send(xmpp.Message(conf,mes,mode))

def rungc(bot,mess):
	#mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')


def getfuncs():
	from ConfigParser import ConfigParser
	config = ConfigParser()
	config.read('au.ini')
	allitems = config.items('AutoitFuncs')
	funcs = {}
	for item in allitems:
		tmp = {item[0].lower():item[1], item[1].lower():item[1]}
		funcs.update(tmp)
	return funcs

def get_key(_dict, val):
	allkeys = [k for k, v in _dict.iteritems() if v.lower() == val]
	if allkeys:
		if len(allkeys[0]) > len(allkeys[1]):
			key = allkeys[1]
		else:
			key = allkeys[0]
	else:
		key = ''
	return key
			
