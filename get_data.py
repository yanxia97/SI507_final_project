from secrets import *
import requests
import csv
import time
import json
from bs4 import BeautifulSoup

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

place_FNAME = 'steam_countries.json'
try:
    place_file = open(place_FNAME, 'r')
    place_contents = place_file.read()
    PLACE_DICTION = json.loads(place_contents)
    place_file.close()

# if there was no file, no worries. There will be soon!
except:
    PLACE_DICTION = {}

player_FNAME = 'simple_player.json'
try:
    player_file = open(player_FNAME, 'r')
    player_contents = player_file.read()
    PLAYER_DICTION = json.loads(player_contents)
    player_file.close()

except:
    PLAYER_DICTION = {}

GAME_FNAME = 'games.json'
try:
    game_file = open(GAME_FNAME, 'r')
    game_contents = game_file.read()
    GAME_DICTION = json.loads(game_contents)
    game_file.close()

# if there was no file, no worries. There will be soon!
except:
    GAME_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}={}".format(k, params[k]))
    return baseurl + "&".join(res)

def make_request_using_cache(baseurl, parameter):
    unique_ident = params_unique_combination(baseurl, parameter)
    # print(unique_ident)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        # print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(unique_ident)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION, indent=4)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

base = "http://api.steampowered.com/"
extension_user = "ISteamUser/GetPlayerSummaries/v0001/?"
extension_friend = "ISteamUser/GetFriendList/v0001/?"
extension_games = "IPlayerService/GetOwnedGames/v0001/?"
base_game = "https://store.steampowered.com/app/"
steam_id = "76561197960435530"

def get_player_summary(steam_id):
    params = {"format":"json", "key": steam_key}
    params["steamids"]=steam_id
    results = make_request_using_cache(base+extension_user, params)
    with open('players.csv', 'w', newline='') as csvfile:
        fieldnames = ['steamid', 'personaname', 'profileurl', 'time_created', 'country', 'state', 'city']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        row = {}
        for player in results["response"]["players"]["player"]:
            if (player.__contains__("steamid")):
                if player["steamid"] in PLAYER_DICTION:
                    pass
                else:
                    PLAYER_DICTION[player["steamid"]] = player
                    dumped_json_cache = json.dumps(PLAYER_DICTION, indent=4)
                    fw = open(player_FNAME,"w")
                    fw.write(dumped_json_cache)
                    fw.close()
                row['steamid'] = player["steamid"]
                row['personaname'] = player['personaname']
                if (player.__contains__("profileurl")):
                    row['profileurl'] = player["profileurl"]
                if (player.__contains__("timecreated")):
                    row['time_created'] = str(time.asctime(time.localtime( player["timecreated"] )))
                if (player.__contains__("loccountrycode")):
                    row['country'] = PLACE_DICTION[player["loccountrycode"]]["name"]
                    if (player.__contains__("locstatecode")):
                        row['state'] = PLACE_DICTION[player["loccountrycode"]]["states"][player["locstatecode"]]["name"]
                        if (player.__contains__("loccityid")):
                            # print (PLACE_DICTION[player["loccountrycode"]]["states"][player["locstatecode"]]["cities"])
                            row['city'] = PLACE_DICTION[player["loccountrycode"]]["states"][player["locstatecode"]]["cities"][str(player["loccityid"])]["name"]
                writer.writerow(row)
    

def add_player_summary(steam_id):
    params = {"format":"json", "key": steam_key}
    params["steamids"]=steam_id
    results = make_request_using_cache(base+extension_user, params)
    with open('players.csv', 'a', newline='') as csvfile:
        fieldnames = ['steamid', 'personaname', 'profileurl', 'time_created', 'country', 'state', 'city']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for player in results["response"]["players"]["player"]:
            row = {}
            if (player.__contains__("steamid")):
                if player["steamid"] in PLAYER_DICTION:
                    pass
                else:
                    PLAYER_DICTION[player["steamid"]] = player
                    dumped_json_cache = json.dumps(PLAYER_DICTION, indent=4)
                    fw = open(player_FNAME,"w")
                    fw.write(dumped_json_cache)
                    fw.close()
                row['steamid'] = player["steamid"]
                row['personaname'] = player['personaname']
                if (player.__contains__("profileurl")):
                    row['profileurl'] = player["profileurl"]
                if (player.__contains__("timecreated")):
                    row['time_created'] = str(time.asctime(time.localtime( player["timecreated"] )))
                if (player.__contains__("loccountrycode")):
                    row['country'] = PLACE_DICTION[player["loccountrycode"]]["name"]
                    if (player.__contains__("locstatecode")):
                        row['state'] = PLACE_DICTION[player["loccountrycode"]]["states"][player["locstatecode"]]["name"]
                        if (player.__contains__("loccityid")):
                            # print (PLACE_DICTION[player["loccountrycode"]]["states"][player["locstatecode"]]["cities"])
                            row['city'] = PLACE_DICTION[player["loccountrycode"]]["states"][player["locstatecode"]]["cities"][str(player["loccityid"])]["name"]
                writer.writerow(row)

def get_friend_list(steam_id):
    params = {"format":"json", "key": steam_key}
    params["steamid"]=steam_id
    results = make_request_using_cache(base+extension_friend, params)
    with open('friends.csv', 'w', newline='') as csvfile:
        fieldnames = ['steamfriend1', 'steamfriend2', 'relationship', 'friend_since']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        try:
            for friend in results["friendslist"]["friends"]:
                row = {}
                friendid = friend["steamid"]
                add_player_summary(friendid)
                row['steamfriend1'] = min(friendid, steam_id)
                row['steamfriend2'] = max(friendid, steam_id)
                row['relationship'] = friend["relationship"]
                if (not friend["friend_since"] == 0):
                    row['friend_since'] = str(time.asctime(time.localtime( friend["friend_since"] )))
                writer.writerow(row)
        except:
            pass

def add_friend_list(steam_id):
    params = {"format":"json", "key": steam_key}
    params["steamid"]=steam_id
    results = make_request_using_cache(base+extension_friend, params)
    with open('friends.csv', 'a', newline='') as csvfile:
        fieldnames = ['steamfriend1', 'steamfriend2', 'relationship', 'friend_since']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        try:
            for friend in results["friendslist"]["friends"]:
                row = {}
                friendid = friend["steamid"]
                add_player_summary(friendid)
                row['steamfriend1'] = min(friendid, steam_id)
                row['steamfriend2'] = max(friendid, steam_id)
                row['relationship'] = friend["relationship"]
                if (not friend["friend_since"] == 0):
                    row['friend_since'] = str(time.asctime(time.localtime( friend["friend_since"] )))
                writer.writerow(row)
        except:
            pass

def get_game_list(steam_id):
    params = {"format":"json", "key": steam_key}
    params["steamid"]=steam_id
    results = make_request_using_cache(base+extension_games, params)
    with open('games.csv', 'w', newline='') as csvfile:
        fieldnames = ['appid', 'appname', 'ownerid', 'playtime_2weeks', 'playtime_forever']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        try:
            for app in results["response"]["games"]:
                row = {}
                appid = app["appid"]
                if str(appid) in GAME_DICTION:
                    appname = GAME_DICTION[str(appid)]
                else:
                    resp = requests.get(base_game+str(appid)).text
                    soup = BeautifulSoup(resp, 'html.parser')
                    appname = soup.find('div', class_="apphub_AppName").get_text(strip=True)
                    GAME_DICTION[str(appid)] = appname
                    dumped_json_cache = json.dumps(GAME_DICTION, indent=4)
                    fw = open(GAME_FNAME,"w")
                    fw.write(dumped_json_cache)
                    fw.close()
                row['appid'] = appid
                row['appname'] = appname
                row['ownerid'] = steam_id
                row['playtime_forever'] = app["playtime_forever"]
                if (app.__contains__('playtime_2weeks')):
                    row['playtime_2weeks'] = app["playtime_2weeks"]
                writer.writerow(row)
        except:
            pass

def add_game_list(steam_id):
    params = {"format":"json", "key": steam_key}
    params["steamid"]=steam_id
    results = make_request_using_cache(base+extension_games, params)
    with open('games.csv', 'a', newline='') as csvfile:
        fieldnames = ['appid', 'appname', 'ownerid', 'playtime_2weeks', 'playtime_forever']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        try:
            for app in results["response"]["games"]:
                row = {}
                appid = app["appid"]
                if str(appid) in GAME_DICTION:
                    appname = GAME_DICTION[str(appid)]
                else:
                    resp = requests.get(base_game+str(appid)).text
                    soup = BeautifulSoup(resp, 'html.parser')
                    appname = soup.find('div', class_="apphub_AppName").get_text(strip=True)
                    GAME_DICTION[str(appid)] = appname
                    dumped_json_cache = json.dumps(GAME_DICTION, indent=4)
                    fw = open(GAME_FNAME,"w")
                    fw.write(dumped_json_cache)
                    fw.close()
                row['appid'] = appid
                row['appname'] = appname
                row['ownerid'] = steam_id
                row['playtime_forever'] = app["playtime_forever"]
                if (app.__contains__('playtime_2weeks')):
                    row['playtime_2weeks'] = app["playtime_2weeks"]
                writer.writerow(row)
        except:
            pass

if __name__ == "__main__":
    get_player_summary(steam_id)
    get_friend_list(steam_id)
    i=0
    while (i<len(PLAYER_DICTION) and len(PLAYER_DICTION)<1000):
        add_friend_list(list(PLAYER_DICTION.keys())[i])
        i += 1
    # get_game_list(steam_id)
    # for id in PLAYER_DICTION:
    #     add_game_list(id)
