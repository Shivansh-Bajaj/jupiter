from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import csv
try:
	from jupiter.sentient.reviews.stop_words import stops
except:
	from reviews.stop_words import stops


class KeywordCount(object):
	def __init__(self):
		self.stopwords_list = stops

	def run(self, text):
		cv = CountVectorizer(min_df=0, stop_words=self.stopwords_list, max_features=20, analyzer = 'word', ngram_range = (1,4))

		counts = cv.fit_transform([text]).toarray().ravel()
		words = np.array(cv.get_feature_names()) 
		# normalize
		counts = counts / float(counts.max())
		final = []
		for i in range(0, len(counts)):
			final.append((words[i], counts[i]))
		return final