"""
Read from csv file .
add to jupiter
"""
import csv
from jupiter.sentient.model import TripAdvisorQ
from mongoengine import *

file_name="jupiter/sentient/custom_data/lilac/trip.csv"
class Relation(Document):
    """docstring for Relation"""
    survey_id = StringField()
    provider = ListField()
    parent = StringField()

class ClientAspects(Document):
	parent_id = StringField(required = True)
	aspects = ListField()

class ClientProviders(Document):
	parent_id = StringField(required = True)
	providers = ListField()

class CustomTask(object):
	"""docstring for CustomTask"""
	def __init__(self,file_name,custom_survey_id,buffer_n=None,mode="csv"):
		self.f= file_name
		self.c= custom_survey_id
		self.b= buffer_n
		self.aspect_list = ["ambience","value_for_money","room_service","cleanliness","amenities"]

	def run_csv(self):
		with open(self.f,"rt") as f:
			reader= list(csv.reader(f))
			if self.b != None:
				reader= reader[self.b:]
				pass
			for i in reader:
				if len(i[2])!=0:
					self.add_task(i)
					self.add_relation(i)
					print (i[0],"added")
		self.add_aspects(self.c)
		self.add_providers(self.c)

	def name_to_id(self,name):
		name = name.replace(" ","")
		return name.lower()
	def add_task(self,i):
		try:
			survey_id= i[1]
			obj2=TripAdvisorQ()
			obj2.base_url=i[2]
			obj2.survey_id=survey_id
			obj2.parent_id=self.c
			obj2.time_review="1980-01-01"
			obj2.unique_identifier=survey_id+"tripadvisor"
			obj2.aspect_notation=self.aspect_list
			obj2.save()
			print(survey_id,"has been added")
		except Exception as e:
			print("Following exception has happened: ",e)
	def add_relation(self,i):
		print ("ADDING RELATIONS")
		survey_id= i[1]
		objects=Relation.objects(survey_id = survey_id)

		print ("Number of objects for ", survey_id, "are", len(objects))
		if len(objects) == 0:
			obj2 = Relation()
			obj2.survey_id=survey_id
			obj2.provider=["tripadvisor"]
			obj2.parent=self.c
			obj2.save()
			print ("added new relation object")
		else:
			if "tripadvisor" not in objects[0].provider:
				newObj = Relation()
				newObj = objects[0]
				newObj.provider.append("tripadvisor")
				newObj.save()
				print ("updated old relation object")

	def add_aspects(self, parent_id):

		print ("ADDING ASPECTS")
		objects = ClientAspects.objects(parent_id = parent_id)

		print ("Number of objects for ", parent_id, "are", len(objects))

		if len(objects) == 0:
			obj = ClientAspects()
			obj.parent_id = parent_id
			obj.aspects = self.aspect_list
			obj.save()

	def add_providers(self, parent_id):

		print ("ADDING PROVIDERS")
		objects = ClientProviders.objects(parent_id = parent_id)
		print ("Number of objects for ", parent_id, "are", len(objects))
		if len(objects) == 0:
			obj = ClientProviders()
			obj.parent_id = parent_id
			obj.providers = ["tripadvisor"]
			obj.save()
		else:
			if "tripadvisor" not in objects[0].providers:
				newObj = ClientProviders()
				newObj = objects[0]
				newObj.providers.append("tripadvisor")
				newObj.save()

def minitask():
		obj2=TripAdvisorQ()
		obj2.base_url=i[2]
		obj2.survey_id=survey_id
		obj2.parent_id=self.c
		obj2.unique_identifier=survey_id+"tripadvisor"
		obj2.save()
if __name__ == '__main__':
	# main()
	CustomTask(file_name,"vOAWLlOmAZyY23AdmZy",2).run_csv()
