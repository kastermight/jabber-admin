# -*- coding: utf-8 -*-
import xmpp


def init(bot):
	return {'status':0,'usage':'<url>','descr':bot.phrases['DESCR_URL'],'gc':2}

def run(bot,mess,mode='chat'):
	command = mess.getBody()[3:]
	mes = getshorturl(command)
	if not mes: mes = u'Для данного URL короткая версия не может быть найдена'
	bot.send(xmpp.Message(mess.getFrom(),mes,mode))

def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')


def getshorturl(url):
	import httplib
	import json
	
	httpServ = httplib.HTTPSConnection("www.googleapis.com")
	httpServ.connect()
	
	header = {'Content-Type': 'application/json'}
	body = '{"longUrl": "%s"}' % url
	httpServ.request('POST', '/urlshortener/v1/url', body, header)
	
	response = httpServ.getresponse()
	ans = ''
	if response.status == httplib.OK: ans = json.load(response)
	httpServ.close()
	return ans['id']
