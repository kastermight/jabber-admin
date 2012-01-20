# -*- coding: utf-8 -*-
import xmpp
import urllib2
import socket
import re
import os
import time
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
	URLRIPE = 'https://apps.db.ripe.net/whois/search.xml?query-string=%s&source=ripe'
	URLARIN = 'http://adam.kahtava.com/services/whois.xml?query=%s'
	if command == 'help':
		mes = u' Плагин для выдачи информации о хосте или ip-адресе. Допускаются русскоязычные домены, например - президент.рф или путин.рф'
	elif not command:
		mes = u'Ввод параметра в виде ip-адреса или имени хоста обязателен'
	else:
		ippat = '\d{1:3}\.\d{1:3}\.\d{1:3}\.\d{1:3}'
		hostpat = '(.+\.)?([^.]+\.\w+)'
		ip = re.search(ippat, command)
		host = re.search(hostpat, command)
		if ip or host:
			if ip:
				ip = ip.group(0)
			elif host:
				host = host.group(2)
				ip = socket.gethostbyname(host)
			url = URLRIPE % ip
			mes = getwhoisRIPE(url)
			if not mes:
				mes = u'Введенный узел в базе данных RIPE (Европа) не обнаружен. Попробую поискать в базе данных ARIN (Северная Америка)\n'
				mes += '-'*100 + '\n'
				url = URLARIN % ip
				mestmp = getwhoisARIN(url)
				if not mestmp:
					mes += u'Введенный узел так же не обнаружен в базе данных ARIN. Других баз пока нет. Попробуйте поискать вручную.'
				else:
					mes += mestmp
		else:
			mes = u'Введеное значение не является ни ip-адресом, ни именем хоста в привычном понимание - something.somesite.xx'
	bot.send(xmpp.Message(mess.getFrom(),mes,mode))

def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')

def getwhoisRIPE(url):
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
	return whoinfo[:-1]

def getwhoisARIN(url):
	import urllib2
	from lxml import etree
	def xmlprint(el, n):
		out = '  '*n
		if el.text:
			out += el.tag + ': ' + el.text + '\n'
		else:
			out += el.tag + '\n'
			for sel in el:
				out += xmlprint(sel, n + 1)
		return out
	db = urllib2.urlopen(url).read().replace('xmlns="http://adam.kahtava.com/services/whois" ', '').replace('&#xD;', '')
	try:
		xmldoc = etree.fromstring(db)
	except:
		return False
	out = ''
	for sxml in xmldoc:
		out += xmlprint(sxml, 0)
	return out[:-1]
