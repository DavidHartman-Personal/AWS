class CustomerSummary:

    class ServiceOffering:


        def __init__(self,
                     service_name,
                     number="",
                     service="",
                     description="",
                     environment=""):
            self.service_name = service_name
            self.number = number
            self.service = service
            self.description = description
            self.environment = environment

        def __repr__(self):
            return "Name:{!r} ({!r})".format(self.service_name, self.number)

    def __init__(self,
                 customer_name,
                 environment,
                 service_offerings={}):
        self.customer_name = customer_name
        self.environment = environment
        self.service_offerings = {}

    def add_service_offering(self, service_number, name, service):
        """A customer can have multiple service offerings across multiple environments"""
        if not self.service_offerings.get(service_number):
            service_offering_new = CustomerSummary.ServiceOffering(service_name=name,
                                                                   number=service_number,
                                                                   service=service,
                                                                   description="",
                                                                   environment=self.environment)
            self.service_offerings.update({service_number: service_offering_new})
