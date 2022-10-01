import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { SNSClient, PublishCommand } from '@aws-sdk/client-sns';

@Injectable()
export class AwsSnsService {
  private readonly logger = new Logger(AwsSnsService.name);
  private snsClient: SNSClient;

  constructor(configService: ConfigService) {
    const region = configService.get('AWS_REGION');
    this.snsClient = new SNSClient({ region: region });
  }

  async publish(topic: string, message: string) {
    this.logger.debug(`Publishing message: ${message} to topic: ${topic}`);
    await this.snsClient.send(
      new PublishCommand({
        Message: message,
        TopicArn: topic,
      }),
    );
  }
}
