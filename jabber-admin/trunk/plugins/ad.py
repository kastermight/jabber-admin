# -*- coding: utf-8 -*-
import xmpp
import time

id = 0

def init():
	return {'status':10,'usage':'<start|stop>','descr':'ADverts','gc':0}

def runAD(bot,mess):
	global id
	time.sleep(600)
	ads = open('ad.txt').read().split('\n')
	if id >= len(ads):
		id = 0
	for room in bot.visitors:
		bot.send(xmpp.Message(room,ads[id],'groupchat'))
	id += 1

class AD():
	def start(self,bot,mess):
		if bot.ad == 1:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['AD_ARUN']))
		else:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['AD_START']))
			bot.ad=1
			while bot.ad==1:
				runAD(bot,mess)
	def stop(self,bot,mess):
		if bot.ad == 0:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['AD_NRUN']))
		else:
			bot.ad = 0
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['AD_STOP']))

def run(bot,mess):
	cmd = unicode(mess.getBody()).split(' ')
	if len(cmd) != 2:
		return
	cmd = cmd[1]
	exec1 = getattr(AD(),cmd)
	if exec1 != None:
		exec1(bot,mess)