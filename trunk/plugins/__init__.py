# -*- coding: utf-8 -*-
import xmpp

def init(bot):
	return {'status':0,'usage':'<template> <usage>','descr':'Template','gc':0}

def run(bot,mess):
	bot.send(xmpp.Message(mess.getFrom(),'Message Here'))