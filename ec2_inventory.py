#/usr/bin/python
import boto3
from pprint import pprint
import csv
#session =boto3.session.Session()
ec2_re=boto3.resource(service_name="ec2", region_name="ap-south-1")
#print(dir(ec2_re))
header_csv=['S_No','Instance-Name','Instance-ID','Private-IP','Instance-Type','Instance-Role','Environment']
S_No=1
fo=open("ec2_inv.csv","wb")
csv_w=csv.writer(fo)
csv_w.writerow(header_csv)
for each_in in ec2_re.instances.all():
    in_id=each_in.instance_id
    in_type=each_in.instance_type
    in_tags=each_in.tags
    in_ip=each_in.private_ip_address
    name = 'unknown'
    role = 'unknown'
    environment = 'unknown'
    for tag in in_tags:
        
        if 'Name' == tag['Key']:
            name=(tag['Value'])
        if 'role' == tag['Key']:
            role=(tag['Value'])
        if 'environment' == tag['Key']:
            environment=(tag['Value'])
                        
    print (S_No,name,in_id,in_ip,in_type,role,environment)
    csv_w.writerow([S_No,name,in_id,in_ip,in_type,role,environment])
    S_No +=S_No
#    pprint (dir(each_in))
#   break
fo.close()