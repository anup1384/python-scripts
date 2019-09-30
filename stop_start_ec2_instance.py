#!/usr/bin/python
import boto3
import os
action= os.getenv("action")
ec2_re=boto3.resource(service_name="ec2",region_name="ap-south-1")
instance_id=[]
if action == "stop":
    state='running'
else:
    state='stopped'

e2_lists=[{'Name': 'tag:environment', 'Values':['nonprod']}, {'Name':'tag:techteam', 'Values':['anup']}, {'Name': 'instance-state-name', 'Values': [state]}]
instances=ec2_re.instances.filter(Filters=e2_lists)

def start_instances(x):
    for instance in x:
        for tag in instance.tags:
            if 'Name' in tag['Key']:
                name=(tag['Value'])
        instance_id.append(instance.id)
        print ("Will start ", instance.id, name)
    ec2_re.instances.filter(InstanceIds = instance_id).start()
    ec2_re.wait_until_running()

def stop_instances(x):
    for instance in x:
        for tag in instance.tags:
            if 'Name' in tag['Key']:
                name=(tag['Value'])
        instance_id.append(instance.id)
        print ("Will stop ", instance.id, name)
    ec2_re.instances.filter(InstanceIds = instance_id).stop()
    ec2_re.wait_until_stopped()

if action == 'start':
    start_instances(instances)
elif action == 'stop':
    stop_instances(instances)