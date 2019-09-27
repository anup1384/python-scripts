#!/usr/bin/python
import boto3
from pprint import pprint
ec2_re=boto3.resource(service_name="ec2", region_name="ap-south-1")
ec2_cli=boto3.client(service_name="ec2", region_name="ap-south-1")
#print(dir(ec2_re))
#for each in ec2_re.volumes.all():
all_volumes_id=[]
availableebs={'Name':'status','Values':['available']}
for each in ec2_re.volumes.filter(Filters=[availableebs]):
    if each.tags==None:
        print(each.id, each.state, each.tags)
        all_volumes_id.append(each.id)

for each in all_volumes_id:
    volume_ob=ec2_re.Volume(each)
#   print(dir(volume_ob))
    print(" Deleting volumes of id",each)
    volume_ob.delete()
waiter = ec2_cli.get_waiter('volumes_deleted')
try:
    waiter.wait(volumeIds=all_volumes_id)
    print("Successfully deleted available and untagged volumes")
except Exception as e:
    print ("e")