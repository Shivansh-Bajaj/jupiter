#!/usr/bin/env python
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
# from datum import DatumBox
from collections import Counter
from multiprocessing import Pool
from mongoengine import ValidationError, NotUniqueError

import sys
try:
	from jupiter.sentient.reviews.models.model import Reviews,Record
	from jupiter.sentient.reviews.nlp import Senti
except:
	from reviews.models.model import Reviews,Record
	from reviews.nlp import Senti
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
		# reviews=[]
		for j in review_link:
			# print ("New Review Link")
			rl = j.find("a",href=True)
			print ("review_link",rl)
			review_res= urlopen(base_url+rl['href']).read()
			if review_res!=None:
				soup2= BeautifulSoup(review_res)
				# print (soup2)
				rating=soup2.find('img',{'class':'sprite-rating_s_fill'})['alt'][0]
				# review= soup2.find('p',{'property':'reviewBody'}).text +"\n"+"#rating: "+ rating
				review= soup2.find('p',{'property':'reviewBody'}).text
				print("*********")
				review_identifier=review[0:100]
				sentiment= Senti(review).sent()
				# print("chunk done")
				# print(rating)
				try:
					save = Reviews(survey_id=self.sid,provider=self.p,review=review,review_identifier=review_identifier,rating=rating,sentiment=sentiment).save()
				except NotUniqueError:
					print ("NotUniqueError")
					raise NotUniqueError("A non unique error found. Skipping review collection")
				except Exception as e:
					print ("An exception occured ignoring ",e)

				# print ("Saved")
				# reviews.append(review)
			else:
				print("Empty Review")
		#

	def get_data(self):
		if isinstance(self.sid,list):print("Ignored")
		else:
			links= self.generate_link()
			# print (links)
			try:
				for i in links:
					self.sub_get(i)
			except NotUniqueError:
				pass
			# links= self.generate_link()
			# if len(Record.objects(links=set(links)))!=0:
			# 	print ("Already Reviews Collected")
			# else:
			# 	# pool= Pool(8)
			# 	# pool.map(self.sub_get,links)
			# 	for i in links:
			# 		try:
			# 			self.sub_get(i)
			# 		except NotUniqueError:
			# 			pass
			# 	Record(survey_id= self.sid,provider="tripadvisor",links= set(links)).save()
	def multi(self):
		links= self.generate_link()
		# return links
		if len(Record.objects(links=set(links)))!=0:
			print ("Already Review Collected")
		else:
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
			print("datum")
			a= Counter(d.get_keywords(revtstr))
			# print (a[4])
			res= res+a
			most_frequent_words_so_far = Counter(res).most_common(20)
			print (most_frequent_words_so_far)
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
	print (end-start)