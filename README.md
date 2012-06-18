ec2-check-reserved-instances
============================

EC2 Check Reserved Instances - Compare instance reservations with running instances

Amazon's reserved instances (ec2-describe-reserved-instances, ec2-describe-reserved-instances-offerings) are a great way to save money when using EC2. An EC2 instance reservation is specified by an availability zone, instance type, and quantity. Correlating the reservations you currently have active with your running instances is a manual, time-consuming, and error prone process.

This quick little Python script uses boto to inspect your reserved instances and running instances to determine if you currently have any reserved instances which are not being used. Additionally, it will give you a list of non-reserved instances which could benefit from additional reserved instance allocations.

To use the program, make sure you have boto installed. If you don't already have it, run:

$ easy_install boto

or

$ pip install boto



The only configuration needed is your AWS keys. These can either be modified at the top of the file, ec2-check-reserved-instances.py, or by exporting your keys in an environment variable:

$ export AWSAccessKeyId=1234567

$ export AWSSecretKey=j3jfijfisa83j+io4jfioajioaw

EXAMPLE OUTPUT
===============
```
vela:~/dev epheph$ ./ec2-check-reserved-instances.py Disqualifying instance i-8bbd8ce7: not running
UNUSED RESERVATION!	(1)	m1.small	us-east-1b
UNUSED RESERVATION!	(1)	m2.xlarge	us-east-1a

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
- Add VPC support
- Currently only supports US-EAST. Make using other regions easy, perhaps just using an environment variable/internal config variable
- External config? Is there some standard place to store AWS credentials?
- Add option to use API to purchase the additional reservations (need to be EXTREMELY careful here, any mistake or miscommunication could cost quite a bit of money)
- Windows? Not taking Windows reserved instances into account
