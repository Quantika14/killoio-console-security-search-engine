from bs4 import BeautifulSoup
import urllib2, re, requests, duckduckgo
import vulnerability, site_fetch

def get_urls_google(html):
	url_google=[]
	soup = BeautifulSoup(html, "html.parser")
	raw_links = soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
	for link in raw_links:
		if link["href"].find("webcache.googleusercontent.com") == -1:
			nlink = link["href"].replace("/url?q=","")
		nlink = re.sub(r'&sa=.*', "", nlink)
		nlink = urllib2.unquote(nlink).decode('utf8')
		url_google.append(nlink)
	print "|----[INFO] Search with Google..."
	return url_google

def SearchGoogle(num,domain):
	start_page = 0
	nlink = ""
	user_agent = {'User-agent': 'Mozilla/5.0'}
	nlink_clean = ""
	response =""
	soup = ""
	raw_links = ""
	dork1 = "site:" + domain + " " + "inurl:.php?id="

	for start in range(start_page, (start_page + num)):
		SearchGoogle = "https://www.google.com/search?q=" + dork1
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
			print "|----[INFO] CAPTCHA detected - Plata or captcha !!!Maybe try form another IP..."
			print "            OR you can use the proxy list OR  we recommend using VPN"
			print ""
			print "|----[INFO] Search with Duck Duck Go..."
			url_scan=Searchduckduckgo(domain)
			return url_scan
		else:
			url_scan=get_urls_google(html)
			return url_scan
	except Exception as e:
		print e

def Searchduckduckgo(domain):
	try:
		url_scan = []
		dork1 = "site:" + domain + " " + "inurl:.php?id="
		links = duckduckgo.search(dork1, max_results=10)
		for link in links:
			url_scan.append(str(link))
		l = len(url_scan)
		if l < 2:
			print "|----[WARNING] The search hasn't results with 'inurl:.php?id='."
			return None
		else:
			print "|----[INFO] Founds the result: " + str(l)
			return url_scan
	except Exception as e:
		print e

def removeDuplicate_url(url_scan):
	clean_url_scan = []
	for url in url_scan:
		if not url in clean_url_scan:
			clean_url_scan.append(url)
		else:
			continue
	#print "Clean target list..."
	return clean_url_scan

def audit_vulnerability(mode, url_scan, var_v):
	type_vul_list=[]
	vulnerb_list=[]
	if url_scan != None:
		print "|--[SCAN VULNERABILITY][>] "
		url_scan=removeDuplicate_url(url_scan)
		if mode == "sqli":
			for target in url_scan:
				type_vul, vulnerb=vulnerability.sqliExploit(target, var_v)
			return type_vul,  vulnerb
		if mode == "xss":
			for target in url_scan:
				type_vul, vulnerb=vulnerability.xssExploit(target, var_v)
			return type_vul, vulnerb		
		if mode == "rce":
			for target in url_scan:
				type_vul, vulnerb=vulnerability.remoteCodeExec(target, var_v)
			return type_vul, vulnerb
		else:
			for target in url_scan:
				type_vul, vulnerb=vulnerability.sqliExploit(target, var_v)
				if vulnerb!="None":
					type_vul_list.append(type_vul)
					vulnerb_list.append(vulnerb)
				type_vul, vulnerb=vulnerability.xssExploit(target, var_v)
				if vulnerb!="None":
					type_vul_list.append(type_vul)
					vulnerb_list.append(vulnerb)
				type_vul, vulnerb=vulnerability.remoteCodeExec(target, var_v)
				if vulnerb!="None":
					type_vul_list.append(type_vul)
					vulnerb_list.append(vulnerb)
			return type_vul_list, vulnerb_list
	else:
		pass
