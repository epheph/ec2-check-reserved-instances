from __future__ import print_function
import sys
import os
import boto3
from pprint import pprint

ec2_conn = boto3.client('ec2')
debug = False

def lambda_handler(event, context):
    reservations = ec2_conn.describe_instances()
    running_instances = {}
    for reservation in reservations['Reservations']:
    	for instance in reservation['Instances']:
    		if debug:
        		if instance['State']['Name'] != "running":
        			print("Disqualifying instance %s: not running" % ( instance['InstanceId'] ) )
        		elif 'SpotInstanceRequestId' in instance:
        			print("Disqualifying instance %s: spot" % ( instance['InstanceId'] ) )
    		if instance['State']['Name'] == "running" and not 'SpotInstanceRequestId' in instance:
				az = instance['Placement']['AvailabilityZone']
				if 'VpcId' in instance:
				    az = az + '_vpc'
				if 'Platform' in instance:
				    az = az + '_windows'
				instance_type = instance['InstanceType']
				running_instances[ (instance_type, az ) ] = running_instances.get( (instance_type, az ) , 0 ) + 1
    
    
    # pprint( running_instances )
    
    
    reserved_instances = {}
    reserved_list = ec2_conn.describe_reserved_instances()
    for reserved_instance in reserved_list['ReservedInstances']:
    	if debug and reserved_instance['State'] != "active":
    		print( "Excluding reserved instances %s: no longer active" % ( reserved_instance['ReservedInstancesId'] ) )
    	if reserved_instance['State'] == "active":
    		az = reserved_instance['AvailabilityZone']
    		if 'VPC' in reserved_instance['ProductDescription']:
    		    az = az + '_vpc'
    		if 'Windows' in reserved_instance['ProductDescription']:
    		    az = az + '_windows'
    		instance_type = reserved_instance['InstanceType']
    		reserved_instances[( instance_type, az) ] = reserved_instances.get ( (instance_type, az ), 0 )  + reserved_instance['InstanceCount']
    
    # pprint( reserved_instances )
    
    
    # this dict will have a positive number if there are unused reservations
    # and negative number if an instance is on demand
    instance_diff = dict([(x, reserved_instances[x] - running_instances.get(x, 0 )) for x in reserved_instances])
    
    # instance_diff only has the keys that were present in reserved_instances. There's probably a cooler way to add a filtered dict here
    for placement_key in running_instances:
    	if not placement_key in reserved_instances:
    		instance_diff[placement_key] = -running_instances[placement_key]
    
    # pprint ( instance_diff )
    
    unused_reservations = dict((key,value) for key, value in instance_diff.iteritems() if value > 0)
    if unused_reservations == {}:
    	print("Congratulations, you have no unused reservations")
    else:
    	for unused_reservation in unused_reservations:
    		print("UNUSED RESERVATION!\t(%s)\t%s\t%s" % ( unused_reservations[ unused_reservation ], unused_reservation[0], unused_reservation[1] ))
    
    print("")
    
    unreserved_instances = dict((key,-value) for key, value in instance_diff.iteritems() if value < 0)
    if unreserved_instances == {}:
    	print("Congratulations, you have no unreserved instances")
    else:
    	for unreserved_instance in unreserved_instances:
    		print("Instance not reserved:\t(%s)\t%s\t%s" % ( unreserved_instances[ unreserved_instance ], unreserved_instance[0], unreserved_instance[1] ))
    
    qty_running_instances = reduce( lambda x, y: x+y, running_instances.values() )
    qty_reserved_instances = reduce( lambda x, y: x+y, reserved_instances.values() )
    
    print("\n(%s) running on-demand instances\n(%s) reservations" % ( qty_running_instances, qty_reserved_instances ))
