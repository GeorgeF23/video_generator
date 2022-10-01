import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { AwsSnsService } from 'libs/aws/src/aws-sns.service';
import { GenerationRequestDto } from './dto/generation.request.dto';
import { snakeKeys, camelKeys } from 'js-convert-case';
import { SqsMessageHandler } from '@ssut/nestjs-sqs';
import { GenerationResponseDto } from './dto/generation.response.dto';

@Injectable()
export class AppService {
  private readonly logger = new Logger(AppService.name);
  private requestTopic: string;

  constructor(private snsService: AwsSnsService, private configService: ConfigService) {
    this.requestTopic = this.configService.get('GENERATION_REQUEST_TOPIC');
  }

  getHello(): string {
    return 'Hello World!';
  }

  async generateVideo(request: GenerationRequestDto) {
    this.logger.log(`Received request to generate video: ${JSON.stringify(request)}`);
    const snakeCase = JSON.stringify(snakeKeys(request));
    await this.snsService.publish(this.requestTopic, snakeCase);
  }

  @SqsMessageHandler('generation_response_queue', false)
  async generatedVideoConsumer(message: AWS.SQS.Message) {
    this.logger.debug(`Got messsage in queue: ${JSON.stringify(message)}`);
    const responseStr = message['Body'];
    const responseJson = JSON.parse(responseStr);
    const response = Object.assign(new GenerationResponseDto(), camelKeys(responseJson));

    this.logger.debug(`Parsed message is: ${JSON.stringify(response)}`);
  }
}
