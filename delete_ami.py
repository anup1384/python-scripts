#!/usr/bin/python
import boto3
import datetime
import dateutil
from dateutil import parser
ec2_re=boto3.resource(service_name="ec2",region_name="ap-south-1")
ec2_cli=boto3.client("sts")
account_id=ec2_cli.get_caller_identity()["Account"]
#Get the 10 days old date
days=10
timeLimit=datetime.datetime.now() - datetime.timedelta(days=days)
for i in ec2_re.images.filter(Filters=[{'Name': 'tag:amitag', 'Values':['yes']},],Owners=[account_id]):
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
        print ("Only Deleting AMI which is older that", days)



            
