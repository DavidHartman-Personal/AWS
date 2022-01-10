import sys
import os
import boto3
import argparse
import configparser
import coloredlogs
import logging

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

def get_hosted_zone_record_sets(r53_client, hosted_zone_id):
    return_record_sets = []
    r53_record_sets_paginator = r53_client.get_paginator('list_resource_record_sets')
    r53_record_sets_iterator = r53_record_sets_paginator.paginate(HostedZoneId=hosted_zone_id)
    for r53_record_sets in r53_record_sets_iterator:
        for r53_record_set in r53_record_sets['ResourceRecordSets']:
            return_record_sets.append(r53_record_set)
            # record_set = {}
            # record_set['Name'] = r53_record_set.get('Name')
            # record_set['Type'] = r53_record_set.get('Type')
            # record_set['TTL'] = r53_record_set.get('TTL')
            # record_set['ResourceRecords'] = r53_record_set.get('ResourceRecords')

            # record_set_type = r53_record_set.get('SetIdentifier')
            # record_set_type = r53_record_set.get('Weight')
            # record_set_type = r53_record_set.get('Region')
            # record_set_type = r53_record_set.get('GeoLocation')
            # record_set_type = r53_record_set.get('Failover')
            # record_set_type = r53_record_set.get('MultiValueAnswer')
            # record_set_type = r53_record_set.get('TTL')
            # record_set_type = r53_record_set.get('ResourceRecords')
            # record_set_type = r53_record_set.get('AliasTarget')
            # record_set_type = r53_record_set.get('HealthCheckId')
            # record_set_type = r53_record_set.get('TrafficPolicyInstanceId')
    return return_record_sets


def get_hosted_zones(r53_client):
    return_hosted_zones = {}
    r53_hosted_zones_paginator = r53_client.get_paginator('list_hosted_zones')
    r53_hosted_zone_iterator = r53_hosted_zones_paginator.paginate()
    for r53_hosted_zones in r53_hosted_zone_iterator:
        for r53_hosted_zone in r53_hosted_zones['HostedZones']:
            return_hosted_zone = {}
            return_hosted_zone['Id'] = r53_hosted_zone.get('Id')
            return_hosted_zone['Name'] = r53_hosted_zone.get('Name')
            return_hosted_zone['ResourceRecordSetCount'] = r53_hosted_zone.get('ResourceRecordSetCount')
            return_hosted_zones[r53_hosted_zone.get('Id')] = return_hosted_zone
    return return_hosted_zones


def create_r53_client(profile_name):
    aws_session = boto3.Session(profile_name=profile_name)
    ec2_client = aws_session.client(service_name='iam')
    account_name = ec2_client.list_account_aliases()['AccountAliases'][0]
    return aws_session.client(service_name='route53')

def main():
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
        ec2_client = aws_session.client(service_name='iam')
        # Lookup the account aliases which provides the name of the AWS Account
        # Note that currently there is only one entry
        account_name = ec2_client.list_account_aliases()['AccountAliases'][0]
        logging.info('Looking up Route53 hosted zones in [%s]', account_name)
        r53_client = aws_session.client(service_name='route53')
        r53_hosted_zones_paginator = r53_client.get_paginator('list_hosted_zones')
        r53_hosted_zone_iterator = r53_hosted_zones_paginator.paginate()
        for r53_hosted_zones in r53_hosted_zone_iterator:
            for r53_hosted_zone in r53_hosted_zones['HostedZones']:
                hosted_zone_id = r53_hosted_zone.get('Id')
                hosted_zone_name = r53_hosted_zone.get('Name')
                hosted_zone_record_set_count = r53_hosted_zone.get('ResourceRecordSetCount')

                r53_record_sets_paginator = r53_client.get_paginator('list_resource_record_sets')
                r53_record_sets_iterator = r53_record_sets_paginator.paginate(HostedZoneId=hosted_zone_id)
                for r53_record_sets in r53_record_sets_iterator:
                    for r53_record_set in r53_record_sets['ResourceRecordSets']:
                        record_set_name = r53_record_set.get('Name')
                        record_set_type = r53_record_set.get('Type')
                        record_set_type = r53_record_set.get('SetIdentifier')
                        record_set_type = r53_record_set.get('Weight')
                        record_set_type = r53_record_set.get('Region')
                        record_set_type = r53_record_set.get('GeoLocation')
                        record_set_type = r53_record_set.get('Failover')
                        record_set_type = r53_record_set.get('MultiValueAnswer')
                        record_set_type = r53_record_set.get('TTL')
                        record_set_type = r53_record_set.get('ResourceRecords')
                        record_set_type = r53_record_set.get('AliasTarget')
                        record_set_type = r53_record_set.get('HealthCheckId')
                        record_set_type = r53_record_set.get('TrafficPolicyInstanceId')
#                        logging.info("Found record set [%s]", record_set_name)



if __name__ == "__main__":
    main()

