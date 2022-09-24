import logging
import os
import boto3
from urllib.parse import urlparse


class S3Client():
	def __init__(self, bucket_name: str | None = None, upload_dir: str = 'tmp'):
		"""Creates a new instance of the S3 Client

		Args:
			bucket_name (str | None, optional): The bucket to connect to. If not provided, then the value in the S3_BUCKET env var will be used.
			upload_dir (str | None, optional): The default upload directory to be used. Defaults to 'tmp'

		Raises:
			err: Raised an error if the connection fails.
		"""
		try:
			if not bucket_name:
				bucket_name = os.environ.get('S3_BUCKET', '')
			self.bucket_name = bucket_name
			self.upload_dir = upload_dir
			self.s3_client = boto3.Session().client('s3')
		except Exception as err:
			logging.error(f'There was an error while connecting to the S3 service: {err}')
			raise err

	def upload_file(self, local_path: str, s3_key: str | None = None) -> str:
		"""Uploads a file to s3

		Args:
			local_path (str): path to the file to upload
			s3_key (str | None, optional): The path to upload to. If None, then it will upload to the upload_dir passed to S3Client. Defaults to None.

		Raises:
			err: Raises an error if the upload fails

		Returns:
			str: Returns the s3 url of the remote file.
		"""
		try:
			if not s3_key:
				s3_key = os.path.join(self.upload_dir, local_path)
			logging.debug(f'Uploading file from {local_path} to bucket: {self.bucket_name} key: {s3_key}')
			
			self.s3_client.upload_file(
				Filename=local_path,
				Bucket=self.bucket_name,
				Key=s3_key
			)
			return f's3://{self.bucket_name}/{s3_key}'
		except Exception as err:
			logging.error(f'There was an error while uploading file {local_path} to {s3_key}: {err}')
			raise err

	def download_file(self, s3_url: str, local_path: str | None = None) -> str:
		"""Downloads a file from s3.

		Args:
			s3_url (str): Url of the file to download. Can be the full url or only the key
			local_path (str | None, optional): Location where to store the file. If not provided then it will be placed in TMP_DIR.

		Raises:
			err: Raised error if downloading fails

		Returns:
			str: Path of the local file)
		"""
		try:
			s3_key = urlparse(s3_url).path[1:] if s3_url.startswith('s3://') else s3_url
			local_tmp_dir = os.environ.get('TMP_DIR', 'tmp')
			filename = s3_key.split('/')[-1]
			local_path = os.path.join(local_tmp_dir, filename)

			logging.debug(f'Downloading file from bucket: {self.bucket_name} key: {s3_key} to {local_path}')
			self.s3_client.download_file(
				Key=s3_key,
				Bucket=self.bucket_name,
				Filename=local_path
			)
			return local_path
		except Exception as err:
			logging.error(f'There was an error while downloading file {s3_url} to {local_path}: {err}')
			raise err
