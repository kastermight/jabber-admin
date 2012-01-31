# -*- coding: utf-8 -*-
import xmpp

def init(bot):
	return {'status':0,'usage':'','descr':bot.phrases['DESCR_BASH'],'gc':2}

def run(bot,mess,mode='chat'):
	command = mess.getBody()[5:]
	full = unicode(mess.getFrom())
	afull = full.split('/')
	try:
		nick = afull[1]
	except:
		nick = ''
	conf = afull[0]
	if command == 'help':
		mes = u'Плагин выводит случайный анекдот с сайта http://anekdot.ru (не больше 5 за раз)'
	elif command.isdigit():
		if int(command) <= 5 and int(command) >= 1:
			mes = getbash(int(command))
		else:
			if mode == 'groupchat':
				mode = 'chat'
				conf = full
				if int(command) > 10:
					mes = u'Больше 10 цитат нельзя даже в личку'
				else:
					mes = getbash(int(command))
	else:
		mes = getbash(1)
	bot.send(xmpp.Message(conf,mes,mode))

def rungc(bot,mess):
	#mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')

def getbash(i):
	import urllib2
	from BeautifulSoup import BeautifulSoup
	import re
	bash = urllib2.urlopen('http://bash.org.ru/random').read().decode('cp1251')
	soup = BeautifulSoup(bash)
	allcontent = soup.findAll('div', 'quote')
	allcites = []
	alldates = []
	allcitnums = []
	outcite = ''
	for content in allcontent:
		citecontent = content.find('div', 'text')
		datecontent = content.find('span', 'date')
		citnumcontent = content.find('a', 'id')
		if datecontent:
			cites = citecontent.contents
			date = datecontent.contents[0]
			citnum = citnumcontent.contents[0]
			cite = ''
			for ct in cites:
				if str(ct) == '<br />':
					cite += '\n'
				else:
					cite += unicode(ct)
			cite = cite.replace('&nbsp;', ' ')
			cite = cite.replace('&quot;', '"')
			cite = cite.replace('&lt;', '<')
			cite = cite.replace('&gt;', '>')
			cite = cite.replace('&#39;', '\'')
			date = unicode(date)
			citnum = unicode(citnum)
			allcites.append(cite)
			alldates.append(date)
			allcitnums.append(citnum)
	for j in range(i):
		outcite += u'Цитата %s от %s\n%s' % (allcitnums[j], alldates[j], allcites[j])
		outcite += '\n' + '-'*75 + '\n'
	return outcite[:-1]
