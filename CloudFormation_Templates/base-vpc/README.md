# CloudFormation - Base VPCs

The 3 AWS CloudFormation stacks are nested stacks that create VPC's with the following resources:

* 2 public subnets (in different AZs for HA)
* 2 private subnets (also across those AZs)
* The needed Internet Gateway + NAT Gateways so the public/private subnets behave correctly.

This [vps.yaml](vps.yaml) fully builds out VPC1 with its subnets, IGW, and routing.
For VPC2 and VPC3, you just replicate the same subnet/IGW/route structure with their own CIDRs.

A parent stack defines 3 VPCs by reusing a nested stack template.
* The nested stack (a separate YAML file) handles:
  * VPC
  * 2 public subnets
  * 2 private subnets
  * Internet Gateway + public route table
  * Outputs for subnet IDs & VPC ID

Use the following steps to deploy the code:

* Upload vpc-module.yaml to an S3 bucket.
* Update TemplateURL in the parent (multi-vpc.yaml).
* Deploy multi-vpc.yaml.

