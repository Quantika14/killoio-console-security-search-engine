#!/usr/bin/env python
#-*- coding:utf-8 -*-
#*******************************************
#APP: killo.io.py                        ***
#AUTHOR: Jorge Websec                    ***
#TWITTER: @JorgeWebsec                   ***
#Email: jorge@quantika14.com             ***
#*******************************************


import smtplib, base64, os, sys, getopt, urllib2, urllib, re, socket, time, httplib, tarfile
import itertools, urlparse, threading, Queue, multiprocessing, cookielib, datetime, zipfile
import platform, signal
from bs4 import BeautifulSoup
from urlparse import urlparse



#Do puntuation of drupal with his functions
def pointsDRUPAL(html, dominio, url, var_v):
	try:
		punctuation = 100
		if get_DruVersion(url)==False:
			punctuation -= 10
		if get_DefaultFiles(url):
			punctuation -= 10
		if get_drupal_modules(html):
			punctuation -= 10
		if get_drupal_themes(html):
			punctuation -= 10
		return punctuation
	except:
		return None

def get_DruVersion(url):
	try:
		htmltext = urllib2.urlopen(url+'/CHANGELOG.txt').read()
		regex = 'Drupal (\d+\.\d+),'
		pattern =  re.compile(regex)
		version = re.findall(pattern,htmltext)
		if version:
			DruVersion = version[0]
		if DruVersion != get_drupal_lastrelease():
			return DruVersion
		else:
			return False
	except:
		return True

def get_drupal_lastrelease():
	try:
		url='https://www.drupal.org/download'
		html=urllib2.urlopen(url).read()
		soup = BeautifulSoup(html, "html.parser")
		lista=[]
		for i in soup.findAll(attrs={"class":"primary-button"}):
			lista.append(''.join(i.findAll(text=True)))
		for x in lista: 
			if 'Drupal' in x:
				text= x.split(' ')
		version = text[2]
		return version
	except:
		return False
def get_DefaultFiles(url):
	try:
		defFilesFound = []
		defFiles=['/README.txt',
			'/INSTALL.mysql.txt',
			'/MAINTAINERS.txt',
			'/profiles/standard/translations/README.txt',
			'/profiles/minimal/translations/README.txt',
			'/INSTALL.pgsql.txt',
			'/UPGRADE.txt',
			'/CHANGELOG.txt',
			'/INSTALL.sqlite.txt',
			'/LICENSE.txt',
			'/INSTALL.txt',
			'/COPYRIGHT.txt',
			'/web.config',
			'/modules/README.txt',
			'/modules/simpletest/files/README.txt',
			'/modules/simpletest/files/javascript-1.txt',
			'/modules/simpletest/files/php-1.txt',
			'/modules/simpletest/files/sql-1.txt',
			'/modules/simpletest/files/html-1.txt',
			'/modules/simpletest/tests/common_test_info.txt',
			'/modules/filter/tests/filter.url-output.txt',
			'/modules/filter/tests/filter.url-input.txt',
			'/modules/search/tests/UnicodeTest.txt',
			'/themes/README.txt',
			'/themes/stark/README.txt',
			'/sites/README.txt',
			'/sites/all/modules/README.txt',
			'/sites/all/themes/README.txt',
			'/modules/simpletest/files/html-2.html',
			'/modules/color/preview.html',
			'/themes/bartik/color/preview.html'
			]
		for file in defFiles:
				req = urllib2.Request(url+file)
				try:
					htmltext = urllib2.urlopen(req).read()
					defFilesFound.append(url+file)
				except urllib2.HTTPError, e:
					pass
		return True, defFilesFound
	except:
		return False

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
	return TAG_RE.sub('', text)

def get_drupal_themes(html):
	try:
		soup=BeautifulSoup(html, "html.parser")
		for link in soup.findAll('link'):
			if "/themes/" in link.get('href'):
				url_themes = link.get('href')
				split_url=url_themes.split('/')
				for i in range (0, len(split_url)):
					if "themes" in split_url[i]:
						j=i+1
						themes=split_url[j]
						return True, themes
	except:
		return False
		
def get_drupal_modules(html):
	try:
		text=[]
		line=[]
		modules=[]
		linetext=[]
		modules_array=[]
		soup=BeautifulSoup(html, "html.parser")
		for node in soup.findAll('script'):
			text.append(''.join(node.findAll(text=True)))
		for lines in text:
			if 'modules' in lines:
				line.append(lines)
				lin=str(line).split(',')
		for i in range (0, len(lin)):
			if "modules" in lin[i]:
				linetext.append(lin[i])
		text_replace=str(linetext).replace("\\", "")
		split_url=str(text_replace).split('/')
		for i in range(0, len(split_url)):
			if "modules" in split_url[i]:
				j=i+1
				modules.append(split_url[j])
		for mod in modules:
			if mod not in modules_array:
				modules_array.append(mod)
		return modules_array
	except:
		False


