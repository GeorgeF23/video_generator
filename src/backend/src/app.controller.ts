import { Body, Controller, Get, Post, UsePipes, ValidationPipe } from '@nestjs/common';
import { ApiBadRequestResponse, ApiCreatedResponse, ApiOperation } from '@nestjs/swagger';
import { AppService } from './app.service';
import { GenerationRequestDto } from './dto/generation.request.dto';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }

  @ApiOperation({ description: 'Creates a generation request to lambda' })
  @ApiCreatedResponse({ description: 'Request successfully made.' })
  @ApiBadRequestResponse({ description: 'Invalid input.' })
  @UsePipes(new ValidationPipe())
  @Post('generate')
  async generateVideo(@Body() request: GenerationRequestDto) {
    await this.appService.generateVideo(request);
  }
}
