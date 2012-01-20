# -*- coding: utf-8 -*-
import xmpp


def init(bot):
	return {'status':0,'usage':'<url>','descr':bot.phrases['DESCR_URL'],'gc':2}

def run(bot,mess,mode='chat'):
	command = mess.getBody()[4:]
	if command == 'help':
		mes = u'Данный плагин преобразовывает длинные (и не очень) ссылки в короткий аналог, используя сервис http://goo.gl. Помните, в ссылке не должны содержаться символы несовместимые с URL, например http://ru.wikipedia.org/wiki/мандрагора, вместо этого дожно быть http://ru.wikipedia.org/wiki/%D0%9C%D0%B0%D0%BD%D0%B4%D1%80%D0%B0%D0%B3%D0%BE%D1%80%D0%B0. Как правило, современные браузеры при копировании адреса страницы из адресной строки автоматически конвертируют подобные символы в нужном направлении. Редкие случаи, когда обратное может произойти - если вы набираете ссылку руками, чего делать, конечно же, не стоит.'
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
