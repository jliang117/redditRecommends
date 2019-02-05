from allennlp.predictors.predictor import Predictor
import pandas as pd


 

def createPredictor():
	return Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/ner-model-2018.12.18.tar.gz")

df = pd.read_csv('data/nyc_ramen.csv')

def extractCandidatesFromSent(sent):
	predictor = createPredictor()
	pJson = predictor.predict(sent)
	d = dict(zip(pJson['words'],pJson['tags']))
	print(d)
	d = {k:v for k,v in d.items() if v is not 'O'}
	print(d)
	return d

extractCandidatesFromSent(df['body'][0])

