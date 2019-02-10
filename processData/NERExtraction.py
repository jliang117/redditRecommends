from allennlp.predictors.predictor import Predictor
import pandas as pd
import spacy


PREDICTOR = None
NLP = None

df = pd.read_csv('../data/nyc_ramen.csv')

#Given a dataframe, extract all named entites and store as a dataframe

def loadSpacy():
    global NLP
    if NLP is None:
        NLP = spacy.load('en_core')
        return NLP
    else:
        return NLP

def createPredictor():
    global PREDICTOR
    if PREDICTOR is None:
        PREDICTOR = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/ner-model-2018.12.18.tar.gz")
        return PREDICTOR
    else:
        return PREDICTOR



def spacyTagging(sents):
    nlp = loadSpacy()
    doc = nlp(sents)
    return pd.DataFrame({
    'Entity': [str(entity) for entity in doc.ents],
    'Label': [entity.label_ for entity in doc.ents]
    })


def spacyValues():
    entityDf = pd.DataFrame()
    for index, row in df.iterrows():
        currDf = spacyTagging(row['body'])
        entityDf = entityDf.append(currDf)
    print(entityDf['Entity'].value_counts())

"""
get candidate values from a list of sentences
"""
def extractCandidatesFromSent(sents):
    predictor = createPredictor()
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


print(extractCandidatesFromSent("My favorite hole-in-the-wall is Minca Ramen in East Village. They have, I believe, a peanut based broth for their Miso that's very good. It's far more quaint than an Ippudo or Momofuku. "))

# print(spacyTagging("My favorite hole-in-the-wall is Minca Ramen in East Village. They have, I believe, a peanut based broth for their Miso that's very good. It's far more quaint than an Ippudo or Momofuku. ").head())

# break each comment into individual sentences
def tokenizeSentences(sents):
    import nltk
    return nltk.sent_tokenize(sents)

#creates column with a list of sentences





