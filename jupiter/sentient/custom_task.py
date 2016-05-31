"""
Read from csv file .
add to jupiter
"""
import csv
from model import TripAdvisorQ
file_name="custom_data/q_links.csv"

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
					print (i[0],"added")
	def name_to_id(self,name):
		# Remove space
		name = name.replace(" ","")
		return name.lower()
	def add_task(self,i):
		survey_id= self.name_to_id(i[0])
		obj2=TripAdvisorQ()
		obj2.base_url=i[2]
		obj2.survey_id=survey_id
		obj2.parent_id=self.c
		obj2.unique_identifier=survey_id+"tripadvisor"
		obj2.save()
		
if __name__ == '__main__':
	# main()
	CustomTask(file_name,"Test",2).run_csv()
