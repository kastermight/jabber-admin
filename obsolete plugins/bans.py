# -*- coding: utf-8 -*-
import xmpp
import re

def onMessage(bot,mess):
	user=unicode(mess.getFrom())
	for i in bot.config['permissions']['banned']:
		if i != '':
			if re.match(i,user,re.IGNORECASE) != None:
				mess.setBody("-")

def onPluginStart(bot):
	bot.config['permissions']['banned'] = bot.config['permissions']['banned'].split(',')

def init(bot):
	return {'status':8,'usage':'list|(add|delete <jid|nick>)','descr':bot.phrases['DESCR_BANS'],'gc':2}

class Bans():
	def add(self,bot,mess,args,mode):
		jid = args[0]
		bot.config['permissions']['banned'].append(jid)
		bot.send(xmpp.Message(mess.getFrom(),bot.phrases['BANS_BANNED']%unicode(jid),mode))
	def delete(self,bot,mess,args,mode):
		jid = args[0]
		bot.config['permissions']['banned'].remove(jid)
		bot.send(xmpp.Message(mess.getFrom(),bot.phrases['BANS_UNBANNED']%jid,mode))
	def list(self,bot,mess,args,mode):
		if len(bot.config['permissions']['banned']) == 0:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['BANS_NOJIDS'],mode))
		else:
			banlist = bot.phrases['BANS_JIDS'] + ':'
			for i in bot.config['permissions']['banned']:
				if i != '':
					banlist += '\n' + unicode(i)
			bot.send(xmpp.Message(mess.getFrom(),banlist,mode))

def run(bot,mess,mode='chat',nick=None):
	if mode=='groupchat':
		priv = bot.visitors[unicode(mess.getFrom()).split('/')[0]][nick][1]
		if (priv != u'admin') and (priv != u'owner'):
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
	nick = unicode(mess.getFrom()).split('/')[1]
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat',nick)