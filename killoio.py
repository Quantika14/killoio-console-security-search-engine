#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys, modules.killo, modules.vulnerability, modules.scanVuln, modules.killo_mongo, urllib2, time, ssl, modules.fuzzer_proces
from urllib2 import HTTPError
import argparse, requests, mechanize
from bs4 import BeautifulSoup
reload(sys)  
sys.setdefaultencoding('utf8')

lista_exploit=["isql", "sqli","xss","rce"]

def search(var_v, exploit, fuser):
	data = raw_input("Search: ")
	rank_killoIO(data, var_v, exploit, "s", fuser)


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
print "AUTHORS: Jorge Coronado (aka @JorgeWebsec) | Ramón Bajona | CONTACT: www.quantika14.com"
print "VERSION: 1.0 DATE: 24-09-2017"
print "VERSION: 1.1 DATE: 05-12-2017"

def create_argumentparser():
	desc = "Killoio version 1.0 \n"
	desc += "GitHub: https://github.com/Quantika14/killoio-console-security-search-engine \n\n"
	desc += """----------EXAMPLES----------

killoio.py -s
killoio.py -s -v
killoio.py -s -e xss -v
killoio.py --fuzzer -u http://target.com
		"""
	parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=desc)
	parser.add_argument("-v", "--verbose", help='To show a verbose process',action='store_true' , default=False)
	parser.add_argument("-s", "--search", help='Search with Google and DuckduckGo',action='store_true',required=False, default=False)
	parser.add_argument("-e", "--exploit", help='Select the exploit to scan; Exploits: isql, sqli, xss, rce', default=False)
	parser.add_argument("--fuzzer", help='To fuzzer xploit',action='store_true', default=False)
	parser.add_argument("-u", "--url", help="To select a concrete url to scan", default=False)
	return parser

def main():
	global lista_exploit
	aparser = create_argumentparser()
	args = aparser.parse_args()
	verbose=args.verbose
	s=args.search
	exploit=args.exploit
	fuser=args.fuzzer
	url=args.url

	if url:
		if exploit:
			if exploit in lista_exploit:
				rank_killoIO(url,verbose, exploit, "u", fuser)
			else:	
				print "Argument -e must go with one exploit of list."
		else:
			rank_killoIO(url.replace("///","&"),verbose,None, "u", fuser)
	else:
		if exploit:
			if exploit in lista_exploit:
				search(verbose, exploit, fuser)
			else:	
				print "Argument -e must go with one exploit of list."
		else:
			search(verbose, None, fuser)

def rank_killoIO(data, var_v, exploit, option, fuser):
	try:
		if option == "s":
			first_links=modules.killo.SearchGoogle(2, data, var_v)
			first_links=modules.scanVuln.removeDuplicate_url(first_links)
			domains_ban=modules.killo.domain_split()
			analyzed_domains=[]
		elif option == "u":
			domains_ban=modules.killo.domain_split()
			analyzed_domains=[]
			first_links=list()
			c = modules.fuzzer_proces.comprobe_url(data)
			if c:
				first_links.append(data)
			else:
				print "Url in arguments is not valid url"
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
#				if exploit!= None:
#					print "|--[SECURITY SCAN][>] \n"
#					try:
#						number = exploit["xss"] 
#						print "|----[TYPE VULNERABILITY][>] XSS"
#						print "|----[>] "+str(number)
#					except:
#						pass
#					try:
#						number = exploit["sqli"] 
#						print "|----[TYPE VULNERABILITY][>] SQLI"
#						print "|----[>] "+str(number)
#					except:
#						pass
#					try:
#						number = exploit["rce"] 
#						print "|----[TYPE VULNERABILITY][>] RCE"
#						print "|----[>] "+str(number)
#					except:
#						pass
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
						#INSERT INTO DB 
						modules.killo_mongo.insert_mongodb(link_dict)
					analyzed_domains.append(domain)
				except Exception as e:
					print e
					continue
				except urllib2.URLError:
					continue
			#SCAN VULNERABILITY
			links_scan = modules.scanVuln.SearchGoogle(1, domain)
			if links_scan != None:
				if len(links_scan)>1:
					type_vul, vulnerb = modules.scanVuln.audit_vulnerability(exploit, links_scan, var_v)
					try:
						if exploit == None and type_vul>0:
							for i in range(len(type_vul)):
								link_dict["vuln."+str(type_vul[i])]=str(vulnerb[i])
						elif exploit != None:
							link_dict["vuln."+str(type_vul)]=str(vulnerb)
					except:
						pass
				else:
					pass
			#FUZZER
			if fuser:
				fus=True
				print "|--[FUZZER][>]"
				while(fus):
					try:
						fuser_steps=int(raw_input("|--[INFO][>] How many steps do you want?: "))
						modules.fuzzer_proces.fuser_process(fuser_steps, link, var_v)
						fus=False
					except Exception as e:
						print e
						print "|--[WARNING][>] Number of steps must be int."
	except Exception as e:
		print e
		pass

if __name__ == "__main__":
	banner()
	main()
