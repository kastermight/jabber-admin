# -*- coding: utf-8 -*-
import xmpp
import time


def init(bot):
	return {'status':0,'descr':bot.phrases['DESCR_THETIME'],'gc':2}

def run(bot,mess,mode='chat'):
	mon = {
		1:'January',
		2:'Febrary',
		3:'March',
		4:'April',
		5:'May',
		6:'June',
		7:'Jule',
		8:'August',
		9:'September',
		10:'October',
		11:'November',
		12:'December'
	}
	tim = time.localtime()
	text = bot.phrases['THE_TIME']%(tim[3],tim[4],tim[5],tim[2],mon[tim[1]],tim[0])
	bot.send(xmpp.Message(mess.getFrom(),text,mode))

def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')