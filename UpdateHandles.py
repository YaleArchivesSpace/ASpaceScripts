import requests
import json

aspace_url = 'http://localhost:8089'
username = 'admin'
password = 'banana'
repo_num = '12'

auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

for d in range(4779,22800):
	digital_objects_json = requests.get(aspace_url+'/repositories/'+repo_num+'/digital_objects/'+str(d), headers=headers).json()
	digital_object_id = digital_objects_json["digital_object_id"]
	if digital_object_id.startswith("http://hdl.handle.net/10079"):
		digital_objects_json["digital_object_id"] = digital_objects_json["digital_object_id"].replace("digcoll:","digcoll/")
		updated = requests.post(aspace_url+'/repositories/'+repo_num+'/digital_objects/'+str(d), headers=headers, data=json.dumps(digital_objects_json))
		print 'Updating handles' + digital_objects_json["digital_object_id"]
