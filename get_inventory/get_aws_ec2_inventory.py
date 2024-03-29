"""Get AWS EC2 Instance definition aws

This script will get AWS EC2 instance definition data from an excel worksheet

It assumes there is a tab in the excel spreadsheet named EC2INSTANCES with named table defined.

This file can also be imported as a module and contains the following functions:

    * get_ec2_instance_ids - returns a array of EC2 instance IDs
    * main - The main function of the script
"""

import sys
import os
import boto3
import argparse
import configparser
import coloredlogs
import logging
from aws.ec2_instance import EC2Instance

# Constants
###############################################################################
#: This effectively defines the root of the project and so adding ..\, etc is not needed in config files
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
# Add script directory to the path to allow searching for modules
sys.path.insert(0, PROJECT_ROOT_DIR)
#: Directory that contains configuration files
CONF_DIR = os.path.join(PROJECT_ROOT_DIR, 'conf')

DEBUG = bool(os.environ.get('DEBUG', 'True'))
#: Directory were data files/extracts/reports will be stored
DATA_DIR = os.path.join(PROJECT_ROOT_DIR, 'data')

FILENAME_INPUT_CONFIG = os.environ.get('CONFIG_FILE_PATH',
                                       os.path.join(CONF_DIR, 'get_inventory.conf'))


def print_config_information(args, config):
    """Print configuraiton information for script"""
    logging.info("***** Printing Configuration Information ******")
    logging.info("Configuration => logging level:[%s]", args.logging.upper())
    logging.info("Configuration => Configuration filename:[%s]", args.filename_config)
    logging.info("Configuration => AWS Profile:[%s]", args.aws_profile)
    logging.info("Configuration => [PROJECT_ROOT_DIR:%s]", PROJECT_ROOT_DIR)
    logging.info("Configuration => [CONF_DIR:%s]", CONF_DIR)
    logging.info("Configuration => [DEBUG:%s]", DEBUG)
    logging.info("Configuration => [DATA_DIR:%s]", DATA_DIR)
    logging.info("AWS regions => [%s]", config.get('aws', 'aws_regions'))
    logging.info("AWS profiles => [%s]", config.get('aws', 'aws_account_profiles'))
    logging.info("***********************************************")
    logging.info("")


def main():
    ec2_instance = EC2Instance(ec2_instance_id="123", private_ip="privateIP")
    # Parse out CLI arguments
    parser = argparse.ArgumentParser(description='get_aws_ec2_inventory configuration')
    parser.add_argument('--log', '-l', dest='logging', action='store', default='INFO',
                        help='Logging verbosity: DEBUG, INFO, WARNING (default), ERROR, CRITICAL')
    parser.add_argument('--config', '-c', dest='filename_config', action='store', default=FILENAME_INPUT_CONFIG,
                        help='config file for script')
    parser.add_argument('--aws_profile', '-a', dest='aws_profile', action='store', default="prod",
                        help='aws profile to use')
    args = parser.parse_args()

    logging_level = getattr(logging, args.logging.upper(), None)
    logging.info("logging level:[%s]", logging_level)
    if not isinstance(logging_level, int):
        raise ValueError('Invalid log level: {}'.format(args.logging))

    coloredlogs.install(level=logging_level,
                        fmt="%(asctime)s %(hostname)s %(name)s %(filename)s line-%(lineno)d %(levelname)s - %(message)s",
                        datefmt='%H:%M:%S')
    config = configparser.ConfigParser()
    logging.info("Reading config file [%s]", args.filename_config)
    # Confirm config file exists before reading
    try:
        with open(args.filename_config) as f:
            config.read(args.filename_config)
    except Exception as e:
        logging.error("Error Reading config file [%s]: [%s]", args.filename_config, str(e))
        raise ValueError("Error Reading config file [%s]: [%s]", args.filename_config, str(e))
    print_config_information(args, config)

    aws_regions = config.get('aws', 'aws_regions').split(',')
    aws_account_profiles = config.get('aws', 'aws_account_profiles').split(',')
    for credentials in aws_account_profiles:
        logging.info('AWS account: %s', credentials)
        aws_session = boto3.Session(profile_name=credentials)
        #ec2_client = aws_session.client(service_name='iam')

if __name__ == "__main__":
    main()

 # aws_regions=config.get('aws','aws_regions').split(',')
 #
 #    aws_account_profiles=config.get('aws','aws_account_profiles').split(',')
 #
 #    aws_access_inventory = {}
 #
 #    logging.info('Open for writing - %s', config.get('aws_access', 'filename_output_csv'))
 #
 #    logging.info('Start polling AWS keys')
 #    for credentials in aws_account_profiles:
 #        logging.debug('AWS account: %s', credentials)
 #
 #        aws_session = boto3.Session(profile_name=credentials)
 #        ec2_client = aws_session.client(service_name='iam')
 #        response = ec2_client.list_users()
 #        logging.debug('response: %s', pprint.pformat(response))
 #
 #        for aws_user in response['Users']:
 #            user = UserAccess()
 #            logging.debug('user: %s', pprint.pformat(aws_user))
 #            user.account = credentials
 #            user.user_name = aws_user['UserName']
 #            user.last_login = aws_user.get('PasswordLastUsed').strftime('%m/%d/%Y') if aws_user.get('PasswordLastUsed') else ''
 #
 #            ### Get all groups this user belongs to
 #            groupResponse = ec2_client.list_groups_for_user(UserName=aws_user['UserName'])
 #            # Concatenate groups in a string
 #            aws_user_groups = []
 #            for aws_user_group in groupResponse['Groups']:
 #                aws_user_groups.append(aws_user_group.get('GroupName'))
 #            aws_user_groups.sort()
 #            user.groups = ' | '.join(aws_user_groups)
 #
 #            ### Determine if there is an inline policy on user.
 #            userPoliciesResponse = ec2_client.list_user_policies(UserName=aws_user['UserName'])
 #            aws_user_inline_policies = []
 #            for aws_user_inline_policy in userPoliciesResponse['PolicyNames']:
 #                aws_user_inline_policies.append(aws_user_inline_policy)
 #                aws_user_inline_policies.sort()
 #            user.inline_policies = ' | '.join(aws_user_inline_policies)
 #
 #            ### List directly attached user policies.
 #            userAttachedPoliciesResponse = ec2_client.list_attached_user_policies(UserName=aws_user['UserName'])
 #            aws_user_attached_policies = []
 #            for aws_user_attached_policy in userAttachedPoliciesResponse['AttachedPolicies']:
 #                aws_user_attached_policies.append(aws_user_attached_policy.get('PolicyName'))
 #                aws_user_attached_policies.sort()
 #            user.attached_policies = ' | '.join(aws_user_attached_policies)
 #
 #            aws_access_inventory[credentials + '-' + aws_user['UserName']] = user
 #
 #    logging.info('Writing inventory to json file: %s', config.get('aws_access', 'filename_output_json'))
 #
 #    rows = []
 #    aws_access_inventory_sorted = sorted(aws_access_inventory)
 #    for user in aws_access_inventory_sorted:
 #        user_object = aws_access_inventory.get(user)
 #        rows.append({'user_name':user_object.user_name,
 #                 'last_login':user_object.last_login,
 #                 'groups':user_object.groups,
 #                 'inline_policies':user_object.inline_policies,
 #                 'attached_policies':user_object.attached_policies})
 #
 #    user_row = RowSpec(ColumnSpec('user_name', 'User Name', width=1.3),
 #                         ColumnSpec('last_login', 'Last Login', width=1),
 #                         ColumnSpec('groups', 'Groups', width=1.7),
 #                         ColumnSpec('inline_policies', 'Inline Policies', width=1.5),
 #                         ColumnSpec('attached_policies', 'Attached Policies', width=1.5))
 #
 #    lines = user_row.makeall(rows)
 #
 #    outfile = open('aws_access_inventory.pdf', 'wb')
 #    outfile.write(PDFTable('AWS Access list', 'List of users, sorted by username', headers=user_row).render(lines))
