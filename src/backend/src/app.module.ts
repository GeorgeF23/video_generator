import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { AwsModule } from 'libs/aws/src';
import { SqsModule } from '@ssut/nestjs-sqs';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    AwsModule,
    SqsModule.registerAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: async (configService: ConfigService) => ({
        consumers: [
          {
            name: 'generation_response_queue',
            queueUrl: configService.get('GENERATION_RESPONSE_QUEUE'),
            region: configService.get('AWS_REGION'),
          },
        ],
      }),
    }),
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
