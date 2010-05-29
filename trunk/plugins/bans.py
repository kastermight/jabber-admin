# -*- coding: utf-8 -*-
import xmpp

def messageEvent(bot,mess):
	user=unicode(mess.getFrom())
	if user.split('/')[0] in bot.config['permissions']['banned']:
		mess.setBody("")
	if user in bot.config['permissions']['banned']:
		mess.setBody("")

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
		banlist = bot.phrases['BANS_BJIDS'] + ':'
		for i in bot.config['permissions']['banned']:
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