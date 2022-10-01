import { IsString } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class GenerationRequestDto {
  @ApiProperty({
    description: 'The url of the background video',
  })
  @IsString()
  videoUrl: string;

  @ApiProperty({
    description: 'The subreddit from which the posts are fetched',
  })
  @IsString()
  subreddit: string;
}
