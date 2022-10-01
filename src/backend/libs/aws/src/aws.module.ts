import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { AwsSnsService } from './aws-sns.service';
import { AwsService } from './aws.service';

@Module({
  imports: [ConfigModule.forRoot()],
  providers: [AwsService, AwsSnsService],
  exports: [AwsService, AwsSnsService],
})
export class AwsModule {}
