#!/usr/bin/env python
#-*- coding:utf-8 -*-
#*******************************************
#APP: killo.io.py                        ***
#AUTHOR: Jorge Websec                    ***
#TWITTER: @JorgeWebsec                   ***
#Email: jorge@quantika14.com             ***
#*******************************************
import sys, cookielib, re, urllib2, httplib, urllib, duckduckgo
from bs4 import BeautifulSoup
from urlparse import urlparse
import mechanize
sys.path.append("lib")
import modules.detect_functions
import modules.audit_joomla
import modules.audit_wp



#Do puntuation of joomla with his functions
def pointsJOOMLA(html, dominio, url, var_v):
	try:
		punctuation = 100
		if get_joomla_administrator(url):
			punctuation -= 10
		if get_joomla_component(html):
			component = []
			component = get_joomla_component(html)
			l = len(component)
			if l >= 20: 
				punctuation-= 20
			else:
				punctuation -= l*2
		if get_joomla_modules(html):
			mod = []
			mod = get_joomla_modules(html)
			l = len(mod)
			if l >= 20: 
				punctuation-= 20
			else:
				punctuation -= l*2
		if get_joomla_templates(html):
			punctuation -= 5
		if get_joomla_plugins(html):
			plugins = []
			plugins = get_joomla_plugins(html)
			l = len(plugins)
			if l >= 20: 
				punctuation-= 20
			else:
				punctuation -= l*2
		return punctuation
	except:
		return None

#audit Joomla
#JA administrator
def get_joomla_administrator(url):
	try:
		url_f = url + "administrator"
		urllib2.urlopen(url_f)
		return True
	except:
		return False

#JA modules
def get_joomla_modules(html):
	try:
		modules=[]
		modules_array=[]
		soup=BeautifulSoup(html, "html.parser")
		for link in soup.findAll('link'):
			if "/mod_" in link.get('href'):
				url_modules = link.get('href')
				fsplit_url=url_modules.split('_')
				ssplit_url=fsplit_url[1].split('/')
				modules.append(ssplit_url[0])
		for mod in modules:
			if mod not in modules_array:
				modules_array.append(mod)
		return modules_array
	except:
		return False



def get_joomla_templates(html):
	try:
		soup=BeautifulSoup(html, "html.parser")
		for link in soup.findAll('link'):
			if "/templates/" in link.get('href'):
				templates = True
		return templates
	except: 
		return False

#JA component
def get_joomla_component(html):
	try:
		component=[]
		component_array=[]
		soup=BeautifulSoup(html, "html.parser")
		for link in soup.findAll('link'):
			if "/com_" in link.get('href'):
				url_modules = link.get('href')
				fsplit_url=url_modules.split('_')
				ssplit_url=fsplit_url[1].split('/')
				component.append(ssplit_url[0])
		for com in component:
			if com not in component_array:
				component_array.append(com)
		return component_array
	except:
		return False
def get_joomla_plugins(html):
	try:
		plugins=[]
		plugins_array=[]
		soup=BeautifulSoup(html, "html.parser")
		for link in soup.findAll('link'):
			if "/plg_" in link.get('href'):
				url_modules = link.get('href')
				fsplit_url=url_modules.split('_')
				if fsplit_url[2]:
					plgtext=fsplit_url[1]+"_"+fsplit_url[2]
					ssplit_url=plgtext.split('/')
				else:
					ssplit_url=fsplit_url[1].split('/')
				plugins.append(ssplit_url[0])
		for plg in plugins:
			if plg not in plugins_array:
				plugins_array.append(plg)
		return plugins_array
	except:
		return False
