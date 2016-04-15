import requests
import json
from urllib.request import urlopen

from bs4 import BeautifulSoup
from multiprocessing import Pool
try:
	from jupiter.sentient.reviews.models.model import Reviews,Scraped,Record
	from jupiter.sentient.reviews.nlp import Senti
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
	def __init__(self,url,survey_id):
		self.url= url
		self.sid= survey_id
	def get_total(self):pass

	def get_id(self):
		response= urlopen(self.url).read()
		soup=BeautifulSoup(response)
		rid= int(soup.find('body')['itemid'])
		return rid
	def sub_get(self,i):
		rid= self.get_id()

		payload={'entity_id':rid,
				'profile_action':'reviews-dd',
				'page':i,
				'limit':5
				}
		r= requests.post(url,data= payload,headers= header).text
		response=json.loads(str(r))
		soup=BeautifulSoup(response['html'])
		data= soup.find_all('div',{'class':'rev-text'})
		for x in data:
			review= x.find('div').next_sibling.strip()
			if review!=None or len(review)!=0:
				rating=x.find('div')['aria-label'].replace("Rated ","")
				sentiment= Senti(review).sent()
				Reviews(provider="zomato",survey_id=self.sid,rating=rating,review=review,sentiment=sentiment).save()
	def get_data(self):
		if isinstance(self.sid,list):
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
			if len(Record.objects(survey_id= self.sid,rid=str(rid)))!=0:
				print ("Already Review Collected")
			else:
				pool= Pool()
				ids=list(range(1,100))
				pool.map(self.sub_get,ids)
				Record(provider="zomato",survey_id=self.sid,rid=str(rid)).save()
if __name__ == '__main__':
	test_url="https://www.zomato.com/ncr/alishas-kitchen-aaya-nagar-new-delhi"
	z= Zomato(test_url)
	z.get_data()

