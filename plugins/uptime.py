# -*- coding: utf-8 -*-
import xmpp
import time

stime = 0.0

def secs2arr(secs):
	years = int(secs/60/60/24/30/12)
	secs -= years*60*60*24*30*12
	months = int(secs/60/60/24/30)
	secs -= months*60*60*24*30
	days = int(secs/60/60/24)
	secs -= days*60*60*24
	hours = int(secs/60/60)
	secs -= hours*60*60
	minutes = int(secs/60)
	secs -= minutes*60
	seconds = int(secs)
	return [years,months,days,hours,minutes,seconds]

def onPluginStart(bot):
	global stime
	stime = time.time()

def noNetworkPre(bot):
	global stime
	stime = time.time() - 300

def noNetworkPost(bot):
	global stime
	stime = time.time() - 300

def init(bot):
	return {'status':1,'descr':bot.phrases['DESCR_UPTIME'],'gc':2}

def run(bot,mess,mode='chat'):
	a = secs2arr(time.time() - stime)
	uptime = ''
	if a[0] > 0: uptime += bot.phrases['UP_YEARS']%int(a[0]) + ' '
	if a[1] > 0: uptime += bot.phrases['UP_MONTHS']%int(a[1]) + ' '
	if a[2] > 0: uptime += bot.phrases['UP_DAYS']%int(a[2]) + ' '
	if a[3] > 0: uptime += bot.phrases['UP_HOURS']%int(a[3]) + ' '
	if a[4] > 0: uptime += bot.phrases['UP_MINS']%int(a[4]) + ' '
	if a[5] > 0: uptime += bot.phrases['UP_SECS']%int(a[5])
	bot.send(xmpp.Message(mess.getFrom(),bot.phrases['UPTIME']%uptime,mode))

def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')