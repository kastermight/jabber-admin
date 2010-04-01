# -*- coding: utf-8 -*-
import xmpp


def init():
	return {'status':8,'usage':'<jid|nick>','descr':'Ban system plugin','gc':2}

class Bans():
	def add(self,bot,mess,args,mode):
		jid = args[0]
		bot.config['bans'].append(jid)
		bot.send(xmpp.Message(mess.getFrom(),bot.phrases['BANS_BANNED']%unicode(jid),mode))
	def delete(self,bot,mess,args,mode):
		jid = args[0]
		bot.config['bans'].remove(jid)
		bot.send(xmpp.Message(mess.getFrom(),bot.phrases['BANS_UNBANNED']%jid,mode))
	def list(self,bot,mess,args,mode):
		banlist = bot.phrases['BANS_BJIDS'] + ':'
		for i in bot.config['bans']:
			if i != '':
				banlist += '\n' + unicode(i)
		bot.send(xmpp.Message(mess.getFrom(),banlist,mode))

def run(bot,mess,mode='chat'):
	if mode=='groupchat':
		priv = bot.visitors[unicode(mess.getFrom()).split('/')[0]][unicode(mess.getFrom()).split('/')[1]][1]
		if (priv != 'admin') or (priv != 'owner'):
			return
	cmd = unicode(mess.getBody()).split(' ')
	if len(cmd) < 2:
		return
	args = cmd[2:]
	cmd = cmd[1]
	exec1 = getattr(Bans(),cmd,None)
	if exec1 != None:
		exec1(bot,mess,args,mode)
def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')