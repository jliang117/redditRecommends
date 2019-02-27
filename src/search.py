import sys
import json

# external
import praw
from googleSearcher import google
import pandas as pd
from loguru import logger

# local
import commentfilter
import spacyner

PAGE_LIMIT = 1
SEARCH_REDDIT = ' site:reddit.com'

# TODO REMOVE ON COMMIT - also find a more automatic solution

# global vars for csv column names
AUTHOR = 'author'
BODY = 'body'
CREATED = 'created_utc'
PERMALINK = 'permalink'
SUBREDDIT = 'subreddit'
SCORE = 'score'


def initRedditClient():
    logger.add("log/file_{time}.log", level="TRACE", rotation="100 MB")
    return praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)


def extractCommentsFromSearch(searchString, googlePageLimit=1, commentDepth=None):

    commentList = []
    reddit = initRedditClient()
    search_results = google.search(searchString, googlePageLimit)

    for result in search_results:
        logger.debug(result)
        try:
            submission = reddit.submission(url=result.link)
            submission.comments.replace_more(limit=commentDepth)
            for comment in submission.comments.list():
                if(filterCommentForRelevancy(comment)):
                    if len(comment.body) > 3:
                        if comment.author is not None:
                            redditName = comment.author.name
                        else:
                            redditName = ''
                        subRedditName = comment.subreddit.display_name
                        buildRow = [{
                            AUTHOR: redditName,
                            BODY: comment.body,
                            CREATED: comment.created_utc,
                            SCORE: comment.score,
                            PERMALINK: comment.permalink,
                            SUBREDDIT: subRedditName}]
                        logger.debug(f'Adding comment {buildRow}')
                        commentList.extend(buildRow)
        except praw.exceptions.ClientException:
            print("Google search returned non submission:" + result.link)

    df = pd.DataFrame(data=commentList)

    return df


def normalizeComment(sent):  #NER should retain original comment
    sent = commentfilter.expandContractions(sent)
    sent = commentfilter.removeSpecialCharacters(sent)
    sent = commentfilter.removeStopwords(sent)
    return sent


def filterCommentForRelevancy(comment):
    return True
    # potentially do preprocessing here as well


# move this to separate dataframe insights script? or create two classes, commentExtractor and dfData?

def readDf(file):
    try:
        df = pd.read_csv(file)
        return df
    except IOError as e:
        print(file + " cannot be read")
        sys.exit()


def getTopScoring(file, n=5):
    df = readDf(file)
    return df.nlargest(n=n, columns=SCORE)


def getSubbreddits(file):
    df = readDf(file)
    return df[SUBREDDIT].value_counts()


def sanitize(value):

    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    """
    import re
    re.sub('[^\w\-_\. ]', '_', value)
    value = value.replace(" ", "_")
    logger.debug(f'Saving file with sanitized name: {value}')
    return value


def searchAndExtract(argv):
    logger.info(f'Search string: {argv}')
    df = extractCommentsFromSearch(argv + SEARCH_REDDIT)
    logger.info('Creating extracted column...')
    spacyner.createExtractedColumn(df)
    filename = sanitize(argv)
    path = f"data/tmp/{filename}.json"
    df.to_json(path)
    logger.info('Returning jsonified dataframe')
    # path = f"data/tmp/ramen_nyc.json" #temp
    return pd.read_json(path_or_buf=path).to_json()
