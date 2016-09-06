#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider

from jupiter.sentient.aspect.reviewProcessing import ReviewP
from jupiter.sentient.aspect.sentimental import Sentiment
from jupiter.sentient.aspect.aspectratings import AspectR
from jupiter.sentient.reviews.nlp import WordCloud

verbose = True

class Sentient(object):
	"""
	1. Scrapes web for reviews.
	2. Runs wordcloud.
	3. Runs ML.
	"""
	def __init__(self, url, survey_id, provider, aspects):
		self.u = url
		self.sid = survey_id
		self.p = provider
		self.aspects = aspects

	def scrap_data(self):
		print(self.aspects)
		# The name of providers are predefined in sub-classes of AspectQ model.
		if self.p == "zomato":
			from jupiter.sentient.reviews.zomatopool import Zomato
			Zomato(self.u, self.sid).get_data()
		if self.p == "tripadvisor":
			from jupiter.sentient.reviews.trippool import TripAdvisor
			TripAdvisor(self.u, self.sid).get_data()
		if self.p == "HolidayIQ":
			from jupiter.sentient.reviews.holidaypool import HolidayIQ
			HolidayIQ(self.u, self.sid).get_data()
		if self.p == "booking":
			from jupiter.sentient.reviews.bookingpool import Booking
			Booking(self.u, self.sid).get_data()

	def wordcloud(self):
		WordCloud(self.sid, self.p).wc()

	def run_ml(self):
		ReviewP(self.sid, self.p, self.aspects).run()
		print("ReviewP Done")
		Sentiment(self.sid, self.p).run()
		print("Sentiment Done")
		AspectR(self.sid, self.p).run()
		print ("AspectR Done")

	def run(self):
		if verbose:
			print ("Starting Scraping")
		self.scrap_data()
		if verbose:
			print("Starting WordCloud")
		self.wordcloud()
		if verbose:
			print("Running ML")
		self.run_ml()
		print("Done")
