import boto3
from datetime import datetime
from pprint import pprint
ec2 = boto3.resource('ec2', region_name='ap-south-1')
volumes = ec2.volumes.all()
EbsReport = "The Following Ebs Volumes are Unused: \n"
today = datetime.now().date()
# print(dir(volumes))
for volume in volumes:
    if volume.state == 'available':
        in_tags=volume.tags
        name = 'unknown'
        for tag in in_tags:
            if ('Name' == tag['Key']) or ('name' == tag['Key']):
                name=(tag['Value'])
        EbsReport = EbsReport + "- " + "Name: " + str(name) +  " - Volume ID: " + str(volume.id) + " - Size: " + str(volume.size) + " - Created: " + str(volume.create_time.strftime('%Y/%m/%d %H:%M')) + "\n"        
print(EbsReport)