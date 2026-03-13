"""Module for interacting with Garage object storage using boto3."""

import os
from typing import override

import boto3
from loguru import logger

from h_rag.object_storage.object_storage import ObjectStorage


class GarageWrapper(ObjectStorage):
    """Class for interacting with Garage object storage."""

    def __init__(self):
        """Initialize the GarageStorage client."""
        self.s3 = boto3.client(
            "s3",
            endpoint_url="http://garage:3900",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
            region_name=os.getenv("AWS_REGION", ""),
        )
        self.bucket_name = os.getenv("BUCKET_NAME", "")

    @override
    def health_check(self) -> bool:
        try:
            self.s3.list_buckets()
            logger.info("Garage health check successful")
            return True
        except Exception as e:
            logger.error(f"Garage health check failed: {e}")
            return False

    @override
    def upload_file(self, file_data: bytes, file_name: str) -> None:
        self.s3.put_object(Bucket=self.bucket_name, Key=file_name, Body=file_data)
        logger.info(f"Uploaded {file_name} to {self.bucket_name}")

    @override
    def delete_file(self, file_name: str) -> None:
        self.s3.delete_object(Bucket=self.bucket_name, Key=file_name)
        logger.info(f"Deleted {file_name} from {self.bucket_name}")

    @override
    def list_files(self) -> list[str]:
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        if "Contents" in response:
            return [obj["Key"] for obj in response["Contents"]]
        else:
            return []

    @override
    def delete_all_files(self) -> None:
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        if "Contents" in response:
            for obj in response["Contents"]:
                self.s3.delete_object(Bucket=self.bucket_name, Key=obj["Key"])
            logger.info(f"Deleted all files from {self.bucket_name}")
        else:
            logger.info(f"No files found in {self.bucket_name} to delete.")

    @override
    def get_file(self, file_name: str) -> bytes:
        response = self.s3.get_object(Bucket=self.bucket_name, Key=file_name)
        return response["Body"].read()
