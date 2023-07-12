FROM python:3.8-slim-bookworm
WORKDIR /app
# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
