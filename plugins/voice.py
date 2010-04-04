# -*- coding: utf-8 -*-
import xmpp


def init():
	return {'status':0,'descr':'Makes you participant','gc':0}

def run(bot,mess):
	iq = xmpp.Iq('set')
	iq.setAttr('to',unicode(mess.getFrom()).split('/')[0])
	query = iq.addChild('query')
	query.setAttr('xmlns','http://jabber.org/protocol/muc#admin')
	item = query.addChild('item')
	item.setAttr('nick',unicode(mess.getFrom()).split('/')[1])
	item.setAttr('role','participant')
	item2 = query.addChild('item')
	item2.setAttr('jid',bot.visitors[unicode(mess.getFrom()).split('/')[0]][unicode(mess.getFrom()).split('/')[1]][0])
	item2.setAttr('affiliation','member')
	bot.visitors[unicode(mess.getFrom()).split('/')[0]][unicode(mess.getFrom()).split('/')[1]][1] = 'member'
	bot.send(iq)
	bot.send(xmpp.Message(mess.getFrom(),bot.phrases['CAN_TALK']))