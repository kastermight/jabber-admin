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
		command = u'Брест,Беларусь'
	elif command == '5':
		command = u'Бат-Ям,Израиль'
	elif command == '6':
		command = u'Ростов-на-Дону,Россия'
	elif command == '7':
		command = u'Ташкент,Узбекистан'
	elif command == '8':
		command = u'Набережные челны,Россия'
	elif command == '9':
		command = u'Краснодар,Россия'
	elif command == '0':
		command = u'Хабаровск,Россия'
	elif command == '10':
		command = u'Курск\n'
	# ---------------------------
	if command == 'help':
		mes = u'Вывод времени для любого заданного географического объекта при наличии в базе карт Goolge maps.\n'
		mes += u'Так как некоторые объекты могут встречаться в нескольких странах, или даже в нескольких регионах в пределах одной страны, плагин может показать несколько ответов\n'
		mes += u'Например, !thetime Saint-Petersburg или !thetime Moscow,USA\n'
		mes += u'Для уточнения результата можете указать административные центры, к которому принадлежит объект.\n'
		mes += u'К примеру, сравните !thetime Трудовое, !thetime Трудовое, Украина, !thetime Трудовое, Запорожская область, Украина и !thetime Трудовое, Акимовский район, Запорожская область, Украина\n'
		mes += '-'*75
		mes += u'Так же, в плагине реализована поддержка сокращений для некоторых городов. Полный список сокращений\n\
		1 = Москва (Москва так же является значением по умолчанию, когда никакой город не выбран)\n\
		2 = Санкт-Петербург\n\
		3 = Boulder\n\
		4 = Брест\n\
		5 = Бат-Ям\n\
		6 = Ростов-на-Дону\n\
		7 = Ташкент\n\
		8 = Набережные Челны\n\
		9 = Краснодар\n\
		0 = Хабаровск\n\
		10 = Курск'
	else:
		mes = getTime(command)
		if not mes: mes = u'Не могу вывести время для ' + command + '\n'
	bot.send(xmpp.Message(mess.getFrom(),mes[:-1],mode))

def rungc(bot,mess):
	mess.setFrom(str(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')

def getTime(location):
	(alltz, locations) = getTimeZones(location)
	n = len(alltz)
	mes = ''
	for i in range(n):
		mes += u'Объект: ' + locations[i] + '\n'
		os.environ['TZ'] = alltz[i]['name']
		time.tzset()
		loctime = time.localtime()
		mes += u'Время: %02d:%02d:%02d, %02d.%02d.%d\n' % (loctime[3], loctime[4], loctime[5], loctime[2], loctime[1], loctime[0])
		mes += '-'*50 + '\n'
	return mes

def getTimeZones(location):
	import urllib2
	import json
	key = 'j3mf52lpisjfaaah5iatjhrltf'
	url = 'http://www.askgeo.com/api/950112/%s/timezone.json?points='
	url = url % key
	(locname, lat, lng) = getlatlong(location)
	n = len(locname)
	urlex = [url, []]
	for i in range(n):
		urlex[0] += lat[i] + ',' + lng[i] + ';'
		urlex[1].append(locname[i])
	url = urlex[0][:-1]
	ans = urllib2.urlopen(url)
	ans = json.load(ans)
	tz = []
	if not ans['code']:
		for data in ans['data']:
			tz.append({'name':data['timeZone'], 'Name':data['windowsStandardName']})
	return (tz, urlex[1])

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
