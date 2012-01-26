# -*- coding: utf-8 -*-
import xmpp


def init(bot):
	return {'status':10,'usage':'','descr':bot.phrases['DESCR_RESTART'],'gc':0}

def run(bot,mess,mode='chat'):
	import os
	import sys
	bot.send(xmpp.Message(mess.getFrom(),bot.phrases['BOT_RS'],mode))
	bot.online = 0
	os.system('nohup python2.7 bot.py')
	#13
	sys.exit()
