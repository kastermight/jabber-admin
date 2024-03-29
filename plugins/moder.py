# -*- coding: utf-8 -*-
import xmpp
import time


def init(bot):
	return {'status':0,'usage':'list [<conference>]|(add|delete <nick>)','descr':bot.phrases['DESCR_MODER'],'gc':1}

class Moders():
	def add(self,bot,mess,args):
		if args[0] not in bot.visitors[unicode(mess.getFrom()).split('/')[0]]:
			return
		priv = bot.visitors[unicode(mess.getFrom()).split('/')[0]][unicode(mess.getFrom()).split('/')[1]][1]
		if (priv == 'owner') or (priv == 'admin'):
			nick = args[0]
			if nick in bot.config['conferences'][unicode(mess.getFrom()).split('/')[0]]:
				bot.send(xmpp.Message(unicode(mess.getFrom()).split('/')[0],bot.phrases['AL_MODER']%nick,'groupchat'))
				return
			if (bot.visitors[unicode(mess.getFrom()).split('/')[0]][nick][1] == 'owner') or (bot.visitors[unicode(mess.getFrom()).split('/')[0]][nick][1] == 'admin'):
				return
			bot.visitors[unicode(mess.getFrom()).split('/')[0]][nick][1] = 'member'
			bot.config['conferences'][unicode(mess.getFrom()).split('/')[0]].append(nick)
			iq = xmpp.Iq('set')
			iq.setAttr('to',unicode(mess.getFrom()).split('/')[0])
			query = iq.addChild('query')
			query.setNamespace('http://jabber.org/protocol/muc#admin')
			item = query.addChild('item')
			item.setAttr('nick',nick)
			item.setAttr('role','moderator')
			item2 = query.addChild('item')
			item2.setAttr('affiliation','member')
			item2.setAttr('jid',bot.visitors[unicode(mess.getFrom()).split('/')[0]][nick][0])
			bot.send(iq)
			bot.send(xmpp.Message(unicode(mess.getFrom()).split('/')[0],bot.phrases['MODER_ADD']%nick,'groupchat'))
	def delete(self,bot,mess,args):
		if args[0] not in bot.visitors[unicode(mess.getFrom()).split('/')[0]]:
			return
		priv = bot.visitors[unicode(mess.getFrom()).split('/')[0]][unicode(mess.getFrom()).split('/')[1]][1]
		if (priv == 'owner') or (priv == 'admin'):
			nick = args[0]
			if (bot.visitors[unicode(mess.getFrom()).split('/')[0]][nick][1] == 'owner') and (bot.visitors[unicode(mess.getFrom()).split('/')[0]][nick][1] == 'admin'):
				return
			if nick not in bot.config['conferences'][unicode(mess.getFrom()).split('/')[0]]:
				bot.send(xmpp.Message(unicode(mess.getFrom()).split('/')[0],bot.phrases['NOT_MODER']%nick,'groupchat'))
				return
			bot.visitors[unicode(mess.getFrom()).split('/')[0]][nick][1] = 'member'
			bot.config['conferences'][unicode(mess.getFrom()).split('/')[0]].remove(nick)
			iq = xmpp.Iq('set')
			iq.setAttr('to',unicode(mess.getFrom()).split('/')[0])
			query = iq.addChild('query')
			query.setNamespace('http://jabber.org/protocol/muc#admin')
			item = query.addChild('item')
			item.setAttr('nick',nick)
			item.setAttr('role','participant')
			item2 = query.addChild('item')
			item2.setAttr('affiliation','member')
			item2.setAttr('jid',bot.visitors[unicode(mess.getFrom()).split('/')[0]][nick][0])
			bot.send(iq)
			time.sleep(1)
			bot.send(xmpp.Message(unicode(mess.getFrom()).split('/')[0],bot.phrases['MODER_DELETE']%nick,'groupchat'))
	def list(self,bot,mess,args):
		if len(args) == 0:
			room = unicode(mess.getFrom()).split('/')[0]
		else:
			room = args[0]
		if len(bot.config['conferences'][room]) == 0:
			text = bot.phrases['NMODERS']
		else:
			text = bot.phrases['MODERS'] + ':'
			for i in bot.config['conferences'][room]:
				text += '\n' + i
		bot.send(xmpp.Message(room,text,'groupchat'))

def rungc(bot,mess):
	cmd = unicode(mess.getBody()).split(' ')
	if len(cmd) < 2:
		return
	args = cmd[2:]
	cmd = cmd[1]
	exec1 = getattr(Moders(),cmd,None)
	if exec1 != None:
		exec1(bot,mess,args)
