import requests
import json
from urllib.request import urlopen

from bs4 import BeautifulSoup
from multiprocessing import Pool
try:
	from jupiter.sentient.reviews.models.model import Reviews,Scraped,Record
	from jupiter.sentient.reviews.nlp import Senti
	from jupiter.sentient.models.model import Status
except:
	from models.model import Reviews,Scraped,Record
	from nlp import Senti
"""from 
VARIABLES
"""
header={
		'Accept':'*/*',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'en-US,en;q=0.5',
		'Content-Length':'58',
		'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
		'Cookie':'PHPSESSID=6663f1bf4c02fcee51337d06c659a5965a67e86e; zl=en; fbtrack=23c5065fe3531defdf8ef5ea5b592bad; fbcity=1; dpr=1; __utmt=1; __utmt_t3=1; __utmt_t7=1; __utmt_t4=1; __jpuri=https%3A//www.zomato.com/ncr/panama-peppers; __utma=141625785.2004000331.1460409387.1460409387.1460409387.1; __utmb=141625785.16.10.1460409387; __utmc=141625785; __utmz=141625785.1460409387.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.2004000331.1460409387',
		'dnt':1,
		'Host':'www.zomato.com',
		'Referer':'https://www.zomato.com/ncr/fork-you-hauz-khas-village-delhi/reviews',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
		'X-NewRelic-ID':'VgcDUF5SGwEDV1RWAgg=',
		'X-Requested-With':'XMLHttpRequest',

		}
url='https://www.zomato.com/php/social_load_more.php'
class Zomato(object):
	"""docstring for Zomato"""
	def __init__(self,url,survey_id,provider="zomato"):
		self.url= url
		self.sid= survey_id
	def get_total(self):
		response= urlopen(self.url).read()
		soup=BeautifulSoup(response)
		total= soup.find('a',{'data-sort':'reviews-dd'}).find("span").text
		return int(total)


	def get_id(self):
		response= urlopen(self.url).read()
		soup=BeautifulSoup(response)
		rid= int(soup.find('body')['itemid'])
		# total= soup.find('a',{'data-sort':'reviews-dd'}).find("span").text
		return rid

	def sub_get(self,i):
		rid= self.get_id()
		print("I",i)
		payload={'entity_id':rid,
				'profile_action':'reviews-dd',
				'page':i,
				'limit':5
				}
		r= requests.post(url,data= payload,headers= header).text
		response=json.loads(str(r))
		soup=BeautifulSoup(response['html'])
		data= soup.find_all('div',{'class':'rev-text'})
		try:
			for x in data:
				review= x.find('div').next_sibling.strip()
				if review!=None or len(review)!=0:
					rating=x.find('div')['aria-label'].replace("Rated ","")
					sentiment= Senti(review).sent()
					# print (review)
					Reviews(provider="zomato",survey_id=self.sid,rating=rating,review=review,sentiment=sentiment).save()
		except :print("lol")
	def get_data(self):
		if isinstance(self.sid,list):
			print ("Zomato ignored",self.sid)
			pass
			# parent_id= self.sid[0]
			# for i in range(len(self.sid)):
			# 	if i==0:
			# 		pass
			# 	else:
			# 		objects=Reviews.objects(survey_id= self.sid[i],provider=self.p)
			# 		for obj in objects:
			# 			Reviews()
			# 		pass
		else:
			rid = self.get_id()
			total= self.get_total()
			turn = int(total/5)+1
			print (turn)
			# 1/0
			if len(Record.objects(survey_id= self.sid,rid=str(rid)))!=0:
				print ("Already Review Collected")
			else:
				pool= Pool()
				ids=list(range(0,turn))
				print (ids)
				# 1/0
				# for i in ids:
				# 	self.sub_get(i)	
				pool.map(self.sub_get,ids)
				
				Record(provider="zomato",survey_id=self.sid,rid=str(rid)).save()
				Status(unique_identifier=self.sid+provider,scraped_status="success").save()
if __name__ == '__main__':
	test_url="https://www.zomato.com/bangalore/petoo-sarjapur-road"
	
	z= Zomato(test_url,"x","y")
	z.get_data()
	print ("Done")
