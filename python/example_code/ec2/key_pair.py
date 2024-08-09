import logging
import os
import tempfile
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


# snippet-start:[python.example_code.ec2.KeyPairWrapper.class]
# snippet-start:[python.example_code.ec2.KeyPairWrapper.decl]
class KeyPairWrapper:
    """Encapsulates Amazon Elastic Compute Cloud (Amazon EC2) key pair actions using the client interface."""

    def __init__(self, ec2_client, key_file_dir):
        """
        :param ec2_client: A Boto3 Amazon EC2 client. This client provides low-level 
                           access to AWS EC2 services.
        :param key_file_dir: The folder where the private key information is stored.
                             This should be a secure folder.
        """
        self.ec2_client = ec2_client
        self.key_file_path = None
        self.key_file_dir = key_file_dir

    @classmethod
    def from_client(cls):
        ec2_client = boto3.client("ec2")
        return cls(ec2_client, tempfile.TemporaryDirectory())

    # snippet-end:[python.example_code.ec2.KeyPairWrapper.decl]

    # snippet-start:[python.example_code.ec2.CreateKeyPair]
    def create(self, key_name):
        """
        Creates a key pair that can be used to securely connect to an EC2 instance.
        The returned key pair contains private key information that cannot be retrieved
        again. The private key data is stored as a .pem file.

        :param key_name: The name of the key pair to create.
        :return: The private key material of the newly created key pair.
        """
        try:
            response = self.ec2_client.create_key_pair(KeyName=key_name)
            self.key_file_path = os.path.join(
                self.key_file_dir.name, f"{response['KeyName']}.pem"
            )
            with open(self.key_file_path, "w") as key_file:
                key_file.write(response['KeyMaterial'])
        except ClientError as err:
            logger.error(
                "Couldn't create key %s. Here's why: %s: %s",
                key_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response['KeyMaterial']

    # snippet-end:[python.example_code.ec2.CreateKeyPair]

    # snippet-start:[python.example_code.ec2.DescribeKeyPairs]
    def list(self, limit):
        """
        Displays a list of key pairs for the current account.

        :param limit: The maximum number of key pairs to list.
        """
        try:
            response = self.ec2_client.describe_key_pairs()
            key_pairs = response['KeyPairs']
            for kp in key_pairs[:limit]:
                print(f"Found {kp['KeyType']} key {kp['KeyName']} with fingerprint:")
                print(f"\t{kp['KeyFingerprint']}")
        except ClientError as err:
            logger.error(
                "Couldn't list key pairs. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    # snippet-end:[python.example_code.ec2.DescribeKeyPairs]

    # snippet-start:[python.example_code.ec2.DeleteKeyPair]
    def delete(self, key_name):
        """
        Deletes a key pair.
        """
        try:
            self.ec2_client.delete_key_pair(KeyName=key_name)
        except ClientError as err:
            logger.error(
                "Couldn't delete key %s. Here's why: %s : %s",
                key_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    # snippet-end:[python.example_code.ec2.DeleteKeyPair]


# snippet-end:[python.example_code.ec2.KeyPairWrapper.class]