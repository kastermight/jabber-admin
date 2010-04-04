# -*- coding: utf-8 -*-
import xmpp
import sqlite3
import random
import time


def init():
	return {'status':0,'usage':'[add|del] <word>','descr':'Words manage','gc':1}

class Word():
	dbs = sqlite3.connect("base.db")
	db = dbs.cursor()
	def add(self,bot,mess,args):
		word = args[0]
		descr = u' '.join(args[1:])
		obj = db.execute("SELECT word,stat FROM words WHERE word=?",(word,)).fetchone()
		if obj != None:
			db.execute("DELETE FROM words WHERE word=?",(word,))
			db.execute("INSERT INTO words VALUES (?,?)",(word,descr))
		else:
			db.execute("INSERT INTO words VALUES (?,?)",(word,descr))
		bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_ADDED']%word,mode))
		dbs.commit()
	def delete(self,bot,mess,args):
		word = args[0]
		dl = db.execute("DELETE FROM words WHERE word=?",(word,))
		if dl.rowcount >= 1:
			dbs.commit()
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_DELETED']%word,mode))
		else:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_NWORD']%word,mode))
	def start(self,bot,mess,args):
		if bot.words==1:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_ARUN'],mode))
		else:
			bot.words=1
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_START'],mode))
			random.seed = unicode(mess.getFrom())
			while bot.words==1:
				time.sleep(1200)
				db = dbs.cursor()
				obj = len(db.execute("SELECT word,stat FROM words").fetchall())
				if obj != 0:
					rand = random.randint(1,obj)
					randphrase = db.execute("SELECT word,stat FROM words LIMIT %d,%d"%(rand-1,rand)).fetchone()
					bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_SAY']%(randphrase[0],randphrase[1]),mode))
				else:
					bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_NWORDS'],mode))
				db.close()
	def stop(self,bot,mess,args):
		if bot.word==0:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_NRUN'],mode))
		else:
			bot.word=0
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_STOP'],mode))
	def list(self,bot,mess,args):
		word = args[0]
		obj = db.execute("SELECT word FROM words",(word,)).fetchall()
		if obj != None:
			bot.send(xmpp.Message(mess.getFrom(),u''.join(obj),mode))
		else:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_NWORDS'],mode))
		dbs.commit()
	def getWord(self,bot,mess,args):
		word = args[0]
		obj = db.execute("SELECT word,stat FROM words WHERE word=?",(word,)).fetchone()
		if obj != None:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_SAY']%(obj[0],obj[1]),mode))
		else:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_NWORD']%word,mode))
def rungc(bot,mess):
	cmd = unicode(mess.getBody()).split(' ')
	if len(cmd) < 2:
		return
	priv = bot.visitors[unicode(mess.getFrom()).split('/')[0]][unicode(mess.getFrom()).split('/')[1]][1]
	if (priv == 'admin') or (priv == 'owner'):
		mess.setFrom(unicode(mess.getFrom()).split('/')[0])
		args = cmd[2:]
		cmd = cmd[1]
		exec1 = getattr(Word(),cmd,None)
		if exec1 == None:
			Word().getWord(bot,mess,args)
		else:
			exec1(bot,mess,args)
	else:
		return