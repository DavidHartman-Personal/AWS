class R53HostZone:
    """
    A class for capturing EC2 Instance information from an excel spreadsheet tab

    This class is used for capturing information from an excel worksheet that contains details for AWS EC2 instances
    that are defined in a single Worksheet.

    Attributes
    ----------
    ec2_instance_id : str
        The AWS EC2 Instance ID
    private_ip : str
        The private IP address of the EC2 instance
    subnet_id : str
        The AWS subnet ID for the EC2 instance
    subnet_cidr : str
        The subnet CIDR for the subnet the instance is in.  This will be in xx.xx.xx.xx/xx format.

    Methods
    -------
    update_subnet(subnet_id, subnet_cidr)
        Updates the subnet_id and subnet_cidr for the EC2 instance
    """

    def __init__(self,
                 ec2_instance_id,
                 private_ip):
        """

        Parameters
        ----------
        ec2_instance_id : str
            The EC2 instance id.  This will typically be in the i-xxxxxx format
        private_ip : str
            The private IP
        subnet_id : str
            Subnet ID in i-xxxx format
        subnet_cidr : str
            The subnet CIDR
        """

        self.ec2_instance_id = ec2_instance_id
        self.private_ip = private_ip
        self.subnet_id = ""
        self.subnet_cidr = ""

    def add_subnet(self, subnet_id, subnet_cidr):
        """Adds a subnet_id and subnet_cidr to the ec2 instance

        Although the subnet CIDR is directly linked to the subnet definition, it is included as an attribute here for
        ease of access.


        Parameters
        ----------
        subnet_id : str
            The subnet id
        subnet_cidr : str
            The subnets CIDR

        """
        self.subnet_id = subnet_id
        self.subnet_cidr = subnet_cidr
