import csv
import os
try:
	from jupiter.sentient.aspect.models.model import Aspect,Reviews,SentR
	from jupiter.sentient.aspect.config import ASPECTS
except:
	from aspect.models.model import Aspect,Reviews,SentR
	from aspect.config import ASPECTS

# from mongoengine import *
# class Reviews(Document):
# 	pass

verbose=False
class AspectRating(object):
	"""docstring for AspectRating"""
	def __init__(self,survey_id):
		self.sid= survey_id
	def get_all(self):
		aspects_p={}
		aspects_n={}
		aspects_nu={}
		for key in ASPECTS:
			aspects_p[key]=0
			aspects_n[key]=0
			aspects_nu[key]=0
		# aspects_p={"food":0,"service":0,"price":0,"neutral":0}
		# aspects_n={"food":0,"service":0,"price":0,"neutral":0}
		# aspects_nu={"food":0,"service":0,"price":0,"neutral":0}
		objs= SentR.objects(survey_id= self.sid)
		for o in objs:
			obj= o.line
			# print(type(obj[2]))
			if obj[5]=="Positive":
				if obj[2]=='0':
					aspects_p['food']+=1
				if obj[2]=='1':
					aspects_p['service']+=1
				if obj[2]=='2':
					aspects_n['price']+=1
				if obj[2]=='-1':
					aspects_n['neutral']+=1
			if obj[5]=="Negative":
				if obj[2]=='0':
					aspects_n['food']+=1
				if obj[2]=='1':
					aspects_n['service']+=1
				if obj[2]=='2':
					aspects_n['price']+=1
				if obj[2]=='-1':
					aspects_n['neutral']+=1
			if obj[5]=="Neutral":
				if obj[2]=='0':
					aspects_nu['food']+=1
				if obj[2]=='1':
					aspects_nu['service']+=1
				if obj[2]=='2':
					aspects_nu['price']+=1
				if obj[2]=='-1':
					aspects_nu['neutral']+=1
		return {"positive":aspects_p,"negative":aspects_n,"neutral":aspects_nu}
				
		"""
		Logic:
			smookifthing const:
			total positive
			total neutral
			total negative

			if negative more than positive:
				give more weight to positive 
			c= mx +ny+oz
			where m , n and o are weight const for x ,y,z
			m= 0.75*n= 0.5 *o
			x,y,z are the negative, positive, neutral values
			weight formula= (1.5 *a + b + 0.5*c)/total

			if b >a  , c refers to neutral
			{'positive': {'food': 48, 'neutral': 0, 'service': 0, 'price': 0}, 'neutral': {'food': 12, 'neutral': 4, 'service': 0, 'price': 0}, 'negative': {'food': 7, 'neutral': 7, 'service': 0, 'price': 1}}



		"""
	def get_c(self,aspect):
		total= self.get_all()
		sum_t=0
		a=0
		b=0
		c=0

		for key in total:
			sum_t+=total[key][aspect]
		# print(sum_t)
		if sum_t==0:
			return 0
		if (0.8 *total['positive'][aspect])>total['negative'][aspect] :
			a= total['negative'][aspect]
			b= total['positive'][aspect]
			c= total['neutral'][aspect]
			# print(a,b,c)
			w=(1.5 *a + b + 0.5*c)/sum_t
		elif total['positive'][aspect]<(0.8*total['negative'][aspect]):
			a= total['positive'][aspect]
			b=total['negative'][aspect]
			c= total['neutral'][aspect]
			w= (1.5 *a + b + 0.5*c)/sum_t
		elif total['positive'][aspect]==total['negative'][aspect]:
			a= total['positive'][aspect]
			b=total['negative'][aspect]
			c= total['neutral'][aspect]
			w= (a+b+c)/sum_t
		return w


				

		
def aspect_rating(review_rows, aspect_rows, overall):
	positive_rows = [row for row in aspect_rows if row[2] == 'Positive']
	negative_rows = [row for row in aspect_rows if row[2] == 'Negative']

	if len(aspect_rows) == 0:
		y = overall
	else:
		if len(positive_rows) == len(negative_rows):
			x = (len(positive_rows) + len(negative_rows))*float(overall)/len(review_rows)
			y = (x + 10)/5

		if len(positive_rows) > len(negative_rows):
			diff = len(positive_rows) - len(negative_rows)
			x = (diff*len(review_rows))/(float(overall) * (len(positive_rows) + len(negative_rows)))
			y = 3 + 2*x/5

		if len(positive_rows) < len(negative_rows):
			diff = len(negative_rows) - len(positive_rows)
			x = (diff*len(review_rows))/(float(overall) * (len(positive_rows) + len(negative_rows)))
			y = 2*x/5

	return y


# os.chdir('..')
# os.chdir('..')
# filename = "Data/sentimentalreviews.csv"
class AspectR(object):
	"""docstring for AspectR"""
	def __init__(self,survey_id,provider):
		self.scopy= survey_id
		if isinstance(survey_id,list):
			self.sid=survey_id[0]
		else:
			self.sid= survey_id
		self.p=provider
	def run(self):
		data = []
		try:
			spamreader=SentR.objects(survey_id=self.sid,provider=self.p)
		except Exception as e: 
			spamreader=SentR.objects(survey_id=self.sid[0],provider=self.p)
			print("aspect_rating",e)
		if verbose:print("spamreader000",spamreader.count(),self.sid)
			# raise e
		# a= spamreader.line
		# reviews= 
		# with open(filename, "rt") as csvfile:
		# 	spamreader = csv.reader(csvfile)
		try:
			for row in spamreader:
				# print("row",row)
				aspect = row.line[2]
				review_ID = row.line[1]
				polarity = row.line[5]
				data_line = [review_ID, aspect, polarity]
				data.append(data_line)
		except Exception as e:
			if verbose:print("aspect_rating1",e)
			raise e
		# print(data)
		try:
			overall_ratings = []
			try:
				spamreader=Reviews.objects(survey_id=self.sid,provider=self.p)
				if verbose:print("spamreader1",spamreader.count(),self.sid)
				spamreader[0]
			except Exception as e:
				spamreader=Reviews.objects(survey_id__in=self.scopy,provider=self.p)
				if verbose:print ("aspect_rating4",e)
				# raise e
				if verbose:print("spamreader2",spamreader.count(),self.scopy)
			# with open('Data/reviews.csv', "rt") as csvfile:
			# 	spamreader = csv.reader(csvfile)

			for row in spamreader:
				# print(row.rating)
				overall_ratings.append(float(row.rating))

			last_review_ID = max(list(map(int,[row[0] for row in data])))
			for review_ID in range(1, last_review_ID):

				review_rows = [row for row in data if row[0] == str(review_ID)]
				food_rows = [row for row in review_rows if row[1] == str(ASPECTS.index('food'))]
				service_rows = [row for row in review_rows if row[1] == str(ASPECTS.index('service'))]
				price_rows = [row for row in review_rows if row[1] == str(ASPECTS.index('price'))]
				ambience_rows=[row for row in review_rows if row[1] == str(ASPECTS.index('ambience'))]
				vfm_rows=[row for row in review_rows if row[1] == str(ASPECTS.index('value_for_money'))]
				rs_rows=[row for row in review_rows if row[1] == str(ASPECTS.index('room_service'))]
				cleanliness_rows=[row for row in review_rows if row[1] == str(ASPECTS.index('cleanliness'))]
				neutral_rows = [row for row in review_rows if row[1] == '-1']
				# print(food_rows)
				overall = overall_ratings[review_ID]

				if len(review_rows) !=0 :
					AR_food = aspect_rating(review_rows, food_rows, overall)
					AR_service = aspect_rating(review_rows, service_rows, overall)
					AR_price = aspect_rating(review_rows, price_rows, overall)
					AR_ambience=aspect_rating(review_rows,ambience_rows,overall)
					AR_vfm=aspect_rating(review_rows,vfm_rows,overall)
					AR_rs=aspect_rating(review_rows,rs_rows,overall)
					AR_cleanliness=aspect_rating(review_rows,cleanliness_rows,overall)


					# if AR_food <=2:
					# 	AR_food=AR_food+AspectRating(self.sid).get_c("food")
					# else:
					# 	AR_food = aspect_rating(review_rows, food_rows, overall)-AspectRating(self.sid).get_c("food")
					# if AR_service <=2:
					# 	AR_service=AR_service+AspectRating(self.sid).get_c("service")
					# else:
					# 	AR_service = aspect_rating(review_rows, service_rows, overall)-AspectRating(self.sid).get_c("service")
					# if AR_price <=2:
					# 	AR_price=AR_price+AspectRating(self.sid).get_c("price")
					# else:
					# 	AR_price = aspect_rating(review_rows, price_rows, overall)-AspectRating(self.sid).get_c("price")
				else :
					AR_food = overall
					AR_service = overall
					AR_price = overall
					AR_ambience=overall
					AR_vfm=overall
					AR_rs=overall
					AR_cleanliness=overall
					
				# OUTPUT
				# print (review_rows)
				# print ("Food: ", AR_food, " Service: ", AR_service, " Price: ", AR_price,"Ambience",AR_ambience,"Crowd",AR_crowd)
				# print ("Overall", overall)
				# return 0
				r= Aspect(sector="food",provider=self.p,survey_id=self.sid,food=str(AR_food),service=str(AR_service),price=str(AR_price),value_for_money=str(AR_vfm),room_service=str(AR_rs),cleanliness=str(AR_cleanliness),overall=str(overall)).save()
				print("Aspect Rating Done")
		except Exception as e:
			# print("aspect_rating3",e)
			raise e
# 	[['1', '1', 'Positive']]
# Food:  2.0  Service:  3.088888888888889  Price:  2.0
if __name__ == '__main__':

# Overall 4.5
	a= AspectR('MAlnDybkavavGkBxn9D',"zomato")
	print(a.run())
