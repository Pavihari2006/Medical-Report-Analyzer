FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    tesseract-ocr \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://pixi.sh/install.sh | bash
ENV PATH="/root/.pixi/bin:$PATH"

WORKDIR /app
COPY . /app

RUN cd /app/mojo && pixi init . -c https://conda.modular.com/max -c conda-forge && pixi add mojo

RUN pip3 install --break-system-packages fastapi uvicorn pytesseract Pillow python-multipart opencv-python-headless google-genai python-dotenv

EXPOSE 8080

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]