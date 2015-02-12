#@Author: Uday Sharma
import json
import string 
import re
import pymongo

#establishing connection to MongoDB
connection = pymongo.Connection("mongodb://localhost", safe=True)

db = connection.twitter
tweets = db.election.find({'lang':'en'}, {'text' :1, '_id':0})
hashtagsList = list()

# This function finds the hashtags in a tweet and appends it in a list
def hashtags(tweetText):
	ht =re.findall('(?<=^|(?<=[^a-zA-Z0-9-_\.]))(#[A-za-z]+[A-Za-z0-9])', tweetText.encode('utf8').lower())
	for h in ht:
		hashtagsList.append(h)

#This function counts the hashtags in the master list and stores the count in a temporary dictionary
def countHashtags(tweets):
	for t in tweets:
		hashtags(t['text'])
	tagCount = dict()

	for tag in hashtagsList:
		if tag in tagCount:
			tagCount[tag] +=1
		else:
			tagCount[tag] = 1

	for key, value in tagCount.iteritems():
		print key, value 



if __name__ == '__main__':
    countHashtags(tweets)
