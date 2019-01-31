# redditRecommends
aggregating reddit comments and employing NLP to sift through various recommendations

## Idea and feature set:

I frequently find myself googling "best \<insert item type, restaurant, thing to do here\> reddit" and so to expedite that, I made something useful to aggregate google results of reddit comments and do some natural language processing to return top results.

So, when I'm using reddit to search for testimonials or recommendations on a topic, I want to know what reddit thinks - how will I ask it questions (as in what forms of questions are possible)?

Given the prompt - `What does reddit think about ___`? A few very simple question structures come to mind:

`Food/Activity/Thing` **IN** `Place` ex. `Ramen in Nyc` - yields places, landmarks, restaurants

`Superlative` `Object` ex. `Best 4k TV` - yields objects, links, shopping sites

Let's focus on the first structure for now.


**Fetch data**

(using https://github.com/abenassi/Google-Search-API) and praw (https://github.com/praw-dev/praw)


**Normalization**

using nltk - https://github.com/nltk/nltk

**Sentence Segmentation**

This is to be implemented in a way that retains and tracks the information of the whole comment, as some
recommendations are multiple sentences where the proper noun being referred to is in one of the beginning sentences. Ex:

>"Naruto Ramen. Very small, cash only (IIRC), but great portions, great broth, great noodles, and great bowls. Go during lunch for some nice specials. "


# Usage

Currently in the middle of messing with things, but searching is basically the `extractCommentsFromSearch` method in `extractSearchData.py`, and data extraction and visualization is `csvToExtractedFreqDist` in `topicExtraction.py`

Updating for usability will come later...

# Output

Currently we get back a frequency distribution with `30` terms plotted using `freq_words` in `topicExtraction.py`. An example when searching for `nyc ramen`:

![Adjectives included](/img/freqDistExtracted.png)

The set of tagged words extracted can be tweaked in `extract_candidate_words`, the default set includes adjectives and looks like: (from https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)

`['JJ','JJR','JJS','NN','NNP','NNS','NNPS']`

Removing adjectives yields a better list specific to this kind of search, and so the frequency distribution gives you a few more places:

![Adjectives NOT included](/img/freqDistNonAdj.png)


