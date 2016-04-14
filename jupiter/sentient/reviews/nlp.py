from textblob import TextBlob
try:
	from jupiter.sentient.reviews.rake import Rake
	from jupiter.sentient.reviews.models.model import Reviews,WordCloudD
except:
	from rake import Rake
	from models.model import Reviews,WordCloudD
from collections import OrderedDict
from operator import itemgetter
class Senti(object):
	"""docstring for Senti"""
	def __init__(self, txt):
		self.t= txt
	def sent(self):
		blob = TextBlob(self.t)
		sentence_sentiment = blob.sentences[0].sentiment.polarity
		if sentence_sentiment > 0:
			return "Positive"
		if sentence_sentiment == 0:
			return "Neutral"
		if sentence_sentiment < 0:
			return "Negative"

class WordCloud(object):
	"""docstring for WordCloud"""
	def __init__(self,survey_id,provider):
		# self.f= stopword_filename
		self.sid= survey_id
		self.p= provider
	def collect_reviews(self):
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
		rake= Rake(stoppath)
		keywords= rake.run(text)
		wc= self.wc_to_dict(keywords)
		
		print (wc)
		# wc= rake_object(text).run()

		# wcd= WordCloudD(survey_id=self.sid,provider=self.p,wc=wc).save()
		# print (wc)
		

						
