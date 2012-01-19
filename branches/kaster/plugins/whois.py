# -*- coding: utf-8 -*-
import xmpp
import urllib2
import socket
import re
import os
try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")

def init(bot):
	return {'status':0,'usage':'<ip/hostname>','descr':bot.phrases['DESCR_WHOIS'],'gc':2}

def run(bot,mess,mode='chat'):
	command = unicode(mess.getBody()[6:])
	URL = 'https://apps.db.ripe.net/whois/search.xml?query-string=%s&source=ripe'
	if command == 'help':
		mes = u' Плагин для выдачи информации о хосте или ip-адресе. Допускаются русскоязычные домены, например - президент.рф или путин.рф'
	elif not command:
		mes = u'Ввод параметра в виде ip-адреса или имени хоста обязателен'
	else:
		puny = command.encode('idna')
		try:
			hostip = socket.gethostbyaddr(puny)
		except socket.gaierror:
			mes = u'Введенное имя хоста или ip-aдрес неверен, либо не содержится в базe DNS'
		except socket.herror:
			ip = socket.gethostbyname(puny)
			host = puny
		else:
			ip = hostip[2][0]
			host = hostip[0].split('.')
		host = host[-2] + '.' + host[-1]
		url = URL % ip
		mes = getwhois(url)
		if not mes:
			mes = u'Данного узла в базе ripe.net нет, попробую поискать в локальной базе\n'
			mes += '-'*50 + '\n'
			ans = getfromcon(host)
			if not ans: mes += u'Для данного узла информация не найдена'
			mes += ans
		mes = mes[:-1]
	bot.send(xmpp.Message(mess.getFrom(),mes,mode))

def rungc(bot,mess):
	print mess.getFrom()
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')

def getwhois(url):
	db = urllib2.urlopen(url)
	xmldoc = etree.parse(db)
	allobj = xmldoc.findall('objects/object')
	whoinfo = ''
	for obj in allobj:
		if obj.attrib == {'type':'inetnum'}:
			subobjall = obj.findall('attributes/attribute')
			for subobj in subobjall:
				attr = subobj.attrib
				if attr['name'] in ['inetnum', 'netname', 'descr', 'country']:
					if attr['name'] == 'netname' and attr['value'] == 'IANA-BLK': return False
					whoinfo += '%s: %s\n' % (attr['name'].ljust(15), attr['value'])
			whoinfo += '-'*50 + '\n'
		if obj.attrib == {'type':'person'}:
			subobjall = obj.findall('attributes/attribute')
			for subobj in subobjall:
				attr = subobj.attrib
				if attr['name'] in ['person', 'address', 'e-mail', 'phone']:
					whoinfo += '%s: %s\n' % (attr['name'].ljust(15), attr['value'])
			whoinfo += '-'*50 + '\n'
		if obj.attrib == {'type':'role'}:
			subobjall = obj.findall('attributes/attribute')
			for subobj in subobjall:
				attr = subobj.attrib
				if attr['name'] in ['role', 'address', 'phone', 'fax-no', 'remarks', 'abuse-mailbox']:
					whoinfo += '%s: %s\n' % (attr['name'].ljust(15), attr['value'])
			whoinfo += '-'*50 + '\n'
		if obj.attrib == {'type':'route'}:
			subobjall = obj.findall('attributes/attribute')
			for subobj in subobjall:
				attr = subobj.attrib
				if attr['name'] in ['route', 'descr', 'origin']:
					whoinfo += '%s: %s\n' % (attr['name'].ljust(15), attr['value'])
			whoinfo += '-'*50 + '\n'
	return whoinfo

def getfromcon(host):
	os.system('whois ' + host + ' > tmp')
	tmp = open('tmp')
	lines = tmp.readlines()
	tmp.close()
	os.remove('tmp')
	pat = '^([^%#,>]+?)\:(.+)'
	ans = ''
	ansre = re.compile(pat)
	for line in lines:
		if 'No match for domain' in line:
			return False
		line = ansre.search(line)
		if line:
			ans += '%s: %s\n' % (line.group(1).ljust(30), line.group(2))
	return ans
