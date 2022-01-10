import sys
import os
import boto3



subnets_list_test = []
subnet_1 =  {'AvailabilityZone': 'eu-west-2a', 'AvailabilityZoneId': 'euw2-az2', 'AvailableIpAddressCount': 10,
         'CidrBlock': '10.118.19.0/28', 'DefaultForAz': False, 'MapPublicIpOnLaunch': False, 'State': 'available', 'SubnetId': 'subnet-e3d13a98', 'VpcId': 'vpc-f4e0279d', 'OwnerId': '717934610271', 'AssignIpv6AddressOnCreation': False, 'Ipv6CidrBlockAssociationSet': [], 'Tags': [{'Key': 'Name', 'Value': 'eulon-thingworx-axa-a'}], 'SubnetArn': 'arn:aws:ec2:eu-west-2:717934610271:subnet/subnet-e3d13a98'}
subnet_2 = {'AvailabilityZone': 'eu-west-2b', 'AvailabilityZoneId': 'euw2-az3', 'AvailableIpAddressCount': 251, 'CidrBlock': '10.118.17.0/24', 'DefaultForAz': False, 'MapPublicIpOnLaunch': False, 'State': 'available', 'SubnetId': 'subnet-5be9e411', 'VpcId': 'vpc-f4e0279d', 'OwnerId': '717934610271', 'AssignIpv6AddressOnCreation': False, 'Ipv6CidrBlockAssociationSet': [], 'Tags': [{'Key': 'Description', 'Value': 'Public subnet b for eulon ThingWorx'}, {'Key': 'Name', 'Value': 'eulon-thingworx-b'}], 'SubnetArn': 'arn:aws:ec2:eu-west-2:717934610271:subnet/subnet-5be9e411'}
subnets_list_test.append(subnet_1)
subnets_list_test.append(subnet_2)

attribute_definitions = {}

def get_root_attr(ec2_instance_object):
    for key, value in ec2_instance_object.items():
        if not attribute_definitions.get(key):
            attribute_definitions[key] = [value]
        else:
            attribute_definitions.get(key).append(value)

    # for key in ec2_instance_object.keys():
    #     # so if the type is an "attribute" then we can just mark it as a class attribute
    #     print(key)

if __name__ == "__main__":
    aws_account_profile = "prod"
    aws_session = boto3.Session(profile_name=aws_account_profile,region_name='eu-west-2')
    ec2_client = aws_session.client(service_name='ec2')
    iam_client = aws_session.client(service_name='iam')
    account_name = iam_client.list_account_aliases()['AccountAliases'][0]
    print("account:" + account_name)
    # ec2_list_instances_paginator = ec2_client.get_paginator('describe_instances')
    # ec2_list_instances_iterator = ec2_list_instances_paginator.paginate()
    # for ec2_list_instances in ec2_list_instances_iterator:
    #     for ec2_reservations in ec2_list_instances['Reservations']:
    #         for ec2_instance in ec2_reservations['Instances']:
    #             get_root_attr(ec2_instance)
    #             # print(str(ec2_instance.get('InstanceId')))

    all_subnets = ec2_client.describe_subnets()

    ec2_subnet_list_paginator = ec2_client.get_paginator('describe_subnets')
    ec2_list_subnets_iterator = ec2_subnet_list_paginator.paginate()
    for ec2_list_subnets in ec2_list_subnets_iterator:
        for subnet in ec2_list_subnets['Subnets']:
            get_root_attr(subnet)
        # for key, value in attribute_definitions.items():
        #     print("Key:" + key + " value: " + str(value))
        print()
        class_def_string = "class {class_name}:"
        init_string = "{attribute_name}=\"\","
        init_method_def = "  def __init__(self,"
        print(class_def_string.format(class_name="EC2_Subnet"))
        print()
        print()
        print(init_method_def)
        for attribute_name in attribute_definitions.keys():
            print(init_string.format(attribute_name=attribute_name))
        # for ec2_reservations in ec2_list_instances['Reservations']:
        #     for ec2_instance in ec2_reservations['Instances']:
        #         get_root_attr(ec2_instance)
                # print(str(ec2_instance.get('InstanceId')))



