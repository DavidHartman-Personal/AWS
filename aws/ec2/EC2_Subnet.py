class EC2_Subnet:
    def __init__(self,
                 SubnetId,
                 AvailabilityZone,
                 AvailabilityZoneId,
                 AvailableIpAddressCount,
                 CidrBlock,
                 DefaultForAz,
                 MapPublicIpOnLaunch,
                 State,
                 VpcId,
                 OwnerId,
                 AssignIpv6AddressOnCreation,
                 Ipv6CidrBlockAssociationSet,
                 Tags,
                 SubnetArn
                 ):
        self.AvailabilityZone = AvailabilityZone
        self.AvailabilityZoneId = AvailabilityZoneId
        self.AvailableIpAddressCount = AvailableIpAddressCount
        self.CidrBlock = CidrBlock
        self.DefaultForAz = DefaultForAz
        self.MapPublicIpOnLaunch = MapPublicIpOnLaunch
        self.State = State
        self.SubnetId = SubnetId
        self.VpcId = VpcId
        self.OwnerId = OwnerId
        self.AssignIpv6AddressOnCreation = AssignIpv6AddressOnCreation
        self.Ipv6CidrBlockAssociationSet = Ipv6CidrBlockAssociationSet
        self.Tags = Tags
        self.SubnetArn = SubnetArn


    
    