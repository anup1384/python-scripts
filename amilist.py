#!/usr/bin/python
import boto3
ec2_re=boto3.resource(service_name="ec2",region_name="ap-south-1")
ec2_cli=boto3.client("sts")
account_id =ec2_cli.get_caller_identity()["Account"]
print("List of ami available")
count=1
for i in ec2_re.images.filter(Owners=[account_id]):
    print(count, i.id)
    count +=count