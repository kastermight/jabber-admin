import xmpp
import time
import xml.dom.minidom as md
import httplib
import re


def init():
	return {'status':9,'usage':'<site>','descr':'RSS News reader','gc':0}

def getTitle(obj):
	try:
		ret = obj.getElementsByTagName('title')[0].firstChild.data
	except:
		ret = ''
	return ret

def replace_all(text,dic):
	for i, j in dic.iteritems():
		text = text.replace(i, j)
	return text


def getDescr(obj):
	rets = obj.getElementsByTagName('description')[0].childNodes
	ret = ''
	for i in rets:
		ret += i.data
	dics = {
		'&nbsp;':' ',
		'<br>':'\n',
		'<br />':'\n',
		'&amp;':'&',
		'&quot;':'"',
	}
	ret = replace_all(ret,dics)
	ret = re.sub('<[^<]*>',' ',ret)
	ret = re.sub('&#[\d]{4}',' ',ret)
	return ret

def getLink(obj):
	try:
		ret = obj.getElementsByTagName('link')[0].firstChild.data
	except:
		ret = ''
	return ret

def getPubDate(obj):
	mons = {
		'Jan':1,
		'Febrary':2,
		'March':3,
		'Apr':4,
		'May':5,
		'Jun':6,
		'Jul':7,
		'Aug':8,
		'Sep':9,
		'Oct':10,
		'Nov':11,
		'Dec':12
	}
	mons2 = {
		1:31,
		2:28,
		3:31,
		4:30,
		5:31,
		6:30,
		7:31,
		8:31,
		9:30,
		10:31,
		11:30,
		12:31
	}
	try:
		date = obj.getElementsByTagName('pubDate')[0].firstChild.data
		res = re.match('(.{3}), ([\d]{2}) (.{3}) [\d]{2}([\d]{2}) ([\d]{2}):([\d]{2}):([\d]{2})',date)
		res = res.groups()
		number = int(res[1])
		month = mons[res[2]]
		year = int(res[3])
		hour = int(res[4])
		min = int(res[5])
		sec = int(res[6])
		ret = year*365*24*60*60+month*mons2[month]*24*60*60+hour*60*60+min*60+sec
	except:
		ret = 0
	return ret

def run(bot,mess):
	try:
		site = re.match('rss http://(.*)',mess.getBody()).groups()[0]
		page2 = site.split('/')
		site = page2[0]
		del page2[0]
		page = ''
		for i in page2:
			page += '/' + i
	except:
		return
	readrss = 1
	fpubdate = 0
	while readrss:
		conn = httplib.HTTPConnection(site)
		conn.request("GET", page)
		response = conn.getresponse()
		data = response.read()
		conn.close()
		data = data.replace('\n',' ')
		data = data.replace('\t','')
		xml = md.parseString(data)
		items = xml.getElementsByTagName('channel')[0].getElementsByTagName('item')
		for i in items:
				if (fpubdate < getPubDate(i)):
					bot.send(xmpp.Message(mess.getFrom(),'New post at http://' + site + ':\n\n' + getTitle(i) + '\n\n' + getDescr(i) + '\n\nRead online: ' + getLink(i)))
				else:
					break
		fpubdate = getPubDate(items[0])
		time.sleep(60)