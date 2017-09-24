#!/usr/bin/env python
#-*- coding:utf-8 -*-
#*******************************************
#APP: lillo.io.py                        ***
#AUTHOR: Jorge Websec                    ***
#TWITTER: @JorgeWebsec                   ***
#Email: jorge@quantika14.com             ***
#*******************************************

#MODULES
import sys, cookielib, re, urllib2, httplib, modules.audit_wp, modules.audit_moodle, modules.audit_joomla, modules.audit_drupal, modules.killo, urllib
from bs4 import BeautifulSoup
from urlparse import urlparse
sys.path.append("lib")

#Check type of cms
def detect_cms(html, dominio, var_v):
	try:
		type_cms=''
		if detect_wp(html, dominio):
			type_cms = 'wordpress'
		elif detect_joomla(html):
			type_cms = 'joomla'
		elif detect_moodle(html):
			type_cms = 'moodle'
		elif detect_drupal(html):
			type_cms = 'drupal'
		else:
			type_cms = "no_cms"
		return type_cms
	except:
		type_cms = 'no_cms'
		return type_cms

#Do audit with the type of cms
def rank_cms(type_cms, html, url, dominio, var_v):
	try:
		points = 0
		if type_cms == 'wordpress':
			points += modules.audit_wp.pointsWP(html, dominio, url, var_v)
			return points
		elif type_cms == 'joomla':
			points += modules.audit_joomla.pointsJOOMLA(html, dominio, url, var_v)
			return points
		elif type_cms == 'moodle':
			points += modules.audit_moodle.pointsMOODLE(html, dominio, url, var_v)
			return points
		elif type_cms == 'drupal':
			points += modules.audit_drupal.pointsDRUPAL(html, dominio, url, var_v)
			return points
		else:
			return 'no_cms'
		
	except:
		return 'no_cms'
		pass


# Detect wordpress
def detect_wp(html, dominio):
	soup = BeautifulSoup(html, "html.parser")
	try:
		#Buscamos generator
		gen = soup.findAll(attrs={"name":"generator"})
		if "WordPress" in str(gen):
			return True, ""
		else: #Buscamos wp-content en el html
			if html.find("/wp-content/")>1:
				return True
			else:#Buscamos links con xmlrpc.php
				links = soup.findAll("link")
				for l in links:
					if "xmlrpc.php" in str(l):
						return True
					else:
						return False
	except:
		return False


#Detect Joomla
def detect_joomla(html):
	soup = BeautifulSoup(html, "html.parser")
	#Buscamos el generator
	try:
		gen = soup.findAll(attrs={"name":"generator"})
		if "Joomla!" in str(gen):
			return True
		else:
			return False
	except:
		return False


#Detect moodle
def detect_moodle(html):
	try:
		soup= BeautifulSoup(html, "html.parser")
		gen = soup.findAll(attrs={"name":"keywords"})
		if "moodle" in str(gen):
			return True
		elif "Moodle" in str(gen):
			return True
		elif "MOODLE" in str(gen):
			return True
		else:
			return False
	except:
		return False

#Detect drupal
def detect_drupal(html):
	soup = BeautifulSoup(html, "html.parser")
	try:
		if soup.findAll(attrs={"name":"Generator"}):
			gen = soup.findAll(attrs={"name":"Generator"})
			if "Drupal" in str(gen):
				return True
		elif soup.findAll(attrs={"name":"generator"}):
			gen = soup.findAll(attrs={"name":"generator"})
			if "Drupal" in str(gen):
				return True
			else:
				return False
		else:
			return False
	except:
		return False




