import logging
import os
from environment import tmp_dir
from subprocess import run
from uuid import uuid4

def download_youtube_resource(url: str) -> str | None:
	logging.info(f'[youtube downloading] Starting downloading of {url}')
	local_filename = uuid4().hex
	local_path = os.path.join(tmp_dir, local_filename)


	yt_dl = os.environ.get('YOUTUBE_DL_PATH')
	timeout = int(os.environ.get('DOWNLOAD_TIMEOUT', '60'))
	command = f'{yt_dl} -o {local_path} {url}'

	logging.debug(f'[youtube downloading] Command is: {command} with timeout {timeout}')

	p = run(command, shell=True, timeout=timeout)

	if p.returncode != 0:
		return None

	return local_path + '.webm'

def download_resource(url: str) -> str | None:
	if url.startswith('https://www.youtube'):
		local_resource = download_youtube_resource(url)
	else:
		local_resource = None

	if local_resource and not os.path.exists(local_resource):
		logging.error('[Resource download] Local resource could not be found after download')
		raise RuntimeError('Could not download resource')

	logging.info(f'[Resource download] Downloaded {url} to {local_resource}')
	return local_resource