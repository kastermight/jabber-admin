# -*- coding: utf-8 -*-
import xmpp
import sqlite3
import re
import time

def init(bot):
	return {'status':0,'usage':'code|help|set','descr':bot.phrases['DESCR_PB'],'gc':2}

def run(bot,mess,mode='chat'):
	conn = sqlite3.connect('maindb')
	cur = conn.cursor()
	command = mess.getBody()[3:].strip()
	full = unicode(mess.getFrom())
	afull = full.split('/')
	nick = afull[1]
	asker = nick.lower()
	conf = afull[0]
	#dconf = {'chat':}
	st = "SELECT username FROM usettings WHERE username = '%s'" % asker
	if not cur.execute(st).fetchall():
		st = "INSERT INTO usettings VALUES ('%s', 'code by %s', 1, '1D', 'autoit')" % (asker, asker)
		cur.execute(st)
		conn.commit()
	if command == 'help':
		mes = u'Данный плагин предназначен для публикации кода на pastebin.com.\n'
		mes += u'Синтаксис команды:\n\
	pb <code>\nв личке у бота. '
		mes += u'По умолчанию, подсветка синтаксиса - AutoIt, время хранения - 1 день, название кода - code by <username> <N>.\n'
		mes += u'Так же, плагин ведет подсчет выложенных кодов каждым пользователем и добавляет в название для различения. '
		mes += u'Все вышеописанные опции могут быть изменены/просмотрены в любой момент командой\n\
	!pb set/get <option:value>.\n'
		mes += u'Для получения синтсиса команды изменения/получения настроек, наберите !pb set/get help в общем чате или личке у бота.\n'
		mes += '-'*75 + '\n'
		mes += u'Внимание, на бесплатный аккаунт pastebin.com наложено ограничение в 25 кодов в сутки. '
		mes += u'Бот ведет счет, поэтому узнать о количестве уже опубликованных кодов можно командой !pb ?\n'
		mes += '-'*75 + '\n'
		mes += u'PS: Помните, в общем чате код не постить, любая попытка запостить большой код или сообщение будет караться киком из комнаты, поэтому не обижайтесь.\n'
	elif command == 'format':
		mes = u'Список наиболее популярных форматов для подсветки кода на http://pastebin.com\n'
		mes += 'autoit - AutoIt\nc - C\ncsharp - C#\ncpp - C++\nhtml4strict - HTML\njava - Java\nlua - Lua\nperl - Perl\nphp - PHP\npython - Python\nvb - Visual Basic\nxml - XML\n'
		mes += u'Полный список можно получить по адресу http://pastebin.com/api#5\n'
	elif command == '?':
		mes = getLimit(conn, cur)
	elif command.startswith(('set', 'get')):
		subcommand = command[4:].strip()
		setget = command[:3]
		if subcommand == 'help':
			mes = u'Синтаксис команды изменения/получения настроек: !pb set/get <option:value>, где в качестве option могут выступать следующие параметры:\n\
	fnb - корневое имя публикуемых кодов в одинарных или двойных кавычках\n\
	fct - изменение значения счетчика, который добавляется к корневому имени\n\
	exd - срок хранения кода на ресурсе. Возможные значения:\n\
		N - Никогда не удалять с сервера\n\
		10M - Удалить через 10 минут\n\
		1H - Удалить через 1 час\n\
		1D - Удалить через 1 день\n\
		1M - Удалить через 1 месяц\n\
	fmt -  формат кода, для подсветки синтаксиса. Перечень наиболее популярных форматов можно получить командой !pb format, остальные по адресу http://pastebin.com/api#5\n'
			mes += u'PS: Если вызвать команду !pb set/get без параметров, то все настройки сбросятся в значения по умолчанию, а счетчик сбросится до 1 (set), '
			mes += u'либо выведутся текущие настройки (get).\n'
			mes += u'Например: !pb set fnb:"MyPBCodes" fct:10 exd:1M fmt:python для установления значений, или !pb get fnb fct для отображения значений.'
		elif setget == 'set':
			if subcommand == '':
				setUDefaults(conn, cur, asker)
			else:
				setUSettings(conn, cur, asker, subcommand)
			mes = nick + u': Значения успешно установлены.'
		elif setget == 'get':
			mes = getUSettings(cur, nick, subcommand)
	else:
		mode = 'groupchat'
		mes = sendpb(conn, cur, nick, command)
		#if mode == 'chat':
		#bot.send(xmpp.Message(conf,mes,mode))
	if mode == 'chat':
		bot.send(xmpp.Message(full,mes,mode))
	else:
		bot.send(xmpp.Message(conf,mes,mode))

def rungc(bot,mess):
	#mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')

def setUDefaults(conn, cur, user):
	st = "UPDATE usettings SET filenamebase = 'code by %s', filecount = 1, expdate = '1D', format = 'autoit' WHERE username = '%s'" % (user, user)
	cur.execute(st)
	conn.commit()

def setUSettings(conn, cur, user, command):
	fnbpat = '\s+fnb\:["\'](.+?)["\']\s+'
	fctpat = '\s+fct\:(\d+?)\s+'
	exdpat = '\s+exd\:([N10MHD]+?)\s+'
	fmtpat = '\s+fmt\:(.+?)\s+'
	command = ' ' + command + ' '
	fnb = re.search(fnbpat, command)
	fct = re.search(fctpat, command)
	exd = re.search(exdpat, command)
	fmt = re.search(fmtpat, command)
	st = "UPDATE usettings SET %s WHERE username = '%s'"
	tmp = ""
	if fnb:
		tmp += "filenamebase = '" + fnb.group(1) + "', "
	if fct:
		tmp += "filecount = " + fct.group(1) + ", "
	if exd:
		tmp += "expdate = '" + exd.group(1) + "', "
	if fmt:
		tmp += "format = '" + fmt.group(1) + "', "
	if tmp:
		st = st % (tmp[:-2], user)
		cur.execute(st)
		conn.commit()

def getUSettings(cur, nick, command):
	user = nick.lower()
	commands = command.split(' ')
	mes = u"Пользовательские настройки для %s\n" % nick
	mes += '-'*50 + '\n'
	st = "SELECT %s FROM usettings WHERE username = '%s'"
	ind = True
	if 'fnb' in commands:
		ind = False
		tmp = st % ('filenamebase', user)
		mes += u'Корневое название для публикуемых кодов: %s (fnb)\n' % cur.execute(tmp).fetchone()[0]
	if 'fct' in commands:
		ind = False
		tmp = st % ('filecount', user)
		mes += u'Состояние индекса для инкремента: %s (fct)\n' % cur.execute(tmp).fetchone()[0]
	if 'exd' in commands:
		ind = False
		tmp = st % ('expdate', user)
		mes += u'Длительность хранения кода: %s (exd)\n' % cur.execute(tmp).fetchone()[0]
	if 'fmt' in commands:
		ind = False
		tmp = st % ('format', user)
		mes += u'Формат для подсветки кода: %s (fmt)\n' % cur.execute(tmp).fetchone()[0]
	if ind:
		st = st % ('filenamebase, filecount, expdate, format', user)
		allmes = cur.execute(st).fetchone()
		mes += u'Корневое название для публикуемых кодов: %s (fnb)\n' % allmes[0]
		mes += u'Состояние индекса для инкремента: %d (fct)\n' % allmes[1]
		mes += u'Длительность хранения кода: %s (exd)\n' % allmes[2]
		mes += u'Формат для подсветки кода: %s (fmt)\n' % allmes[3]
	return mes

def getLimit(conn, cur):
	st = "SELECT number, lastdate FROM dlimit"
	lastdate = time.localtime()[2]
	ans = cur.execute(st).fetchone()
	if ans:
		if ans[1] == lastdate:
			return (u'Количество выложенных кодов за сегодня: ' + unicode(ans[0])) + '/25'
		else:
			st = "UPDATE dlimit SET number = 0, lastdate = %d" % lastdate
			cur.execute(st)
			conn.commit()
			return u'Количество выложенных кодов за сегодня: 0/25'
	else:
		return u'В базе еще нет ни одного значения.'

def setLimit(conn, cur):
	st = "SELECT number, lastdate FROM dlimit"
	lastdate = time.localtime()[2]
	ans = cur.execute(st).fetchone()
	if ans:
		if ans[1] == lastdate:
			st = "UPDATE dlimit SET number = %d" % (ans[0] + 1)
			cur.execute(st)
			conn.commit()
		else:
			st = "UPDATE dlimit SET number = 1, lastdate = %d" % lastdate
			cur.execute(st)
			conn.commit()
	else:
		st = "INSERT INTO dlimit VALUES (1, %d)" % lastdate
		cur.execute(st)
		conn.commit()

def sendpb(conn, cur, user, code):
	import httplib
	import urllib
	st = "SELECT filenamebase, filecount, expdate, format FROM usettings WHERE username = '%s'" % user.lower()
	ans = cur.execute(st).fetchone()
	st = "SELECT number FROM dlimit"
	limit = cur.execute(st).fetchone()
	if not limit:
		limit = 0
	else:
		limit = limit[0]
	if limit < 25:
		body = {'api_option':'paste',
			'api_dev_key':'eb2a198d69ffc3cbccd4b567a6f69946',
			'api_paste_code':code.encode('utf-8'),
			'api_paste_private':'0',
			'api_paste_name':ans[0] + ' ' + unicode(ans[1]),
			'api_paste_expire_date':ans[2],
			'api_paste_format':ans[3],
			'api_user_key':''}
		body = urllib.urlencode(body)
		header = {"Content-type": "application/x-www-form-urlencoded"}
		httpServ = httplib.HTTPConnection("pastebin.com")
		httpServ.connect()
		httpServ.request('POST', '/api/api_post.php', body, header)
		resp = httpServ.getresponse().read()
		httpServ.close()
		st = "UPDATE usettings SET filecount = %d WHERE username = '%s'" % (ans[1] + 1, user.lower())
		cur.execute(st)
		conn.commit()
		setLimit(conn, cur)
	else:
		resp= u'Лимит в 25 кодов на сегодня истек. Попробуйте завтра.'
	return resp
