import queue
import threading
import os
import urllib.request

threads = 10
target = input("Enter URL: ")
directory = "/home/strike/Downloads/Joomla"
filters = [".jpg", ".png", ".txt", ".pdf", ".zip", ".gif", ".css", ".html", ".php",]
os.chdir(directory)
web_paths = queue.Queue()
for r,d,f in os.walk("."):
	for files in f:
		remote_path = "%s/%s" % (r, files)
		if remote_path.startswith("."):
			remote_path = remote_path[1:] 
		
		if os.path.splitext(files)[1] not in filters:
			web_paths.put(remote_path)

def test_remote():
	while not web_paths.empty():
		path = web_paths.get()
		url = "%s%s" % (target,path)
		request = urllib.request.Request(url)
		try:
			response = urllib.request.urlopen(url)
			content = response.read()
			print("[%d-OK] => %s" % (response.code,path))
			response.close() 
		
		except:
			print("[404-NOT FOUND] => %s" % (path))
			pass

for i in range(threads):
	print("Spawning Threads: %d" % i)
	t=threading.Thread(target=test_remote)
	t.start()			
