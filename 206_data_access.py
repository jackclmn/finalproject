#Final Project
#Option 2
#John Coleman

#import statements
import unittest
import itertools
import collections
import tweepy
import twitter_info
import json, requests
import sqlite3
import re
import pprint

#tweepy setup
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

#Caching setup
CACHE_FNAME = "SI206_final_cache.json"
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

#function get_tweets() to get and cache data from twitter based on a search term
def get_tweets(query): #from project 3 line 52 and HW5
	unique_identifier = "twitter_{}".format(query)

	if unique_identifier in CACHE_DICTION:
		print('using cached data for', query)
		twitter_results = CACHE_DICTION[unique_identifier]
	else:
		print('getting data from internet for', query)
		twitter_results = api.search(query)
		twitter_results = twitter_results['statuses']
		CACHE_DICTION[unique_identifier] = twitter_results 
		f = open(CACHE_FNAME,'w', encoding = 'utf-8') 
		f.write(json.dumps(CACHE_DICTION))
		f.close()
	return twitter_results

#function get_twitter_user() to get and cache data from twitter based on a twitter user
def get_twitter_user(user): #from project 4
	unique_identifier = "twitter_{}".format(user)

	if unique_identifier in CACHE_DICTION:
		print('using cached data for', user)
		twitter_results = CACHE_DICTION[unique_identifier]
	else:
		print('getting data from internet for', user)
		twitter_results = api.get_user(user)
		CACHE_DICTION[unique_identifier] = twitter_results
		f = open(CACHE_FNAME,'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()
	return twitter_results

#function get_omdb() to get and cache data from OMDB based on movie title
def get_omdb(query):
	unique_identifier = "OMDB_{}".format(query)

	if unique_identifier in CACHE_DICTION:
		print('using cached data for', query)
		omdb_results = CACHE_DICTION[unique_identifier]
	else:
		print('getting data from internet for', query)
		url = 'http://www.omdbapi.com/?t='
		omdb_results = requests.get(url + query)
		omdb_results = json.loads(omdb_results.text)
		CACHE_DICTION[unique_identifier] = omdb_results 
		f = open(CACHE_FNAME,'w') 
		f.write(json.dumps(CACHE_DICTION))
		f.close()
	return omdb_results

#define a class called Movie
#define __init__ such that it takes a dictionary representing a movie
#include an instance variable "title" that holds a string for the movie's title
#include an instance variable "director" that holds a string for the movie's director
#include an instance variable "actors" that holds a list of strings of the actors in the movie
#include an instance variable "rating" that holds the IMDB rating
#include a method __str__ that prints details about the movie in the form: "MOVIE TITLE by DIRECTOR starring ACTOR 1, ACTOR 2, ACTOR 3..."
#include a method num_languages that calculates the number of languages the movie is available in
#will need to store title, director, IMDB rating, list of actors, and the number of languages

#define class Movie here:
class Movie(object):
	def __init__(self, dict):
		self.title = dict['Title']
		self.director = dict['Director']
		self.actors = dict['Actors']
		self.rating = dict['imdbRating']
		self.languages = dict['Language']
		self.num_languages = self.calc_num_languages()

	def __str__(self):
		return self.title + ' by ' + self.director + ' starring ' + self.actors

	def calc_num_languages(self):
		return len(self.languages)

	def set_movie_id(self, id):
		self.movie_id = id


#define a class called Tweet
#define __init__ such that it takes a dictionary representing a tweet and stores the values as instance variables

#define class Tweet here:
#text, id, user, movie, num favs, num rts
class Tweet(object):
	def __init__(self, dict):
		self.text = dict['text']
		self.num_favorites = dict['favorite_count']
		self.num_retweets = dict['retweet_count']
		self.id = dict['id_str']
		self.user_id = dict['user']['id_str']

	def set_movie(self, m):
		self.movie = m


#define a class called TwitterUser
#define __init__ such that it takes a dictionary representing a twitter user and stores the values as intance variables

#define class TwitterUser here:
#user_id, screen_name, num_favs
class TwitterUser(object):
	def __init__(self, dict):
		self.user_id = dict['id_str']
		self.screen_name = dict['screen_name']
		self.num_favorites = dict['favourites_count']
		

#create a list of three movie titles
movie_title_list = ['The Dark Knight', 'Django Unchained', 'Good Will Hunting']


#use get_omdb() on each movie title and accumulate the dictionaries into a list
movie_dict_list = []
for range in (0, 1, 2):
	movie_dict_list.append(get_omdb(movie_title_list[range]))



#use the list of dictionaries to accumulate a list of instances of Movie classes
movie_class_list = []
for range in (0, 1, 2):
	movie_class_list.append(Movie(movie_dict_list[range]))
	movie_class_list[range].set_movie_id(range)



#invoke get_tweets() for each movie title and accumulate a list of Tweet instances


tweet_class_list = []

for range in (0, 1, 2):
	tweets_dictionary = get_tweets(movie_class_list[range].title)
	tweets_list = tweets_dictionary['statuses']
	for tweet in tweets_list:
		temp = Tweet(tweet)
		temp.set_movie(movie_class_list[range].title)
		tweet_class_list.append(temp)


#invoke get_twitter_user() on each user in the neighborhood of the previous tweets. This means anybody who posted the tweet or was mentioned. Save this in a list of TwitterUser instances.
twitter_user_list = []

#find all users in the neighborhood
for range in (0, 1, 2):
	t = tweet_class_list[range]
	re_result = re.findall('\'screen_name\':\s\'([^\']+)', str(t))
	for user in re_result:
		twitter_user_list.append(user)
twitter_user_set = list(set(twitter_user_list))
print(twitter_user_set)

twitter_user_class_list = []
for user in twitter_user_set:
	temp = TwitterUser(get_twitter_user(user))
	twitter_user_class_list.append(temp)
a = get_tweets("The Dark Knight")
pp = pprint.PrettyPrinter(indent = 4)
print(type(a['statuses'][0]))



#now we have a list of twitter users in the neighborhood

######DATABASE TIME#########


#create a database file with the following three tables
#Tweets: Tweet text, Tweet ID (primary key), User (reference to user table), movie search (reference to movies table), number favorites, number retweets
#Users: User ID (Primary key), Screen Name, Num favorites made
#Movies: ID (primary key), Title, Director, num languages, IMDB rating, top billed actor

#Create database file here:
conn = sqlite3.connect('fp.db')
cur = conn.cursor()

#ADD MOVIE SEARCH
cur.execute('DROP TABLE IF EXISTS Tweets')
table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Tweets (tweet_id INTEGER PRIMARY KEY, '
table_spec += 'text TEXT, user_id TEXT, favorites INTEGER, retweets INTEGER)'
cur.execute(table_spec)

cur.execute('DROP TABLE IF EXISTS Users')
table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Users (user_id INTEGER PRIMARY KEY, '
table_spec += 'screen_name TEXT, num_favs INTEGER)'
cur.execute(table_spec)

cur.execute('DROP TABLE IF EXISTS Movies')
table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Movies (movie_id INTEGER PRIMARY KEY, '
table_spec += 'title TEXT, director TEXT, num_languages INTEGER, '
table_spec += 'imdb_rating INTEGER, top_actor TEXT)'
cur.execute(table_spec)

#Load data from the lists of class instances above into the database file

######LOAD TWEETS########
tweet_upload = []
for tweet in tweet_class_list:
	tweet_upload.append((tweet.id, tweet.text, tweet.user_id, tweet.num_favorites, tweet.num_retweets))
statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?)'

for t in tweet_upload:
	cur.execute(statement, t)

conn.commit()

#######LOAD USERS#######
user_upload = []
for user in twitter_user_class_list:
	user_upload.append((user.user_id, user.screen_name, user.num_favorites))
statement = 'INSERT INTO Users VALUES (?, ?, ?)'

for u in user_upload:
	cur.execute(statement, u)

conn.commit()

#######LOAD MOVIES######
movie_upload = []
for movie in movie_class_list:
	movie_upload.append((movie.movie_id, movie.title, movie.director, movie.num_languages, movie.rating, movie.actors[0]))
statement = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?)'

for m in movie_upload:
	cur.execute(statement, m)

conn.commit()


#Queries and Output



conn.close()
#####TESTS#####
#class Tests(unittest.TestCase):
#	def test_cache(self):
#		fstr = open("SI206_project3_cache.json","r").read()
#		self.assertTrue("umich" in fstr)
#	def test_get_tweets(self):
#	def test_get_twitter_user(self):
#	def test_get_omdb(self):
#	def test_movie_class(self):
#	def test_tweet_class(self):
#	def test_twitter_user_class(self):
#	def test_movie_titles(self):
#	def test(self):
































if __name__ == "__main__":
	unittest.main(verbosity=2)