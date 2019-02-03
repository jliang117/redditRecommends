import praw
from google import google
import pandas as pd

import processWord

DATA_DIR = 'data/'

PAGE_LIMIT = 1
SEARCH_REDDIT = ' site:reddit.com'

# TODO REMOVE ON COMMIT - also find a more automatic solution


#global vars for csv column names
AUTHOR = 'author'
BODY = 'body'
CREATED = 'created_utc'
PERMALINK = 'permalink'
SUBREDDIT = 'subreddit'
SCORE = 'score'


def initRedditClient():
	return praw.Reddit(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,user_agent=USER_AGENT)


def extractCommentsFromSearch(searchString, googlePageLimit = 1, commentDepth = None):
	
	commentList = []
	reddit = initRedditClient()
	search_results = google.search(searchString, googlePageLimit)

	for result in search_results:
		try:
			submission = reddit.submission(url=result.link)
			submission.comments.replace_more(limit=commentDepth)
			for comment in submission.comments.list():
				if(filterCommentForRelevancy(comment)):
					buildRow = [{
						AUTHOR:comment.author,
						BODY:comment.body,
						CREATED:comment.created_utc,
						SCORE:comment.score,
						PERMALINK:comment.permalink,
						SUBREDDIT:comment.subreddit
						}]
					commentList.extend(buildRow)
		except praw.exceptions.ClientException as e:
			print("Google search returned non submission:" + result.link)

	df = pd.DataFrame(commentList)
	df = df[[AUTHOR, BODY, CREATED, SCORE, PERMALINK, SUBREDDIT]]
	
	return df

def normalizeComment(sent):
	sent = processWord.expandContractions(sent)
	sent = processWord.removeStopwords(sent)
	return sent

def filterCommentForRelevancy(comment):
	return True
	#potentially do preprocessing here as well


#move this to separate dataframe insights script? or create two classes, commentExtractor and dfData?

def readDf(file):
	try:
		df = pd.read_csv(file)
		return df
	except IOError as e:
		print(file + " cannot be read")
		sys.exit()

def getTopScoring(file, n = 5):
	df = readDf(file)
	return df.nlargest(n = n, columns = SCORE)

def getSubbreddits(file):
	df = readDf(file)
	return df[SUBREDDIT].value_counts()


df = extractCommentsFromSearch("nyc ramen" + SEARCH_REDDIT)
df.to_csv(DATA_DIR+'nyc_ramen.csv',index = False, encoding = 'utf-8')

#Usage examples

print(getTopScoring(file = DATA_DIR + 'nyc_ramen.csv', n = 10 )['body'])

print(getSubbreddits(file = DATA_DIR + 'nyc_ramen.csv'))

