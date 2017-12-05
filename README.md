# KILLOIO CONSOLE
The script does security audits the results of Google and Duck Duck Go.
Version: 1.1

# How to install
1. Install MongoDB: sudo apt-get install mongodb
2. pip install -r dependencies.txt
3. Install https://github.com/thibauts/duckduckgo
4. And enjoy! python killoio.py 

# Parameter
		-h Help
		-s Search with Google and DuckduckGo
		-v To show all process of audit
		-e Select the exploit to scan, exploits: isql, sqli, xss, rce
		--fuzzer Make an attack trying to inject code
		-u Select tarjet for attack
    
# Thanks
+ Thanks for your code for payloads https://github.com/souviik/NetSecure
+ Thanks PyConEs 2017 for accepting our talk https://2017.es.pycon.org/es/schedule/killoio-el-google-espanol-creado-en-python/
+ Thanks to @Enelpc for the Parameterfuzz (http://www.enelpc.com/p/parameterfuzz.html) dictionaries

# Authors
- Jorge Coronado (aka @JorgeWebsec)
- Ramon Bajona
