# -*- coding: utf-8 -*-
import xmpp

def init(bot):
	return {'status':0,'usage':'[i]','descr':bot.phrases['DESCR_ANEK'],'gc':2}

def run(bot,mess,mode='chat'):
	command = mess.getBody()[5:]
	if command == 'help':
		mes = u'Плагин выводит случайный анекдот с сайта http://anekdot.ru (не больше 5 за раз)'
	elif command.isdigit() and int(command) <= 5:
		mes = getjoke(int(command))
	else:
		mes = getjoke(1)
	bot.send(xmpp.Message(mess.getFrom(),mes,mode))

def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')

def getjoke(i):
	import re, urllib2
	from BeautifulSoup import BeautifulSoup
	html = urllib2.urlopen('http://www.anekdot.ru/scripts/rand_anekdot.php?t=j').read()
	html = html.replace('<br />', '\n')
	soup = BeautifulSoup(html)
	allcontent = soup.findAll('div', 'topicbox')
	alljokes = []
	alldates = []
	allauthors = []
	for content in allcontent:
		date = content.find('p', 'title')
		joke = content.find('div', 'text')
		author = content.find('a', 'button_author')
		if date:
			date = date.a.contents[0]
			joke = joke.contents[0].replace('&nbsp;', ' ').replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>').replace('&#39;', '\'')
			try:
				author = author.contents[0]
			except:
				author = u'Неизвестен'
			alljokes.append(joke)
			alldates.append(date)
			allauthors.append(author)
	outjoke = ''
	for j in range(i):
		outjoke += u'Шутка от %s, Автор %s\n%s' % (alldates[j], allauthors[j], alljokes[j])
		outjoke += '\n' + '-'*75 + '\n'
	return outjoke[:-1]
