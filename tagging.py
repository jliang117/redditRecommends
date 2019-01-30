import spacy
from spacy import displacy
import pandas as pd
"""
local
"""
from chunker import NGramTagChunker
import process_word



nlp = spacy.load('en_core', parse=True, tag=True, entity=True)
#nlp_vec = spacy.load('en_vecs', parse = True, tag=True, #entity=True)

ramen_df = pd.read_csv('nyc_ramen_normalized.csv')

#build tagged sentences
sentence = str(ramen_df.iloc[9].body)
sentence_nlp = nlp(sentence)

print(sentence_nlp)

print([(word,word.ent_type_) for word in sentence_nlp if word.ent_type_])

# displacy.render(sentence_nlp, style='ent', jupyter=True)
# POS tagging with Spacy 
# spacy_pos_tagged = [(word, word.tag_, word.pos_) for word in sentence_nlp]
# spacy_tag_df = pd.DataFrame(spacy_pos_tagged, columns=['Word', 'POS tag', 'Tag type'])

# POS tagging with nltk
# nltk_pos_tagged = nltk.pos_tag(sentence.split())
# nltk_tag_df = pd.DataFrame(nltk_pos_tagged, columns=['Word', 'POS tag'])

# ntc = build_model_chunker()
# print(ntc.parse(nltk_pos_tagged))






	