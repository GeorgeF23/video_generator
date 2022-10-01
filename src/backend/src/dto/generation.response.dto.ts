export class GenerationResponseDto {
  status: 'success' | 'error';
  ouputUrl?: string;
  error?: string;
}
