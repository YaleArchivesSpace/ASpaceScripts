import requests
import json

aspace_url = 'http://**.library.yale.edu:8089'
username = '**'
password = '**'
repo_num = '3'

auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

for resource_id in range(5369,5451):
	resource_uri = aspace_url+'/repositories/'+repo_num+'/resources/'+str(resource_id)
	resource_json = requests.get(resource_uri,headers=headers).json()
	resource_json["publish"]=False
	resource_update = requests.post(resource_uri,headers=headers,data=json.dumps(resource_json))
	print str(resource_id) + ' updated!'
