import itertools
import nltk
from nltk import FreqDist
import pandas as pd
import numpy as np
import spacy
import gensim
from gensim import corpora

# visuals
import pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt
import seaborn as sns

# local
import processWord


def freq_words(texts, terms=30, show=False):

    all_words = ' '.join([text for text in texts])
    all_words = all_words.split()

    fdist = FreqDist(all_words)
    dfobj = {'word': list(fdist.keys()), 'count': list(fdist.values())}
    words_df = pd.DataFrame(dfobj)

    data = words_df.nlargest(n=terms, columns='count')
    plt.figure(figsize=(20, 5))

    ax = sns.barplot(data=data, x='word', y='count')
    ax.set(ylabel='Count', autoscale_on=True)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    if show:
        plt.show()


# nlp = process_word.initSpacy()


# normal = lambda comment: process_word.normalizeText(text = comment, remove_stopwords = True, remove_special_chars = True, lower_case_text = True)

# normal_with_lemma = lambda comment: process_word.normalizeText(text = comment, remove_stopwords = True, remove_special_chars = True, lower_case_text = True, lemmatize_text = True, nlp = nlp)

# df['bodyNormalized'] = df['body'].apply(normal)

# freq_words(df['bodyNormalized'])

def extract_candidate_chunks(text, grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'):
    import itertools
    import nltk
    import string
    import operator

    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize, POS-tag, and chunk using regular expressions
    chunker = nltk.chunk.regexp.RegexpParser(grammar)
    # get list of tagged sentences

    tagged_sents = [nltk.pos_tag(tokens=nltk.word_tokenize(sent))
                    for sent in nltk.sent_tokenize(text)]
    all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(
        chunker.parse(tagged_sent)) for tagged_sent in tagged_sents))
    # join constituent chunk words into a single chunked phrase

    grouped = itertools.groupby(all_chunks, lambda x: x[2] != 'O')
    for key, chunks in grouped:
        for chunk in chunks:
            print(chunk)
    # candidates = [' '.join(word for word, pos, chunk in group).lower() for key, group in itertools.groupby(all_chunks, keyfunction) if key]
    # return [cand for cand in candidates if cand not in stop_words and not all(char in punct for char in cand)]


def extract_candidate_words(text, good_tags=set(['NN', 'NNP', 'NNS', 'NNPS'])):
    import itertools
    import nltk
    import string

    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize and POS-tag words
    tagged_words = itertools.chain.from_iterable([nltk.pos_tag(
        tokens=nltk.word_tokenize(sent)) for sent in nltk.sent_tokenize(text)])

    # filter on certain POS tags and lowercase all words
    candidates = [word.lower() for word, tag in tagged_words
                  if tag in good_tags and word.lower() not in stop_words and not all(char in punct for char in word)]

    return candidates


def score_keyphrases_by_tfidf(texts):
    import gensim
    import nltk

    boc_texts = [extract_candidate_words(text) for text in texts]
    # make gensim dictionary and corpus
    dictionary = gensim.corpora.Dictionary(boc_texts)
    corpus = [dictionary.doc2bow(boc_text) for boc_text in boc_texts]
    # transform corpus with tf*idf model
    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    return corpus_tfidf, dictionary

# tfidfs, id2word = score_keyphrases_by_tfidf(body)


def csvToExtractedFreqDist(file, mute=True):
    df = pd.read_csv(file)
    body = df['body']

    def appFunc(txt): return extract_candidate_words(txt)
    df['candidateWords'] = df['body'].apply(appFunc)
    freq_words(df['candidateWords'].sum())
    return df


csvToExtractedFreqDist('data/headphone_recommend.csv')
