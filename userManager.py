import json
import copy
import threading
import time
from passlib.hash import sha256_crypt

userFile = open("userDatabase.json")
data = json.load(userFile)
userFile.close()
userMutex = threading.Lock()

def saveUserData():
	saveFile = None
	try:
		saveFile=open("userDatabase.json","w")
	except:
		print "error when attempting to save user file"
		return
	userMutex.acquire()
	json.dump(data,saveFile)
	saveFile.close()
	#print "saved1"
	userMutex.release()

def saveUserData2():
	saveFile = None
	try:
		saveFile=open("userDatabase2.json","w")
	except:
		print "error when attempting to save user file"
		return
	userMutex.acquire()
	json.dump(data,saveFile)
	saveFile.close()
	#print "saved2"
	userMutex.release()


def isValid(candidate):
	return len(candidate) >= 8

def checkLogin(username, password):
	hashy = sha256_crypt.encrypt(password)
	if username not in data:
		return "Error: No record of the account"
	if sha256_crypt.verify(password, data[username]["passcode"]):
		return "check successful"
	return "Error: No record of the account"

def registerLogin(username, password):
	if "@" in username:
		return "Error: Username cannot contain '@' cahracter"
	if username in data:
		return "Error: Username already exists"
	if not isValid(password):
		return "Error: Password must be at least 8 characters in length"
	if password == "password":
		return "Really? you really want to use password? No, just no. Try again"
	userMutex.lock()
	data[username] = {}
	data[username]["streamers"] = []
	data[username]["champions"] = []
	data[username]["summoners"] = []
	data[username]["news"] = []
	data[username]["showStreams"] = True
	data[username]["showSummoners"] = True
	data[username]["showNews"] = True
	data[username]["passcode"] = sha256_crypt.encrypt(password)
	userMutex.release()
	return "registration successful"

def addSummoner(username, summoner):
	if summoner not in data[username]["summoners"]:
		userMutex.acquire()
		data[username]["summoners"].append(summoner)
		userMutex.release()
	#saveUserData()

def addStreamer(username, streamer):
	if streamer not in data[username]["streamers"]:
		userMutex.acquire()
		data[username]["streamers"].append(streamer)
		userMutex.release()
	#saveUserData()

def addChampion(username, champ):
	if champ not in data[username]["champions"]:
		userMutex.acquire()
		data[username]["champions"].append(champ)
		userMutex.release()
	#saveUserData()

def addNews(username, news):
	if news not in data[username]["news"]:
		userMutex.acquire()
		data[username]["news"].append(news)
		userMutex.release()
	#saveUserData()

def toggleNews(username,val):
	data["username"]["showNews"] = val

def toggleStreamers(username,val):
	data["username"]["showStreams"] = val

def toggleSummoners(username,val):
	data["username"]["showSummoners"] = val

def getToggleNews(username,val):
	return data["username"]["showNews"]

def getToggleStreamers(username,val):
	return data["username"]["showStreams"]

def getToggleSummoners(username,val):
	return data["username"]["showSummoners"]

def removeSummoner(username, summoner):
	if summoner in data[username]["summoners"]:
		userMutex.acquire()
		data[username]["summoners"].remove(summoner)
		userMutex.release()
	#saveUserData()

def removeStreamer(username, streamer):
	if streamer in data[username]["streamers"]:
		userMutex.acquire()
		data[username]["streamers"].remove(streamer)
		userMutex.release()
	#saveUserData()

def removeChampion(username, champ):
	if champ in data[username]["champions"]:
		userMutex.acquire()
		data[username]["champions"].remove(champ)
		userMutex.release()
	#saveUserData()

def removeNews(username, news):
	if news in data[username]["news"]:
		userMutex.acquire()
		data[username]["news"].remove(news)
		userMutex.release()
	#saveUserData()

def getStreamers(username):
	userMutex.acquire()
	ret = copy.deepcopy(data[username]["streamers"])
	userMutex.release()
	return ret

def getNews(username):
	userMutex.acquire()
	ret = copy.deepcopy(data[username]["news"])
	userMutex.release()
	return ret

def getChampions(username):
	userMutex.acquire()
	ret = copy.deepcopy(data[username]["champions"])
	userMutex.release()
	return ret

def getSummoners(username):
	userMutex.acquire()
	ret = copy.deepcopy(data[username]["summoners"])
	userMutex.release()
	return ret

#method for thread to periodically save database
def upkeep():
	#print "upkeeping"
	while True:
		#print "in loop"
		time.sleep(300)
		saveUserData()
		time.sleep(300)
		saveUserData2()


def test():
	#checkLogin("spleen", "lala") 
	#checkLogin("rommba","spleeeeeeeen")	
	print registerLogin("spleen", "lala")
	print registerLogin("El spleeno","password1")
	print checkLogin("El spleeno","password1")
	addNews("El spleeno","FOTM")
	addChampion("El spleeno","Elise")
	addStreamer("El spleeno","Faker")
	addSummoner("El spleeno", "El Spleeno")
	addNews("El spleeno","Queue")
	addNews("El spleeno","Jaja")
	removeNews("El spleeno","Queue")
	removeNews("El spleeno","Queue")
	registerLogin("oola","poinsetta")
	addNews("El spleeno","Viktor foud to be OP3")
	print getNews("El spleeno")
	saveUserData()

upkeepThread = threading.Thread(target = upkeep)
upkeepThread.start()
test()
#saveUserData()
