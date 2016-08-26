#!/usr/bin/env python
import sys
print ("*******************")

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
# from datum import DatumBox
from collections import Counter
from multiprocessing import Pool
from mongoengine import ValidationError, NotUniqueError
from datetime import datetime as dt
#import sys

from jupiter.sentient.reviews.models.model import Reviews,Record
from jupiter.sentient.model import AspectQ
from jupiter.sentient.reviews.nlp import Senti
#from jupiter.sentient.model import AspectQ

# import ssl
# from functools import wraps
# def sslwrap(func):
#     @wraps(func)
#     def bar(*args, **kw):
#         kw['ssl_version'] = ssl.PROTOCOL_ntienTLSv1
#         return func(*args, **kw)
#     return bar

# ssl.wrap_socket = sslwrap(ssl.wrap_socket)
import time
start= time.time()
# verbose=True
class TripAdvisor(object):

	"""docstring for"""
	def __init__(self,url,survey_id,provider="tripadvisor"):
		self.url= url
		self.p=provider
		self.sid=survey_id
	def last_links(self):
		response= urlopen(self.url).read()
		soup = BeautifulSoup(response)
		links= soup.find_all('a',{'class':'pageNum'})
		# return links
		try:
			return int(links[-1].text)
		except Exception as e:
			return 1

	def generate_link(self):
		endvalue= self.last_links()
		links=[self.url]
		if endvalue==1:
			return links


		add= len('Reviews-')
		marker= self.url.index('Reviews-')+add
		for i in range(1,endvalue):
			new_url= self.url[:marker]+"or"+str(i*10)+"-"+self.url[marker:]
			links.append(new_url)
		return links
	def sub_get(self,link):
		response= urlopen(link).read()
		soup= BeautifulSoup(response)
		review_link=soup.find_all('div',{'class':'quote'})
		base_url= "https://www.tripadvisor.in"
		obj=Reviews.objects(survey_id=self.sid).order_by('-datetime').first()
		record= Record.objects(survey_id=self.sid)
		last_update=AspectQ.objects(survey_id=self.sid, unique_identifier=self.sid+"tripadvisor")[0].last_update
		time_review = AspectQ.objects(survey_id=self.sid, unique_identifier=self.sid+"tripadvisor")[0].time_review
		if last_update!=None:
			time_reviewed=time_review if (time_review>=last_update) else last_update
		else:
			time_reviewed=time_review

		for j in review_link:
			rl = j.find("a",href=True)
			temp= rl['href'].encode('utf-8')
			rl = rl.encode('utf-8').strip()
			rl= rl.decode('utf-8')
			temp = str(temp)[2:]
			temp=temp[:-1]
			full_url= base_url+temp
			import requests
			review_res= requests.get(base_url+temp)

			review_res= review_res.text

			if review_res!=None:
				# Check if review exists
				# obj=Reviews.objects(survey_id=self.sid).order_by('-datetime').first()


				soup2= BeautifulSoup(review_res)
				date=soup2.find('span',{'class':'ratingDate'})['content']
				if len(date)==0 or date==None:
					raw_date=soup2.find('span',{'class':'ratingDate'}).text
					to_remove=len("Reviewed ")
					raw_date= raw_date[to_remove:]
					parse_date=dt.strptime(raw_date,'%d %B %Y')
					#Reviewed 15 March 2016
				#date=date.replace('l','1')

				else:parse_date= dt.strptime(date,"%Y-%m-%d")
				if time_reviewed!=None:
					# get the most recent date
					if record!=None:

						#msd= obj.datetime
						print (time_reviewed,"|",parse_date)
						if time_reviewed>=parse_date:

							raise Exception("Not collecting reviews")
				rating=soup2.find('img',{'class':'sprite-rating_s_fill'})['alt'][0]

				review= soup2.find('p',{'property':'reviewBody'}).text
				print("*********")
				from random import randrange
				r= str(randrange(100,999999))
				review_identifier=review[0:100]+r
				sentiment= Senti(review).sent(rating)

				try:
					save = Reviews(review_identifier=review_identifier,survey_id=self.sid,datetime=parse_date,date_added=date,provider=self.p,review=review,rating=rating,review_link=full_url,sentiment=sentiment).save(validate=False)
				except NotUniqueError:
					print("NotUniqueError")
				except Exception as e:
					pass

			else:
				print("Empty Review")
		#

	def get_data(self):
		if isinstance(self.sid,list):print("Ignored")
		else:
			# links= self.generate_link()
			# # print (links)
			# try:
			# 	for i in links:
			# 		self.sub_get(i)
			# except NotUniqueError:
			# 	pass
			b=1
			links= self.generate_link()
			#links= links.reverse()
			if len(Record.objects(links=set(links)))!=0:
				print ("Already Reviews Collected")
			else:
				# pool= Pool(8)
				# pool.map(self.sub_get,links)
				for i in links:
					try:
						self.sub_get(i)
					except Exception as e:
						print("trippool: exception",e)
						break
				Record(survey_id= self.sid,provider="tripadvisor",links= set(links)).save()
	def multi(self):
		links= self.generate_link()
		# return links
		# if len(Record.objects(links=set(links)))!=0:
		# 	print ("Already Review Collected")
		# else:
		pool= Pool(8)
		results= pool.map(self.get_data,[links])
		return results

	def main(self):
		counter=0
		links=self.generate_link()

		flag= len(links)
		res=Counter({})
		while counter<flag:
			rev= self.get_data(links[counter:counter+1])
			revtstr= " ".join(rev)
			d= DatumBox()
			# print("datum")
			a= Counter(d.get_keywords(revtstr))
			# print (a[4])
			res= res+a
			most_frequent_words_so_far = Counter(res).most_common(20)
			# print (most_frequent_words_so_far)
			# print (most_frequent_words_so_far)
			counter+=1

if __name__ == '__main__':
	pass
	test_url="https://www.tripadvisor.in/Restaurant_Review-g1062901-d4696931-Reviews-Country_Inn_Suites_by_Carlson_Sahibabad-Ghaziabad_Uttar_Pradesh.html"
	test= TripAdvisor(test_url)
	r= test.get_data()
	# for i in r:


	end = time.time()
	print ("Time Taken")
	print (end)
	# print ("Time Taken")
	# print (end-start)
