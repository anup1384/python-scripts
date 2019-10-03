#!/usr/local/opt/python/bin/python3.7 
import boto3
import os
import datetime
import dateutil
from dateutil import parser
action= os.getenv("action")
ec2_re=boto3.resource(service_name="ec2",region_name="ap-south-1")
ec2_cli=boto3.client("sts")
account_id=ec2_cli.get_caller_identity()["Account"]
e2_lists=[{'Name': 'tag:environment', 'Values':['nonprod']}, {'Name':'tag:techteam', 'Values':['anup']}, {'Name': 'tag:amitag', 'Values': ['yes']}]
instances=ec2_re.instances.filter(Filters=e2_lists)
images=ec2_re.images.filter(Filters=[{'Name': 'tag:amitag', 'Values':['yes']},],Owners=[account_id])
#Get the 10 days old date
days=10
timeLimit=datetime.datetime.now() - datetime.timedelta(days=days)
def createImage(x):
    for instance in x:
        for tag in instance.tags:
            if 'Name' in tag['Key']:
                name=(tag['Value'])
        ami_name=name + "-" + str(instance.id) + "-" + str(datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
        print ("Creating AMI Named " + ami_name)           
        createdImageId=instance.create_image(Name=ami_name, NoReboot=True, Description=ami_name)
        print("AMI ID of", ami_name, "is", createdImageId.id)
        ami_image=ec2_re.Image(createdImageId.id)
        print("Tagging", ami_name)
        ami_image.create_tags(Tags=[{'Key': 'amitag','Value': 'yes'},])

def deleteImage(x):
    for i in x:
        if parser.parse(i.creation_date).date() <= timeLimit.date():
            print ("Deleting AMI ID " + str(i.id) + " Created On " + str(i.creation_date))
            blockDeviceMapping=i.block_device_mappings
            # print(blockDeviceMapping)
            amidelete=i.deregister()      
            for snapshot in blockDeviceMapping:
                snapshotID=blockDeviceMapping[0]['Ebs']['SnapshotId']
                # print(snapshotID)
                if snapshotID is not None:
                    print ("Deleting Snapshot " + str(snapshotID))
                    snapshot=ec2_re.Snapshot(snapshotID)
                    # print(dir(snapshot))
                    snapshotdelete=snapshot.delete()
        else:
            # this section will have all snapshots which is created before 10 days
            print ("Only Deleting AMI which is older than", days)



if action == 'create':
    createImage(instances)
elif action == 'delete':
    deleteImage(images)