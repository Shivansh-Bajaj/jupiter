from textblob import TextBlob
try:
	from jupiter.sentient.reviews.rake import Rake
	from jupiter.sentient.reviews.models.model import Reviews,WordCloudD
	from jupiter.sentient.reviews.keywordcount import KeywordCount
except:
	from reviews.rake import Rake
	from reviews.models.model import Reviews,WordCloudD
	from reviews.keywordcount import KeywordCount
from collections import OrderedDict
from operator import itemgetter

class Senti(object):
	"""docstring for Senti"""
	def __init__(self, txt):
		self.t= txt
	def sent(self, overall_rating):
		# blob = TextBlob(self.t)
		# sentence_sentiment = blob.sentences[0].sentiment.polarity
		# if sentence_sentiment > 0:
		# 	return "Positive"
		# if sentence_sentiment == 0:
		# 	return "Neutral"
		# if sentence_sentiment < 0:
		# 	return "Negative"
		overall_rating = float(overall_rating)
		if overall_rating > 3.2:
			return "Positive"
		if overall_rating >= 2.8 or overall_rating <= 3.2:
			return "Neutral"
		if overall_rating < 2.8:
			return "Negative"

class WordCloud(object):
	"""docstring for WordCloud"""
	def __init__(self,survey_id,provider):
		# self.f= stopword_filename
		self.sid= survey_id
		self.p= provider
	def collect_reviews(self):
		if isinstance(self.sid,list):

			if self.p=="all":
				reviews= Reviews.objects(survey_id__in=self.sid)
			else:
				reviews= Reviews.objects(survey_id__in=self.sid,provider=self.p)
		else:
			if self.p=="all":
				reviews= Reviews.objects(survey_id=self.sid)
			else:
				reviews= Reviews.objects(survey_id=self.sid,provider=self.p)
		text=""
		for i in reviews:
			text+=i.review
		return text
	def wc_to_dict(self,alist):
		v= 10
		alist=alist[0:v]
		adict={}
		for i in alist:
			adict[i[0]]=i[1]
	
		return adict
	def wc(self):
		"""
		"""
		stoppath="jupiter/sentient/reviews/models/stopwords.txt"

		text= self.collect_reviews()
		# rake= Rake(stoppath)
		# keywords= rake.run(text)
		keywordcounts = KeywordCount()
		keywords = keywordcounts.run(text)

		wc= self.wc_to_dict(keywords)
		
		print (wc)
		if len(wc)!=0:
		# wc= rake_object(text).run()
			if isinstance(self.sid,list):
				wcd= WordCloudD(survey_id=self.sid[0],provider=self.p,wc=wc).save()
			else:wcd= WordCloudD(survey_id=self.sid,provider=self.p,wc=wc).save()
		# print (wc)
		

						
