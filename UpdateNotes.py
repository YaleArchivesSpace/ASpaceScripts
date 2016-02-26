import requests
import json
import csv

#This is the final step in a process to associate machine-actionable restriction end dates with conditions governing access notes.
#I pulled conditions governing access notes from MySQL and then analyzed them in OpenRefine.
#From there, I created a list of restriction end dates associated with archival objects.
#This script fetches the existing archival upbject and updates the note to include the new restriction end date.

aspace_url = ''
username = ''
password = ''
repo_num = ''

restrictions_to_update = 'infile.txt'

auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

#opens and iterates through spreadsheet
with open(restrictions_to_update,'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # Get archival object from CSV
        ao_uri = row[0]
        # Get end date from csv
        end_date = row[1]
        end_date = str(end_date)
        # Get the archival object's ASpace archival_object ID
        archival_object_uri = aspace_url+'/repositories/'+repo_num+'/archival_objects/'+ao_uri
        archival_object_json = requests.get(archival_object_uri,headers=headers).json()
        notes = archival_object_json['notes']
        #Iterates through notes to find accessrestrict
        for index, n in enumerate(notes):
            if n["type"] == 'accessrestrict':
                #Create the JSON elements we want to add to the note
                restrict = {'rights_restriction':{'end': end_date}}
                #Update the note/archival object to include the end date
                n.update(restrict)
                archival_object_json.update(n)

        archival_object_data = json.dumps(archival_object_json)
            # Repost the archival object
        archival_object_update = requests.post(archival_object_uri,headers=headers,data=archival_object_data).json()
        print archival_object_update