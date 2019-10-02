#!/usr/bin/python
import boto3
ec2_re=boto3.resource(service_name="ec2",region_name="ap-south-1")
ec2_cli=boto3.client("sts")
account_id=ec2_cli.get_caller_identity()["Account"]
for i in ec2_re.images.filter(Filters=[{'Name': 'tag:amitag', 'Values':['yes']},],Owners=[account_id]):
    print("List of amiIds to be delete", i.id)
   
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



            
