

"""
Read from csv file .
add to jupiter
"""
import csv
from jupiter.sentient.model import BookingQ,facebookDetails,facebookQ
from mongoengine import *

file_name="jupiter/sentient/custom_data/webcrs/facebook.csv"
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
    def __init__(self,custom_survey_id,buffer_n=None):
        self.c=custom_survey_id
        self.b=buffer_n
        self.aspect_list=[""]
        self.f=file_name
        self.base_url="https://graph.facebook.com/v2.7/me?fields=id,name,ratings"
    def name_to_id(self,name):
            name = name.replace(" ","")
            return name.lower()
    def add_task(self,access_token,user_id,page_id):
        try:
            obj3=facebookQ()
            obj3.base_url=self.base_url
            obj3.survey_id=user_id
            obj3.parent_id=self.c
            obj3.time_review="1980-01-01"
            obj3.unique_identifier=user_id+"facebook"
            obj3.aspect_notation=self.aspect_list
            obj3.access_token=access_token
            obj3.facebook_page_id=page_id
            obj3.save()
            print(user_id,"has been added")
        except Exception as e:
            print("Following exception has happened in add task function: ",e)
    def add_relation(self,i):
        print ("ADDING RELATIONS")
        survey_id= i
        objects=Relation.objects(survey_id = survey_id)
        print ("Number of objects for ", survey_id, "are", len(objects))
        if len(objects) == 0:
            obj2 = Relation()
            obj2.survey_id=survey_id
            obj2.provider=["facebook"]
            obj2.parent=self.c
            obj2.save()
            print ("added new relation object")
        else:
            newObj = Relation()
            newObj = objects[0]
            newObj.provider.append("facebook")
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
            obj.providers = ["facebook"]
            obj.save()
        else:
            if "facebook" not in objects[0].providers:
                newObj = ClientProviders()
                newObj = objects[0]
                newObj.providers.append("HolidayIQ")
                newObj.save()

    def get_facebook_pages(self):
        try:
            with open(self.f,"rt") as f:
                reader= list(csv.reader(f))
                if self.b != None:
                        reader= reader[self.b:]
                        pass
                for i in reader:
                    facebook_obj=facebookDetails.objects(user_id=i[1])
                    for i in facebook_obj:
                        self.add_task(i['access_token'],i['user_id'],i['facebook_page_id'])
                        self.add_relation(i['user_id'])
                        print (i['user_id'],"added")
            self.add_aspects(self.c)
            self.add_providers(self.c)
        except Exception as e:
            print("following exception occur",e)

if __name__ == '__main__':
	# main()
    CustomTask("jgBgKALz4mA3dNa5J36",1).get_facebook_pages()
