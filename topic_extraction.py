import nltk
from nltk import FreqDist

import pandas as pd
import numpy as np
import spacy
import gensim
from gensim import corpora

#visuals
import pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt
import seaborn as sns

#local
import process_word


df = pd.read_csv('data/nyc_ramen.csv')

def freq_words(x, terms = 30): 
	
	all_words = ' '.join([text for text in x])
	all_words = all_words.split()
	
	fdist = FreqDist(all_words)
	dfobj = {'word':list(fdist.keys()), 'count':list(fdist.values())}
	words_df = pd.DataFrame(dfobj)

	data = words_df.nlargest(n = terms, columns = 'count')
	plt.figure(figsize = (20,5))

	ax = sns.barplot(data = data, x = 'word', y = 'count')
	ax.set(ylabel = 'Count', autoscale_on = True)
	ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
	plt.show()

body = df['body'] # series of comments

# nlp = process_word.initSpacy()


# normal = lambda comment: process_word.normalizeText(text = comment, remove_stopwords = True, remove_special_chars = True, lower_case_text = True)

# normal_with_lemma = lambda comment: process_word.normalizeText(text = comment, remove_stopwords = True, remove_special_chars = True, lower_case_text = True, lemmatize_text = True, nlp = nlp)

# df['bodyNormalized'] = df['body'].apply(normal)

# freq_words(df['bodyNormalized'])

def extract_candidate_chunks(text, grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'):
    import itertools, nltk, string, operator
    
    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize, POS-tag, and chunk using regular expressions
    chunker = nltk.chunk.regexp.RegexpParser(grammar)
    #get list of tagged sentences

    tagged_sents = [nltk.pos_tag(tokens = nltk.word_tokenize(sent)) for sent in nltk.sent_tokenize(text)]
    all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent)) for tagged_sent in tagged_sents))
    # join constituent chunk words into a single chunked phrase


    grouped = itertools.groupby(all_chunks,lambda x: x[2] != 'O' )
    for key, chunks in grouped:
    	for chunk in chunks:
    		print(chunk)
    # candidates = [' '.join(word for word, pos, chunk in group).lower() for key, group in itertools.groupby(all_chunks, keyfunction) if key]
    # return [cand for cand in candidates if cand not in stop_words and not all(char in punct for char in cand)]

# print(extract_candidate_chunks(body[9]))

def extract_candidate_words(text, good_tags=set(['JJ','JJR','JJS','NN','NNP','NNS','NNPS'])):
    import itertools, nltk, string

    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize and POS-tag words
    tagged_words = itertools.chain.from_iterable([nltk.pos_tag(tokens = nltk.word_tokenize(sent)) for sent in nltk.sent_tokenize(text)])
    
                                                                    
    # filter on certain POS tags and lowercase all words
    # this originally was this horrible unreadable thing - chunk this
    candidates = [word.lower() for word, tag in tagged_words 
    if tag in good_tags and word.lower() not in stop_words and not all(char in punct for char in word)]

    return candidates

# print(extract_candidate_words(body[9]))

def score_keyphrases_by_tfidf(texts):
    import gensim, nltk
    
    boc_texts = [extract_candidate_words(text) for text in texts]
    # make gensim dictionary and corpus
    dictionary = gensim.corpora.Dictionary(boc_texts)
    corpus = [dictionary.doc2bow(boc_text) for boc_text in boc_texts]
    # transform corpus with tf*idf model
    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    
    return corpus_tfidf, dictionary

# tfidfs, id2word = score_keyphrases_by_tfidf(body)

import heapq
from operator import itemgetter
tfidfs, id2word = score_keyphrases_by_tfidf(body)

for idx, doc in enumerate(tfidfs):
	for wid,score in heapq.nlargest(10, doc, key = itemgetter(1)):
		print("{:0.3f}: {}".format(score, id2word[wid]))
		print("")

 

