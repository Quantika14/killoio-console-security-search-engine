#!/usr/bin/env python
#-*- coding:utf-8 -*-
#*******************************************
#APP: killo.io.py                        ***
#AUTHOR: Jorge Websec                    ***
#TWITTER: @JorgeWebsec                   ***
#Email: jorge@quantika14.com             ***
#*******************************************

import sys, cookielib, re, urllib2, httplib, urllib, duckduckgo, json
from bs4 import BeautifulSoup
from urlparse import urlparse
import mechanize
sys.path.append("lib")
import modules.detect_functions
import modules.audit_joomla
import modules.audit_wp


#TAGS REMOVER
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
	return TAG_RE.sub('', text)


#Do puntuation of moodle with his functions
def pointsWP(html, dominio, url, var_v):
	try:	
		punctuation = 100
		if get_wp_versionReadme(dominio):
			punctuation-=10
		if detect_wpadmin(html):
			punctuation-=10
		if detect_wpcontent(html, url):
			punctuation-=5
		if wp_bruteforce(dominio):
			punctuation-=15
		if get_wp_nameTheme(html):
			punctuation-=20
		if detect_user_wp_api(url):
			users = detect_user_wp_api(url)[0]
			admin = detect_user_wp_api(url)[1]
			l = len (users)
			if l > 10: 
				punctuation-= 10
			else:
				punctuation -= l
			if admin :
				punctuation -= 20
		else:
			users = detect_user_wp_napi(html)[0]
			admin = detect_user_wp_napi(html)[1]
			l = len(users)
			if l > 10: 
				punctuation -= 10
			else:
				punctuation -= l
			if admin :
				punctuation -= 20
		if get_wp_plugins(html) > 0: 
			plugins = get_wp_plugins(html)
			l = len (plugins)
			if l >= 10:
				punctuation-=10
			else:
				punctuation-=l
		return punctuation
	except:
		return None

#audit WP
#WP admin
def detect_wpadmin(html):
	try:
		soup=BeautifulSoup(html, "html.parser")
		if "/wp-admin/" in str(soup):
			return True
	except:
		return False


#WP content
def detect_wpcontent(html, url):
	try:
		soup=BeautifulSoup(html, "html.parser")
		url_wp_content=url+"/wp-content/"
		if url_wp_content in str(soup):
			return True
	except:
		return False

#WP version and readme
def get_wp_versionReadme(dominio):
	try:
		url = dominio + "/readme.html"
		html = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html, "html.parser")
		for h1 in soup.find_all('h1', {'id':"logo"}):
			h1 = remove_tags(str(h1)) #PARSER
			if h1:
				last_version = compare_version_wp(h1)
				return True, last_version
	except urllib2.HTTPError, e:
		return False
	except urllib2.URLError, e:
		return False
	except httplib.HTTPException, e:
		return False

def compare_version_wp(version):
	try:
		url = 'https://api.wordpress.org/core/version-check/1.6/'
		html = urllib2.urlopen(url)
		soup=BeautifulSoup(html, "html.parser")
		fulltext=soup.get_text()
		text=fulltext.split(':')
		text=text[18].split('-')
		text=text[1].split('.zip')
		if text == version: 
			return True
		else:
			return False
	except:
		return False
#WP theme 
def get_wp_nameTheme(html):
	try:
		soup=BeautifulSoup(html, "html.parser")
		for link in soup.findAll('link'):
			if "/themes/" in link.get('href'):
				return True
	except:
		return False

#WP users for API
def detect_user_wp_api(url_base):
	try:
		dat = []
		url_f = url_base + "wp-json/wp/v2/users"
		html = urllib2.urlopen(url_f).read()
		data = json.loads(html)
		l=len(data)
		for i in range (0,l):
			dat.append(data[i]["name"])
		if "admin" in dat:
			return dat , True
		else:
			return dat , False
	except Exception as e:
		return False

#WP users without API
def detect_user_wp_napi(html):
	try:
		soup = BeautifulSoup(html, "html.parser")
		gen = soup.findAll(attrs={"class":"url fn"})
		users = remove_tags(str(gen))
		if "admin" in users : 
			return users , True
		else:
			return users , False
	except Exception as e:
		return False

#WP plugins
def get_wp_plugins(html):
	try:
		plugins=[]
		plugins_array=[]
		soup=BeautifulSoup(html, "html.parser")
		for link in soup.findAll('link'):
			if "/plugins/" in link.get('href'):
				url_plugins = link.get('href')
				split_url=url_plugins.split('/')
				for i in range (0, len(split_url)):
					if "plugins" in split_url[i]:
						j=i+1
						plugins.append(split_url[j])
		for plu in plugins:
			if plu not in plugins_array:
				plugins_array.append(plu)
		return plugins_array
	except:
		return False

#WP BruteForce


def wp_bruteforce(dominio):
	dominio_nothttp=dominio.split('://')
	url = dominio +"/wp-login.php?redirect_to="+dominio_nothttp[0]+"%3A%2F%2F" + dominio_nothttp[1].replace('/', '') +"%2Fwp-admin%2F&reauth=1"
	url_login= dominio +"/wp-login.php"
	url_admin= dominio +"/wp-admin"
	br=mechanize.Browser()
	br.set_handle_equiv(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	count=0
	user='admin'
	passwords = ["123456", "root", "admin", "12345", ""]
	for pas in passwords:
		try:
			br.open(url_login)
			br.select_form(name="loginform")
			br.form['log']=user
			br.form['pwd']=pas
			response=br.submit()
			html = br.response().read()
			soup=BeautifulSoup(html, "html.parser")
			login_error = soup.findAll(attrs={"id":"login_error"})
			msg_error  = remove_tags(str(login_error))
			if "ERROR:" in msg_error:
				count+=1
		except:
			pass
		try:
			br.open(url_admin)
			br.select_form(nr=0)
			br.form['log']=user
			br.form['pwd']=pas
			response=br.submit()
			html = br.response().read()
			soup=BeautifulSoup(html, "html.parser")
			login_error = soup.findAll(attrs={"id":"login_error"})
			msg_error  = remove_tags(str(login_error))
			if "ERROR:" in msg_error:
				count+=1
		except:
			pass
				
		try:
			br.open(url)
			br.select_form(nr=0)
			br.form['log']=user
			br.form['pwd']=pas
			response=br.submit()
			html = br.response().read()
			soup=BeautifulSoup(html, "html.parser")
			login_error = soup.findAll(attrs={"id":"login_error"})
			msg_error  = remove_tags(str(login_error))
			if "ERROR:" in msg_error:
				count+=1
		except:
			pass
			
	if count == 5:
		return True
	else:
		return False


