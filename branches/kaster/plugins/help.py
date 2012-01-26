# -*- coding: utf-8 -*-
import xmpp


def init(bot):
	return {'status':0,'descr':bot.phrases['DESCR_HELP'],'gc':2}

def run(bot,mess):
	user=unicode(mess.getFrom()).split('/')[0]
	priv = bot.get_priv(user)
	text = bot.phrases['ACC_LEVEL']%priv
	for i in range(priv,-1,-1):
		geted = bot.plugins.get('commands_'+unicode(i))
		if ((geted != None)):
			text += '\n----' + bot.phrases['LEVEL_CMD']%i + '----'
			for x in geted:
				plug = getattr(bot.plugins['plugins'],x)
				if plug.init(bot).get('gc') != 1:
					gets = plug.init(bot).get('usage')
					if (gets != None):
						text += '\n' + x + ' ' + plug.init(bot)['usage'] + ' - ' + plug.init(bot)['descr']
					else:
						text += '\n' + x +  ' - ' + plug.init(bot)['descr']
	bot.send(xmpp.Message(mess.getFrom(),text))

def rungc(bot,mess):
	room=unicode(mess.getFrom()).split('/')[0]
	text = bot.phrases['AV_COMMANDS'] + ':'
	for cmds in bot.plugins.items():
		if cmds[0] != 'plugins':
			for plugname in cmds[1]:
				plug = getattr(bot.plugins['plugins'],plugname)
				if plug.init(bot).get('gc') != 0:
					gets = plug.init(bot).get('usage')
					if (gets != None):
						text += '\n' + plugname + ' ' + plug.init(bot)['usage'] + ' - ' + plug.init(bot)['descr']
					else:
						text += '\n' + plugname +  ' - ' + plug.init(bot)['descr']
	bot.send(xmpp.Message(room,text,'groupchat'))
