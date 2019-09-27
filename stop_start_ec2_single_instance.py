#!/usr/local/opt/python/bin/python3.7
import boto3
ec2_re = boto3.resource(service_name="ec2", region_name="ap-south-1")
#print(dir(ec2_re))
instance_id=input("Enter your Instance ID for action: ")
my_instance=ec2_re.Instance(id=instance_id)
# print(dir(my_instance))
instance_state=my_instance.state['Name']
if instance_state == 'stopped':
    print("Starting Instance", instance_id)
    my_instance.start()
    my_instance.wait_until_running()
    print("Instance Started", instance_id)
else :
    print("Stopping Instance", instance_id)
    my_instance.stop()
    my_instance.wait_until_stopped()
    print("Instance Stopped", instance_id)
