import csv
from textblob import TextBlob
import os
try:
	from jupiter.sentient.aspect.models.model import ChiFinal,SentR
except Exception as e:
	from models.model import ChiFinal,SentR

provider="none"
survey_id="none"

filename = "Data/annotated_sentences_chi_final.csv"
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
		data = []
		filename="aspect/Data/annotated_sentences_chi_final.csv#"+survey_id+"#"+self.p

		with open(filename, "rt") as csvfile:	
			spamreader = csv.reader(csvfile)
		# spamreader=ChiFinal.objects(survey_id=self.sid)
			for row in spamreader:
				data.append(row)
		# print (data)
		# spamreader= ChiFinal.objects()
		# for row in spamreader:
		# 	data.append(row)

		number_of_sentences = len(data)

		# with open("Data/sentimentalreviews.csv", "w") as out_file:
		# 	writer = csv.writer(out_file)

		for i in range(1, number_of_sentences):
			# sentence = data[i][3]
			# sentence= data.sentences
			# print(sentence)
			# sentiment = get_sentiment(sentence)
			# #print("sent",sentiment)
			# line=[]
			
			# line = data[i]
			sentence = data[i][3]
			sentiment = get_sentiment(sentence)
			line = data[i]
			line.append(sentiment)
			# print ("line",line)
			SentR(provider=self.p,survey_id=survey_id,line=line).save()
			# writer.writerow(line)
		#print("Sentiment Done")
if __name__ == '__main__':
	
	Sentiment("1","2").run()