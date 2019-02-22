import pandas as pd
import spacy


NLP = None

#Given a dataframe, extract all named entites 

def loadSpacy(): 
    global NLP
    if NLP is None:
        NLP = spacy.load('en')
        return NLP
    else:
        return NLP



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

# break each comment into individual sentences
def tokenizeSentences(sents):
    import nltk
    return nltk.sent_tokenize(sents)


def createExtractedColumn(df):
    df['extracted'] = df['body'].apply(lambda text: spacyTagging(text)) 
 
