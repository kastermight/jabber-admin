# -*- coding: utf-8 -*-
import xmpp
import sqlite3
import random
import time

def onPluginStart(bot):
	bot.words = 0

def init(bot):
	return {'status':8,'usage':'[add|del] <word>','descr':bot.phrases['DESCR_WORD'],'gc':1}

class Word():
	def __init__(self,mode):
		self.dbs = sqlite3.connect("base.db")
		self.db = self.dbs.cursor()
		self.mode = mode
	def add(self,bot,mess,args):
		word = args[0]
		descr = u' '.join(args[1:])
		obj = self.db.execute("SELECT word,stat FROM words WHERE word=?",(word,)).fetchone()
		if obj != None:
			self.db.execute("DELETE FROM words WHERE word=?",(word,))
			self.db.execute("INSERT INTO words VALUES (?,?)",(word,descr))
		else:
			self.db.execute("INSERT INTO words VALUES (?,?)",(word,descr))
		bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_ADDED']%word,self.mode))
		self.dbs.commit()
	def delete(self,bot,mess,args):
		word = args[0]
		dl = self.db.execute("DELETE FROM words WHERE word=?",(word,))
		if dl.rowcount >= 1:
			self.dbs.commit()
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_DELETED']%word,self.mode))
		else:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_NWORD']%word,self.mode))
	def start(self,bot,mess,args):
		if bot.words==1:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_ARUN'],self.mode))
		else:
			bot.words=1
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_START'],self.mode))
			random.seed = unicode(mess.getFrom())
			while bot.words==1:
				time.sleep(1200)
				obj = len(self.db.execute("SELECT word,stat FROM words").fetchall())
				if obj != 0:
					rand = random.randint(1,obj)
					randphrase = self.db.execute("SELECT word,stat FROM words LIMIT %d,%d"%(rand-1,rand)).fetchone()
					bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_SAY']%(randphrase[0],randphrase[1]),self.mode))
				else:
					bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_NWORDS'],self.mode))
				db.close()
	def stop(self,bot,mess,args):
		if bot.word==0:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_NRUN'],self.mode))
		else:
			bot.word=0
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_STOP'],self.mode))
	def list(self,bot,mess,args):
		obj = self.db.execute("SELECT word FROM words").fetchall()
		if obj != None:
			a = u''
			for i in obj:
				a += unicode(i[0]) + u', '
			a = a[:-2]
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_KNOW']%a,self.mode))
		else:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_NWORDS'],self.mode))
	def getWord(self,bot,mess,word):
		obj = self.db.execute("SELECT word,stat FROM words WHERE word=?",(word,)).fetchone()
		if obj != None:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_SAY']%(obj[0],obj[1]),self.mode))
		else:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['WORD_NWORD']%word,self.mode))

def run(bot,mess):
	cmd = unicode(mess.getBody()).split(' ')
	if len(cmd) < 2:
		return
	args = cmd[2:]
	cmd = cmd[1]
	exec1 = getattr(Word('chat'),cmd,None)
	if exec1 == None:
		Word('chat').getWord(bot,mess,cmd)
	else:
		exec1(bot,mess,args)
def rungc(bot,mess):
	cmd = unicode(mess.getBody()).split(' ')
	if len(cmd) < 2:
		return
	priv = bot.visitors[unicode(mess.getFrom()).split('/')[0]][unicode(mess.getFrom()).split('/')[1]][1]
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	args = cmd[2:]
	cmd = cmd[1]
	exec1 = getattr(Word('groupchat'),cmd,None)
	if (exec1 == None) or ((priv != 'admin') and (priv != 'owner')):
		Word('groupchat').getWord(bot,mess,cmd)
	else:
		exec1(bot,mess,args)