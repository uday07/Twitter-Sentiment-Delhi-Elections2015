#@Author: Uday Sharma, Harshit Pandey
#Printing tweets to tabular format

import json
import string 
import re
import pymongo


#establishing connection to MongoDB and local files
connection = pymongo.Connection("mongodb://localhost", safe=True)
positiveWords = open('positive-words.txt', 'r')
negativeWords = open('negative-words.txt', 'r')

#Querying the desired database collection
db = connection.twitter
tweets = db.election.find({'lang':'en'}, {'created_at' :1, 'text' :1,  "retweet_count":1, "favorite_count":1, 'user':1 , 'posted':1})

posWords = re.split(r'\n', positiveWords.read())
negWords = re.split(r'\n', negativeWords.read())


#Method for performing parties score analysis based on the occurance of key hashtags

def score_analysis(tweetText): 
	aapList = ["#5saalkejriwal", "#aapkamanifesto", "#aamaadmikisarkaar", "#shahbag" , "#vote4ak", "#mycmkejriwal" ,  "#vote4mufflerman",
				"#istandWithKejriwal", "#thistimeaap", "#aapspycamsena", "#myvote4kejriwal", " #thankuaap", "#mufflermania", "#aapsweep", "#kiskidilli" , " #delhidecides","#anarchistaap", "#anarchist", "#vote4aap", "#joinaap" ]
	bjpList = ["#modiforpm", "#modipmbedicm", "#bjp4delhi" , "#kejriwaltest", "#abkibaarbedisarkaar", "#nationalists4bedi", "#modibedivision",
				"#umeedkikiran", "#delhiwithmodi", "#hawalaatmidnight", "#kiranbedi4cm", "#bjp=43+" , "#delhiwithkiranbedi", "#kiranbedi4cm", "#aapfundingscam"
				 ,"#aapfakesurvey", "#mypmnamo", "#irunbedi", "#kiranbedi", "#vote4bjp", "#vote4bbtyagi", "#joinbjp", "#bjp4delhi"]
	aap_score = 0
	bjp_score = 0 
	wordList = tweetText.lower().split() 
	bjp_score =lookup_for(tweetText, 4,'bjp')
	aap_score =  lookup_for(tweetText, 4, 'aap')

	for word in wordList:
		if word in aapList:
			aap_score +=1
			bjp_score -=1
		if word in bjpList:
			bjp_score +=1
			aap_score = -1


	if bjp_score >0 and aap_score<0:
		aap_score = -1
	elif aap_score >0 and bjp_score<0:
		bjp_score = -1

	return  str(bjp_score) + "\t" + str(aap_score)

    
# A method for generating score based on the positive-negative words 

def lookup_for(text, indexoffset, keyword):
	text=text.lower().partition(keyword)
	score =0
	#offset of words you want to look for 
	for s in text[1 :] : 
		keywords = s.split()
		for word in keywords[ :indexoffset]:
			if word in posWords:
				score +=1
			if word in negWords:
				score -=1

	for s in text[ :1]:
		keywords = s.split()
	
		for word in keywords[: indexoffset]:
			if word in posWords:
				score +=1
			if word in negWords:
				score -=1

	return score

# Method for getting the twitter user id whose tweets have been retweeted
def retweetedFrom(tweetText):
	name = re.findall('(?<=^|(?<=[^a-zA-Z0-9-_\.]))(@[A-Za-z]+[A-Za-z0-9]+:)', tweetText.encode('utf8'))
	for n in name:
		return n
		

# This function prints the final tab delimited output
def print_tweets(tweets):
	print "\"" + "created_at" + "\"", '\t',"\"" + "retweetedUser" + "\"", '\t',"\"" + "BJP Score" + "\"", '\t',"\"" + "AAP Score" + "\"", '\t',"\""+ "Tweet" + "\"", '\t', "\""+ "User Name" + "\"", '\t', "\""+ "user_twitter_id" + "\"", '\t', "\""+ "posted" + "\"", '\t'
	for t in tweets:
		print "\"" + t['created_at'][4:10] + "\"", '\t', retweetedFrom(t['text']),'\t', score_analysis(t['text'].encode('utf8')),'\t', "\"" + t['text'].encode('utf8').replace('\n', ' ') + "\"", '\t', "\"" + t['user']['name'].encode('utf8') + "\"", '\t', "\"" + t['user']['screen_name'].encode('utf8') + "\"",  '\t', "\"" + t['posted'].encode('utf8') + "\"", '\t'





if __name__ == '__main__':
    print_tweets(tweets)



