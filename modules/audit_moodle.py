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


#Do puntuation of moodle with his functions
def pointsMOODLE(html, dominio, url, var_v):
	try:
		punctuation = 100
		if get_moodle_version(url)== False:
			punctuation -=20
		if getmoodle_mods(html):
			moduls=getmoodle_mods(html)
			l = len(moduls)
			if l >= 20: 
				punctuation-= 20
			else:
				punctuation -= l*2
		if get_moodle_theme(html):
			punctuation -=20
		return punctuation
	except:
		return None


#audit Moodle

def get_moodle_version(url):
	try:
		urlc = url + "/lib/upgrade.txt"
		txt = urllib2.urlopen(urlc).read()
		string = ""
		for line in txt:
			string += line
		splited = string.replace('developers.\n\n', '')
		splited = splited.split(' ')
		n = splited.index('===')
		if splited[n+1]==get_moodle_lastrelease():
			return False
		else:
			return True
	except:
		return False

def get_moodle_lastrelease():
	try:
		url='https://download.moodle.org/'
		html=urllib2.urlopen(url).read()
		soup = BeautifulSoup(html, "html.parser")
		lista=[]
		for i in soup.findAll(attrs={"href":"/releases/latest/"}):
			lista.append(''.join(i.findAll(text=True)))
		for x in lista: 
			if 'Moodle' in x:
				text= x.split(' ')
		version = text[1].replace('+',' ')
		return version
	except:
		return False

def getmoodle_mods(html):
	try:
		soup = BeautifulSoup(html, "html.parser")
		lista = []
		modules = []
		for i in soup.findAll("script"):
			lista.append(''.join(i.findAll(text=True)))
		splited = str(lista).split('"')
		for i in splited: 
			if "moodle-mod" in i: 
				x = i.split('_')
				modules.append(x[1])
		return modules
	except:
		return False

def get_moodle_theme(html):
	try:
		soup=BeautifulSoup(html, "html.parser")
		a = soup.findAll('link')
		for link in soup.findAll('link'):
			if "stylesheet" in link.get('rel'):
				url_themes=link.get('href')
				if "theme" in url_themes:
					return True
	except:
		return False

