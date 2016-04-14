import csv
import os

def aspect_rating(review_rows, aspect_rows, overall):
	positive_rows = [row for row in aspect_rows if row[2] == 'Positive']
	negative_rows = [row for row in aspect_rows if row[2] == 'Negative']

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
filename = "Data/sentimentalreviews.csv"

data = []
with open(filename, "rt") as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		aspect = row[2]
		review_ID = row[1]
		polarity = row[5]
		data_line = [review_ID, aspect, polarity]
		data.append(data_line)

overall_ratings = []
with open('Data/reviews.csv', "rt") as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		overall_ratings.append(row[1])

last_review_ID = max(list(map(int,[row[0] for row in data])))

for review_ID in range(1, last_review_ID):

	review_rows = [row for row in data if row[0] == str(review_ID)]

	food_rows = [row for row in review_rows if row[1] == '0']
	service_rows = [row for row in review_rows if row[1] == '1']
	price_rows = [row for row in review_rows if row[1] == '2']
	neutral_rows = [row for row in review_rows if row[1] == '-1']

	overall = overall_ratings[review_ID]

	if len(review_rows) !=0 :
		AR_food = aspect_rating(review_rows, food_rows, overall)
		AR_service = aspect_rating(review_rows, service_rows, overall)
		AR_price = aspect_rating(review_rows, price_rows, overall)
	else :
		AR_food = overall
		AR_service = overall
		AR_price = overall
	
	# OUTPUT
	print (review_rows)
	print ("Food: ", AR_food, " Service: ", AR_service, " Price: ", AR_price)
	print ("Overall", overall)
