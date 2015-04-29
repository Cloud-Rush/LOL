import requests

import json
import time
import praw
import time
import copy
import threading
from riotwatcher import RiotWatcher
from riotwatcher import EUROPE_WEST
from riotwatcher import EUROPE_NORDIC_EAST
from riotwatcher import KOREA
from riotwatcher import OCEANIA
from riotwatcher import BRAZIL
from riotwatcher import LATIN_AMERICA_SOUTH
from riotwatcher import LATIN_AMERICA_NORTH
from riotwatcher import NORTH_AMERICA
from riotwatcher import RUSSIA
from riotwatcher import TURKEY
from twitch import *

cacheMutex = threading.Lock()

riot = RiotWatcher('24d89b10-e6ee-469a-91bd-f5e2d15c9e31')
twitch = TwitchTV()
reddit = praw.Reddit(user_agent = 'TheFountain by /u/tstarrs')
#submissions = reddit.get_subreddit('leagueoflegends').get_top(limit = 10)
#submissions2 = reddit.get_subreddit('summonerschool').get_top(limit = 10)
#submissions3 = reddit.get_subreddit('loleventvods').get_top(limit = 10)
#allSubmissions = (submissions + submissions2 + submissions3)
cacheFile = open("cacheDatabase.json")
cacheData = json.load(cacheFile)
cacheFile.close()

CHAMPION_TOLERANCE = 180000 #3min
NEWS_TOLERANCE =  15 #2.5 min	
STREAMER_TOLERANCE = 1800000 #30 min
SUMMONER_TOLERANCE = 3600000 #1 hour


#used for setupDatabase
def saveCacheDef(saveData):
	saveFile = open("cacheDatabase.json","w")
	json.dump(saveData,saveFile)
	saveFile.close()

def saveCache():
	try:
		saveFile = open("cacheDatabase.json","w")
	except:
		print "error attempting to save cache"
		return
	cacheMutex.acquire()
	json.dump(cacheData,saveFile)
	saveFile.close()
	cacheMutex.release()


def saveCache2():
	try:
		saveFile = open("cacheDatabase2.json","w")
	except:
		print "error attempting to save cache"
		return
	cacheMutex.acquire()
	json.dump(cacheData,saveFile)
	saveFile.close()
	cacheMutex.release()

def extractSummoner(sumName):
	summer = riot.get_summoner(name=sumName)
	sumnum = summer['id']
	statsList = (riot.get_ranked_stats(sumnum))['champions']
	stats = None
	for entry in statsList:
		if entry['id'] == 0:
			stats = entry['stats']
	infor = {}
	infor['rankedGames'] = stats['totalSessionsPlayed']
	infor['pentakills'] = stats['totalPentaKills']
	if infor['rankedGames'] != 0:
		infor['goldPerGame'] = stats['totalGoldEarned'] / infor['rankedGames']
	else:
		infor['goldPerGame'] = 0
	objy = riot.get_league_entry(summoner_ids=[sumnum])
	infor['league'] = objy[str(sumnum)][0]['tier'] + " " + objy[str(sumnum)][0]['entries'][0]['division']
	updateSummoner(sumName,infor)

def extractStreams():
	infor = twitch.getGameStreams("League of Legends")
	for key in infor:
		updateStreamer(key['channel']['name'],key)

def extractRedditData():
	submissions = reddit.get_subreddit('leagueoflegends').get_top(limit = 10)
	submissions2 = reddit.get_subreddit('summonerschool').get_top(limit = 10)
	submissions3 = reddit.get_subreddit('loleventvods').get_top(limit = 10)
	lolred = []
	for x in submissions:
		lolred.append(str(x))
	updateNews('leagueoflegends',lolred)
	ssred = []
	for x in submissions2:
		ssred.append(str(x))
	updateNews('summonerschool',ssred)
	vred = []
	for x in submissions3:
		vred.append(str(x))
	updateNews('loleventvods',vred)
#used for starting a database from scratch
#this will reset the database
def setupDatabase():
	initData = {}
	initData["champions"] = {}#{riot.get_all_champions()}
	initData["news"] = {}#{allSubmissions}
	initData["summoners"] = {}
	initData["streamers"] = {}#{twitch.getGameStreams("League of Legends")}
	saveCacheDef(initData)

#update methods take what is requested to update, and the new information for it
#adds timestamp information
def updateChampion(name,info):
	if name in cacheData["champiions"]:
		cacheData["champions"][name]["time"] = time.time()
		cacheData["champions"][name]["info"] = info
		cacheData["champions"][name]["stale"] = False
	else:
		cacheMutex.acquire()
		cacheData["champions"][name] = {}
		cacheData["champions"][name]["time"] = time.time()
		cacheData["champions"][name]["info"] = info
		cacheData["champions"][name]["stale"] = False
		cacheMutex.release()
	#saveCache()

def updateNews(name,info):
	if name in cacheData["news"]:
		cacheData["news"][name]["time"] = time.time()
		cacheData["news"][name]["info"] = info
		cacheData["news"][name]["stale"] = False
	else:
		cacheMutex.acquire()
		cacheData["news"][name] = {}
		cacheData["news"][name]["time"] = time.time()
		cacheData["news"][name]["info"] = info
		cacheData["news"][name]["stale"] = False
		cacheMutex.release()
	#saveCache()

def updateStreamer(name,info):
	if name in cacheData["streamers"]:
		cacheData["streamers"][name]["time"] = time.time()
		cacheData["streamers"][name]["info"] = info
		cacheData["streamers"][name]["stale"] = False
	else:
		cacheMuetex.acquire()
		cacheData["streamers"][name] = {}
		cacheData["streamers"][name]["time"] = time.time()
		cacheData["streamers"][name]["info"] = info
		cacheData["streamers"][name]["stale"] = False
		cacheMutex.release()
	#saveCache()
	
def updateSummoner(name,info):
	if name in cacheData["summoners"]:
		cacheData["summoners"][name]["time"] = time.time()
		cacheData["summoners"][name]["info"] = info
		cacheData["summoners"][name]["stale"] = False
	else:
		cacheMutex.acquire()
		cacheData["summoners"][name] = {}
		cacheData["summoners"][name]["time"] = time.time()
		cacheData["summoners"][name]["info"] = info
		cacheData["summoners"][name]["stale"] = False
		cacheMutex.release()
	#saveCache()

#get basic data
#returns {} if no ifo exists, or if the data is marked as stale
def getChampionInfo(name):
	if name in cacheData["champions"] and cacheData["champions"][name]["stale"] == False:
		cacheMutex.acquire()
		ret = copy.deepcopy(cacheData["champions"][name]["info"])
		cacheMutex.release()
		return ret
	else:
		return {}

def getSummonerInfo(name):
	if name in cacheData["summoners"] and cacheData["summoners"][name]["stale"] == False:
		cacheMutex.acquire()
		ret = copy.deepcopy(cacheData["summoners"][name]["info"])
		cacheMutex.release()
		return ret
	else:
		return {}

def getNewsInfo(name):
	if name in cacheData["news"] and cacheData["news"][name]["stale"] == False:
		cacheMutex.acuire()
		ret = copy.deepcopy(cacheData["news"][name]["info"])
		cacheMutex.release()
		return ret
	else:
		return {}

def getStreamerInfo(name):
	if name in cacheData["streamers"] and cacheData["streamers"][name]["stale"] == False:
		cacheMutex.acquire()
		ret = copy.deepcopy(cacheData["streamers"][name]["info"])
		cacheMutex.release()
		return ret
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
	cacheMutex.acquire()
	for pruner in prunableSummonerKeys:
		del cacheData["summoners"][pruner]
	for pruner in prunableStreamerKeys:
		del cacheData["streamers"][pruner]
	for pruner in prunableNewsKeys:
		del cacheData["news"][pruner]
	for pruner in prunableChampionKeys:
		del cacheData["champions"][pruner]
	cacheMutex.release()
	saveCache()

def upkeep():
	while True:
		time.sleep(300)
		saveCache()
		time.sleep(300)
		saveCache2()

def test():
	updateStreamer("Emorelleum",{"url":"www.spleen.com","title":"Viktor epic fail"})
	updateNews("Blah", {"Art 1":"la"})
	#extractRedditData()
	extractSummoner('CloudRush')
	extractSummoner('Taikohn')
	#extractStreams()
	saveCache()

#setupDatabase()
upkeepThread = threading.Thread(target = upkeep)
upkeepThread.start()
test()
#trimCache()
#don't uncomment this unless you want to reset the database
#setupDatabase()
