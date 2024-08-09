# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


# snippet-start:[python.example_code.ec2.ElasticIpWrapper.class]
# snippet-start:[python.example_code.ec2.ElasticIpWrapper.decl]
class ElasticIpWrapper:
    """Encapsulates Amazon Elastic Compute Cloud (Amazon EC2) Elastic IP address actions."""

    def __init__(self, ec2_client, elastic_ip=None):
        """
        :param ec2_client: A Boto3 Amazon EC2 client. This low-level client
                           is used to perform Elastic IP address actions.
        :param elastic_ip: A Boto3 VpcAddress object. This is a high-level object that
                           wraps Elastic IP actions.
        """
        self.ec2_client = ec2_client
        self.elastic_ip = elastic_ip

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

        :return: The newly created Elastic IP object. By default, the address is not
                 associated with any instance.
        """
        try:
            response = self.ec2_client.allocate_address(Domain="vpc")
            self.elastic_ip = self.ec2_client.describe_addresses(AllocationIds=[response["AllocationId"]])[
                "Addresses"
            ][0]
        except ClientError as err:
            logger.error(
                "Couldn't allocate Elastic IP. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return self.elastic_ip

    # snippet-end:[python.example_code.ec2.AllocateAddress]

    # snippet-start:[python.example_code.ec2.AssociateAddress]
    def associate(self, instance):
        """
        Associates an Elastic IP address with an instance. When this association is
        created, the Elastic IP's public IP address is immediately used as the public
        IP address of the associated instance.

        :param instance: A Boto3 Instance object. This is a high-level object that wraps
                         Amazon EC2 instance actions.
        :return: A response that contains the ID of the association.
        """
        if self.elastic_ip is None:
            logger.info("No Elastic IP to associate.")
            return

        try:
            response = self.ec2_client.associate_address(InstanceId=instance.id, AllocationId=self.elastic_ip["AllocationId"])
        except ClientError as err:
            logger.error(
                "Couldn't associate Elastic IP %s with instance %s. Here's why: %s: %s",
                self.elastic_ip["AllocationId"],
                instance.id,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        return response

    # snippet-end:[python.example_code.ec2.AssociateAddress]

    # snippet-start:[python.example_code.ec2.DisassociateAddress]
    def disassociate(self):
        """
        Removes an association between an Elastic IP address and an instance. When the
        association is removed, the instance is assigned a new public IP address.
        """
        if self.elastic_ip is None:
            logger.info("No Elastic IP to disassociate.")
            return

        try:
            self.ec2_client.disassociate_address(AssociationId=self.elastic_ip["AssociationId"])
        except ClientError as err:
            logger.error(
                "Couldn't disassociate Elastic IP %s from its instance. Here's why: %s: %s",
                self.elastic_ip["AllocationId"],
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    # snippet-end:[python.example_code.ec2.DisassociateAddress]

    # snippet-start:[python.example_code.ec2.ReleaseAddress]
    def release(self):
        """
        Releases an Elastic IP address. After the Elastic IP address is released,
        it can no longer be used.
        """
        if self.elastic_ip is None:
            logger.info("No Elastic IP to release.")
            return

        try:
            self.ec2_client.release_address(AllocationId=self.elastic_ip["AllocationId"])
        except ClientError as err:
            logger.error(
                "Couldn't release Elastic IP address %s. Here's why: %s: %s",
                self.elastic_ip["AllocationId"],
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    # snippet-end:[python.example_code.ec2.ReleaseAddress]


# snippet-end:[python.example_code.ec2.ElasticIpWrapper.class]