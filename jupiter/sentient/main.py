from jupiter.sentient.aspect.reviewProcessing import ReviewP
from jupiter.sentient.aspect.sentimental import Sentiment
from jupiter.sentient.aspect.aspectratings import AspectR
from jupiter.sentient.reviews.trippool import TripAdvisor
try:
	from jupiter.sentient.reviews.zomatopool import Zomato
except:
	from sentient.reviews.zomatopool import Zomato
from jupiter.sentient.reviews.nlp import WordCloud
verbose= True
class Sentient(object):
	"""docstring for Sentient"""
	def __init__(self,url,survey_id,provider):
		self.u=url
		self.sid= survey_id
		self.p= provider
	def scrap_data(self):
		if "zomato.com" in self.u:
			# self.p= "zomato"
			Zomato(self.u,self.sid).get_data()
			print("zomato")
		if "tripadvisor" in self.u:
			# self.p="tripadvisor"
			TripAdvisor(self.u,self.sid).get_data()
			print("tripadvisor")
	def wordcloud(self):
		WordCloud(self.sid,self.p).wc()
	def run_ml(self):
		ReviewP(self.sid,self.p).run()
		Sentiment(self.sid,self.p).run()
		AspectR(self.sid,self.p).run()
	def run(self):
		if verbose:print ("Starting Scraping")
		self.scrap_data()
		if verbose:print("Starting WordCloud")
		self.wordcloud()
		if verbose: print("Running ML")
		self.run_ml()
		print("Done")
if __name__ == '__main__':
	url= "https://www.zomato.com/ncr/purani-dilli-restaurant-zakir-nagar-new-delhi"
	url="https://www.tripadvisor.in/Restaurant_Review-g1162523-d4009998-Reviews-The_Beer_Cafe-Kirtinagar_Uttarakhand.html"
	survey_id="djxLoj855WwprrpAvXw"
	provider="tripadvisor"
	Sentient(url,survey_id,provider).run()
	