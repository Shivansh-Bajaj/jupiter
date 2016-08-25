import requests
from mongoengine import ValidationError,NotUniqueError
import datetime
from jupiter.sentient.reviews.models.model import Reviews,Record
from jupiter.sentient.reviews.nlp import Senti
from jupiter.sentient import model
from random import randrange
class facebookCollector(object):
    """collect review from facebook"""
    def __init__(self,survey_id,provider="facebook"):
        self.survey_id=survey_id
        self.provider=provider
        self.base_url="https://graph.facebook.com/v2.7"
    def get_facebook_details(self):
        obj=model.AspectQ.objects(survey_id=self.survey_id)
        return obj
    def get_reviews(self):
        facebook_details=self.get_facebook_details()
        review_list=[]
        for i in facebook_details:
            try:
                access_token=i['access_token']
                page_id=i['facebook_page_id']
                url=i['base_url']
                time_review=i['time_review']
                last_updated=i['last_update']
                if last_updated!=None:
                    time_reviewed=time_review if time_review>=last_updated else last_updated
                else:
                    time_reviewed=last_updated
                params={
                        'access_token':access_token
                        }
                response=requests.get(url,params)
                response.raise_for_status()
                review_list.append({
                    "id":page_id,
                    "time_reviewed":time_reviewed,
                    "rating":response.json()
                    })
            except Exception as e:
                print("following error occur in facebookCollector while running function get_reviews:",e)
        return review_list

    def run(self):
        reviews_list=self.get_reviews()
        for reviews in reviews_list:
            facebook_page_id=reviews["id"]
            time_reviewed=reviews["time_reviewed"]
            review_url="https://www.facebook.com/"+facebook_page_id+"/reviews"
            for review in reviews["rating"]["ratings"]["data"]:
                string_date=review['created_time'].split('T')[0]
                review_date=datetime.datetime.strptime(string_date, "%Y-%m-%d")
                if review_date>=time_reviewed:
                    content=review['review_text']
                    aspect=review['rating']
                    r=str(randrange(100,999999))
                    review_identifier=content[0:25]+r
                    sentiment=Senti(content).sent(aspect)
                    try:
                         save=Reviews(provider=self.provider,review_identifier=review_identifier,survey_id=self.survey_id,date_added=review_date,review=content,rating=str(aspect),sentiment=sentiment,review_url=review_url).save()
                         print("review saved from page id:"+facebook_page_id+"\nreview idenifier:"+review_identifier+"\n*******************\n")
                    except Exception as e:
                        print("following exception occur while saving review",e)
            try:
                new_record=Record(survey_id=self.survey_id,provider="facebook",links={review_url}).save()
            except Exception as e:
                print("following error occur while saving Record",e)
if __name__=='__main__':
    test=facebookCollector("jgBgKALz4mA3dNa5J36","facebook").run()
