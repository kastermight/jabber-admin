# -*- coding: utf-8 -*-
import xmpp
import thread


def init():
	return {'status':0,'usage':'<question>','descr':'Voting','gc':1}

def voteResult(bot,theme,room):
	import time
	time.sleep(60)
	bot.send(xmpp.Message(room,bot.phrases['VOTE_RESULT']%(bot.vote[room]['yes'],bot.vote[room]['no']),'groupchat'))
	time.sleep(1)
	if bot.vote[room]['yes'] > bot.vote[room]['no']:
		bot.send(xmpp.Message(room,bot.phrases['VOTE_YES']%theme,'groupchat'))
	elif bot.vote[room]['yes'] < bot.vote[room]['no']:
		bot.send(xmpp.Message(room,bot.phrases['VOTE_NO']%theme,'groupchat'))
	else:
		bot.send(xmpp.Message(room,bot.phrases['VOTES_EQUAL'],'groupchat'))
	bot.vote[room] = {}

def rungc(bot,mess):
	room = unicode(mess.getFrom()).split('/')[0]
	x1 = bot.vote.get(room,None)
	if x1 != None:
		if len(x1) != 0:
			bot.send(xmpp.Message(room,bot.phrases['WAIT_VOTE_END'],'groupchat'))
			return
	inic = unicode(mess.getFrom()).split('/')[1]
	vr = mess.getBody().split(' ',1)
	del vr[0]
	if len(vr) == 0:
		return
	theme = unicode(vr[0])
	bot.vote.update({room:{'yes':0,'no':0,'al':[inic]}})
	bot.send(xmpp.Message(room,bot.phrases['INIT_VOTE']%(inic,theme),'groupchat'))
	thread.start_new_thread(voteResult,(bot,theme,room))