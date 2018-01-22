

from subprocess import call



instance_address = "ubuntu@ec2-52-207-239-48.compute-1.amazonaws.com"
aws_sshkey_location = "/Users/hongru.liu/Code/cloud_credentials/AWS/Adam_AWS.pem"

def access_aws():
	print("ssh -i", aws_sshkey_location, instance_address)
	call(["ls", "-l"])


def access_monsta_nectar():
	monsta_key_location = "/Users/hongru.liu/Code/cloud_credentials/Nectar/monsta.pem"
	monsta_address = "ubuntu@203.101.224.240"
	# print("ssh", "-i", monsta_key_location, monsta_address)
	# call(["du", "-sh", monsta_key_location])
	call(["scp", "-i", monsta_key_location, "/Users/hongru.liu/Code/cloud_credentials/Nectar/some.sh", "monsta_address" + ":/home/ubuntu/install/"])
	# call(["ssh -i", monsta_key_location, monsta_address])

access_monsta_nectar()