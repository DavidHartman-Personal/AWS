import sys
import os
import boto3
import argparse
import configparser
import coloredlogs
import logging
import get_inventory.setup_aws_connection

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


if __name__ == "__main__":
    r53_client = get_inventory.setup_aws_connection.create_r53_client("prod")
    hosted_zones = get_inventory.setup_aws_connection.get_hosted_zones(r53_client)
    record_set_search_string = "innio"
    # https://innio.ptcmscloud.com/Windchill or https://innio-pf.ptcmscloud.com
    for zone_id in hosted_zones:
        hosted_zone = hosted_zones[zone_id]
        record_sets = get_inventory.setup_aws_connection.get_hosted_zone_record_sets(r53_client, zone_id)
        for rs in record_sets:
            if "innio" in rs['Name']:
                print(hosted_zone['Name'] + " => " + str(rs))

                # print("Hosted zone [{}] has [{}] records".format(hosted_zone['Name'], hosted_zone['ResourceRecordSetCount']))
                # hosted_zone_id_search = "/hostedzone/Z25FRYMHKQEZP8"


