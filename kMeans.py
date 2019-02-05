from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import pandas as pd
import nltk

df = pd.read_csv('data/ramen_normalized.csv')


ramendocs = df['body']


def stem(text):
    from nltk.stem.snowball import SnowballStemmer
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(text)]
    stemmer = SnowballStemmer('english')
    return [stemmer.stem(t) for t in tokens]

vectorizer = TfidfVectorizer(stop_words='english', ngram_range= (1,4))
X = vectorizer.fit_transform(ramendocs)

true_k = 10
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=500, n_init=1)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print

print("\n")
print("Prediction")

