import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { AwsSnsService } from 'libs/aws/src/aws-sns.service';
import { GenerationRequestDto } from './dto/generation.request.dto';
import { snakeKeys } from 'js-convert-case';

@Injectable()
export class AppService {
  private readonly logger = new Logger(AppService.name);
  private requestTopic;

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
}
