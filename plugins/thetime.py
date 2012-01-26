# -*- coding: utf-8 -*-
import xmpp
import time
import os


def init(bot):
	return {'status':0,'descr [location]':bot.phrases['DESCR_THETIME'],'gc':2}

def run(bot,mess,mode='chat'):
	command = mess.getBody()[8:].strip().replace(' ', '')
	if command == '1' or command == '':
		command = u'Москва,Московскаяобласть,Россия'
	elif command == '2':
		command = u'Cанкт-Петербург,Россия'
	elif command == '3':
		command = 'Boulder80305'
	elif command == '4':
		command = u'Киев,Украина'
	elif command == '5':
		command = u'Бат-Ям,Израиль'
	elif command == '6':
		command = u'Ростов-на-Дону,Россия'
	elif command == '7':
		command = u'Ташкент,Узбекистан'
	elif command == '8':
		command = u'Набережныечелны,Россия'
	elif command == '9':
		command = u'Краснодар,Россия'
	elif command == '0':
		command = u'Хабаровск,Россия'
	elif command == '10':
		command = u'Курск'
	# ---------------------------
	if command == 'help':
		mes = u'Вывод времени для любого заданного географического объекта при наличии в базе карт Goolge maps.\n'
		mes += u'Так как некоторые объекты могут встречаться в нескольких странах, или даже в нескольких регионах в пределах одной страны, плагин может показать несколько ответов\n'
		mes += u'Например, !thetime Saint-Petersburg или !thetime Moscow,USA\n'
		mes += u'Для уточнения результата можете указать административные центры, к которому принадлежит объект.\n'
		mes += u'К примеру, сравните !thetime Трудовое, !thetime Трудовое, Украина, !thetime Трудовое, Запорожская область, Украина и !thetime Трудовое, Акимовский район, Запорожская область, Украина\n'
		mes += '-'*75 + '\n'
		mes += u'Так же, в плагине реализована поддержка сокращений для некоторых городов. Полный список сокращений\n\
		1 = Москва (Москва так же является значением по умолчанию, когда никакой город не выбран)\n\
		2 = Санкт-Петербург\n\
		3 = Boulder\n\
		4 = Киев\n\
		5 = Бат-Ям\n\
		6 = Ростов-на-Дону\n\
		7 = Ташкент\n\
		8 = Набережные Челны\n\
		9 = Краснодар\n\
		0 = Хабаровск\n\
		10 = Курск\n'
		mes += '-'*75 + '\n'
		mes += u'Для предотвращения многочисленных однотипных запросов на веб-ресурс с которого берутся данные, '
		mes += u'единожды запрошенные данные заносятся в базу данных SQL. Наберите !thetime version для получения версии SQL-библиотеки используемой плагином\n'
	elif command == 'version':
		import sqlite3
		mes = u'Я использую SQLite3 версии ' + sqlite3.version + '\n'
	else:
		mes = getTime(command)
		if not mes: mes = u'Не могу вывести время для ' + command + '\n'
	bot.send(xmpp.Message(mess.getFrom(),mes[:-1],mode))

def rungc(bot,mess):
	mess.setFrom(str(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')

def getTime(location):
	(alltz, locations) = getTZFromTable(location)
	mes = ''
	for tz, location in zip(alltz, locations):
		mes += u'Объект: ' + location + '\n'
		os.environ['TZ'] = tz['name']
		time.tzset()
		loctime = time.localtime()
		mes += u'Время: %02d:%02d:%02d, %02d.%02d.%d%s\n' % (loctime[3], loctime[4], loctime[5], loctime[2], loctime[1], loctime[0], tz['Comment'])
		mes += '-'*50 + '\n'
	return mes

def getlatlong(location):
	import urllib2
	import json
	URL = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true&language=ru'
	url = URL % location
	url = iriToUri(url)
	ans = urllib2.urlopen(url)
	ans = json.load(ans)
	locname = []
	lat = []
	lng = []
	if ans['status'] == 'OK':
		for result in ans['results']:
			locname.append(result['formatted_address'])
			lat.append(unicode(result['geometry']['location']['lat']))
			lng.append(unicode(result['geometry']['location']['lng']))
	return (locname, lat, lng)

def urlEncodeNonAscii(b):
	import re
	return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
	import urlparse
	parts= urlparse.urlparse(iri)
	return urlparse.urlunparse(part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8')) for parti, part in enumerate(parts))

def getTZFromTable(location):
	import sqlite3
	import json
	import urllib2
	key = 'j3mf52lpisjfaaah5iatjhrltf'
	url = 'http://www.askgeo.com/api/950112/%s/timezone.json?points='
	conn = sqlite3.connect('maindb')
	tz = []
	(locs, lats, lngs) = getlatlong(location)
	url = url % key
	urlex = [url, []]
	ind = False
	tobeadd = []
	unloc = []
	cur = conn.cursor()
	for loc, lat, lng in zip(locs, lats, lngs):
		latlng = lat + ';' + lng
		gettz = "SELECT tz, sttime FROM tzdata WHERE geodata = '" + latlng + "'"
		ans = cur.execute(gettz).fetchone()
		if ans:
			tz.append({'name':ans[0], 'Name':ans[1], 'Comment': u' (Взято из базы)'})
		else:
			ind = True
			urlex[0] += lat + ',' + lng + ';'
			tobeadd.append(latlng)
			unloc.append(loc)
		urlex[1].append(loc)
	if ind:
		url = urlex[0][:-1]
		ans = urllib2.urlopen(url)
		ans = json.load(ans)
		if not ans['code']:
			for data, latlng, location in zip(ans['data'], tobeadd, unloc):
				tz.append({'name':data['timeZone'], 'Name':data['windowsStandardName'], 'Comment': u' (Взято c сайта, добавлено в базу)'})
				settz = "INSERT INTO tzdata values ('%s', '%s', '%s', '%s')" % (latlng, location, data['windowsStandardName'], data['timeZone'])
				cur.execute(settz)
			conn.commit()
	cur.close()
	conn.close()
	return (tz, urlex[1])
