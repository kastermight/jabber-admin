# coding: utf-8
import xmpp
import time
import thread
from xmpp.roster import Roster

def loadConfig():
	import ConfigParser
	config = ConfigParser.ConfigParser()
	config.read('config.ini')
	login = config.get('connect', 'login')
	password = config.get('connect', 'password')
	autojoin = int(config.get('connect', 'autojoin'))
	allow_password = config.get('permission', 'allow_password')
	allow_password = allow_password.split(',')
	conf_moders = {}
	for i in config.items('conferences'):
		conf_moders.update({i[0]:i[1].split(',')})
	standart_password = config.get('permission', 'standart_password')
	max_level=int(config.get('permission', 'max_level'))
	conf_nick=config.get('connect', 'conf_nick')
	ol = []
	for i in range(0,len(allow_password)):
		allow_password[i] = allow_password[i].split(':')
		allow_password[i][1] = int(allow_password[i][1])
		ol.append(allow_password[i][1])
	for i in range(0,max_level+1):
		if i not in ol:
			allow_password.append([standart_password,i])
	user_no_pass = config.get('permission', 'user_no_pass')
	user_no_pass = user_no_pass.split(',')
	for i in range(0,len(user_no_pass)):
		user_no_pass[i] = user_no_pass[i].split(':')
		user_no_pass[i][1] = int(user_no_pass[i][1])
	bans = config.get('permission', 'banned')
	bans = bans.split(',')
	return {
		'login':login,
		'password':password,
		'allow_password':allow_password,
		'user_no_pass':user_no_pass,
		'bans': bans,
		'max_level':max_level,
		'conf_moders':conf_moders,
		'autojoin':autojoin,
		'conf_nick':conf_nick
	}

def get_priv(user):
	global bot
	isf = 0
	for i in bot.config['user_no_pass']:
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
				isf = plugin.init()['status']
				if isf <= bot.config['max_level']:
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
		i = phrase.split('=')
		ret.update({i[0]:unicode(i[1],'utf-8')})
	return ret

def runPlugin(command,bot,mess,mode):
	plugin = getattr(bot.plugins['plugins'],command)
	if mode=='gc':
		if (plugin.init()['gc'] == 1) or (plugin.init()['gc'] == 2):
			plugin.rungc(bot,mess)
	elif (plugin.init()['gc'] == 2) or (plugin.init()['gc'] == 0):
		plugin.run(bot,mess)

def message(conn,mess):
	user=unicode(mess.getFrom())
	if mess.getType() == 'chat':
		if user in bot.config['bans']:
			return
		text = mess.getBody()
		if ( text == None ):
			return
		command = text.split(' ')
		command = command[0]
		isf = get_priv(user)
		for i in range(isf,-1,-1):
			geted = bot.plugins.get('commands_'+unicode(i))
			if ((geted != None) and (command in geted)):
				thread.start_new_thread(runPlugin,(command,bot,mess,'chat'))
				break
		return
	elif (mess.getType() == 'groupchat') and (mess.getBody()[0] == '!'):
		if user in bot.config['bans']:
			return
		text = mess.getBody()
		if ( text == None ):
			return
		text = text[1:]
		mess.setBody(unicode(mess.getBody())[1:])
		command = text.split(' ')
		command = command[0]
		isf = get_priv(user)
		for i in range(isf,-1,-1):
			geted = bot.plugins.get('commands_'+unicode(i))
			if ((geted != None) and (command in geted)):
				thread.start_new_thread(runPlugin,(command,bot,mess,'gc',))
				break
		return

def subscribeHandler(conn, pres):
	global bot
	jid = pres.getFrom().getStripped()
	Roster.Authorize(bot.getRoster(),jid)
	Roster.Subscribe(bot.getRoster(),jid)

def unsubscribeHandler(conn, pres):
	global bot
	jid = pres.getFrom().getStripped()
	Roster.Unauthorize(bot.getRoster(),jid)
	Roster.Unsubscribe(bot.getRoster(),jid)
	Roster.delItem(bot.getRoster(),jid)

def presenseHandler(conn, pres):
	global bot
	if pres.getFrom() in bot.config['bans']:
		return
	if pres.getTags('x') != []:
		x = 0
		for i in pres.getTags('x'):
			if i.getAttr('xmlns').find('http://jabber.org/protocol/muc') != -1:
				x = i
				break
		if (x == 0) or (x.getTag('item') == None):
			return
		if (x.getTag('item').getAttr('role') == 'none') and (x.getTag('item').getAttr('role') == 'none'):
			if unicode(pres.getFrom()).split('/')[1] != bot.config['conf_nick']:
				del bot.visitors[unicode(pres.getFrom()).split('/')[0]][unicode(pres.getFrom()).split('/')[1]]
			return
		if x.getTag('item').getAttr('role') == 'visitor':
			bot.send(xmpp.Message(pres.getFrom(),bot.phrases['VISITOR_HELP'],'chat'))
		print str(pres)
		bot.visitors[unicode(pres.getFrom()).split('/')[0]].update({unicode(pres.getFrom()).split('/')[1]:[x.getTag('item').getAttr('jid'),x.getTag('item').getAttr('affiliation')]})
		if (unicode(pres.getFrom()).split('/')[1] not in bot.config['conf_moders'][unicode(pres.getFrom()).split('/')[0]]) or (x.getTag('item').getAttr('affiliation') == 'owner') or (x.getTag('item').getAttr('affiliation') == 'admin'):
			return
		iq = xmpp.Iq('set')
		iq.setAttr('to',unicode(pres.getFrom()).split('/')[0])
		query = iq.addChild('query')
		query.setAttr('xmlns','http://jabber.org/protocol/muc#admin')
		item = query.addChild('item')
		item.setAttr('nick',unicode(pres.getFrom()).split('/')[1])
		item.setAttr('role','moderator')
		item2 = query.addChild('item')
		item2.setAttr('affiliation','member')
		item2.setAttr('jid',x.getTag('item').getAttr('jid'))
		bot.send(iq)

config = loadConfig()
jid = xmpp.JID(config['login'])
user,server,password,res=jid.getNode(),jid.getDomain(),config['password'],jid.getResource()
bot = xmpp.Client(server,debug=[])
bot.config = config
bot.phrases = loadPhrases()
bot.plugins = loadPlugins()
bot.get_priv = get_priv
bot.message = message
bot.presenseHandler = presenseHandler
bot.unsubscribeHandler = unsubscribeHandler
bot.subscribeHandler = subscribeHandler
bot.runPlugin = runPlugin
c = 0
while c == 0:
	try:
		bot.connect()
		bot.auth(user,password,res)
		c=1
	except:
		time.sleep(300)
print '# Connected!'
bot.RegisterHandler('message',message)
bot.RegisterHandler('presence', subscribeHandler,'subscribe')
bot.RegisterHandler('presence', unsubscribeHandler,'unsubscribe')
bot.RegisterHandler('presence', presenseHandler)
bot.sendInitPresence()
bot.online = 1
last_time = 0
keepalive = 30
for cmds in bot.plugins.items():
	if cmds[0] != 'plugins':
		for i in cmds[1]:
			if getattr(getattr(bot.plugins['plugins'],i,None),'onPluginStart',None) != None:
				getattr(bot.plugins['plugins'],i,None).onPluginStart(bot)
while bot.online:
	bot.Process(1)
	now = int(time.time())
	delta = now - last_time
	if delta > keepalive:
		bot.send(' ')
		last_time = now
for cmds in bot.plugins.items():
	if cmds[0] != 'plugins':
		for i in cmds[1]:
			if (getattr(getattr(bot.plugins['plugins'],i,None),'onPluginEnd',None) != None):
				bot.plugins[i].onPluginEnd(bot)
bot.disconnect()