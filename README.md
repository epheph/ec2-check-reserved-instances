ec2-check-reserved-instances
============================

EC2 Check Reserved Instances - Compare instance reservations with running instances

Amazon's reserved instances (ec2-describe-reserved-instances, ec2-describe-reserved-instances-offerings) are a great way to save money when using EC2. An EC2 instance reservation is specified by an availability zone, instance type, and quantity. Correlating the reservations you currently have active with your running instances is a manual, time-consuming, and error prone process.

This quick little Python script uses boto to inspect your reserved instances and running instances to determine if you currently have any reserved instances which are not being used. Additionally, it will give you a list of non-reserved instances which could be reserved.

To use the program, make sure you install boto:

$ easy_install boto

or

$ pip install boto



The only configuration needed is your AWS keys. These can either be modified at the top of the file, ec2-check-reserved-instances.py, or by exporting your keys in an environment variable:

$ export AWSAccessKeyId=1234567
$ export AWSSecretKey=j3jfijfisa83j+io4jfioajioaw


