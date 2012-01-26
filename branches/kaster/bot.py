#!/usr/bin/env python2.7
import xmpp
import time
import thread
from xmpp.roster import Roster
#some comment
def createDataBases():
	import sqlite3
	conn = sqlite3.connect('maindb')
	cur = conn.cursor()
	userscreate = 'CREATE TABLE IF NOT EXISTS users (username UNIQUE ON CONFLICT REPLACE, lastdate)'
	helpcreate = 'CREATE TABLE IF NOT EXISTS help (plugname UNIQUE ON CONFLICT REPLACE, helpcont)'
	tzcreate = 'CREATE TABLE IF NOT EXISTS tzdata (geodata UNIQUE ON CONFLICT REPLACE, location, sttime, tz)'
	cur.execute(userscreate)
	cur.execute(helpcreate)
	cur.execute(tzcreate)
	conn.commit()
	cur.close()
	conn.close()

def loadConfig():
	import ConfigParser
	config = ConfigParser.ConfigParser()
	config.read('config.ini')
	ret = {}
	for section in config.sections():
		ret[section] = {}
		for item in config.items(section):
			ret[section][item[0]] = item[1]
	ol = []
	level_passwords = ret['permissions']['level_passwords'].split(',')
	for i in range(0,len(level_passwords)):
		level_passwords[i] = level_passwords[i].split(':')
		level_passwords[i][1] = int(level_passwords[i][1])
		ol.append(level_passwords[i][1])
	ret['permissions']['max_level'] = int(ret['permissions']['max_level'])
	for i in range(1,ret['permissions']['max_level']+1):
		if i not in ol:
			level_passwords.append([ret['permissions']['standart_password'],i])
	ret['permissions']['level_passwords'] = level_passwords
	private_users = ret['permissions']['private_users'].split(',')
	for i in range(0,len(private_users)):
		private_users[i] = private_users[i].split(':')
		private_users[i][1] = int(private_users[i][1])
	ret['permissions']['private_users'] = private_users
	return ret

def get_priv(user):
	global bot
	isf = 0
	for i in bot.config['permissions']['private_users']:
		if user in i:
			isf = i[1]
			break
	return isf

def loadPlugins():
	import os
	ret = {}
	global bot
	pluginstmp = None
	for fname in os.listdir('plugins/'):
		if fname.endswith('.py'):
			plugin_name = fname[:-3]
			if plugin_name != '__init__':
				pluginstmp=__import__('plugins.'+plugin_name)
				plugin = getattr(pluginstmp,plugin_name)
				isf = plugin.init(bot)['status']
				if isf <= bot.config['permissions']['max_level']:
					plugins=__import__('plugins.'+plugin_name)
					geted = ret.get('commands_'+unicode(isf))
					y = {}
					if (geted == None):
						y = {'commands_'+unicode(isf):[plugin_name,]}
					else:
						geted.append(plugin_name)
						y = {'commands_'+unicode(isf):geted}
					ret.update(y)
	del pluginstmp
	ret.update({'plugins':plugins})
	return ret

def loadPhrases():
	phrases = open('phrases.txt').read().split('\n')
	ret = {}
	for phrase in phrases:
		if (not phrase.startswith("//")) and (len(phrase)>=3):
			i = phrase.split('=')
			ret.update({i[0]:unicode(i[1],'utf-8')})
	return ret

def plugins_exec(func,*args):
	global bot
	for cmds in bot.plugins.items():
		if cmds[0] != 'plugins':
			for i in cmds[1]:
				if getattr(getattr(bot.plugins['plugins'],i,None),func,None) != None:
					if (func != 'onPluginStart') or (func != 'onPluginEnd'):
						a = [bot]
						for b in args:
							a.append(b)
						thread.start_new_thread(getattr(getattr(bot.plugins['plugins'],i,lambda: None),func,lambda x: None),tuple(a))
					else:
						getattr(getattr(bot.plugins['plugins'],i,lambda: None),func,lambda x,*args: None)(bot,*args)

def runPlugin(command,mess,mode):
	global bot
	user = unicode(mess.getFrom()).split('/')[1]
	plugin = getattr(bot.plugins['plugins'],command)
	if (mode=='gc') and (plugin.init(bot)['gc'] != 0):
		plugin.rungc(bot,mess)
	elif (mode == 'chat') and (plugin.init(bot)['gc'] != 1):
		plugin.run(bot,mess)

def message(conn,mess):
	global bot
	user=unicode(mess.getFrom()).split('/')[0]
	plugins_exec('onMessage',mess)
	if mess.getType() == 'chat':
		if mess.getFrom() == bot.config['connect']['login']:
			return None
		text = mess.getBody()
		if (text == None):
			return
		command = text.split(' ')
		command = command[0]
		isf = get_priv(user)
		for i in range(isf,-1,-1):
			geted = bot.plugins.get('commands_'+unicode(i))
			if ((geted != None) and (command in geted)):
				thread.start_new_thread(runPlugin,(command,mess,'chat'))
				break
	elif (mess.getType() == 'groupchat') and (unicode(mess.getBody())[0] == u'!'):
#		if (len(unicode(mess.getFrom()).split('/')) > 1) and (unicode(mess.getFrom()).split('/')[1] == bot.config['conferences']['nick']):
#			return None
		text = mess.getBody()
		if ( text == None ):
			return
		text = text[1:]
		mess.setBody(unicode(mess.getBody())[1:])
		command = text.split(' ')
		command = command[0]
		for i in range(bot.config['permissions']['max_level'],-1,-1):
			geted = bot.plugins.get('commands_'+unicode(i))
			if ((geted != None) and (command in geted)):
				thread.start_new_thread(runPlugin,(command,mess,'gc',))
				break

def subscribeHandler(conn, pres):
	plugins_exec('onSubscribe',pres)
	jid = pres.getFrom().getStripped()
	Roster.Authorize(bot.getRoster(),jid)
	Roster.Subscribe(bot.getRoster(),jid)

def unsubscribeHandler(conn, pres):
	plugins_exec('onUnsubscribe',pres)
	jid = pres.getFrom().getStripped()
	Roster.Unauthorize(bot.getRoster(),jid)
	Roster.Unsubscribe(bot.getRoster(),jid)
	Roster.delItem(bot.getRoster(),jid)

def presenseHandler(conn, pres):
	global bot
	if pres.getTags('x') != []:
		x = 0
		for i in pres.getTags('x'):
			if i.getNamespace().startswith('http://jabber.org/protocol/muc'):
				x = i
				break
		if (x == 0) or (x.getTag('item') == None):
			return
		if unicode(pres.getFrom()).split('/')[1] == bot.config['conferences']['nick']:
			return
		bot.plugins_exec('onConference',pres,x)


createDataBases()
status = open('status.txt', 'a')
ltime = time.localtime()
towrite = 'I was run at %02d:%02d:%02d, on %02d/%02d/%d' % (ltime[3], ltime[4], ltime[5], ltime[2], ltime[1], ltime[0])
status.write(towrite + '\n')
status.close()

config = loadConfig()
jid = xmpp.JID(config['connect']['login'])
user,server,password,res=jid.getNode(),jid.getDomain(),config['connect']['password'],jid.getResource()
bot = xmpp.Client(server,debug=[])
bot.config = config
bot.phrases = loadPhrases()
bot.plugins = loadPlugins()
bot.get_priv = get_priv
bot.messageHandler = message
bot.presenseHandler = presenseHandler
bot.unsubscribeHandler = unsubscribeHandler
bot.subscribeHandler = subscribeHandler
bot.runPlugin = runPlugin
bot.plugins_exec = plugins_exec
bot.reloadPhrases = loadPhrases
bot.reloadPlugins = loadPlugins
c = 0
while c == 0:
	try:
		bot.connect()
		bot.auth(user,password,res)
		c=1
	except:
		print 'There is no network, reconnecting in 5 minutes'
		plugins_exec('noNetwork')
		time.sleep(300)
print '\n# Connected!\n'
bot.online = 1
last_time = 0
keepalive = 30
bot.RegisterHandler('message',message)
bot.RegisterHandler('presence', subscribeHandler,'subscribe')
bot.RegisterHandler('presence', unsubscribeHandler,'unsubscribe')
bot.RegisterHandler('presence', presenseHandler)
bot.sendInitPresence()
plugins_exec('onPluginStart')
nonet = 0
while bot.online:
	bot.Process(1)
	now = int(time.time())
	delta = now - last_time
	if delta > keepalive:
		try:
			bot.send(' ')
		except:
			print 'No network, trying to restart'
			nonet = 1
			bot.online = 0
		last_time = now
plugins_exec('onPluginEnd')
if nonet == 1:
	import os
	import sys
	os.system('python ' + sys.argv[0])
	sys.exit()
else:
	bot.disconnect()
