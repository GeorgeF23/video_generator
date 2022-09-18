FROM public.ecr.aws/lambda/python:3.9

COPY src/video_generator/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
	mkdir /dependencies && yum install wget tar xz -y && wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -O ffmpeg.tar.xz && \
	tar -xf ffmpeg.tar.xz && find . -name "ffmpeg" -exec mv {} /dependencies/ \; && find . -name "ffprobe" -exec mv {} test_dir/ \; && \
	rm -rf ffmpeg* && yum clean all

ENV PATH="$PATH:/dependencies"

COPY src/video_generator/ .