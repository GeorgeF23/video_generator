import logging
import os
import boto3
from urllib.parse import urlparse


class S3Client():
	instance = None

	@staticmethod
	def get_instance():
		if not S3Client.instance:
			S3Client.instance = S3Client()
		return S3Client.instance

	def __init__(self):
		"""Creates a new instance of the S3 Client

		Raises:
			err: Raised an error if the connection fails.
		"""
		try:
			self.s3_client = boto3.Session().client('s3')
		except Exception as err:
			logging.error(f'There was an error while connecting to the S3 service: {err}')
			raise err

	def upload_file(self, local_path: str, s3_bucket: str | None = None, s3_key: str | None = None) -> str:
		"""Uploads a file to s3

		Args:
			local_path (str): path to the file to upload
			s3_bucket (str | None, optional): Bucket to upload to. Defaults to S3_BUCKET env var.
			s3_key (str | None, optional): The path to upload to. Defaults to 'tmp/{filename}'.

		Raises:
			err: Raises an error if the upload fails

		Returns:
			str: Returns the s3 url of the remote file.
		"""
		try:
			if not s3_bucket:
				s3_bucket = os.environ.get('S3_BUCKET', 'not defined')
			if not s3_key:
				s3_key = 'tmp/' + local_path.split('/')[-1]
			logging.debug(f'Uploading file from {local_path} to bucket: {s3_bucket} key: {s3_key}')
			
			self.s3_client.upload_file(
				Filename=local_path,
				Bucket=s3_bucket,
				Key=s3_key
			)
			return f's3://{s3_bucket}/{s3_key}'
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
			parsed_url = urlparse(s3_url) 
			s3_key = parsed_url.path[1:]
			s3_bucket = parsed_url.hostname

			if not local_path:
				local_tmp_dir = os.environ.get('TMP_DIR', 'tmp')
				filename = s3_key.split('/')[-1]
				local_path = os.path.join(local_tmp_dir, filename)

			logging.debug(f'Downloading file from bucket: {s3_bucket} key: {s3_key} to {local_path}')
			self.s3_client.download_file(
				Key=s3_key,
				Bucket=s3_bucket,
				Filename=local_path
			)
			return local_path
		except Exception as err:
			logging.error(f'There was an error while downloading file {s3_url} to {local_path}: {err}')
			raise err
