# -*- coding: utf-8 -*-
import xmpp
import urllib2, re, os, time

def init(bot):
	return {'status':0,'usage':'[list|list of currency names] [date]','descr':bot.phrases['DESCR_CURR'],'gc':2}

def run(bot,mess,mode='chat'):
	command = unicode(mess.getBody()[4:])
	if command == '': command += 'USD'
	shortcutlist = {'1':'USD', '2':'EUR', '3':'GBP', '4':'CNY', '5':'JPY', '6':'UAH', '7':'BYR', '8':'KZT'}
	if command == 'help':
		fmtstr = u'Плагин для вывода курса валют на текущую или заданную дату для всех (по ЦБ) или избранной валют.\n'
		fmtstr += u'-----------------------------------------------------------------------------------------------\n'
		fmtstr += u'Список сокращений:\n\
		1 = Доллар США\n\
		2 = Евро\n\
		3 = Фунт стерлингов\n\
		4 = Китайский юань\n\
		5 = Японская йена\n\
		6 = Украинская гривна\n\
		7 = Белорусский рубль\n\
		8 = Казахский тенге\n'
		fmtstr += u'-----------------------------------------------------------------------------------------------\n'
		fmtstr += u'Примеры использования:\n'
		fmtstr += '!cur USD, !cur eur, !cur 1, !cur 1 2 3, !cur usd eur 1 2 3, !cur UAH 12/04/2007, !cur UAH usd 5 7 8 01/05/2006, !cur 1/2/2005, !cur\n'
	else:
		URL = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req=%s'
		date_pat = '(\d{1,2})/(\d{1,2})/(\d{4})' # dd/mm/yyyy
		date = re.search(date_pat, command)
		dateind = False
		if not date:
			os.environ['TZ'] = 'Europe/Moscow'
			time.tzset()
			tim = time.localtime()
			date = '%02d/%02d/%d' % (tim[2], tim[1], tim[0])
		else:
			dateind = True
			command = command.replace(date.group(0), '')
			if not command: command += 'list'
			date = '%02d/%02d/%d' % (int(date.group(1)), int(date.group(2)), int(date.group(3)))
		cur_list = {}
		url = URL % date
		f = urllib2.urlopen(url)
		alldata = f.read()
		curall_pat = '(?s)Valute\sID="R\d+"\>(.+?)\</Valute\>'
		curall = re.findall(curall_pat, alldata)
		charcode_re = re.compile('CharCode\>(\w\w\w)\</CharCode')
		nominal_re = re.compile('Nominal\>(\d+)\</Nominal')
		curname_re = re.compile('Name\>(.+)\</Name')
		val_re = re.compile('Value\>(\d*,?\d*)\</Value')
		for cur in curall:
			charcode = charcode_re.search(cur).group(1)
			nominal = nominal_re.search(cur).group(1)
			curname = curname_re.search(cur).group(1)
			val = val_re.search(cur).group(1)
			tmp = {charcode:{'nominal':nominal, 'curname':curname, 'value':val.replace(',', '.')}}
			cur_list.update(tmp)
		fmtstr = u'На ' + date + u' ЦБРФ установил следующий курс валют:\n'
		fmtstr += '-----------------------------------------------------\n'
		if 'list' in command:
			for cur in cur_list.keys():
				fmtstr += cur_list[cur]['nominal'] + ' ' + cur_list[cur]['curname'].decode('cp1251') + ' (' + cur + ')' + u' составляе(ю)т ' + cur_list[cur]['value'] + u' рублей\n'
		else:
			curid_pat = '[a-zA-Z]{3}'
			curidall = re.findall(curid_pat, command)
			ind = True
			if curidall:
				ind = False
				for cur in curidall:
					cur = cur.upper()
					if cur_list.has_key(cur):
						fmtstr += cur_list[cur]['nominal'] + ' ' + cur_list[cur]['curname'].decode('cp1251') + ' (' + cur + ')' + u' составляе(ю)т ' + cur_list[cur]['value'] + u' рублей\n'
					else:
						fmtstr += cur + u' - валюты с таким кодом в базе ЦБРФ на ' + date + u' нет\n'
			shortcut_pat = '\d'
			shortcuts = re.findall(shortcut_pat, command)
			if shortcuts:
				ind = False
				for shortcut in shortcuts:
					if shortcutlist.has_key(shortcut):
						if cur_list.has_key(shortcutlist[shortcut]):
							fmtstr += cur_list[shortcutlist[shortcut]]['nominal'] + ' ' + \
							    cur_list[shortcutlist[shortcut]]['curname'].decode('cp1251') + ' (' + \
							    shortcutlist[shortcut]+ ')' + u' составляе(ю)т ' + cur_list[shortcutlist[shortcut]]['value'] + u' рублей\n'
						else:
							fmtstr += shortcutlist[shortcut] + u' - валюты с таким кодом в базе ЦБРФ на ' + date + u' нет'
					else:
						fmtstr += shortcut + u' - такого сокращения в базе нет. Наберите !cur help для списка сокращений\n'
			if ind: fmtstr = u'По вашему запросу ничего не найдено\n'
	bot.send(xmpp.Message(mess.getFrom(),fmtstr[:-1],mode))

def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')
