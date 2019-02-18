from allennlp.predictors.predictor import Predictor
import pandas as pd
import spacy

import logging

PREDICTOR = None
NLP = None

#Given a dataframe, extract all named entites 

def loadSpacy(): 
    global NLP
    if NLP is None:
        NLP = spacy.load('en_core')
        return NLP
    else:
        return NLP

def loadAllenNlp():
    global PREDICTOR
    if PREDICTOR is None:
        PREDICTOR = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/ner-model-2018.12.18.tar.gz")
        return PREDICTOR
    else:
        return PREDICTOR



def spacyTagging(sents): # looks like spacy is able to recognize n-gram named entities
    nlp = loadSpacy()
    doc = nlp(sents)

    return [str(entity) for entity in doc.ents]

def spacyValues():
    entityDf = pd.DataFrame()
    for index, row in df.iterrows():
        currDf = spacyTagging(row['body'])
        entityDf = entityDf.append(currDf)
    print(entityDf['Entity'].value_counts())

"""
get candidate values from a corpus
"""
def extractCandidatesFromSent(sents):
    predictor = loadAllenNlp()
    pJson = predictor.predict(sents)
    zipFiltered = list(filter(lambda tup: tup[1] is not 'O', zip(pJson['words'],pJson['tags'])))
#[('Minca', 'B-LOC'), ('Ramen', 'L-LOC'), ('East', 'B-LOC'), ('Village', 'L-LOC'), ('Miso', 'U-MISC'), ('Ippudo', 'U-MISC'), ('Momofuku', 'U-MISC')]
    
    toBeConcat = [] #store locations of all 
    for i in range(len(zipFiltered)):
        if zipFiltered[i][1].startswith('L'):
            toBeConcat.append(i)

    toBeRmv = [] #remove from original individual phrases tuples with tags beginning with 'B' or 'L' [('Ramen', 'L-LOC'), ('Minca', 'B-LOC'), ('Village', 'L-LOC'), ('East', 'B-LOC')]
    updated = [] #create list with concated BIO [('Minca Ramen', 'LOC'), ('East Village', 'LOC')]
    
    #join together all identified discrete entites ex. B-LOC followed by I-LOC becomes one tuple with tag LOC
    for index in toBeConcat:
        if zipFiltered[index] not in toBeRmv: #skip inner I-Loc
            tmpRmv = [zipFiltered[index]]
            n = 1
            while (index - n) >= 0:
                if zipFiltered[index - n][1].startswith('L'):
                    tmpRmv.append(zipFiltered[index-n])
                elif zipFiltered[index - n][1].startswith('B'):
                    tmpRmv.append(zipFiltered[index-n])
                    break
                n = n+1
            f = ' '.join(tup[0] for tup in reversed(tmpRmv))
            s = tmpRmv[0][1].split('-')[1]
            toBeRmv.extend(tmpRmv)
            updated.append((f,s))
    
    zipFiltered = [tup for tup in zipFiltered if tup not in toBeRmv]
    zipFiltered.extend(updated)
    return zipFiltered

# break each comment into individual sentences
def tokenizeSentences(sents):
    import nltk
    return nltk.sent_tokenize(sents)


def freq_words(listOfWords, terms=30, show=False):
    from nltk import FreqDist
    import seaborn as sns
    import matplotlib.pyplot as plt

    fdist = FreqDist(listOfWords)
    dfobj = {'word': list(fdist.keys()), 'count': list(fdist.values())}
    words_df = pd.DataFrame(dfobj)

    data = words_df.nlargest(n=terms, columns='count')
    plt.figure(figsize=(20, 5))

    ax = sns.barplot(data=data, x='word', y='count')
    ax.set(ylabel='Count', autoscale_on=True)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    if show:
        plt.show()


def displayFreqDist(df):
    eList = df['extracted'].sum()
    # deTupled = [tup[0] for tup in eList]
    freq_words(listOfWords = eList, show=False)

def createExtractedColumn(df):
    df['extracted'] = df['body'].apply(lambda text: spacyTagging(text)) 
    # df['extracted'] = df['body'].apply(lambda text: extractCandidatesFromSent(text))
    

# df = pd.read_csv('../../data/nyc_ramen.csv')
# createExtractedColumn(df)
# print(df.to_json())

