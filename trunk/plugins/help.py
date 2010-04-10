# -*- coding: utf-8 -*-
import xmpp
from __main__ import get_priv


def init():
	return {'status':0,'descr':'Commands helper','gc':2}

def run(bot,mess):
	user=unicode(mess.getFrom())
	priv = get_priv(user)
	text = bot.phrases['ACC_LEVEL']%priv
	for i in range(priv,-1,-1):
		geted = bot.plugins.get('commands_'+unicode(i))
		if ((geted != None)):
			text += '\n----' + bot.phrases['LEVEL_CMD']%i + '----'
			for x in geted:
				plug = getattr(bot.plugins['plugins'],x)
				if (plug.init().get('gc') == 2) or (plug.init().get('gc') == 0):
					gets = plug.init().get('usage')
					if (gets != None):
						text += '\n' + x + ' ' + plug.init()['usage'] + ' - ' + plug.init()['descr']
					else:
						text += '\n' + x +  ' - ' + plug.init()['descr']
	bot.send(xmpp.Message(mess.getFrom(),text))

def rungc(bot,mess):
	room=unicode(mess.getFrom()).split('/')[0]
	text = bot.phrases['AV_COMMANDS'] + ':'
	geted = bot.plugins.get('commands_0')
	if ((geted != None)):
		for x in geted:
			plug = getattr(bot.plugins['plugins'],x)
			if plug.init().get('gc') != 0:
				gets = plug.init().get('usage')
				if (gets != None):
					text += '\n' + x + ' ' + plug.init()['usage'] + ' - ' + plug.init()['descr']
				else:
					text += '\n' + x +  ' - ' + plug.init()['descr']
	bot.send(xmpp.Message(room,text,'groupchat'))