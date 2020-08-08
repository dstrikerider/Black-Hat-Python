import urllib.request
import urllib.parse
import urllib.error
import threading
import queue
import os

os.system("clear")
print("\n\t\t\t\t\t\t\t    ********** ~~ Website Content Brute Force Attack ~~ **********")
print("\t\t\t\t\t\t\t    Developed in Python 3 by Debshubra Chakraborty (Strike Rider)\n\n") 
target = input("Enter Target URL: ")
wordlist = "/home/strike/Downloads/SVNDigger/all.txt"
threads = 50
user_agent = "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0"
resume = None
print("\n\n[+] Targeted URL: %s" % (target))
print("[+] Wordlist: %s" % (wordlist))
print("[+] Threads: %d" % (threads))
print("[+] User-Agent: %s" % (user_agent))
	
def build_wordlist(wordlist):
	print("[*] Building Wordlist")
	fd = open(wordlist,"r")
	raw_words = [line.rstrip('\n') for line in fd]
	fd.close()
	word = raw_words
	found_resume = False
	words = queue.Queue()
	for word in raw_words:
		if resume:
			if found_resume:
				words.put(word)
			else:
				if word == resume:
					found_resume = True
					print("[*] Resuming wordlist form: %s" % (resume))
						
		else:
			words.put(word)
	
	print("[+] Wordlist Build\n")
	return words

def dir_bruter(extensions=None):
	while not word_queue.empty():
		attempt = word_queue.get()
		attempt_list = []
		if "." not in attempt:
			attempt_list.append("/%s/" % (attempt))
		else:
			attempt_list.append("/%s" % (attempt))
		
		if extensions:
			for extension in extensions:
				attempt_list.append("/%s%s" % (attempt, extension))
		
		for brute in attempt_list:
			url = "%s%s" % (target, urllib.parse.quote(brute))
			try:
				header = {"User-Agent": user_agent}
				request = urllib.request.Request(url, headers=header)
				response = urllib.request.urlopen(request)
				if len(response.read()):
					print("[%d] => %s" % (response.code, url))
			
			except urllib.error.HTTPError as e:
				if e.code != 404:
					print("!!! [%d] => %s" % (e.code,url))
				
				pass
			
			except urllib.error.URLError:
				pass

word_queue = build_wordlist(wordlist)
extensions = [".php",".bak",".orig",".inc"]
print("[*] Starting Content Brute Forcing with Wordlist\n")
temp = 0
for i in range(threads):
	temp = temp + 1;
	task = threading.Thread(target=dir_bruter,args=(extensions,))
	task.start()
	
if temp == 49:
	print("\n[+] Brute Force Attack Satus: Completed\n")
