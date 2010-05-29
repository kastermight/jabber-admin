# -*- coding: utf-8 -*-
import xmpp
import os


def init(bot):
	return {'status':10,'usage':'<command>','descr':bot.phrases['DESCR_CMD'],'gc':0}

def run(bot,mess):
	cmd = mess.getBody()
	cmd = cmd[4:]
	output = os.popen(cmd).read()

	if not isinstance(output, unicode):
		output = unicode(output,'utf-8','ignore')
	bot.send(xmpp.Message(mess.getFrom(),output))