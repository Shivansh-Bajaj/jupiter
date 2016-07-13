#!/usr/bin/env python
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from multiprocessing import Pool
from mongoengine import ValidationError, NotUniqueError
import sys
import re
try:
	from jupiter.sentient.reviews.models.model import Reviews,Record
	from jupiter.sentient.reviews.nlp import Senti
except:
	from reviews.models.model import Reviews,Record
	from reviews.nlp import Senti
class HolidayIQ(object):
	"""docstring for"""
	def __init__(self,url,survey_id,provider="HolidayIQ"):
		self.url= url
		self.p=provider
		self.sid=survey_id
	def get_total_review(self):
		response=urlopen(self.url).read()
		soup=BeautifulSoup(response,"html.parser")
		more_reviews=int(soup.find('input',{'id':'textReviewToBeDisplay'})['value'])
		page_reviews=len(soup.find('div',{'id':'result-items'}).find_all('div',{'class':'srm'}))
		return more_reviews+page_reviews
	def get_next_link(self,page_no):
		return self.url[:self.url.find(".html")]+'-p'+str(page_no)+'.html'
	def get_reviews(self,soup):
		reviews=soup.find('div',{'id':'result-items'}).find_all('div',{'class':'srm'})
		for review in reviews:
			more_content=re.compile("^moreReviewContent[0-9]+")
	#		less_content=re.compile("^lessReviewContent[0-9]+")
			if review!=None:
				rating=str(float(review.find('meta',{'itemprop':'ratingValue'})['content'])*5/7)
				content=str(review.find('p',{'id':more_content}).text)
				review_identifier=review.find('a',{'class':'featured-blog-clicked'}).text
				sentiment=Senti(review).sent(rating)
				try:
					print("review save"+review_identifier)
					save = Reviews(survey_id=self.sid,provider=self.p,review=content,review_identifier=review_identifier,rating=rating,sentiment=sentiment).save()
				except NotUniqueError:
					print ("NotUniqueError")
					raise NotUniqueError("A non unique error found. Skipping review collection")
				except Exception as e:
					print ("An exception occured ignoring ",e)

			else:
				print("Empty Review")
	
	def get_data(self):
		page_no=1
		current_url=self.url
		links=[]
		while True:
			response=urlopen(current_url)
			soup=BeautifulSoup(response,"html.parser")
			try:
				self.get_reviews(soup)
			except NotUniqueError:
				pass
			print("reviews url:"+current_url+"#complete\n")
			links.append(current_url)
			more_reviews=int(soup.find('input',{'id':'textReviewToBeDisplay'})['value'])
			if more_reviews==0:
				break
			page_no=page_no+1
			current_url=self.get_next_link(page_no)	
		Record(survey_id=self.sid,provider="HolidayIQ",links=set(links))	

if __name__ == '__main__':
	test_url="http://www.holidayiq.com/Hari-Mahal-Hotel-Jaipur-hotel-2249.html"
	test= HolidayIQ(test_url,"2WzzBWZAvVKoJonJvW2")
	r= test.get_data()
	print ("end")
