# -*- coding: utf-8 -*-
import xmpp
import time
import os
import os.path

log = 0

def writeLog(bot,filename,text):
	nowtime = list(time.localtime())
	path = bot.config['plugins_settings']['logs_path'] + "/" + str(nowtime[0]) + "/" + bot.phrases['MONTH_' + str(nowtime[1])] + "/" + str(nowtime[2])
	if not os.path.exists(path):
		os.makedirs(path)
	if len(str(nowtime[3])) < 2: nowtime[3] = '0' + str(nowtime[3])
	if len(str(nowtime[4])) < 2: nowtime[4] = '0' + str(nowtime[4])
	if len(str(nowtime[5])) < 2: nowtime[5] = '0' + str(nowtime[5])
	text = '[' + str(nowtime[3]) + ':' + str(nowtime[4]) + ':' + str(nowtime[5]) + '] ' + text
	fl = open(path + "/" + filename + '.txt',"ab+")
	fl.write(text.encode('utf-8') + "\n")
	fl.close()

def onMessage(bot,mess):
	if log == 1:
		if mess.getType() == 'chat':
			writeLog(bot,str(mess.getFrom()).replace("/","-"),"%s: %s"%(str(mess.getFrom()).split('@')[0],mess.getBody()))
		elif mess.getType() == 'groupchat':
			if len(unicode(mess.getFrom()).split('/')) > 1:
				writeLog(bot,str(mess.getFrom()).split('/')[0],"%s: %s"%(str(mess.getFrom()).split('/')[1],mess.getBody()))
			else:
				writeLog(bot,str(mess.getFrom()),"The topic is %s"%mess.getBody())

def onConference(bot,pres,x):
	if log == 1:
		writeLog(bot,str(pres.getFrom()).split('/')[0],"%s changed role to %s and affiliation to %s"%(str(pres.getFrom()).split('/')[1],x.getTag('item').getAttr('role'),x.getTag('item').getAttr('affiliation')))

def onSubscribe(bot,pres):
	if log == 1:
		writeLog(bot,str(pres.getFrom()),"%s subscribed"%str(pres.getFrom()))

def onUnsubscribe(bot,pres):
	if log == 1:
		writeLog(bot,str(pres.getFrom()),"%s unsubscribed"%str(pres.getFrom()))

def init(bot):
	global log
	log = int(bot.config['plugins_settings']['logging'])
	return {'status':10,'usage':'start|stop','descr':bot.phrases['DESCR_LOG'],'gc':0}

def run(bot,mess):
	cmd = mess.getBody().split(' ')[1]
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
