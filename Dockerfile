FROM nvidia/cuda:12.5.1-base-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /code/app/data/audios \
  && mkdir -p /code/app/data/videos \
  && mkdir -p /code/app/data/subtitles

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Install python3
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev python-is-python3 ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3 -m pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt \
  # && argospm install translate # Install all languages
  && argospm install translate-en_es \
  && argospm install translate-es_en

COPY ./app /code/app

# CMD ["python3", "app/app/main.py"]