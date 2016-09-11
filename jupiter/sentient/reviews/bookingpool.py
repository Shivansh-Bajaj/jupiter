#!/usr/bin/env python
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from multiprocessing import Pool
from mongoengine import ValidationError, NotUniqueError
import sys
import re
import datetime
from jupiter.sentient.reviews.models.model import Reviews,Record
from jupiter.sentient.reviews.nlp import Senti
from jupiter.sentient import model


#except:
#	from reviews.models.model import Reviews,Recor,AspectQ
#	from reviews.nlp import Senti

class Booking(object):
	"""docstring for"""
	def __init__(self,url,survey_id,provider="booking"):
		self.url= url
		self.p=provider
		self.sid=survey_id
		self.base_url='http://www.booking.com'
	def get_total_review(self):
		response=urlopen(self.url).read()
		soup=BeautifulSoup(response,"html.parser")
		total=int(soup.find('a',{'class':'hp_nav_reviews_link toggle_review track_review_link_zh'}).text.strip().replace('(','').replace(')','').split()[-1])
		return total
	def get_next_link(self,soup):
		next_page=soup.find('a',{'id':'review_next_page_link'})
		new_url=self.base_url+next_page['href'] if next_page!=None else None
		return new_url
	def get_reviews(self,soup,time_reviewed,soup_url):
		links=[]
		total_reviews_collected=0
		while True:
			new_data=urlopen(soup_url)
			new_soup=BeautifulSoup(new_data,'html.parser')
			print("collection reviews from url:"+soup_url)
			lists=new_soup.find_all('li',{'class':'review_item'})
			for li in lists:
				review_date=li.find('meta',{'itemprop':'datePublished'})
				review_date=review_date['content'] if review_date!=None else None
				parsed_date=datetime.datetime.strptime(review_date,'%Y-%m-%d')
				print(time_reviewed,"|",parsed_date)
				if parsed_date>=time_reviewed:
					review=li.find('div',{'class':'review_item_review'})
					content=review.find('div',{'class':'review_item_review_content'}).find_all('span',{'itemprop':'reviewBody'})
					header=review.find('div',{'class':'review_item_review_header'})
					review_link=header.find('a',{'class':'review_item_header_content'})['href']
					print(review_link,parsed_date)
					rating=str(float(header.find('meta',{'itemprop':'ratingValue'})['content'])/2.0)
					sentiment=Senti(review).sent(rating)
					review_identifier=header.find('span',{'itemprop':'name'}).text.strip()
					for texts in content:
						texts=texts.text.strip() if texts!=None else None
						review_identifier += texts[0:10]
						try:
							save=Reviews(survey_id=self.sid,provider=self.p,review=texts,review_identifier=review_identifier,rating=rating,sentiment=sentiment).save()
							print("reviews saved identified by:",review_identifier)
							total_reviews_collected+=1
						except NotUniqueError:
							print ("NotUniqueError")
							raise NotUniqueError("A non unique error found. Skipping review collection")
						except Exception as e:
							print ("An exception occured ignoring ",e)
				else:
					print('empty review')

			links.append(soup_url)
			next_url=self.get_next_link(new_soup)
			if next_url==None:
				break
			else:
				soup_url=next_url
		print("total reviews collected =",total_reviews_collected)
		Record(survey_id=self.sid,provider="booking",links=set(links))
	def get_data(self):
		print ("Getting data for ",self.sid)
		page_no=1
		current_url=self.url
		response=urlopen(current_url)
		soup=BeautifulSoup(response,"html.parser")
		aspect_q=model.AspectQ.objects(survey_id=self.sid)
		# print ("\nFor survey: ", len(aspect_q[0].survey_id))
		time_review = aspect_q[0].time_review
		last_update=aspect_q[0].last_update

		if last_update!=None:
			time_reviewed=time_review if (time_review>=last_update) else last_update
		else:
			time_reviewed=time_review
		start=soup.find_all('a',{"class":"show_all_reviews_btn"})
		# print ("\n start: ", start)
		if start:
			start_url=self.base_url+start[0]['href']
			# print ("\nStart URL: ", start_url)
			try:
				self.get_reviews(soup,time_reviewed,start_url)
			except NotUniqueError:
				pass
		else:
			print("total reviews collected 0")
if __name__ == '__main__':
	test_url="http://www.booking.com/hotel/in/swissa-tel-goa.html?label=gen173nr-1FCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYATG4AQ_IAQ_YAQHoAQH4AQKoAgM;sid=69a80e530b4bd33d6a2ce0e128061485;dcid=12;dest_id=4127;dest_type=region;dist=0;group_adults=2;room1=A%2CA;sb_price_type=total;srfid=39183e2a96da4c1e9df94a8b1555fa36ec6494ddX4;type=total;ucfs=1&#"
	test= Booking(test_url,"2WzzBWZAvVKoJonJvW2")
	r= test.get_data()
	print ("end")
