ec2-check-reserved-instances
============================

EC2 Check Reserved Instances - Compare instance reservations with running instances

Amazon's reserved instances (ec2-describe-reserved-instances, ec2-describe-reserved-instances-offerings) are a great way to save money when using EC2. An EC2 instance reservation is specified by an availability zone, instance type, and quantity. Correlating the reservations you currently have active with your running instances is a manual, time-consuming, and error prone process.

This quick little Python script uses boto to inspect your reserved instances and running instances to determine if you currently have any reserved instances which are not being used. Additionally, it will give you a list of non-reserved instances which could benefit from additional reserved instance allocations.

To use the program, make sure you have boto installed. If you don't already have it, run:

$ easy_install boto

or

$ pip install boto



The script will attempt to use the environment variables AWSAccessKeyId and AWSSecretKey. If these are not present it will fall back to using config details from the 'aws' cli tool ( ~/.aws/config ) 

Either:

$ export AWSAccessKeyId=1234567
$ export AWSSecretKey=j3jfijfisa83j+io4jfioajioaw

Or, put in: ~/.aws/config :
```
[default]
aws_access_key_id = 1234567
aws_secret_access_key = j3jfijfisa83j+io4jfioajioaw
region = eu-west-1
output = json
```


EXAMPLE OUTPUT
===============
```
vela:~/dev epheph$ ./ec2-check-reserved-instances.py
UNUSED RESERVATION!	(1)	m1.small	us-east-1b
UNUSED RESERVATION!	(1)	m2.2xlarge	us-east-1a

Instance not reserved:	(1)	t1.micro	us-east-1c
Instance not reserved:	(2)	m1.small	us-east-1d
Instance not reserved:	(3)	m1.medium	us-east-1d
Instance not reserved:	(1)	m2.2xlarge	us-east-1b

(23) running on-demand instances
(18) reservations
```

In this example, you can easily see that an m2.2xlarge was spun up in the wrong AZ (us-east-1b vs. us-east-1a), as well as an m1.small. The "Instance not reserved" section shows that you could benefit from reserving:
* (1) t1.micro
* (1) m1.small (not 2, since you'll likely want to move your us-east-1b small to us-east-1d)
* (3) m1.medium


TODO
===============
- Add some sort of sorting, by Availability Zone/instance type
- Add option to use API to purchase the additional reservations (need to be EXTREMELY careful here, any mistake or miscommunication could cost quite a bit of money)
- Windows? Not taking Windows reserved instances into account
