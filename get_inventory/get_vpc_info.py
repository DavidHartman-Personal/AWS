import sys
import os
import boto3
import configparser

# The AWS profiles to use
aws_profile_list = ['ptc-ms-dev']

def get_session_token():
    # Open config file and replace DEFAULT section
    homedir = os.path.expanduser('~')
    separator = os.path.sep

    configFilePath = homedir + separator + '.aws' + separator + 'config'
    config = configparser.ConfigParser()
    config.read(configFilePath)

    profile = input('Enter one of your profiles' + str(config.sections()).strip('[]') + ": ")

    session = boto3.Session(profile_name=profile)
    client = session.client('sts')

    mfaCode = input("Enter the MFA code: ")

    response = client.get_session_token(
            DurationSeconds=3600,
            SerialNumber=config[profile]['mfa_serial'],
            TokenCode=mfaCode
    )
    print("aws_access_key_id = " + response.get("Credentials").get("AccessKeyId"))
    print("aws_secret_access_key = " + response.get("Credentials").get("SecretAccessKey"))
    print("aws_session_token = " + response.get("Credentials").get("SessionToken"))
    return(response.get("Credentials").get("AccessKeyId"),
           response.get("Credentials").get("SecretAccessKey"),
           response.get("Credentials").get("SessionToken"))
    # credFilePath = homedir + separator + '.aws' + separator + 'credentials'
    # credentials = configparser.ConfigParser()
    # credentials.read(credFilePath)
    #
    # credentials['default']['AWS_ACCESS_KEY_ID'] = response.get("Credentials").get("AccessKeyId")
    # credentials['default']['AWS_SECRET_ACCESS_KEY'] = response.get("Credentials").get("SecretAccessKey")
    # credentials['default']['AWS_SESSION_TOKEN'] = response.get("Credentials").get("SessionToken")
    #
    # with open(credFilePath, 'w') as configfile:
    #     credentials.write(configfile)

    print("Profile 'default' has been updated successfully with session credentials.")


if __name__ == "__main__":
    for aws_profile in aws_profile_list:
        print("Connecting to AWS using profile: " + aws_profile)
        (aws_access_key_id,aws_secret_access_key,aws_session_token) = get_session_token()

        # aws_session = boto3.Session(aws_access_key_id='AKIA2QFUTHJPG67QNCLJ',
        #                             aws_secret_access_key='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',
        #                             aws_session_token='FwoGZXIvYXdzEMf//////////wEaDIWsReCO4J+sR3OjCSKGAVtexubEU6bDMEt7A3lpKyYd8K27mhzHoTWAjRVTGs98JitdxUPupk68g/id7/m0C5qg7bUEEcfTJq5X5W5eXKlgJY54/8EJf0ZLJomiB5lFEDnQxfEvVR1Jw5eId0AS9iimQzq2nKVjJnDhMgc1cjKNnJZy4zcg3x8trw3Dc32VgAKudI+pKMS+4PEFMii5lpMPMvxjo5VFnZ2CSCBtrMNDFMUfsCDR4hCyObLgwp2KiAItmPbX',
        #                             region_name='us-west-2')
        # ec2_client = aws_session.client(service_name='ec2')
        # iam_client = aws_session.client(service_name='iam')
        # account_name = iam_client.list_account_aliases()['AccountAliases'][0]
        # print("account:" + account_name)
        # regions = ec2_client.describe_regions()
        # for region in regions:
        #     print("Region: " + region)

    # ec2_list_instances_paginator = ec2_client.get_paginator('describe_instances')
    # ec2_list_instances_iterator = ec2_list_instances_paginator.paginate()
    # for ec2_list_instances in ec2_list_instances_iterator:
    #     for ec2_reservations in ec2_list_instances['Reservations']:
    #         for ec2_instance in ec2_reservations['Instances']:
    #             get_root_attr(ec2_instance)
    #             # print(str(ec2_instance.get('InstanceId')))

    # all_subnets = ec2_client.describe_subnets()
    #
    # ec2_subnet_list_paginator = ec2_client.get_paginator('describe_subnets')
    # ec2_list_subnets_iterator = ec2_subnet_list_paginator.paginate()
    # for ec2_list_subnets in ec2_list_subnets_iterator:
    #     for subnet in ec2_list_subnets['Subnets']:
    #         get_root_attr(subnet)
    #     # for key, value in attribute_definitions.items():
    #     #     print("Key:" + key + " value: " + str(value))
    #     print()
    #     class_def_string = "class {class_name}:"
    #     init_string = "{attribute_name}=\"\","
    #     init_method_def = "  def __init__(self,"
    #     print(class_def_string.format(class_name="EC2_Subnet"))
    #     print()
    #     print()
    #     print(init_method_def)
    #     for attribute_name in attribute_definitions.keys():
    #         print(init_string.format(attribute_name=attribute_name))
    #     # for ec2_reservations in ec2_list_instances['Reservations']:
    #     #     for ec2_instance in ec2_reservations['Instances']:
    #     #         get_root_attr(ec2_instance)
    #             # print(str(ec2_instance.get('InstanceId')))



