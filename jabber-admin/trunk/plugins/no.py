# -*- coding: utf-8 -*-
import xmpp


def init():
	return {'status':0,'descr':'Vote no','gc':1}

def rungc(bot,mess):
	user = unicode(mess.getFrom()).split('/')[1]
	room = unicode(mess.getFrom()).split('/')[0]
	x1 = bot.vote.get(room)
	if x1 != {}:
		if user not in bot.vote[room]['al']:
			bot.vote[room]['no'] += 1
			bot.vote[room]['al'].append(user)
		else:
			bot.send(xmpp.Message(room,bot.phrases['AL_VOTED']%user,'groupchat'))