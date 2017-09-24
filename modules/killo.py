#!/usr/bin/env python
#-*- coding:utf-8 -*-
#*******************************************
#APP: killo.io.py                        ***
#AUTHOR: Jorge Websec                    ***
#TWITTER: @JorgeWebsec                   ***
#Email: jorge@quantika14.com             ***
#*******************************************

#MODULES
import sys, cookielib, re, urllib2, httplib, urllib, duckduckgo, ast, requests, wikipedia
from bs4 import BeautifulSoup
from urlparse import urlparse
from unidecode import  unidecode
from urlparse import unquote
import mechanize
sys.path.append("lib")
import modules.detect_functions, modules.audit_joomla, modules.audit_wp, modules.audit_drupal, modules.audit_moodle
list_domain = []

#TAGS REMOVER
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
	return TAG_RE.sub('', text)

#search data in duckduckgo
def search_DuckDuckGO(data):
	try:
		links = duckduckgo.search(data, max_results=10)
		array_links = []
		for link in links:
			if link not in array_links:
				array_links.append(link)
		return array_links
	except:
		return None

#get Domain of the link
def get_domain(url):
	try:
		global list_domain
		parsed_uri = urlparse(url)
		domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)	
		return domain
	except:
		return None

#get Domains of the txt file to split this domains in rank_cms
def domain_split():
	domains_ban=[]
	infile = open('dic/no_audit_domains.txt', 'r')
	for line in infile:
		domains_ban.append(line.replace("\n",""))
	infile.close()
	return domains_ban


#check link for not in list domains_ban
def check_domains(link , domains_ban, var_v):
	for domain in domains_ban:
		if domain in link:
			return False
	return True



#search on google
def get_urls_google(html):
	url_google=[]
	#Parser HTML of BeautifulSoup
	soup = BeautifulSoup(html, "html.parser")
	#Parser url's throught regular expression
	raw_links = soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
	#print raw_links
	for link in raw_links:
		#Cache Google
		if link["href"].find("webcache.googleusercontent.com") == -1:
			nlink = link["href"].replace("/url?q=","")
		#Parser links
		nlink = re.sub(r'&sa=.*', "", nlink)
		nlink = urllib2.unquote(nlink).decode('utf8')
		url_google.append(nlink)
	return url_google

def SearchGoogle(num,target,var_v):
	start_page = 0
	nlink = ""
	user_agent = {'User-agent': 'Mozilla/5.0'}
	nlink_clean = ""
	response =""
	soup = ""
	raw_links = ""
	#Split the target in domain and extension
	domain = target.replace(".es",'')
	#extension = target.split(".")[1]
	for start in range(start_page, (start_page + num)):
		SearchGoogle = "https://www.google.com/search?q=" + target
	try:
		response = requests.get(SearchGoogle, headers = user_agent)
		html = response.text
	except requests.exceptions.RequestException as e:
		print "\nError connection to server!"
		pass	
	except requests.exceptions.ConnectTimeout as e:
		print "\nError Timeout",target
		pass
	try:
		if html.find("Our systems have detected unusual traffic") != -1:
			print "CAPTCHA detected - Plata or captcha !!!Maybe try form another IP..."
			print "OR you can use the proxy SOCKS5 list in proxy.txt. [YES=1, no=2]"
			url_duckduck=search_DuckDuckGO(target)
			return url_duckduck
		else:
			url_google=get_urls_google(html)
			return url_google
	except Exception as e:
		print e


#get Title of the link
def get_title(url):
	try:
		html = urllib2.urlopen(url)
		soup= BeautifulSoup(html, "html.parser")
		title=soup.title.text
		title_str=str(title)
		return remove_tags(title_str)
	except:
		return " "

#get Description of the link
def get_description(url):
	try:
		html = urllib2.urlopen(url)
		soup = BeautifulSoup(html, "html.parser")
		if 'wikipedia.org' in url:
			split_name = url.split('/')
			name = split_name[len(split_name)-1]
			name = unidecode(unquote(name))
			description = wikipedia.summary(name, sentences=2)
			return description
		else:
			description = soup.findAll(attrs={"name":"description"})
			if description:
				return description[0]['content']
			else:
				description = soup.findAll(attrs={"name":"DESCRIPTION"})
				if description:
					return description
				else:
					description = soup.findAll(attrs={"property":"og:description"})
					return description[0]['content']
	except:
		return ""


def get_website_factors(domain):
	try:
		final_list=[]
		url = "http://app.upguard.com/webscan?url=" + domain
		req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
		con = urllib2.urlopen(req, timeout=1)
		soup = BeautifulSoup(con, "html.parser")
		html = str(soup).replace("]", "[")
		html = html.split("[")
		for i in html: 
			if "SSL Enabled" in i:
				n = html.index(i)
		lista = html[n]
		lista = str(lista).replace("},{", "}|{")
		lista = str(lista).replace("true", "'true'")
		lista = str(lista).replace("false", "'false'")
		lista = lista.split("|")
		for i in lista:
			try:
				final_list.append(ast.literal_eval(i))
			except:
				continue	
		return final_list
	except Exception as e:
		final_list = "None"
		return final_list
