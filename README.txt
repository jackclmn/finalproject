README

Project 2

What This Project Does:
	-This Project gathers and caches data from Twitter and OMDB and loads it into a database.
	-It then performs queries on the database to output a file with summary statistics on three movies.

How To Run It:
	-When in the correct directory, enter "python 206_final_project.py" to run the file

Dependencies:
	-You must have a twitter-info.py file with twitter api credentials
	-You must also have sqlite3

Files:
	-206_final_project.py
		-The file you run to execute the code
	-README.txt
		-This file with documentation
	-fp.db
		-A database file that stores information on Movies, Tweets, and Twitter Users
	-SI206_final_cache.json
		-A cache file that holds data gathered from the internet from Twitter and OMDB



Functions:

get_tweets()
	-This function takes a query and checks whether that query has been cached or not. It will either
	return the cached data as a dictionary or gather it from the twitter api.

get_twitter_user()
	-This function takes a Twitter user's screenname and returns a dictionary with information about
	the user either from the cache or from the twitter api.

get_omdb()
	-This function takes a movie title as input and returns a dictionary with information about
	the movie either from the cache or the OMDB api.



Classes:

Movie
	-This class represents an instance of a Movie. It stores the information gathered from OMDB.
	__init__
		-This takes a dictionary returned from get_omdb() and stores select information as instance
		variables.
	__str__
		-This returns a string describing the movie
	calc_num_languages
		-This calculates the number of languages and sets it as an instance variable
	set_movie_id
		-This sets the movie id as an instance variable to be used in the database

Tweet
	-This class represents an instance of a Tweet and stores tweet information from the twitter api
	__init__
		-This takes a dictionary returned from get_tweets() and stores select information as instance variables
	set_movie
		-This sets the movie id relating to the tweet to be used later in the database

TwitterUser
	-This class represents an instance of a twitter user and stores user information from the twitter api
	__init__
		-This takes a dictionary returned from get_twitter_user() and stores select information
		as instance variables



Database:

Movies
	-Each row in this table represents a movie
	-The attributes are (movie_id, title, director, num_languages, imdb_rating, top_actor)

Tweets
	-Each row in this table represents a tweet
	-The attributes are (tweet_id, text, user_id (reference to Users table), favorites, retweets, 
	movie_id (reference to Movies table))

Users
	-Each row in this table represents a twitter user
	-The attributes are (user_id, screen_name, favorites)



Data Manipulation:

Set Comprehension (line 191)
	-This creates a list of usernames without duplicates for processing into the database

Dictionary Comprehension 1
	-This provides the number of tweets about each movie

Dictionary Comprehension 2
	-This provides the number of favorites from tweets about each movie

Sorting with Key Parameter
	-This sorts the tweets by most favorites and outputs a list of them



SI 206 Specifics:

Line(s) on which each of your data gathering functions begin(s): 36, 53, 69
Line(s) on which your class definition(s) begin(s): 97, 121, 138
Line(s) where your database is created in the program: 214-235
Line(s) of code that load data into your database: 240-270
Line(s) of code (approx) where your data processing code occurs — where in the file can we see all the processing techniques you used? 191, 275-314
Line(s) of code that generate the output: 275-314
OK to be approximate here — ok if it ends up off by 1 or 2. Make it easy for us to find!





















