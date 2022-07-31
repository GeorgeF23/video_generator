from dataclasses import dataclass

@dataclass()
class GenerationConfigurationDto:
    local_video_path: str
    voice_path: str
    timestamps_path: str