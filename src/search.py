import sys
import json
import re

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
CLIENT_ID = 'TGx9s4azwjK2wQ'
CLIENT_SECRET = 'C39wISck0di0SdxYBQLbqeFTwCo'
USER_AGENT = 'script:redditRecommends:v0.0.1 (by /u/coldbumpysparse)'

GOOGLE_PAGE_LIM = 1

# global vars for csv column names
AUTHOR = 'author'
BODY = 'body'
CREATED = 'created_utc'
PERMALINK = 'permalink'
SUBREDDIT = 'subreddit'
SCORE = 'score'

# match on reddit links only
LINK_REGEX = 'www\.reddit\.(com)\/(.?)'


def initRedditClient():
    logger.add("log/file_{time}.log", level="TRACE", rotation="100 MB")
    return praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)


def getGoogleResultsFromSearch(searchString, googlePageLimit=GOOGLE_PAGE_LIM):
    return google.search(searchString, googlePageLimit)


def convertSearchResultsToDataframe(googleResults):
    reddit = initRedditClient()
    resultLinkData = []
    for result in googleResults:
        if isValidLink(result):
            resultLinkData.extend(convertResultToData(result, reddit))
    return pd.DataFrame(data=resultLinkData)


def isValidLink(result):
    if re.search(LINK_REGEX, result.link) is None:
        logger.warn(f'bad link averted:{result.link}')
        return False
    return True


def convertResultToData(result, reddit):
    resultData = []
    logger.debug(f'Getting comments from link:{result.link}')
    try:
        submission = reddit.submission(url=result.link)
        submission.comments.replace_more()
        for comment in submission.comments.list():
            if(filterCommentForRelevancy(comment)):
                resultData.extend(buildRowFromComment(comment))
    except praw.exceptions.ClientException:
        logger.warn("Google search returned non submission:" + result.link)
    return resultData


def buildRowFromComment(comment):
    redditName = checkCommentAuthor(comment)
    subredditName = comment.subreddit.display_name
    builtRow = [{
        AUTHOR: redditName,
        BODY: comment.body,
        CREATED: comment.created_utc,
        SCORE: comment.score,
        PERMALINK: comment.permalink,
        SUBREDDIT: subredditName}]
    return builtRow


def checkCommentAuthor(comment):
    return comment.author.name if comment.author is not None else ''


def normalizeComment(sent):  # NER should retain original comment
    sent = commentfilter.expandContractions(sent)
    sent = commentfilter.removeSpecialCharacters(sent)
    sent = commentfilter.removeStopwords(sent)
    return sent


def filterCommentForRelevancy(comment):
    return len(comment.body) > 3
    # potentially do preprocessing here as well


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
    googleResults = getGoogleResultsFromSearch(argv + SEARCH_REDDIT)
    df = convertSearchResultsToDataframe(googleResults)
    logger.info('Creating extracted column...')
    spacyner.createExtractedColumn(df)
    json = df.to_json()
    return json
