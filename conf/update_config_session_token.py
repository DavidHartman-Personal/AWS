import os
import boto3
import configparser

# Open config file and replace DEFAULT section
FEDRAMP_CMDBS_ROOT_DIR = "C:\\Users\\dhartman\\Documents\\FedRAMP\\CMDB\\"

AWS_CONFIG_ROOT = "C:\\Users\\dhartman\\.aws"
CREDENTIALS_CONFIG = "credentials.cfg"
CREDENTIALS_FILE = "credentials"
COMMENT_DELIMITER = "#"

# configFilePath = homedir + separator + '.aws' + separator + 'config'
credentials_file_full_path = os.path.join(AWS_CONFIG_ROOT, CREDENTIALS_FILE)
cred_config_file_full_path = os.path.join(AWS_CONFIG_ROOT, CREDENTIALS_CONFIG)

cred_config = configparser.ConfigParser()
credentials = configparser.ConfigParser(allow_no_value=True)

credentials.read(credentials_file_full_path)
cred_config.read(cred_config_file_full_path)

aws_configs = cred_config.sections()

def get_profile(in_config_names):
    invalid_profile = True
    return_profile = ""
    while invalid_profile:
        print("Choose one of the following profiles to generate an STS Token for:")
        for ind in range(len(in_config_names)):
            print(str(ind) + ". " + in_config_names[ind])
        in_profile_ind = input('Enter the number of the profile:')
        if int(in_profile_ind) in range(0, len(in_config_names)):
            invalid_profile = False
            profile_name = in_config_names[int(in_profile_ind)]
            if profile_name == "default":
                return_profile = "default"
            else:
                return_profile = in_config_names[int(in_profile_ind)]
        else:
            print("Invalid selection.")
        # if in_profile == "":
        #     return_profile = "default"
        #     invalid_profile = False
        # else:
        #     if in_profile in in_config_names:
        #         invalid_profile = False
        #         return_profile = "profile " + in_profile
        #     else:
        #         print("Invalid profile entered")
    return return_profile


def update_default_profile():
    invalid_response = True
    while invalid_response:
        update_default_profile_response = input("Update default profile? [y/n]")
        if update_default_profile_response.lower() not in ("y","n"):
            print("Invalid default profile update response [y/n]")
            invalid_response = True
        elif update_default_profile_response.lower() == "y":
            return True
        else:
            return False


if __name__ == "__main__":
    clean_config_names = [value.strip('[]').strip() for value in aws_configs]
    # profile = get_profile(clean_config_names)
    # temp hardcode to dev
    profile = "ptc-ms-dev-non-mfa"
    target_profile = cred_config["profile-mapping"][profile]
    # print("target:" + target_profile)
    print("Generating token for: " + target_profile + " using non-mfa profile: " + profile)
    mfa_serial_arn = cred_config[profile]['mfa_serial']
    aws_access_key = cred_config[profile]['aws_access_key_id']
    aws_secret_access_key = cred_config[profile]['aws_secret_access_key']
    mfaCode = input("Enter the MFA Token for profile [" + profile + "]:")
    sts_client = boto3.client('sts',
                              aws_access_key_id=aws_access_key,
                              aws_secret_access_key=aws_secret_access_key
                              )
    response = sts_client.get_session_token(
            DurationSeconds=43200,
            SerialNumber=mfa_serial_arn,
            TokenCode=mfaCode)
    aws_access_key_target = response.get("Credentials").get("AccessKeyId")
    aws_secret_access_key_target = response.get("Credentials").get("SecretAccessKey")
    aws_session_token_target = response.get("Credentials").get("SessionToken")
    expiration_datetime = response.get("Credentials").get("Expiration")

    # import datetime
    # import dateutil
    # import pytz
    # local_expire_datetime = expiration_datetime.astimezone
    #
    # print("time:" + str(local_expire_datetime) + " expiration local timezone: " + str(local_expire_datetime.tzname()))
    # expiration_datetime_str = "{COMMENT_DELIMITER} The token expires at [{EXPIRE_DATETIME}]"
    # expiration_datetime_config_entry = expiration_datetime_str.format(COMMENT_DELIMITER=COMMENT_DELIMITER,
    #                                                                   EXPIRE_DATETIME=str(expiration_datetime))
    # print(expiration_datetime_config_entry)

    # Update default and named profile...leave others as is
    if update_default_profile():
        print("Updating default profile")
        credentials['default']['# Expiration Timestamp:'] = str(expiration_datetime)  # expiration_datetime_config_entry
        credentials['default']['AWS_ACCESS_KEY_ID'] = aws_access_key_target
        credentials['default']['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key_target
        credentials['default']['AWS_SESSION_TOKEN'] = aws_session_token_target

    credentials[target_profile]['# Expiration Timestamp:'] = str(expiration_datetime)  # expiration_datetime_config_entry
    credentials[target_profile]['AWS_ACCESS_KEY_ID'] = aws_access_key_target
    credentials[target_profile]['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key_target
    credentials[target_profile]['AWS_SESSION_TOKEN'] = aws_session_token_target
    with open(credentials_file_full_path, 'w') as configfile:
        credentials.write(configfile)
#
# print("Profile 'default' has been updated successfully with session credentials.")
 # iam_client = boto3.client('iam',
    #                           aws_access_key_id=aws_access_key,
    #                           aws_secret_access_key=aws_secret_access_key
    #                           #                           aws_session_token=SESSION_TOKEN
    #                           )
# client = sts_session.client('sts')
# iam_client = session.client('iam')
# mfa_device = iam_client.list_mfa_devices(UserName='dhartman')
# print(str(mfa_device))
#  mfaCode = input("Enter the MFA Token for profile [" + profile + "]:")
