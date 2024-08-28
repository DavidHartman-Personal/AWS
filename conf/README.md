This folder contains files used for configuration of various scripts, etc for this project.  

- [ ] Order of determining which profile to use.
- [ ] Create environment variable to show current profile that will be used for aws commands and add this to the prompt (PS1)

TODO: adding one from readme


## Configuration

- Configuration related files - config, credentials, etc
- Customizing configurations
- Order of processing to determine profile to use (e.g. Env vars, --profile, etc.)

The AWS CLI uses credentials and configuration settings located in multiple places, such as the system or user environment variables, local AWS configuration files, or explicitly declared on the command line as a parameter. Certain locations take precedence over others. The AWS CLI credentials and configuration settings take precedence in the following order:
1. Command line options – Overrides settings in any other location. You can specify --region, --output, and --profile as parameters on the command line.
2. Environment variables – You can store values in your system's environment variables.
3. CLI credentials file – The credentials and config file are updated when you run the command aws configure. The credentials file is located at ~/.aws/credentials on Linux or macOS, or at C:\Users\USERNAME\.aws\credentials on Windows. This file can contain the credential details for the default profile and any named profiles.
4. CLI configuration file – The credentials and config file are updated when you run the command aws configure. The config file is located at ~/.aws/config on Linux or macOS, or at C:\Users\USERNAME\.aws\config on Windows. This file contains the configuration settings for the default profile and any named profiles.
5. Container credentials – You can associate an IAM role with each of your Amazon Elastic Container Service (Amazon ECS) task definitions. Temporary credentials for that role are then available to that task's containers. For more information, see IAM Roles for Tasks in the Amazon Elastic Container Service Developer Guide.
6. Instance profile credentials – You can associate an IAM role with each of your Amazon Elastic Compute Cloud (Amazon EC2) instances. Temporary credentials for that role are then available to code running in the instance. The credentials are delivered through the Amazon EC2 metadata service. For more information, see IAM Roles for Amazon EC2 in the Amazon EC2 User Guide for Linux Instances and Using Instance Profiles in the IAM User Guide.

### Environment variables

`AWS_PROFILE` - Specifies the name of the AWS CLI profile with the credentials and options to use. This can be the name of a profile stored in a credentials or config file, or the value default to use the default profile.

If defined, this environment variable overrides the behavior of using the profile named [default] in the configuration file. You can override this environment variable by using the --profile command line parameter.

```
export AWS_ACCESS_KEY_ID=<Key>
export AWS_SECRET_ACCESS_KEY=<Secret Key>
export AWS_DEFAULT_REGION=<Default Region>
```

### profiles

To list/show the current defined profiles
```
aws configure list
```

To list/show the named profiles defined.
```
aws configure list-profiles
```

Creating alias to define a particular profile.

```
alias aws='aws --profile dave-personal '
alias aws='aws --profile usaid-ghsc-dhartman-dev '
```

## Install/Setup AWS CLI


### AWS CLI V2

Change to a good directory to download the aws cli zip file.

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

