import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ConfigModule } from '@nestjs/config';
import { AwsModule } from 'libs/aws/src';

@Module({
  imports: [ConfigModule.forRoot({ isGlobal: true }), AwsModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
