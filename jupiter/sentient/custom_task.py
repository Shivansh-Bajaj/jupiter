"""
Read from csv file .
add to jupiter
"""
import csv
from jupiter.sentient.model import TripAdvisorQ
from mongoengine import *

file_name="jupiter/sentient/custom_data/q_links_taj.csv"
class Relation(Document):
    """docstring for Relation"""
    survey_id = StringField()
    provider = StringField()
    parent = StringField()
   
class CustomTask(object):
	"""docstring for CustomTask"""
	def __init__(self,file_name,custom_survey_id,buffer_n=None,mode="csv"):
		self.f= file_name
		self.c= custom_survey_id
		self.b= buffer_n
	def run_csv(self):
		with open(self.f,"rt") as f:
			reader= list(csv.reader(f))
			if self.b != None:
				reader= reader[self.b:]
				pass
			for i in reader:
				if len(i[2])!=0:
					# print ("Something")
					# print(i[2])
					self.add_task(i)
					self.add_relation(i)
					print (i[0],"added")
	def name_to_id(self,name):
		# Remove space
		name = name.replace(" ","")
		return name.lower()
	def add_task(self,i):
		survey_id= i[1]
		try:
			obj2=TripAdvisorQ()
			obj2.base_url=i[2]
			#See the numbering 2 in i[2], it refers to column number 0,1,2..n
			#So whenever you add a new header(aka column) lets say date_limit in 
			#csv file for time_review, you go like this
			#obj2.time_review=i[column_number]
			#the buffer is the total number of rows which are not to be included. 2 means
			#upper 2 rows. i.e the header row, and an empty row.
			obj2.survey_id=survey_id
			obj2.parent_id=self.c
			obj2.aspects=["ambience"]#extend the list till the aspeccts you want to be calculated
			obj2.time_review="2016-04-01" #default date. okay?k change it to suit your limit
			obj2.unique_identifier=survey_id+"tripadvisor"
			obj2.save()
		except Exception as e:
			print("Following exception has happened: ",e)
	def add_relation(self,i):
		survey_id= i[1]
		obj= Relation()
		obj.survey_id=survey_id
		obj.provider="tripadvisor"
		obj.parent=self.c
		obj.save()

def minitask():
		obj2=TripAdvisorQ()
		obj2.base_url=i[2]
		obj2.survey_id=survey_id
		obj2.parent_id=self.c
		obj2.unique_identifier=survey_id+"tripadvisor"
		obj2.save()
if __name__ == '__main__':
	CustomTask(file_name,"djp1rj8NL31jjB5mp3q",2).run_csv()
