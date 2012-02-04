# -*- coding: utf-8 -*-
import xmpp

def init(bot):
	return {'status':0,'usage':'','descr':bot.phrases['DESCR_IT'],'gc':2}

def run(bot,mess,mode='chat'):
	command = mess.getBody()[3:]
	full = unicode(mess.getFrom())
	afull = full.split('/')
	try:
		nick = afull[1]
	except:
		nick = ''
	conf = afull[0]
	if command == 'help':
		mes = u'Плагин выводит случайную историю с сайта http://ithappens.ru'
	else:
		(date, rank, id, text, title) = getit()
		mes = u'История №%s от %s - "%s" (%s)\n' % (id, date, title, rank)
		mes += '-'*75 + '\n'
		mes += text
		if len(text) >= 400 and mode == 'groupchat':
			pmes = mes
			mes = nick + u' вовсю хохочет над историей №%s с рейтингом %s от %s' % (id, rank, date)
			bot.send(xmpp.Message(full,pmes,'chat'))
		elif mode == 'chat':
			conf = full
	bot.send(xmpp.Message(conf,mes,mode))

def rungc(bot,mess):
	#mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')

def getit():
	import re
	import urllib2
	from BeautifulSoup import BeautifulSoup
	#url = 'http://ithappens.ru/story/53'
	url = 'http://ithappens.ru/random'
	html = urllib2.urlopen(url).read()
	html = urlreplace(html)
	soup = BeautifulSoup(html)
	text = soup.find('div', 'text')
	date = text.findAll('p', 'date')
	title = text.h3.contents[0]
	title = re.search('#\d+\:\s(.*)', title).group(1)
	rank = date[1].contents[0][9:].strip()
	date = date[0].contents[0]
	text = text.find('p', 'text')
	id = text['id'][6:]
	text = text.contents[0]
	return (date, rank, id, text, title)

def urlreplace(text):
	text = text.replace('<br />', '\n')
	text = text.replace('<nobr>', '')
	text = text.replace('</nobr>', '')
	text = text.replace('<br>', '\n')
	text = text.replace('&nbsp;', ' ')
	text = text.replace('&gt;', '>')
	text = text.replace('&lt;', '<')
	text = text.replace('&quot;', '"')
	text = text.replace('&#39;', '\'')
	text = text.replace('<i>', '')
	text = text.replace('</i>', '')
	text = text.replace('<b>', '')
	text = text.replace('</b>', '')
	return text