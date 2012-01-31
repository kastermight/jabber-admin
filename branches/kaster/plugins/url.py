# -*- coding: utf-8 -*-
import xmpp


def init(bot):
	return {'status':0,'usage':'<url>','descr':bot.phrases['DESCR_URL'],'gc':2}

def run(bot,mess,mode='chat'):
	command = mess.getBody()[4:]
	if command == 'help':
		mes = u'Данный плагин преобразовывает длинные (и не очень) ссылки в короткий аналог, используя сервис http://goo.gl.'
	else:
		mes = getshorturl(command)
		if not mes: mes = u'Для данного URL короткая версия не может быть найдена'
	bot.send(xmpp.Message(mess.getFrom(),mes,mode))

def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')


def getshorturl(url):
	import httplib
	import json
	url = iriToUri(url)
	ans = ''
	httpServ = httplib.HTTPSConnection("www.googleapis.com")
	httpServ.connect()
	
	header = {'Content-Type': 'application/json'}
	body = '{"longUrl": "%s"}' % url
	try:
		httpServ.request('POST', '/urlshortener/v1/url', body, header)
		response = httpServ.getresponse()
		if response.status == httplib.OK: ans = json.load(response)
		httpServ.close()
	except:
		ans = {'id':u'В ссылке находятся символы недопустимые с форматом URL'}
	return ans['id']

def urlEncodeNonAscii(b):
	import re
	return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
	import urlparse
	parts= urlparse.urlparse(iri)
	return urlparse.urlunparse(part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8')) for parti, part in enumerate(parts))
