import spacy
import wmd

nlp = spacy.load('en_core')
nlp.add_pipe(wmd.WMD.SpacySimilarityHook(nlp), last=True)
doc1 = nlp("brooklyn is a part of nyc")
doc2 = nlp("new york city has many boroughs")
print(doc1.similarity(doc2))