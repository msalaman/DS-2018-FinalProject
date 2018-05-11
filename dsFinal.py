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

def calculateScore(twitUser, RTs, Hashtag55):
    score = twitUser.followerCount / 10 + 150 / twitUser.degrees + (100 * (getHashCount(twitUser, Hashtag55, RTs)))
    return score

class node:
    def __init__(self, twitUser, val):
        self.t = twitUser
        self.v = val

class maxHeap:
 # Constructor to initialize a heap
    def __init__(self):
        self.heap = []

    def size(self):
        return len(self.heap)

    #index of parent of node at index i
    def parent(self, i):
        return (i-1)//2

    #index of left child of node at index i
    def left(self, i):
        return 2*i + 1

    #index of right child of node at index i
    def right(self, i):
        return 2*i + 2

    def swap(self, parent, child):
        temp = self.heap[child]
        self.heap[child] = self.heap[parent]
        self.heap[parent] = temp

    # Pushes node to heap
    def push(self, node):
        i = self.size()
        self.heap.append(node)

        while (i > 0 and self.heap[self.parent(i)].v < self.heap[i].v ):
            self.swap(self.parent(i), i)
            i = self.parent(i)

    def pop(self):
        if (self.size() == 0):
            return None
        i = 0
        heapMax = self.heap[i]
        self.heap[i] = self.heap[self.size() - 1]
        del self.heap[self.size() - 1]
        while (self.left(i) < self.size()):
            if (self.right(i) < self.size()):
                if (self.heap[i].v < self.heap[self.left(i)].v or self.heap[i].v < self.heap[self.right(i)].v):
                    if (self.heap[self.left(i)].v > self.heap[self.right(i)].v):
                        self.swap(i, self.left(i))
                        i = self.left(i)
                    else:
                        self.swap(i, self.right(i))
                        i = self.right(i)
                else:
                    break
            else:
                if (self.heap[i].v < self.heap[self.left(i)].v):
                    self.swap(i, self.left(i))
                    i = self.left(i)
                else:
                    break

        return heapMax


    # Get the minimum element from the heap
    def getMax(self):
        return self.heap[0]

    def printHeap(self, count=10):
        i = 0
        sz = self.size()
        while(i < count and i < sz):
            node = self.pop()
            print("Score: {} {} {} {}".format(node.v, node.t.name, node.t.screenName, node.t.followerCount))#, showNode.v)
            i = i + 1


    def delHeap(self):
        del self.heap[:]
        return None

def getHashCount(user, hashtag1, retweets): #get number of tweets with a given hashtag
    HashCount = 0
    tester1 = t.statuses.user_timeline(screen_name=user, count = 3)
    for TweetList in tester1:# I believe count is number of tweets
        #These are just checks right now above
        if TweetList["is_quote_status"] and not retweets: #should we look for retweets too?
            continue
        for HashList in TweetList["entities"]["hashtags"]:
            if HashList["text"].lower() == hashtag1.lower(): #match
                HashCount = HashCount + 1
    return HashCount

def getFollowers(user, degree, maxFollowers, RT=False, Hashtag=""): #recursive function that access followers
    heap = maxHeap()
    if degree == 3:
        return 0
    x = t.followers.list(screen_name=user, count = 200) #dictionary containing list of followers
    while True:
        for i in range(0,len(x['users'])): #iterate through list of followers
            follower = x['users'][i] #access follower object
            if follower['followers_count'] > maxFollowers: # don't want users with too many followers b/c unrealistic
                continue
            twitFollower = twitUser(follower['name'], follower['screen_name'], follower['followers_count'], follower['location'], degree, follower['profile_image_url'])
            twitNode = node(twitFollower, calculateScore(twitFollower, RT, Hashtag))
            heap.push(twitNode)

            if not follower['protected'] and not follower['verified'] and follower['followers_count'] < 2000: #recursively get follower's followers if account is not private
                getFollowers(follower['screen_name'], degree + 1, maxFollowers)
        cursor = x['next_cursor'] #get next page
        if cursor == 0: #no next page
            break
        x = t.followers.list(screen_name=user, cursor = cursor, count = 200) #turn to next page
    heap.printHeap(10)

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
    getFollowers(TWITHANDLE, DEGREES, MAXFOLLOWERS, True, Hashtag="gbr")
