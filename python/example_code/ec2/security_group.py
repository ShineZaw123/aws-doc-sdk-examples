import logging
from pprint import pp
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


# snippet-start:[python.example_code.ec2.SecurityGroupWrapper.class]
# snippet-start:[python.example_code.ec2.SecurityGroupWrapper.decl]
class SecurityGroupWrapper:
    """Encapsulates Amazon Elastic Compute Cloud (Amazon EC2) security group actions using the client interface."""

    def __init__(self, ec2_client, security_group_id=None):
        """
        :param ec2_client: A Boto3 Amazon EC2 client. This client provides low-level 
                           access to AWS EC2 services.
        :param security_group_id: The ID of the security group.
        """
        self.ec2_client = ec2_client
        self.security_group_id = security_group_id

    @classmethod
    def from_client(cls):
        ec2_client = boto3.client("ec2")
        return cls(ec2_client)

    # snippet-end:[python.example_code.ec2.SecurityGroupWrapper.decl]

    # snippet-start:[python.example_code.ec2.CreateSecurityGroup]
    def create(self, group_name, group_description, vpc_id):
        """
        Creates a security group in the specified virtual private cloud (VPC).

        :param group_name: The name of the security group to create.
        :param group_description: The description of the security group to create.
        :param vpc_id: The ID of the VPC in which to create the security group.
        :return: The ID of the newly created security group.
        """
        try:
            response = self.ec2_client.create_security_group(
                GroupName=group_name,
                Description=group_description,
                VpcId=vpc_id
            )
            self.security_group_id = response["GroupId"]
        except ClientError as err:
            logger.error(
                "Couldn't create security group %s. Here's why: %s: %s",
                group_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return self.security_group_id

    # snippet-end:[python.example_code.ec2.CreateSecurityGroup]

    # snippet-start:[python.example_code.ec2.AuthorizeSecurityGroupIngress]
    def authorize_ingress(self, ip_permissions):
        """
        Adds a rule to the security group to allow inbound access.

        :param ip_permissions: The IP permissions to add to the security group.
        :return: The response to the authorization request. The 'Return' field of the
                 response indicates whether the request succeeded or failed.
        """
        if self.security_group_id is None:
            logger.info("No security group to update.")
            return

        try:
            response = self.ec2_client.authorize_security_group_ingress(
                GroupId=self.security_group_id,
                IpPermissions=ip_permissions
            )
        except ClientError as err:
            logger.error(
                "Couldn't authorize inbound rules for %s. Here's why: %s: %s",
                self.security_group_id,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response

    # snippet-end:[python.example_code.ec2.AuthorizeSecurityGroupIngress]

    # snippet-start:[python.example_code.ec2.DescribeSecurityGroups]
    def describe(self):
        """
        Displays information about the security group.
        """
        if self.security_group_id is None:
            logger.info("No security group to describe.")
            return

        try:
            response = self.ec2_client.describe_security_groups(
                GroupIds=[self.security_group_id]
            )
            security_group = response["SecurityGroups"][0]
            print(f"Security group: {security_group['GroupName']}")
            print(f"\tID: {security_group['GroupId']}")
            print(f"\tVPC: {security_group['VpcId']}")
            if "IpPermissions" in security_group:
                print(f"Inbound permissions:")
                pp(security_group["IpPermissions"])
        except ClientError as err:
            logger.error(
                "Couldn't get data for security group %s. Here's why: %s: %s",
                self.security_group_id,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    # snippet-end:[python.example_code.ec2.DescribeSecurityGroups]

    # snippet-start:[python.example_code.ec2.DeleteSecurityGroup]
    def delete(self):
        """
        Deletes the security group.
        """
        if self.security_group_id is None:
            logger.info("No security group to delete.")
            return

        try:
            self.ec2_client.delete_security_group(GroupId=self.security_group_id)
        except ClientError as err:
            logger.error(
                "Couldn't delete security group %s. Here's why: %s: %s",
                self.security_group_id,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    # snippet-end:[python.example_code.ec2.DeleteSecurityGroup]


# snippet-end:[python.example_code.ec2.SecurityGroupWrapper.class]