# pip install Flask
# pip install pymongo
# pip install pandas
#
# For this assessment I setup my environment using Mongodb (data store) and Python Flask as a webframework

# Tested with the following curl commands
# curl -i -H "Content-Type: application/json" -X POST -d '{"Name":"Peter", "Age":  34, "Balance" : 100, "Email": "peter@testmail.com", "Address": "123 Fake Street"}' http://localhost:2000/app/people/
# curl -X GET http://localhost:2000/app/people/search/?Name=Peter
# curl -X DELETE http://localhost:2000/app/people/delete/?Name=Peter

from flask import Flask, request
from pymongo import MongoClient
from IPython.display import HTML
import json
import pandas as pd

app = Flask(__name__)

# Connect to Mongo
try:
    client = MongoClient('localhost', 27017)
    print("Connected to Mongo")
except:
    print("Could not connect")
db = client.FlexeraAssessment

# POST method
@app.route('/app/people/', methods=['POST'])

def add_people():

    receivedData = request.data

    try:
        json_object = json.loads(receivedData)
        print("About to insert into Mongo")
        collection=db.FlexTest
        collection.insert_one(json_object)
        print("Inserted into Mongo")
    except:
        print("There was an error")

    return receivedData

# GET method
@app.route('/app/people/', methods=['GET'])

def get_people():

    collection=db.FlexTest
    if collection.count() > 0:
        print("Getting details..")
        # creating a data frame to display the records in a table (part 2 of assessment)
        dataFrame = pd.DataFrame(list(collection.find({}, {"Name": 1, "Age": 1, "Balance": 1, "Email": 1, "Address": 1})))
        dataFrame = dataFrame.drop('_id',axis=1)
        print(dataFrame)
        dataTable = dataFrame.to_html()
        return dataTable
    else:
        message = 'Empty database, add some records first'
        print(message)
        return message

# GET method with search parameters
@app.route('/app/people/search/', methods=['GET'])

def search_people():

    search_param = request.args
    print(f"Search parameters: {search_param}")
    collection=db.FlexTest
    if len(search_param) > 0:
        print("Searching details..")

        qrylist = []
        for i in search_param.keys():
            qrylist.append(i)
        # creating a search query from the passed parameters
        myquery = {qrylist[0] : search_param[qrylist[0]]}
        print(myquery)
        return str(list(collection.find(myquery)))
    else:
        message = "No search parameter provided"
        print(message)
        return message

# DELETE method with parameters
@app.route('/app/people/delete/', methods=['DELETE'])

def delete_people():

    delete_param = request.args
    collection=db.FlexTest
    if len(delete_param) >0:
        print(f"Removing details: {delete_param}")

        qrylist = []

        for i in delete_param.keys():
            qrylist.append(i)

        myquery = {qrylist[0] : delete_param[qrylist[0]]}
        collection.delete_one(myquery)
        return str(list(collection.find()))
    else:
        message = "Please provided paramaters for delete method"
        print(message)
        return message


app.run(host='0.0.0.0', port=2000)
