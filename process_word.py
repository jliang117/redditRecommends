import spacy
import pandas as pd
import numpy as np
import nltk
import re
from nltk.tokenize.toktok import ToktokTokenizer
from contractions import CONTRACTION_MAP
import unicodedata

LANG = 'english'
#nlp_vec = spacy.load('en_vecs', parse = True, tag=True, #entity=True)

def initSpacy():
	return spacy.load('en_core', parse=True, tag=True, entity=True)

def initTokenizer():
	return ToktokTokenizer()

def initStopwordList():
	#list contains possesive pronouse - how important to a recommendation i that
	stopword_list = nltk.corpus.stopwords.words(LANG)

	#retain comparative words
	stopword_list.remove('than')
	stopword_list.remove('more')

	#retain negative
	stopword_list.remove("mustn't")
	stopword_list.remove("don't")
	stopword_list.remove('no')
	stopword_list.remove('not')
	stopword_list.remove("wouldn't")
	stopword_list.remove("won't")
	return stopword_list

def removeAccentedChars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


def stripHtmlTags(text):
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text()
    return stripped_text

def expandContractions(text, contraction_mapping=CONTRACTION_MAP):
    
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

# print(expandContractions("test'ng that this'll work shouldn't it?"))

def removeSpecialCharacters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text

def stemText(text):
    ps = nltk.porter.PorterStemmer()
    text = ' '.join([ps.stem(word) for word in text.split()])
    return text


def lemmatizeText(text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text

def removeStopwords(text, is_lower_case = False): 
	tokenizer = initTokenizer()
	stopword_list = initStopwordList()
	tokens = tokenizer.tokenize(text)

	tokens = [token.strip() for token in tokens]
	if is_lower_case:
		filtered_tokens = [token for token in tokens if token not in stopword_list]
	else:
		filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
		filtered_text = ' '.join(filtered_tokens)
	return filtered_text

# print(removeStopwords("test have me please a the to their thing"))

def sentence_separation(text):
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	print('\n-----\n'.join(sent_detector.tokenize(text.strip())))


def normalize_corpus(corpus, expand_contractions = False, remove_stopwords = False, 
	remove_accented_chars = False, remove_special_chars = False, lower_case_text = False, lemmatize_text = False):
	normalized = []
	for doc in corpus:
		if remove_accented_chars:
			doc = removeAccentedChars(doc)
		if expand_contractions:
			doc = expandContractions(doc)
		if lower_case_text:
			doc = doc.lower()
		if lemmatize_text:
			doc = lemmatizeText(doc)
		if remove_special_chars:
			doc = removeSpecialCharacters(doc)
		if remove_stopwords:
			doc = removeStopwords(doc,lower_case_text)
		normalized.append(doc)
	return normalized

