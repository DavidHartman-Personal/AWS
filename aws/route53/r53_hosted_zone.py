class r53_hosted_zone:
    """AWS Route53 Hosted Zone
    """

    def __init__(self,
                 id,
                 name,
                 caller_reference,
                 config_private_zone_flag,
                 config_comment,
                 resource_record_count):
        self.id = id
        self.name = name
        self.caller_reference = caller_reference
        self.config_private_zone_flag = config_private_zone_flag
        self.config_comment = config_comment
        self.resource_record_count = resource_record_count