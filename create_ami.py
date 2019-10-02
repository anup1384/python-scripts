#!/usr/bin/python
import boto3
import os
from datetime import datetime
action= os.getenv("action")
ec2_re=boto3.resource(service_name="ec2",region_name="ap-south-1")

e2_lists=[{'Name': 'tag:environment', 'Values':['nonprod']}, {'Name':'tag:techteam', 'Values':['anup']}, {'Name': 'tag:amitag', 'Values': ['yes']}]
instances=ec2_re.instances.filter(Filters=e2_lists)
def createImage(x):
    for instance in x:
        for tag in instance.tags:
            if 'Name' in tag['Key']:
                name=(tag['Value'])
        ami_name=name + "-" + str(instance.id) + "-" + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
        print ("Creating AMI Named " + ami_name)           
        createdImageId=instance.create_image(Name=ami_name, NoReboot=True, Description=ami_name)
        print("AMI ID of", ami_name, "is", createdImageId.id)
        ami_image=ec2_re.Image(createdImageId.id)
        print("Tagging", ami_name)
        ami_image.create_tags(Tags=[{'Key': 'amitag','Value': 'yes'},])


# for instance in ec2_re.instances.filter(Filters=e2_lists):
#     for tag in instance.tags:
#         if 'Name' in tag['Key']:
#             name=(tag['Value'])
#             print ("Will create ami of", instance.id, name)
#     ami_name=name + "-" + str(instance.id) + "-" + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
#     print ("Creating AMI Named " + ami_name)           
#     createdImageId=instance.create_image(Name=ami_name, NoReboot=True, Description=ami_name)
#     amiid=createdImageId.id
#     print("AMI ID of", ami_name, "is", amiid)
#     ami_image=ec2_re.Image(amiid)
#     print("Tagging", ami_name)
#     ami_image.create_tags(Tags=[{'Key': 'amitag','Value': 'yes'},])

if action == 'create':
    createImage(instances)