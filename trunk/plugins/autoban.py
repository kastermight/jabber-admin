# -*- coding: utf-8 -*-
import xmpp
import re

auban = 0

def onPluginStart(bot):
	global auban
	auban = int(bot.config['plugins_settings']['auban'])
	bot.config['plugins_settings']['autoban'] = bot.config['plugins_settings']['autoban'].split(',')

def init(bot):
	return {'status':10,'usage':'start|stop','descr':bot.phrases['DESCR_AUBAN'],'gc':1}

def onConference(bot,pres,x):
	if auban == 1:
		if pres.getJid() != None:
			jid = pres.getJid()
			for i in bot.config['plugins_settings']['autoban']:
				if re.match(i,jid,re.IGNORECASE) != None:
					iq = xmpp.Iq(to=unicode(pres.getFrom()).split('/')[0],typ='set')
					query = iq.appendChild('query')
					query.setAttr('xmlns','http://jabber.org/protocol/muc#admin')
					item = query.appendChild('item')
					item.setAttr('affiliation','outcast')
					item.setAttr('jid',jid)
					bot.send(iq)

def rungc(bot,mess):
	priv = bot.visitors[unicode(mess.getFrom()).split('/')[0]][unicode(mess.getFrom()).split('/')[1]][1]
	if (priv == 'admin') or (priv == 'owner'):
		mess.setFrom(unicode(mess.getFrom()).split('/')[0])
		global auban
		cmd = unicode(mess.getBody()).split(' ')
		if len(cmd) < 2:
			return
		cmd = cmd[1]
		if cmd == 'start':
			if auban == 0:
				bot.send(xmpp.Message(mess.getFrom(),bot.phrases['AUBAN_STARTED'],'groupchat'))
			else:
				bot.send(xmpp.Message(mess.getFrom(),bot.phrases['AUBAN_ARUN'],'groupchat'))
		elif cmd == 'stop':
			if auban == 1:
				bot.send(xmpp.Message(mess.getFrom(),bot.phrases['AUBAN_STOPPED'],'groupchat'))
			else:
				bot.send(xmpp.Message(mess.getFrom(),bot.phrases['AUBAN_NRUN'],'groupchat'))