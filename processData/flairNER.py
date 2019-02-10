from flair.data import Sentence
from flair.models import SequenceTagger
import pandas as pd

# make a sentence
sentence = Sentence('I love Berlin .')

# load the NER tagger
tagger = SequenceTagger.load('ner')

# run NER over sentence
tagger.predict(sentence)

print(sentence.to_tagged_string())

from flair.embeddings import FlairEmbeddings, WordEmbeddings, StackedEmbeddings,BertEmbeddings

embedList = [WordEmbeddings('en-crawl'), FlairEmbeddings('multi-forward'),BertEmbeddings()]
stackedEmbed = StackedEmbeddings(embedList)

