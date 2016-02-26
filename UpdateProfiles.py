import requests
import json
import csv

# This script posts updates to container profile records.
# We realized after some time that we needed to simplify our container profile records.
# We decided that we would round to the nearest inch, and would simplify a set of custom boxes.
# I made the changes in a spreadsheet and use this to post them.

# Login information here
aspace_url = ''
username = ''
password = ''

container_profiles_to_update = 'infile.csv'

auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

# Open and iterate through the spreadsheet
with open(container_profiles_to_update,'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        #First column has the container_profile ID (pulled from MySQL db)
        cp_uri = row[0]
        #Second column has the container profile name
        name = row[1]
        #Dimensions
        height = row[2]
        width = row[3]
        depth = row[4]
        #Create variable for the URI
        container_profile_uri = aspace_url+'/container_profiles/'+cp_uri
        #Get the json for the existing container profiles
        container_profile_json = requests.get(container_profile_uri,headers=headers).json()
        #Create the updated fields in JSON, based on the spreadsheet columns
        payload = {'name':name,'height':height, 'width':width, 'depth':depth}
        #Update the existing container profile JSON to include the new information
        container_profile_json.update(payload)
        container_profile_data = json.dumps(container_profile_json)
        #Send it back to ArchivesSpace!
        container_profile_update = requests.post(container_profile_uri,headers=headers,data=container_profile_data).json()
        print container_profile_update