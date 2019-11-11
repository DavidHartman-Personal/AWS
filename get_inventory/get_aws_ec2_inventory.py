"""Get AWS EC2 Instance definition aws

This script will get AWS EC2 instance definition data from an excel worksheet

It assumes there is a tab in the excel spreadsheet named EC2INSTANCES with named table defined.

This file can also be imported as a module and contains the following functions:

    * get_ec2_instance_ids - returns a array of EC2 instance IDs
    * main - The main function of the script
"""

import sys
import os
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


def print_config_information(args):
    """Print configuraiton information for script"""
    logging.info("***** Printing Configuration Information ******")
    logging.info("Configuration => logging level:[%s]", args.logging.upper())
    logging.info("Configuration => Configuration filename:[%s]", args.filename_config)
    logging.info("Configuration => AWS Profile:[%s]", args.aws_profile)
    logging.info("Configuration => [PROJECT_ROOT_DIR:%s]", PROJECT_ROOT_DIR)
    logging.info("Configuration => [CONF_DIR:%s]", CONF_DIR)
    logging.info("Configuration => [DEBUG:%s]", DEBUG)
    logging.info("Configuration => [DATA_DIR:%s]", DATA_DIR)
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
    print_config_information(args)

    logging.info("Reading config file [%s]", args.filename_config)
    # Confirm config file exists before reading
    try:
        with open(args.filename_config) as f:
            config.read(args.filename_config)
    except Exception as e:
        logging.error("Error Reading config file [%s]: [%s]", args.filename_config, str(e))
        raise ValueError("Error Reading config file [%s]: [%s]", args.filename_config, str(e))

if __name__ == "__main__":
    main()