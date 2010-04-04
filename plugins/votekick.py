# -*- coding: utf-8 -*-
import xmpp
import thread


def init():
	return {'status':0,'usage':'<who>','descr':'Kick user','gc':1}

def voteResult(bot,tokick,room):
	import time
	time.sleep(60)
	bot.send(xmpp.Message(room,bot.phrases['VOTE_RESULT']%(bot.vote[room]['yes'],bot.vote[room]['no']),'groupchat'))
	time.sleep(1)
	if bot.vote[room]['yes'] > bot.vote[room]['no']:
		iq = xmpp.Iq('set')
		iq.setAttr('to',room)
		iq.addChild('query')
		iq.getTag('query').setAttr('xmlns','http://jabber.org/protocol/muc#admin')
		iq.getTag('query').addChild('item')
		iq.getTag('query').getTag('item').setAttr('nick',tokick)
		iq.getTag('query').getTag('item').setAttr('role','none')
		iq.getTag('query').getTag('item').addChild('reason')
		iq.getTag('query').getTag('item').getTag('reason').setData('You kicked by voting')
		bot.send(iq)
		bot.send(xmpp.Message(room,bot.phrases['NICK_KICKED']%tokick,'groupchat'))
	elif bot.vote[room]['yes'] < bot.vote[room]['no']:
		bot.send(xmpp.Message(room,bot.phrases['NICK_NOT_KICKED']%tokick,'groupchat'))
	else:
		bot.send(xmpp.Message(room,bot.phrases['VOTES_EQUAL'],'groupchat'))
	bot.vote[room] = {}

def rungc(bot,mess):
	room = unicode(mess.getFrom()).split('/')[0]
	x1 = bot.vote.get(room)
	if x1 != None:
		if len(x1) != 0:
			bot.send(xmpp.Message(room,bot.phrases['WAIT_VOTE_END'],'groupchat'))
			return
	inic = unicode(mess.getFrom()).split('/')[1]
	vr = unicode(mess.getBody()).split(' ')
	if len(vr) != 2:
		return
	tokick = vr[1]
	bot.vote.update({room:{'yes':0,'no':0,'al':[inic,tokick]}})
	bot.send(xmpp.Message(room,bot.phrases['INIT_KICK']%(inic,tokick),'groupchat'))
	thread.start_new_thread(voteResult,(bot,tokick,room))