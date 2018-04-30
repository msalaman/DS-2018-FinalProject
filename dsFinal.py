#!/usr/bin/env python3

import sys
import os
from twitter import *

ACCESS_TOKEN = "988216913284255744-qBZJ3IAkrjBAPLaMRMjhkQrLtKIzn31"
ACCESS_TOKEN_SECRET = "WpcZY8dTZAQVWEJkZBlS8hMQaR9ckqOs8ErFML2x2bVAk"
CONSUMER_KEY = "sRKZDEri6WsOhDmJmxxbnLvyC"
CONSUMER_SECRET = "OJO5n71PvgNE6B6JLePAlRTyOlDoTFFpWziUEE4stu0pbNNLHo"
DEGREES = 1
MAXFOLLOWERS = 2000
TWITHANDLE = "dijkstra_edsger"
ARGUMENTS = sys.argv[1:]

class twitUser:
    def __init__(self, name, screenName, followerCount, location, degrees, profileImageURL):
        self.name = name
        self.screenName = screenName
        self.followerCount = followerCount
        self.location = location
        self.degrees = degrees
        self.profileImageURL = profileImageURL    
    
def calculateScore(twitUser):
    score = twitUser.followerCount / 3 + 200 / twitUser.degrees
    if twitUser.location == 'Omaha, NE':
        score += 50
    return score

def getFollowers(user, degree, maxFollowers): #recursive function that access followers
    if degree == 3:
        return 0
    x = t.followers.list(screen_name=user, count = 200) #dictionary containing list of followers  
    while True:
        for i in range(0,len(x['users'])): #iterate through list of followers
            follower = x['users'][i] #access follower object
            if follower['followers_count'] > maxFollowers: # don't want users with too many followers b/c unrealistic
                continue
            twitFollower = twitUser(follower['name'], follower['screen_name'], follower['followers_count'], follower['location'], degree, follower['profile_image_url'])
            print(twitFollower.name, calculateScore(twitFollower))
            
            if not follower['protected'] and not follower['verified'] and follower['followers_count'] < 2000: #recursively get follower's followers if account is not private
                getFollowers(follower['screen_name'], degree + 1, maxFollowers)
        cursor = x['next_cursor'] #get next page
        if cursor == 0: #no next page
            break
        x = t.followers.list(screen_name=user, cursor = cursor, count = 200) #turn to next page

def usage(exit_code=0):
    print('''Usage: {} HANDLE [-d DEGREES -m MAXFOLLOWERS]
    -d DEGREES The max amount of degrees away from the user (3 is the request max
    -m MAXFOLLOWERS Set the threshold for what the max followers should be capped at
    twitterHandle: the Twitter handle of the user without the @'''.format(os.path.basename(sys.argv[0])))
    sys.exit(exit_code)

if __name__ == '__main__':
    # Parse command line arguments
    if (len(sys.argv) > 1):
        arg = ARGUMENTS.pop(0)
        if (arg == "-h"):
            usage(0)
        else:
            TWITHANDLE = arg
        
    while ARGUMENTS and len(ARGUMENTS[0]) > 1:
        arg = ARGUMENTS.pop(0)
        if arg == '-h':
            usage(0)
        elif arg == '-d':
            DEGREES = int(ARGUMENTS.pop(0))
        elif arg == '-m':
            MAXFOLLOWERS = int(ARGUMENTS.pop(0))
        else:
            usage(1)

    # Put in token, token_key, con_secret, con_secret_key
    t = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
    getFollowers(TWITHANDLE, DEGREES, MAXFOLLOWERS)
