# -*- coding: utf-8 -*-
import xmpp
import time
import os
import os.path

log = 0

def writeLog(bot,filename,text):
	nowtime = time.localtime()
	path = bot.config['plugins_settings']['logs_path'] + "/" + unicode(nowtime[0]) + "/" + bot.phrases['MONTH_' + unicode(nowtime[1])] + "/" + unicode(nowtime[2])
	if not os.path.exists(path):
		os.makedirs(path)
	text = '[' + unicode(nowtime[3]) + ':' + unicode(nowtime[4]) + ':' + unicode(nowtime[5]) + '] ' + text
	fl = open(path + "/" + filename + '.txt',"ab+")
	fl.write(text + "\n")
	fl.close()

def onMessage(bot,mess):
	if log == 1:
		if mess.getType() == 'chat':
			writeLog(bot,unicode(mess.getFrom()).split('/')[0],"%s: %s"%(unicode(mess.getFrom()).split('@')[0],unicode(mess.getBody())))
		elif mess.getType() == 'groupchat':
			writeLog(bot,unicode(mess.getFrom()).split('/')[0],"%s: %s"%(unicode(mess.getFrom()).split('/')[1],mess.getBody()))

def onConference(bot,pres,x):
	if log == 1:
		writeLog(bot,unicode(pres.getFrom()).split('/')[0],"%s changed role to %s and affiliation to %s"%(unicode(pres.getFrom()).split('/')[1],x.getTag('item').getAttr('role'),x.getTag('item').getAttr('affiliation')))

def onSubscribe(bot,pres):
	if log == 1:
		writeLog(bot,unicode(pres.getFrom()),"%s subscribed"%unicode(pres.getFrom()))

def onUnsubscribe(bot,pres):
	if log == 1:
		writeLog(bot,unicode(pres.getFrom()),"%s unsubscribed"%unicode(pres.getFrom()))

def init(bot):
	global log
	log = int(bot.config['plugins_settings']['logging'])
	return {'status':10,'usage':'start|stop','descr':bot.phrases['DESCR_LOG'],'gc':0}

def run(bot,mess):
	cmd = unicode(mess.getBody()).split(' ')[1]
	if cmd == 'start':
		if log == 1:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['LOG_ARUN']))
		else:
			log = 1
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['LOG_START']))
	elif cmd == 'stop':
		if log == 0:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['LOG_NRUN']))
		else:
			log = 0
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['LOG_STOP']))