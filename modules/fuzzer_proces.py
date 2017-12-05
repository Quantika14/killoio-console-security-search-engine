#!/usr/bin/env python
# -*- coding: utf-8 -*
import sys, modules.killo, modules.vulnerability, modules.scanVuln, modules.killo_mongo, urllib2, time, ssl
from urllib2 import HTTPError
import argparse, requests, mechanize, cookielib
from bs4 import BeautifulSoup
reload(sys)  
sys.setdefaultencoding('utf8')

brow = mechanize.Browser()
dat=""

def fuser_process(steps, link, var_v):
	errors = get_errors()
	val_br = False
	text=""
	for i in range(steps):
		menu=True
		while(menu):
			try:
				type_fus=int(raw_input("|--[MENU] Select: 1.Login\n                  2.Form \n                  3.Exit\n"))
				try:
					if type_fus == 1:
						conf=True
						while(conf):
							is_link=raw_input("|--[INFO][>] Do you want change the link? (S/N):\n")
							if is_link.lower() == "n":
								id_=raw_input("|--[INFO][>] Select login\n|---[>]Enter id, class or name to username: ")
								id_p=raw_input("|---[>]Enter id, class or name to password: ")
								conf=False
							elif is_link.lower() == "s":
								link = raw_input("|--[INFO][>]Enter new sub link login: ")
								c = comprobe_url(link)
								if c:
									id_=raw_input("|--[INFO][>] Select login\n|---[>]Enter id, class or name to username: ")
									id_p=raw_input("|---[>] Enter id, class or name to password: ")
									conf=False
								else:
									print "|--[WARNING][>] Url not valid"
							else:
								print "|--[WARNING][>] Select Y/N"
						val_tag, name_f=check_tag(id_, link)
						val_tag_p, name_p=check_tag(id_p, link)
						if val_tag and val_tag_p:
							print "|--[INFO][>] Login form found."
							user=raw_input("|---[>] Enter the username: ")
							password=raw_input("|---[>] Enter the password: ")
							n=0
							if name_f != None and name_p != None:
								print "|--[INFO][>] Making Login Fuzzer, wait... "
								count_f=0
								while (n<1000):
									try:
											global brow
											global dat
											br = mechanize.Browser()
											cj = cookielib.LWPCookieJar()
											br.set_cookiejar(cj)
											br.set_handle_robots(False)
											br.set_handle_equiv(False)
											br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] 
											br.open(link)
											br.select_form(nr= n)
											br.form[ name_f ] = user
											br.form[ name_p ] = password
											data = br.submit()
											print "|--[INFO][>] Correct Login"
											n=5000
											brow = br
											dat = data
											val_br = True
									except Exception as e:
											n+=1
											print e
											continue
							menu=False
						else:
							print "|--[WARNING][>] Login form not found"
					elif type_fus == 2:
						val_tag=False
						id_=raw_input("|--[INFO][>] Select Form\n|---[>] Enter id, class or name: ")
						if val_br:
							global dat
							val_tag, name_f=check_form_pf(id_, dat)
						else:
							val_tag, name_f=check_form(id_, link)
						if val_tag:
							print "|--[INFO][>] Form found."
#							option = raw_input("|---[>] what do you want to enter: ")
							n=0
							if name_f != None:
								print "|--[INFO][>] Making Fuzzer, wait... "
								count_f=0
								for injection in open("modules/fuzzer_dic/Injections.txt").readlines():
									injection = injection.replace("\n", "")
									try:
										if val_br:
											global brow
											brow.open(link)
											brow.select_form(nr= n)
											for name in name_f:
												brow.form[ name ] = injection#option
											data = brow.submit()
											url_s = brow.geturl()
											htmlcontent = data.read()
											soup = BeautifulSoup(htmlcontent, "html.parser")
											title=str(soup.title.text)
											print "|--[INFO][>] Response: "+str(data)
											print "|--[INFO][>] URL: "+url_s
											print "|--[INFO][>] Title: "+title
											if var_v:
												print "|--[INFO][>] Injection: "+injection
											for e in errors:
												if e in htmlcontent:
													text+= chr(27)+"[0;36m"+"|--[INFO][>] Error -> "+ e +" on injection -> "+ injection + chr(27)+"[0m"+"\n"
											count_f+=1
										else:
											br = mechanize.Browser()
											cj = cookielib.LWPCookieJar()
											br.set_cookiejar(cj)
											br.set_handle_robots(False)
											br.set_handle_equiv(False)
											br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] 
											br.open(link)
											br.select_form(nr= n)
											for name in name_f:
												br.form[ name ] = injection#option
											data = br.submit()
											url_s = br.geturl()
											htmlcontent = data.read()
											soup = BeautifulSoup(htmlcontent, "html.parser")
											title=str(soup.title.text)
											print "|--[INFO][>] Response: "+str(data)
											print "|--[INFO][>] URL: "+url_s
											print "|--[INFO][>] Title: "+title
											for e in errors:
												if e in htmlcontent:
													text+= chr(27)+"[0;36m"+"|--[INFO][>] Error -> "+ e +" on injection -> "+ injection + chr(27)+"[0m"+"\n"
											count_f+=1
									except Exception as e:
										print e
#										n+=1
										continue
								if var_v:
									print "|--[FUZZER][>] Se enviaron "+str(count_f)+" peticiones correctamente de "+str(count_f)
								print text
						else:
							print "|--[WARNING][>] Text box not found"
						menu=False
					elif type_fus == 3:
						return "exit"
					else:
						print "|--[WARNING][>] Select option 1, 2 or 3"
					
				except Exception as e:
					print e
					print "|--[WARNING][>] Error finding tags"
			except:
				print "|--[WARNING][>] Select option 1, 2 or 3"

def check_tag(id_, link):
	type_id=["id", "class", "name"]
	name_f=None
	response = requests.get(link)
	html = response.text
	soup = BeautifulSoup(html, "html.parser")
	for tag in type_id:
		val = soup.find("input",{tag:id_})
		if val != None:
			try:
				name_f = val.get("name")
				val_tag=True
				break
			except:
				name_f=None
	return val_tag,name_f

def check_form(id_, link):
	type_id=["id", "class", "name"]
	val_tag=False
	name_f=list()
	response = requests.get(link)
	html = response.text
	soup = BeautifulSoup(html, "html.parser")
	for tag in type_id:
		val = soup.find("form",{tag:id_})
		if val != None:
			try:
				val_tag=True
				inputs = val.findAll("input")
				for i in inputs:
					if i.get("type")=="text" or i.get("type")=="password":
						print i.get("name")
						name_f.append(i.get("name"))
				break
			except:
				name_f=None
	return val_tag,name_f

def check_form_pf(id_, data):
	type_id=["id", "class", "name"]
	val_tag=False
	name_f=list()
	soup = BeautifulSoup(data, "html.parser")
	for tag in type_id:
		val = soup.find("form",{tag:id_}) #Si el form no tiene nombre modificar 
		if val != None:
			try:
				val_tag=True
				inputs = val.findAll("input")
				for i in inputs:
					#print i.get("name")----para comprobar si coge el formulario deseado
					if i.get("type")=="text" and i.get("name") != None:
						name_f.append(i.get("name"))
				break
			except:
				name_f=None
	return val_tag,name_f

def comprobe_url(url):
	try:
		headers = {'user-agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'}
		response= requests.get(url, headers=headers)
		print str(response)
		if "200" in str(response):
			return True
		else:
			return False
	except:
		return False

def get_errors():
	arch = open("modules/fuzzer_dic/Errors.txt")
	errors = arch.readlines()
	arch.close()
	return errors

