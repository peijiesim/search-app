import os
import re
import codecs
import pickle

from nltk.stem.porter import PorterStemmer
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

class SearchEngine:

	def __init__(self):
		self.corpusDir = './static/gutenberg'
		self.filenames_ = os.listdir(self.corpusDir)
		self.stopwords = open('stopwords.txt', 'r').read().split()
		self.stemmer = PorterStemmer()
		self.count = CountVectorizer()
		self.tfidf = TfidfVectorizer(min_df=1)
		self.buildIndex()

	def buildIndex(self):
		self.index= []
		for filename in self.filenames_:
			with codecs.open(os.path.join(self.corpusDir, filename), "r", encoding='utf-8', errors='ignore') as f:
				tokens = f.read().lower().split()
				cleaned = ''
				# cleaned = self.normalize(filename)
				for token in tokens:
					cleaned += self.normalize(token) + ' '
				self.index.append(cleaned)
		self.index = np.array(self.index)
		self.index = self.tfidf.fit_transform(self.index).toarray()

	def normalize(self, token):
		pattern = re.compile('[\W]+')
		token = pattern.sub('', token)
		if not token or token in self.stopwords:
			return ''
		return self.stemmer.stem(token)

	def getKMostRelevantDocs(self, queryVector, k):
		res = self.index.dot(np.reshape(queryVector, (queryVector.shape[1], 1))).flatten()
		topKDocs = res.argsort()[-k:][::-1]
		# allDocs = res.argsort()[::-1]
		files = []
		for d in topKDocs:
			file = self.filenames_[d]
			with codecs.open(os.path.join(self.corpusDir, file), "r", encoding='utf-8', errors='ignore') as f:
				content = f.read()[0:250] # display the first 250 characters of the relevant documents
				files.append((file, content, res[d]))
		return files

	def query(self, text, k=10):
		inputTokens = [self.normalize(word) 
						for word in text.lower().split()]
		query = ' '.join(token for token in inputTokens)
		queryVector = self.tfidf.transform(np.array([query])).toarray()
		return self.getKMostRelevantDocs(queryVector, k)

search = SearchEngine()
# f = open('index.pkl', 'wb')
# pickle.dump(search, f)
