import boto3

class SqsClient:
  instance = None

  @staticmethod
  def get_instance():
    if SqsClient.instance is None:
      SqsClient.instance = SqsClient()
    return SqsClient.instance

  def __init__(self):
    self.client = boto3.client('sqs')

  def send_message(self, message: str, queue_url: str):
    self.client.send_message(
      QueueUrl=queue_url,
      MessageBody=message 
    )