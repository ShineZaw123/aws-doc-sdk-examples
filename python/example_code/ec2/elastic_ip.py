import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# snippet-start:[python.example_code.ec2.ElasticIpWrapper.class]
# snippet-start:[python.example_code.ec2.ElasticIpWrapper.decl]
class ElasticIpWrapper:
    """Encapsulates Amazon Elastic Compute Cloud (Amazon EC2) Elastic IP address actions using the client interface."""

    def __init__(self, ec2_client, allocation_id=None):
        """
        :param ec2_client: A Boto3 Amazon EC2 client. This client provides low-level 
                           access to AWS EC2 services.
        :param allocation_id: The allocation ID of an Elastic IP address.
        """
        self.ec2_client = ec2_client
        self.allocation_id = allocation_id

    @classmethod
    def from_client(cls):
        ec2_client = boto3.client("ec2")
        return cls(ec2_client)

    # snippet-end:[python.example_code.ec2.ElasticIpWrapper.decl]

    # snippet-start:[python.example_code.ec2.AllocateAddress]
    def allocate(self):
        """
        Allocates an Elastic IP address that can be associated with an Amazon EC2
        instance. By using an Elastic IP address, you can keep the public IP address
        constant even when you restart the associated instance.

        :return: The allocation ID of the newly created Elastic IP address.
        """
        try:
            response = self.ec2_client.allocate_address(Domain="vpc")
            self.allocation_id = response["AllocationId"]
        except ClientError as err:
            # Improved error handling to catch specific errors like InvalidAddress.Unavailable and InvalidInput,
            # providing more informative error messages for these cases.
            if err.response["Error"]["Code"] in ["InvalidAddress.Unavailable", "InvalidInput"]:
                logger.error(
                    "Couldn't allocate Elastic IP. The requested IP address is not available or the input is invalid."
                )
            else:
                logger.error(
                    "Couldn't allocate Elastic IP. Here's why: %s: %s",
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
            raise err
        else:
            return self.allocation_id

    # snippet-end:[python.example_code.ec2.AllocateAddress]

# snippet-end:[python.example_code.ec2.ElasticIpWrapper.class]