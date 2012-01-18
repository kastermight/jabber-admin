# -*- coding: utf-8 -*-
import xmpp
import time
import os


def init(bot):
	return {'status':0,'descr':bot.phrases['DESCR_THETIME'],'gc':2}

def run(bot,mess,mode='chat'):
	os.environ['TZ'] = 'Europe/Moscow'
	time.tzset()
	tim = time.localtime()
	text = bot.phrases['THE_TIME']%(tim[3],tim[4],tim[5],tim[2],bot.phrases['MONTHTIME_' + str(tim[1])],tim[0]) + u' (Время московское)'
	bot.send(xmpp.Message(mess.getFrom(),text,mode))

def rungc(bot,mess):
	mess.setFrom(str(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')
