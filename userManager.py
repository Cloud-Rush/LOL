import json
from passlib.hash import sha256_crypt

userFile = open("userDatabase.json")
data = json.load(userFile)
userFile.close()


def saveUserData():
	saveFile=open("userDatabase.json","w")
	json.dump(data,saveFile)
	saveFile.close()


def isValid(candidate):
	return len(candidate) >= 8

def checkLogin(username, password):
	hashy = sha256_crypt.encrypt(password)
	if username not in data:
		return "Error: No record of the account1"
	if sha256_crypt.verify(password, data[username]["passcode"]):
		return "check successful"
	return "Error: No record of the account2"

def registerLogin(username, password):
	if username in data:
		return "Error: Username already exists"
	if not isValid(password):
		return "Error: Password must be at least 8 characters in length"
	if password == "password":
		return "Really? you really want to use password? No, just no. Try again"
	data[username] = {}
	data[username]["streamers"] = []
	data[username]["champions"] = []
	data[username]["summoners"] = []
	data[username]["news"] = []
	data[username]["passcode"] = sha256_crypt.encrypt(password)
	return "registration successful"

def addSummoner(username, summoner):
	if summoner not in data[username]["summoners"]:
		data[username]["summoners"].append(summoner)
	saveUserData()

def addStreamer(username, streamer):
	if streamer not in data[username]["streamers"]:
		data[username]["streamers"].append(streamer)
	saveUserData()

def addChampion(username, champ):
	if champ not in data[username]["champions"]:
		data[username]["champions"].append(champ)
	saveUserData()

def addNews(username, news):
	if news not in data[username]["news"]:
		data[username]["news"].append(news)
	saveUserData()

def removeSummoner(username, summoner):
	if summoner in data[username]["summoners"]:
		data[username]["summoners"].remove(summoner)
	saveUserData()

def removeStreamer(username, streamer):
	if streamer in data[username]["streamers"]:
		data[username]["streamers"].remove(streamer)
	saveUserData()

def removeChampion(username, champ):
	if champ in data[username]["champions"]:
		data[username]["champions"].remove(champ)
	saveUserData()

def removeNews(username, news):
	if news in data[username]["news"]:
		data[username]["news"].remove(news)
	saveUserData()

def getStreamers(username):
	return data[username]["streamers"]

def getNews(username):
	return data[username]["news"]

def getChampions(username):
	return data[username]["champions"]

def getSummoners(username):
	return data[username]["summoners"]

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
	print getNews("El spleeno")

#test()
saveUserData()
