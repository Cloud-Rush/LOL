import json
import time

cacheFile = open("cacheDatabase.json")
cacheData = json.load(cacheFile)
cacheFile.close()

CHAMPION_TOLERANCE = 180000 #3min
NEWS_TOLERANCE =  15 #2.5 min	
STREAMER_TOLERANCE = 1800000 #30 min
SUMMONER_TOLERANCE = 3600000 #1 hour


#used for setupDatabase
def saveCache(saveData):
	saveFile = open("cacheDatabase.json","w")
	json.dump(saveData,saveFile)
	saveFile.close()

def saveCache():
	saveFile = open("cacheDatabase.json","w")
	json.dump(cacheData,saveFile)
	saveFile.close()

#used for starting a database from scratch
#this will reset the database
def setupDatabase():
	initData = {}
	initData["champions"] = {}
	initData["news"] = {}
	initData["summoners"] = {}
	initData["streamers"] = {}
	saveCache(initData)

#update methods take what is requested to update, and the new information for it
#adds timestamp information
def updateChampion(name,info):
	if name in cacheData["champiions"]:
		cacheData["champions"][name]["time"] = time.time()
		cacheData["champions"][name]["info"] = info
		cacheData["champions"][name]["stale"] = False
	else:
		cacheData["champions"][name] = {}
		cacheData["champions"][name]["time"] = time.time()
		cacheData["champions"][name]["info"] = info
		cacheData["champions"][name]["stale"] = False
	saveCache()

def updateNews(name,info):
	if name in cacheData["news"]:
		cacheData["news"][name]["time"] = time.time()
		cacheData["news"][name]["info"] = info
		cacheData["news"][name]["stale"] = False
	else:
		cacheData["news"][name] = {}
		cacheData["news"][name]["time"] = time.time()
		cacheData["news"][name]["info"] = info
		cacheData["news"][name]["stale"] = False
	saveCache()

def updateStreamer(name,info):
	if name in cacheData["streamers"]:
		cacheData["streamers"][name]["time"] = time.time()
		cacheData["streamers"][name]["info"] = info
		cacheData["streamers"][name]["stale"] = False
	else:
		cacheData["streamers"][name] = {}
		cacheData["streamers"][name]["time"] = time.time()
		cacheData["streamers"][name]["info"] = info
		cacheData["streamers"][name]["stale"] = False
	saveCache()
	
def updateSummoner(name,info):
	if name in cacheData["summoners"]:
		cacheData["summoners"][name]["time"] = time.time()
		cacheData["summoners"][name]["info"] = info
		cacheData["summoners"][name]["stale"] = False
	else:
		cacheData["summoners"][name] = {}
		cacheData["summoners"][name]["time"] = time.time()
		cacheData["summoners"][name]["info"] = info
		cacheData["summoners"][name]["stale"] = False
	saveCache()

#get basic data
#returns {} if no ifo exists, or if the data is marked as stale
def getChampionInfo(name):
	if name in cacheData["champions"] and cacheData["champions"][name]["stale"] == False:
		return cacheData["champions"][name]["info"]
	else:
		return {}

def getSummonerInfo(name):
	if name in cacheData["summoners"] and cacheData["summoners"][name]["stale"] == False:
		return cacheData["summoners"][name]["info"]
	else:
		return {}

def getNewsInfo(name):
	if name in cacheData["news"] and cacheData["news"][name]["stale"] == False:
		return cacheData["news"][name]["info"]
	else:
		return {}

def getStreamerInfo(name):
	if name in cacheData["streamers"] and cacheData["streamers"][name]["stale"] == False:
		return cacheData["streamers"][name]["info"]
	else:
		return {}


#trim the database, mark items as stale
def trimCache():
	prunableSummonerKeys = []
	prunableStreamerKeys = []
	prunableNewsKeys = []
	prunableChampionKeys = []
	#for each listing, check how old the data is
	#if the data is old, mark as stale and reset timestamp
	#if data is already stale, mark for deletion
	for name in cacheData["summoners"]:
		if time.time() - SUMMONER_TOLERANCE > cacheData["summoners"][name]["time"]:
			if cacheData["summoners"][name]["stale"] == False:
				cacheData["summoners"][name]["stale"] = True
				cacheData["summoners"][name]["time"] = time.time()
			else:
				prunableSummonerKeys.append(name)
	for name in cacheData["streamers"]:
		if time.time() - STREAMER_TOLERANCE > cacheData["streamers"][name]["time"]:
			if cacheData["streamers"][name]["stale"] == False:
				cacheData["streamers"][name]["stale"] = True
				cacheData["streamers"][name]["time"] = time.time()
			else:
				prunableStreamerKeys.append(name)
	for name in cacheData["news"]:
		if time.time() - NEWS_TOLERANCE > cacheData["news"][name]["time"]:
			if cacheData["news"][name]["stale"] == False:
				cacheData["news"][name]["stale"] = True
				cacheData["news"][name]["time"] = time.time()
			else:
				prunableNewsKeys.append(name)
	for name in cacheData["champions"]:
		if time.time() - CHAMPION_TOLERANCE > cacheData["champions"][name]["time"]:
			if cacheData["champions"][name]["stale"] == False:
				cacheData["champions"][name]["stale"] = True
				cacheData["champions"][name]["time"] = time.time()
			else:
				 prunableChampionKeys.append(name)
	#delete the elements marked for deletion
	for pruner in prunableSummonerKeys:
		del cacheData["summoners"][pruner]
	for pruner in prunableStreamerKeys:
		del cacheData["streamers"][pruner]
	for pruner in prunableNewsKeys:
		del cacheData["news"][pruner]
	for pruner in prunableChampionKeys:
		del cacheData["champions"][pruner]
	saveCache()

def test():
	updateStreamer("Emorelleum",{"url":"www.spleen.com","title":"Viktor epic fail"})
	updateNews("Blah", {"Art 1":"la"})
	saveCache()

trimCache()
#don;t uncomment this unless you want to reset the database
#setupDatabase()
