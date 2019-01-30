# redditRecommends
aggregating reddit comments and employing NLP to sift through various recommendations

## Idea and feature set:

I frequently find myself googling "best <insert thing> reddit" and so to expedite that, I figured I'd make a tool
to aggregate google results of reddit comments and do some natural language processing to return top results.

The pipeline sort of looks like this:

**Input**: 

simple search query - it was initially going to be **Place** and **Action**, as in *NYC* and *eat ramen*, 
but clearly other usages such as online shopping recommendations do **not** include a place. 

So at the moment, we let google take care of figuring out the intent of a user's search, but I imagine there would be
better results by requiring more specificity on inputs and then subsequently being able to tweak the results processing based
on those inputs.


**Fetch data**

(using https://github.com/abenassi/Google-Search-API) and praw (https://github.com/praw-dev/praw)


**Normalization**

using nltk - https://github.com/nltk/nltk

**Sentence Segmentation**

This is to be implemented in a way that retains and tracks the information of the whole comment, as some
recommendations are multiple sentences where the proper noun being referred to is in one of the beginning sentences. Ex:

>"Naruto Ramen. Very small, cash only (IIRC), but great portions, great broth, great noodles, and great bowls. Go during lunch for some nice specials. "

**Named Entity Recognition**

using spacy - https://spacy.io/usage/spacy-101#annotations-ner

This also needs exploration, but the idea is that a top-level comment will have one, if not more referrals mentioned.
These referrals would then get tagged and extracted where frequency and sentiment can then also be calculated?
