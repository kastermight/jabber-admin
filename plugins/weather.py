# -*- coding: utf-8 -*-
import xmpp
import urllib2, urllib, re

def init(bot):
	return {'status':0,'usage':'<city|help>','descr':bot.phrases['DESCR_WEATHER'],'gc':2}

def run(bot,mess,mode='chat'):
	city_raw = unicode(mess.getBody()[8:])
	if city_raw == 'help':
		fmtstr = u'Список сокращений для нахождения погоды (плагин weather):\n\
		1 = Москва\n\
		2 = Санкт-Петербург\n\
		3 = Boulder\n\
		4 = Киев\n\
		5 = Бат-Ям\n\
		6 = Ростов-на-Дону\n\
		7 = Ташкент\n\
		8 = Набережные Челны\n\
		9 = Краснодар\n\
		0 = Хабаровск\n\
		10 = Курск'
	else:
		if city_raw == '': city_raw = u'Москва'
		if city_raw == '1': city_raw = u'Москва'
		if city_raw == '2': city_raw = u'Санкт-Петербург'
		if city_raw == '3': city_raw = u'Boulder'
		if city_raw == '4': city_raw = u'Киев'
		if city_raw == '5': city_raw = u'Бат-Ям'
		if city_raw == '6': city_raw = u'Ростов-на-Дону'
		if city_raw == '7': city_raw = u'Ташкент'
		if city_raw == '8': city_raw = u'Набережные Челны'
		if city_raw == '9': city_raw = u'Краснодар'
		if city_raw == '0': city_raw = u'Хабаровск'
		if city_raw == '10': city_raw = u'Курск'
		URL = 'http://www.google.com/ig/api?weather=%s&hl=ru'
		city = urllib.urlencode({'city':city_raw.encode('utf-8')}).split('=')[1]
		url = URL % city
		f = urllib2.urlopen(url)
		alldata = f.read()
		date_pat = '\<forecast_date\sdata\="([^=<>/"]*)"/\>'
		allcond_pat = '\<current_conditions\>(.+)\</current_conditions\>'
		cond_pat = '\<condition\sdata\="([^=<>/"]*)"/\>'
		temp_pat = '\<temp_c\sdata="([^=<>/"]*)"/\>'
		hum_pat = '\<humidity\sdata="([^=<>/"]*)"/\>'
		wind_pat = '\<wind_condition\sdata="([^=<>"]*)"/\>'
		
		date = re.search(date_pat, alldata)
		if date:
			date = date.group(1)
		else:
			date = u'Дата: '
		
		allcond = re.search(allcond_pat, alldata)
		if allcond:
			allcond = allcond.group(1)
			cond = re.search(cond_pat, allcond)
			if cond:
				cond = cond.group(1).decode('cp1251')
			else:
				cond = ''
				
			temp = re.search(temp_pat, allcond)
			if temp:
				temp = temp.group(1)
			else:
				temp = ''
				
			hum = re.search(hum_pat, allcond)
			if hum:
				hum = hum.group(1).decode('cp1251')
			else:
				hum = u'Влажность: '
				
			wind = re.search(wind_pat, allcond)
			if wind:
				windir = {u'С':unichr(0x21d1), u'Ю':unichr(0x21d3), u'В':unichr(0x21d2), u'З':unichr(0x21d0), \
				       u'СВ':unichr(0x21d7), u'СЗ':unichr(0x21d6), u'ЮВ':unichr(0x21d8), u'ЮЗ':unichr(0x21d9)}
				wind = unicode(wind.group(1).decode('cp1251'))
				wind_pat = u'(Ветер\:\s)(.+)(,\s\d+\sм/с)'
				wind = re.search(wind_pat, wind)
				#wind = wind.group(1) + windir[wind.group(2)] + '(' + wind.group(2) + ')' + wind.group(3)
				wind = wind.group(1) + windir[wind.group(2)] + wind.group(3)
			else:
				wind = u'Ветер:'
				
			fmt = u'Погода в городе %s на %s\nПогодные условия: %s\nТемпература воздуха: %s\n%s\n%s'
			fmtstr = fmt % (city_raw, date, cond, temp, hum, wind)
		else:
			fmtstr = u'Для данного города погода недоступна. Попробуйте ввести название на латинице'
	bot.send(xmpp.Message(mess.getFrom(),fmtstr,mode))

def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')
