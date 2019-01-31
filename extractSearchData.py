import praw
from google import google
import pandas as pd

import process_word

DATA_DIR = 'data/'

PAGE_LIMIT = 1
SEARCH_REDDIT = ' site:reddit.com'

# TODO REMOVE ON COMMIT - also find a more automatic solution


reddit = praw.Reddit(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,user_agent=USER_AGENT)

def initRedditClient():
	return praw.Reddit(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,user_agent=USER_AGENT)


def extractCommentsFromSearch(searchString, googlePageLimit = 1, commentDepth = None):
	author = 'author'
	body = 'body'
	created = 'created_utc'
	permalink = 'permalink'
	subreddit = 'subreddit'

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
						author:comment.author,
						body:comment.body,
						created:comment.created_utc,
						permalink:comment.permalink,
						subreddit:comment.subreddit
						}]
					commentList.extend(buildRow)
		except praw.exceptions.ClientException as e:
			print("Google search returned non submission:" + result.link)

	df = pd.DataFrame(commentList)
	df = df[[author, body, created, permalink, subreddit]]
	
	return df

def normalizeComment(sent):
	sent = process_word.expandContractions(sent)
	sent = process_word.removeStopwords(sent)
	return sent

def filterCommentForRelevancy(comment):
	return True
	#potentially do preprocessing here as well



df = extractCommentsFromSearch("nyc ramen" + SEARCH_REDDIT)
df.to_csv(DATA_DIR+'nyc_ramen.csv',index = False, encoding = 'utf-8')

