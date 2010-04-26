# coding: utf-8
import xmpp
import time

def onPluginStart(bot):
	bot.vote = {}
	bot.visitors = {}
	if bot.config['autojoin'] == 1:
		for room in bot.config['conf_moders']:
			p=xmpp.Presence(to='%s/%s'%(room,bot.config['conf_nick']))
			p.addChild('x')
			p.getTag('x').setAttr('xmlns','http://jabber.org/protocol/muc')
			p.getTag('x').addChild('password')
			p.getTag('x').getTag('password').setData('japass')
			p.getTag('x').addChild('history',{'maxchars':'0','maxstanzas':'0'})
			p.setStatus('JAdmin - mobile life')
			bot.send(p)
			bot.vote.update({room:{}})
			bot.visitors.update({room:{}})
			time.sleep(0.2)

def init():
	return {'status':10,'usage':'<join|leave> <room>','descr':'Rooms management','gc':0}

class Rooms():
	def join(self,bot,mess,args):
		conf = args[0]
		if conf not in bot.visitors:
			p=xmpp.Presence(to='%s/%s'%(conf,bot.config['conf_nick']))
			p.addChild('x')
			p.getTag('x').setAttr('xmlns','http://jabber.org/protocol/muc')
			p.getTag('x').addChild('password')
			p.getTag('x').getTag('password').setData('japass')
			p.getTag('x').addChild('history',{'maxchars':'0','maxstanzas':'0'})
			p.setStatus('JAdmin - mobile life')
			bot.send(p)
			bot.vote.update({conf:{}})
			bot.visitors.update({conf:{}})
			bot.config['conf_moders'].update({conf:[]})
			time.sleep(0.2)
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['ROOMS_JOINED']%conf))
		else:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['ROOMS_AIN']%conf))
	def leave(self,bot,mess,args):
		conf = args[0]
		if conf in bot.visitors:
			p=xmpp.Presence(to='%s/%s'%(conf,bot.config['conf_nick']))
			p.setAttr('type','unavailable')
			p.setStatus('JAdmin - mobile life')
			bot.send(p)
			del bot.visitors[conf]
			del bot.vote[conf]
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['ROOMS_LEAVED']%conf))
		else:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['ROOMS_NIN']%conf))

def run(bot,mess):
	data = mess.getBody().split(' ')
	if len(data) < 2:
		return
	exec1 = getattr(Rooms(),data[1],None)
	if exec1 != None:
		exec1(bot,mess,data[2:])