#!/bin/bash

docker run -t -i -w /opt/video_bot -v $(pwd):/opt/video_bot video_bot_env:latest 