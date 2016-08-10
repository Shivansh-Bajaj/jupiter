import csv
from textblob import TextBlob
import os

from jupiter.sentient.aspect.models.model import ChiFinal,SentR,AnnotationSentences


provider="none"
survey_id="none"

filename = "jupiter/sentient/Data/annotated_sentences_chi_final.csv"
def get_sentiment(text):
	blob = TextBlob(text)
	sentence_sentiment = blob.sentences[0].sentiment.polarity
	if sentence_sentiment > 0:
		return "Positive"
	if sentence_sentiment == 0:
		return "Neutral"
	if sentence_sentiment < 0:
		return "Negative"


class Sentiment():
	"""docstring for Sentiment"""
	def __init__(self,survey_id,provider):
		self.sid= survey_id
		self.p= provider
	def run(self):
		if isinstance(self.sid,list):
			survey_id= self.sid[0]
		else:survey_id=self.sid
		#data = []
		data=AnnotationSentences.objects(survey_id=survey_id,provider=self.p)
		print("sentence /////////////////")
		number_of_sentences = 0
		# with open("Data/sentimentalreviews.csv", "w") as out_file:
		# 	writer = csv.writer(out_file)
		SentR.objects(provider=self.p,survey_id=survey_id).delete()
		for element in data:
			# sentence = data[i][3]
			# sentence= data.sentences
			# print(sentence)
			# sentiment = get_sentiment(sentence)
			# #print("sent",sentiment)
			# line=[]
			
			# line = data[i]
			sentence = element.original
			sentiment = get_sentiment(sentence)
			line = [number_of_sentences,element.RID,element.aspect,element.original,element.sentences]
			line.append(sentiment)
			# print ("line",line)
			# print ("Saving SentR",survey_id)
			print(line)
			SentR(provider=self.p,survey_id=survey_id,line=line).save()
			number_of_sentences=number_of_sentences+1	
			# writer.writerow(line)
		#print("Sentiment Done")
if __name__ == '__main__':
	
	Sentiment("1","2").run()
