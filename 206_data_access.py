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
		twitter_results = api.search(search_term)
		CACHE_DICTION[unique_identifier] = twitter_results 
		f = open(CACHE_FNAME,'w', encoding = 'utf-8') 
		f.write(json.dumps(CACHE_DICTION))
		f.close()
	return twitter_results

#function get_twitter_user() to get and cache data from twitter based on a twitter user
def get_user_tweets(user): #from project 4
	unique_identifier = "twitter_{}".format(user)

	if unique_identifier in CACHE_DICTION:
		print('using cached data for', user)
		twitter_results = CACHE_DICTION[unique_identifier]
	else:
		print('getting data from internet for', user)
		twitter_results = api.user_timeline(user, count = 100, include_rts = 1)
		if len(twitter_results) >= 20:
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
		CACHE_DICTION[unique_identifier] = omdb_results 
		f = open(CACHE_FNAME,'w', encoding = 'utf-8') 
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
	def __init__(self, title_in, director_in, actors_in, rating_in):
		self.title = title_in
		self.director = director_in
		self.actors = self.actors_in
		self.rating = self.rating_in
		self.num_languages = self.calc_num_languages()

	def __str__(self):
		return self.title + ' by ' + self.director + ' starring ' + self.actors

	def calc_num_languages(self):
		return len(self.actors)


#define a class called Tweet
#define __init__ such that it takes a dictionary representing a tweet and stores the values as instance variables

#define class Tweer here:
class Tweet(object):
	def __init__(self, dict):
		self.text = dict['text']


#define a class called TwitterUser
#define __init__ such that it takes a dictionary representing a twitter user and stores the values as intance variables

#define class TwitterUser here:

#create a list of three movie titles

#use get_omdb() on each movie title and accumulate the dictionaries into a list

#use the list of dictionaries to accumulate a list of instances of Movie classes

#invoke get_tweets() for each movie title and accumulate a list of Tweet instances

#invoke get_twitter_user() on each user in the neighborhood of the previous tweets. This means anybody who posted the tweet or was mentioned. Save this in a list of TwitterUser instances.

#create a database file with the following three tables
#Tweets: Tweet text, Tweet ID (primary key), User (reference to user table), movie search (reference to movies table), number favorites, number retweets
#Users: User ID (Primary key), Screen Name, Num favorites made
#Movies: ID (primary key), Title, Director, num languages, IMDB rating, top billed actor

#Create database file here:

#Load data from the lists of class instances above into the database file




#Queries and Output




#####TESTS#####
class Tests(unittest.TestCase):
	def test_cache(self):
		fstr = open("SI206_project3_cache.json","r").read()
		self.assertTrue("umich" in fstr)
	def test_get_tweets(self):
	def test_get_twitter_user(self):
	def test_get_omdb(self):
	def test_movie_class(self):
	def test_tweet_class(self):
	def test_twitter_user_class(self):
	def test_movie_titles(self):
	def test(self):
































if __name__ == "__main__":
	unittest.main(verbosity=2)