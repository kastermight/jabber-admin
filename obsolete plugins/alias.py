# -*- coding: utf-8 -*-
import xmpp
import re
import time


def init(bot):
	return {'status':1,'usage':'add <name>:<level> <body>|del <name>','descr':bot.phrases['DESCR_ALIAS'],'gc':0}

def run(bot,mess):
	reg = re.match('alias (?:(add) ([^ ]*):([\d]{1,3}) (.*)|(del) (.*))', mess.getBody())
	if reg == None:
		return
	reg = list(reg.groups())
	while None in reg:
		reg.remove(None)
	if reg[0] == 'add':
		name = reg[1]
		level = int(reg[2])
		albody = reg[3]
		if (bot.get_priv(unicode(mess.getFrom()).split('/')[0]) >= level):
			if getattr(bot.plugins['plugins'],name,None) == None:
				class Alias():
					def init(self):
						return {'status':level,'usage':'[body]','descr': unicode(mess.getFrom()).split('/')[0] + "'s alias",'alias':1}
					def run(self,bot2,mess2):
						import re
						rg = re.match('([^ ]+) body',mess2.getBody())
						if rg == None:
							for i in albody.split(';'):
								msg = xmpp.Message()
								msg.setFrom(mess2.getFrom())
								msg.setBody(i)
								bot2.message(-1,msg)
								time.sleep(0.1)
						else:
							bot.send(xmpp.Message(mess.getFrom(),rg.groups()[0] + "'s body:\n" + albody))
				setattr(bot.plugins['plugins'],name,Alias())
				bot.plugins['commands_'+unicode(level)].append(name)
				bot.send(xmpp.Message(mess.getFrom(),'Alias ' + name + ' maked'))
			else:
				bot.send(xmpp.Message(mess.getFrom(),bot.phrases['ALIAS_AEXISTS']%name))
		else:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['ALIAS_NOPERM']%level))
	elif reg[0] == 'del':
		name = reg[1]
		al = getattr(bot.plugins['plugins'],name,None)
		if (al != None):
			if ('alias',1) in al.init(bot).iteritems():
				for i in range(bot.get_priv(unicode(mess.getFrom()).split('/')[0])+1):
					if ('commands_'+unicode(i) in bot.plugins) and (name in bot.plugins['commands_'+unicode(i)]):
						bot.plugins['commands_'+unicode(i)].remove(name)
						delattr(bot.plugins['plugins'],name)
						bot.send(xmpp.Message(mess.getFrom(),bot.phrases['ALIAS_DELETED']%name))
						break
			else:
				bot.send(xmpp.Message(mess.getFrom(),bot.phrases['ALIAS_NCOMMAND']%name))
		else:
			bot.send(xmpp.Message(mess.getFrom(),bot.phrases['ALIAS_NEXISTS']%name))
	else:
		return