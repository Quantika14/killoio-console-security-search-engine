#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys, modules.killo, modules.vulnerability, modules.scanVuln, modules.killo_mongo, urllib2, time, ssl
from urllib2 import HTTPError
reload(sys)  
sys.setdefaultencoding('utf8')


lista_exploit=["isql", "sqli","xss","rce"]

def search(var_v, exploit):
	data = raw_input("Search: ")
	rank_killoIO(data, var_v, exploit)


def banner():
	print """
 ▄    ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄            ▄▄▄▄▄▄▄▄▄▄▄     ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░▌  ▐░▌▐░░░░░░░░░░░▌▐░▌          ▐░▌          ▐░░░░░░░░░░░▌   ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░▌ ▐░▌  ▀▀▀▀█░█▀▀▀▀ ▐░▌          ▐░▌          ▐░█▀▀▀▀▀▀▀█░▌    ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌
▐░▌▐░▌       ▐░▌     ▐░▌          ▐░▌          ▐░▌       ▐░▌        ▐░▌     ▐░▌       ▐░▌
▐░▌░▌        ▐░▌     ▐░▌          ▐░▌          ▐░▌       ▐░▌        ▐░▌     ▐░▌       ▐░▌
▐░░▌         ▐░▌     ▐░▌          ▐░▌          ▐░▌       ▐░▌        ▐░▌     ▐░▌       ▐░▌
▐░▌░▌        ▐░▌     ▐░▌          ▐░▌          ▐░▌       ▐░▌        ▐░▌     ▐░▌       ▐░▌
▐░▌▐░▌       ▐░▌     ▐░▌          ▐░▌          ▐░▌       ▐░▌        ▐░▌     ▐░▌       ▐░▌
▐░▌ ▐░▌  ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌ ▄  ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌
▐░▌  ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
 ▀    ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 
                                                                                         
"""
print "***************************************************************************************"
print "AUTHORS: Jorge Coronado (aka @JorgeWebsec) | Ramón Bajona | CONTACT: www.quantika14.com
print "VERSION: 1.0"

def helpi():
	print """
		Killoio version 1.0
		GitHub: https://github.com/Quantika14/killoio-console-security-search-engine
		
		----------PARAMETER----------
		
		-h Help
		-s Search with Google and DuckduckGo
		-v To show all process of audit
		-e Select the exploit to scan, exploits: isql, sqli, xss, rce

		----------EXAMPLES----------

		killoio.py -s
		killoio.py -s -v
		killoio.py -s -e xss -v 
		"""

def main():
	validator = False
	var_v = False
	parameter1 = None
	parameter2 = " "
	parameter3 = " "
	parameter4 = " "
	try:	
		parameter1=sys.argv[1] 
		parameter2=sys.argv[2]
		parameter3=sys.argv[3]
		parameter4=sys.argv[4]
	except: 
		pass

	if parameter1!="-s" or parameter1=="h":	
		return helpi()
	elif "-e" in sys.argv:
		if len(sys.argv)>3:
			for u in range(len(sys.argv)):
				if sys.argv[u]=="-e":
					for i in lista_exploit:
						if i == sys.argv[u+1]: 
							validator = True
						else:
							fail_option = 1
		else:
			fail_option = 2
	else:
		validator = True

	if validator:
		if parameter2 == "-v":
			var_v=True
			if parameter3 == "-e":
				search(var_v, parameter4)

			else:		
				search(var_v, None)

			
		elif parameter2 == "-e":
			if parameter4 == "-v":
				var_v=True
				search(var_v, parameter3)

			else:
				search(var_v, parameter3)

		else:

				search(var_v, None)
	else:
		if fail_option==2:	
			print "Argument -e must go with one exploit of list."
		elif fail_option==1:
			print "Check the sintax of exploit list."

def rank_killoIO(data, var_v, exploit):
	try:
		first_links=modules.killo.SearchGoogle(2, data, var_v)
		first_links=modules.scanVuln.removeDuplicate_url(first_links)
		domains_ban=modules.killo.domain_split()
		analyzed_domains=[]
		for link in first_links:

			id_link = modules.killo_mongo.get_id(link)
			if modules.killo_mongo.get_link(id_link):
				domain = modules.killo.get_domain(link)
				bol, data = modules.killo_mongo.get_link(id_link)
				title = data["title"]
				description = data["description"]
				type_cms = data["type_cms"]
				rank_cms = data["rank_cms"]
				try:
					factors = data["factors_up"]
				except:
					factors = None
				try:
					exploit = data["vuln"]
				except:
					exploit = None
				print "|||||||||||||||||||||||||||||||||||||||||||||||||||||"
				print "[TARGET][>] " + link
				print "|--[INFO][TITLE][>] " + title
				print "|--[INFO][DESCRIPTION][>] " + description
				if type_cms != "no_cms":
					print "|--[CMS DETECT][>] \n"
					print "|----[CMS][>] " + type_cms
					print "|----[CMS SECURITY RANK][>] " + str(rank_cms) + "%" + "\n"
				if factors != None:
					print "|--[SECURITY SCAN][>] \n"
					for i in factors:
						try:
							if i["pass"] == "false":
								print "|----[WARNING]-> " + i["name"] +", "+ i["description"]
							else:
								if var_v:
									print "|----[ENABLED]-> " + i["name"] +", "+ i["description"]
						except:
							continue
				if exploit!= None:
					print "|--[SECURITY SCAN][>] \n"
					try:
						number = exploit["xss"] 
						print "|----[TYPE VULNERABILITY][>] XSS"
						print "|----[>] "+str(number)
					except:
						pass
					try:
						number = exploit["sqli"] 
						print "|----[TYPE VULNERABILITY][>] SQLI"
						print "|----[>] "+str(number)
					except:
						pass
					try:
						number = exploit["rce"] 
						print "|----[TYPE VULNERABILITY][>] RCE"
						print "|----[>] "+str(number)
					except:
						pass
			else:
				try:
					link_dict = {"rank_cms":"None", "type_cms":"no_cms", "vuln":""} 
					domain = modules.killo.get_domain(link)
					if modules.killo.check_domains(link, domains_ban, var_v) and domain not in analyzed_domains:

						context = ssl._create_unverified_context()
						html = urllib2.urlopen(link, "html.parser", context=context).read()
						type_cms = modules.detect_functions.detect_cms(html, domain, var_v)
						title = modules.killo.get_title(link)
						description = modules.killo.get_description(link)
						factors_up = modules.killo.get_website_factors(domain)

						print "\n"
						print "|||||||||||||||||||||||||||||||||||||||||||||||||||||"
						print "[TARGET][>] " + link
						print "|--[INFO][TITLE][>] " + title
						print "|--[INFO][DESCRIPTION][>] " + description
					
						link_dict["title"]=title
						link_dict["link"]=link
						link_dict["description"]=description
						
						#SCAN CMS SECURITY
						if type_cms!="no_cms":
							print "|--[CMS DETECT][>] \n"
							rank_cms = modules.detect_functions.rank_cms(type_cms, html, link, domain, var_v)
							print "|----[CMS][>] " + type_cms
							print "|----[CMS SECURITY RANK][>] " + str(rank_cms) + "%" + "\n"
							link_dict["type_cms"]=type_cms
							link_dict["rank_cms"]=rank_cms
						
						#SCAN SECURITY
						if factors_up == None:
							pass
						else:
							print "|--[SECURITY SCAN][>] \n"
							for i in factors_up:
									try:
										if i["pass"] == "false":
											print "|----[WARNING]-> " + i["name"] +", "+ i["description"]
										else:
											if var_v:
												print "|----[ENABLED]-> " + i["name"] +", "+ i["description"]
									except:
										continue
							link_dict["factors_up"]=factors_up
						#SCAN VULNERABILITY
						links_scan = modules.scanVuln.SearchGoogle(1, domain)
						if links_scan != None:
							if len(links_scan)>1:
								type_vul, vulnerb = modules.scanVuln.audit_vulnerability(exploit, links_scan, var_v)
								if exploit == None and type_vul>0:
									for i in range(len(type_vul)):
										link_dict["vuln."+type_vul[i]]=vulnerb[i]
								elif exploit != None:
									link_dict["vuln."+type_vul]=vulnerb
							else:
								pass
						#INSERT INTO DB 
						modules.killo_mongo.insert_mongodb(link_dict)
					analyzed_domains.append(domain)
				except urllib2.HTTPError:
					continue
				except urlib2.URLError:
					continue
	except Exception as e:
		pass

if __name__ == "__main__":
	main()
